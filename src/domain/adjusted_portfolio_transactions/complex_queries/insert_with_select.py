from sqlalchemy import select, insert, case, and_, func

from src.domain.adjusted_portfolio_transactions.adjusted_portfolio_transaction_model import (
    AdjustedPortfolioTransaction,
)
from src.domain.portfolio_transactions.portfolio_transaction_model import (
    PortfolioTransaction,
)
from src.domain.portfolio_transaction_files.portfolio_transaction_file_model import (
    PortfolioTransactionFile,
)
from src.domain.adjusted_currency_pair_pricings.adjusted_currency_pair_pricing_model import (
    AdjustedCurrencyPairPricing,
)
from src.domain.settings.settings_model import Settings


OHLC_OPTIONS = [
    "open",
    "high",
    "low",
    "close",
    "average",
    "typical price",
    "weighted close price",
]


def insert_with_select(user_id: int):
    cte_1 = (
        select(
            PortfolioTransaction.portfolio_transaction_file_id,
            PortfolioTransactionFile.portfolio_id,
            PortfolioTransaction.asset_id,
            PortfolioTransaction.date,
            PortfolioTransaction.transaction_type,
            PortfolioTransaction.quantity,
            PortfolioTransaction.transaction_value,
            PortfolioTransaction.fee_amount,
            PortfolioTransaction.tax_amount,
            case(
                (
                    Settings.ohlc_currencies == OHLC_OPTIONS[0],
                    AdjustedCurrencyPairPricing.open_price,
                ),
                (
                    Settings.ohlc_currencies == OHLC_OPTIONS[1],
                    AdjustedCurrencyPairPricing.high_price,
                ),
                (
                    Settings.ohlc_currencies == OHLC_OPTIONS[2],
                    AdjustedCurrencyPairPricing.low_price,
                ),
                (
                    Settings.ohlc_currencies == OHLC_OPTIONS[3],
                    AdjustedCurrencyPairPricing.close_price,
                ),
                (
                    Settings.ohlc_currencies == OHLC_OPTIONS[4],
                    (
                        AdjustedCurrencyPairPricing.open_price
                        + AdjustedCurrencyPairPricing.high_price
                        + AdjustedCurrencyPairPricing.low_price
                        + AdjustedCurrencyPairPricing.close_price
                    )
                    / 4,
                ),
                (
                    Settings.ohlc_currencies == OHLC_OPTIONS[5],
                    (
                        AdjustedCurrencyPairPricing.high_price
                        + AdjustedCurrencyPairPricing.low_price
                        + AdjustedCurrencyPairPricing.close_price
                    )
                    / 3,
                ),
                (
                    Settings.ohlc_currencies == OHLC_OPTIONS[6],
                    (
                        AdjustedCurrencyPairPricing.high_price
                        + AdjustedCurrencyPairPricing.low_price
                        + (2 * AdjustedCurrencyPairPricing.close_price)
                    )
                    / 4,
                ),
                else_=0.0,
            ).label("exchange_rate"),
        )
        .join_from(
            PortfolioTransaction,
            PortfolioTransactionFile,
            PortfolioTransactionFile.id
            == PortfolioTransaction.portfolio_transaction_file_id,
        )
        .outerjoin(
            AdjustedCurrencyPairPricing,
            and_(
                PortfolioTransactionFile.currency_pair_id
                == AdjustedCurrencyPairPricing.currency_pair_id,
                PortfolioTransaction.date == AdjustedCurrencyPairPricing.date,
            ),
        )
        .join(Settings, Settings.user_id == PortfolioTransactionFile.user_id)
        .where(PortfolioTransactionFile.user_id == user_id)
    ).cte(name="cte_1")

    cte_2 = select(
        cte_1.c.portfolio_transaction_file_id,
        cte_1.c.portfolio_id,
        cte_1.c.asset_id,
        cte_1.c.date,
        cte_1.c.transaction_type,
        case(
            (
                cte_1.c.transaction_type == "buy",
                cte_1.c.quantity,
            ),
            (
                cte_1.c.transaction_type == "sell",
                -cte_1.c.quantity,
            ),
            else_=0,
        ).label("quantity"),
        (
            case(
                (
                    cte_1.c.transaction_type.in_(
                        ["deposit", "sell", "distribution", "interest"]
                    ),
                    cte_1.c.transaction_value,
                ),
                (
                    cte_1.c.transaction_type.in_(["withdrawal", "buy"]),
                    -cte_1.c.transaction_value,
                ),
                else_=0.0,
            )
            * func.coalesce(cte_1.c.exchange_rate, 1)
        ).label("transaction_value"),
        (
            case(
                (
                    cte_1.c.transaction_type.in_(
                        [
                            "deposit",
                            "withdrawal",
                            "sell",
                            "distribution",
                            "interest",
                            "buy",
                            "fee",
                        ]
                    ),
                    -cte_1.c.fee_amount,
                ),
                else_=0.0,
            )
            * func.coalesce(cte_1.c.exchange_rate, 1)
        ).label("fee_amount"),
        (
            case(
                (
                    cte_1.c.transaction_type.in_(
                        [
                            "sell",
                            "distribution",
                            "interest",
                        ]
                    ),
                    -cte_1.c.tax_amount,
                ),
                else_=0.0,
            )
            * func.coalesce(cte_1.c.exchange_rate, 1)
        ).label("tax_amount"),
    ).cte(name="cte_2")

    query = select(
        cte_2,
        (cte_2.c.transaction_value + cte_2.c.fee_amount + cte_2.c.tax_amount).label(
            "cash_flow"
        ),
        case(
            (
                cte_2.c.transaction_type == "buy",
                cte_2.c.transaction_value,
            ),
            else_=0.0,
        ).label("invested_amount"),
        case(
            (
                cte_2.c.transaction_type.in_(["buy", "fee"]),
                cte_2.c.transaction_value + cte_2.c.fee_amount,
            ),
            else_=0.0,
        ).label("invested_amount_total"),
        case(
            (
                cte_2.c.transaction_type == "sell",
                cte_2.c.transaction_value,
            ),
            else_=0.0,
        ).label("asset_disposal_income"),
        case(
            (
                cte_2.c.transaction_type == "sell",
                cte_2.c.transaction_value + cte_2.c.fee_amount + cte_2.c.tax_amount,
            ),
            else_=0.0,
        ).label("asset_disposal_income_total"),
        case(
            (
                cte_2.c.transaction_type == "distribution",
                cte_2.c.transaction_value,
            ),
            else_=0.0,
        ).label("asset_holding_income"),
        case(
            (
                cte_2.c.transaction_type == "distribution",
                cte_2.c.transaction_value + cte_2.c.fee_amount + cte_2.c.tax_amount,
            ),
            else_=0.0,
        ).label("asset_holding_income_total"),
        case(
            (
                cte_2.c.transaction_type == "interest",
                cte_2.c.transaction_value,
            ),
            else_=0.0,
        ).label("interest_income"),
        case(
            (
                cte_2.c.transaction_type == "interest",
                cte_2.c.transaction_value + cte_2.c.fee_amount + cte_2.c.tax_amount,
            ),
            else_=0.0,
        ).label("interest_income_total"),
        case(
            (
                cte_2.c.transaction_type.in_(["sell", "distribution", "interest"]),
                cte_2.c.transaction_value,
            ),
            else_=0.0,
        ).label("investment_income"),
        case(
            (
                cte_2.c.transaction_type.in_(["sell", "distribution", "interest"]),
                cte_2.c.transaction_value + cte_2.c.fee_amount + cte_2.c.tax_amount,
            ),
            else_=0.0,
        ).label("investment_income_total"),
    )

    return insert(AdjustedPortfolioTransaction).from_select(
        [
            "portfolio_transaction_file_id",
            "portfolio_id",
            "asset_id",
            "date",
            "transaction_type",
            "quantity",
            "transaction_value",
            "fee_amount",
            "tax_amount",
            "cash_flow",
            "invested_amount",
            "invested_amount_total",
            "asset_disposal_income",
            "asset_disposal_income_total",
            "asset_holding_income",
            "asset_holding_income_total",
            "interest_income",
            "interest_income_total",
            "investment_income",
            "investment_income_total",
        ],
        query,
    )
