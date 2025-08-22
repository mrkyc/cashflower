from sqlalchemy import select, insert, and_, func, case

from src.domain.portfolio_asset_performances.portfolio_asset_performance_model import (
    PortfolioAssetPerformance,
)
from src.domain.portfolio_aggregates.portfolio_aggregate_model import PortfolioAggregate
from src.domain.portfolios.portfolio_model import Portfolio
from src.domain.portfolio_groups.portfolio_group_model import PortfolioGroup
from src.domain.portfolio_group_assets.portfolio_group_asset_model import (
    PortfolioGroupAsset,
)
from src.domain.adjusted_asset_pricings.adjusted_asset_pricing_model import (
    AdjustedAssetPricing,
)
from src.domain.adjusted_currency_pair_pricings.adjusted_currency_pair_pricing_model import (
    AdjustedCurrencyPairPricing,
)
from src.domain.adjusted_portfolio_transactions.adjusted_portfolio_transaction_model import (
    AdjustedPortfolioTransaction,
)
from src.domain.currency_pairs.currency_pair_model import CurrencyPair
from src.domain.assets.asset_model import Asset
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
    cte_first_transaction_date = (
        select(
            AdjustedPortfolioTransaction.portfolio_id,
            AdjustedPortfolioTransaction.asset_id,
            func.min(AdjustedPortfolioTransaction.date).label("first_transaction_date"),
        )
        .join_from(
            AdjustedPortfolioTransaction,
            Portfolio,
            Portfolio.id == AdjustedPortfolioTransaction.portfolio_id,
        )
        .join(
            PortfolioAggregate,
            PortfolioAggregate.id == Portfolio.portfolio_aggregate_id,
        )
        .where(PortfolioAggregate.user_id == user_id)
        .group_by(
            AdjustedPortfolioTransaction.portfolio_id,
            AdjustedPortfolioTransaction.asset_id,
        )
        .cte("cte_first_transaction_date")
    )

    cte_portfolio_assets = (
        select(PortfolioGroupAsset.asset_id, Asset.currency)
        .join_from(
            PortfolioGroup,
            PortfolioGroupAsset,
            PortfolioGroupAsset.portfolio_group_id == PortfolioGroup.id,
        )
        .join(Asset, Asset.id == PortfolioGroupAsset.asset_id)
        .where(PortfolioGroup.user_id == user_id)
        .group_by(Asset.id)
    ).cte("cte_portfolio_assets")

    cte_adjusted_currency_pair_pricings = (
        select(
            CurrencyPair.first_currency_name,
            CurrencyPair.second_currency_name,
            AdjustedCurrencyPairPricing.date,
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
            CurrencyPair,
            AdjustedCurrencyPairPricing,
            AdjustedCurrencyPairPricing.currency_pair_id == CurrencyPair.id,
        )
        .join(Settings, Settings.user_id == user_id)
        .where(
            and_(
                CurrencyPair.first_currency_name.in_(
                    select(cte_portfolio_assets.c.currency)
                ),
                CurrencyPair.second_currency_name == Settings.analysis_currency,
            )
        )
    ).cte("cte_adjusted_currency_pair_pricings")

    cte_adjusted_asset_pricings = (
        select(
            AdjustedAssetPricing.asset_id,
            AdjustedAssetPricing.date,
            (
                case(
                    (
                        Settings.ohlc_assets == OHLC_OPTIONS[0],
                        AdjustedAssetPricing.open_price,
                    ),
                    (
                        Settings.ohlc_assets == OHLC_OPTIONS[1],
                        AdjustedAssetPricing.high_price,
                    ),
                    (
                        Settings.ohlc_assets == OHLC_OPTIONS[2],
                        AdjustedAssetPricing.low_price,
                    ),
                    (
                        Settings.ohlc_assets == OHLC_OPTIONS[3],
                        AdjustedAssetPricing.close_price,
                    ),
                    (
                        Settings.ohlc_assets == OHLC_OPTIONS[4],
                        (
                            AdjustedAssetPricing.open_price
                            + AdjustedAssetPricing.high_price
                            + AdjustedAssetPricing.low_price
                            + AdjustedAssetPricing.close_price
                        )
                        / 4,
                    ),
                    (
                        Settings.ohlc_assets == OHLC_OPTIONS[5],
                        (
                            AdjustedAssetPricing.high_price
                            + AdjustedAssetPricing.low_price
                            + AdjustedAssetPricing.close_price
                        )
                        / 3,
                    ),
                    (
                        Settings.ohlc_assets == OHLC_OPTIONS[6],
                        (
                            AdjustedAssetPricing.high_price
                            + AdjustedAssetPricing.low_price
                            + (2 * AdjustedAssetPricing.close_price)
                        )
                        / 4,
                    ),
                    else_=0.0,
                )
                * cte_adjusted_currency_pair_pricings.c.exchange_rate
            ).label("price"),
            (
                AdjustedAssetPricing.adj_close_price
                * cte_adjusted_currency_pair_pricings.c.exchange_rate
            ).label("adj_close_price"),
        )
        .join_from(
            AdjustedAssetPricing,
            cte_portfolio_assets,
            cte_portfolio_assets.c.asset_id == AdjustedAssetPricing.asset_id,
        )
        .join(Settings, Settings.user_id == user_id)
        .join(
            cte_adjusted_currency_pair_pricings,
            and_(
                cte_adjusted_currency_pair_pricings.c.first_currency_name
                == cte_portfolio_assets.c.currency,
                cte_adjusted_currency_pair_pricings.c.date == AdjustedAssetPricing.date,
            ),
        )
    ).cte("cte_adjusted_asset_pricings")

    cte_1 = (
        select(
            Portfolio.id.label("portfolio_id"),
            PortfolioGroup.id.label("portfolio_group_id"),
            cte_adjusted_asset_pricings.c.asset_id,
            PortfolioAggregate.checkpoint_date,
            cte_adjusted_asset_pricings.c.date,
            cte_adjusted_asset_pricings.c.price.label("unit_price"),
            cte_adjusted_asset_pricings.c.adj_close_price.label("unit_price_adj"),
            func.coalesce(AdjustedPortfolioTransaction.quantity, 0).label("quantity"),
            func.coalesce(AdjustedPortfolioTransaction.quantity, 0).label(
                "delta_quantity"
            ),
            func.coalesce(AdjustedPortfolioTransaction.invested_amount, 0.0).label(
                "invested_amount"
            ),
            func.coalesce(
                AdjustedPortfolioTransaction.invested_amount_total, 0.0
            ).label("invested_amount_total"),
            func.coalesce(
                AdjustedPortfolioTransaction.asset_disposal_income, 0.0
            ).label("asset_disposal_income"),
            func.coalesce(
                AdjustedPortfolioTransaction.asset_disposal_income_total, 0.0
            ).label("asset_disposal_income_total"),
            func.coalesce(AdjustedPortfolioTransaction.asset_holding_income, 0.0).label(
                "asset_holding_income"
            ),
            func.coalesce(
                AdjustedPortfolioTransaction.asset_holding_income_total, 0.0
            ).label("asset_holding_income_total"),
            func.coalesce(AdjustedPortfolioTransaction.investment_income, 0.0).label(
                "investment_income"
            ),
            func.coalesce(
                AdjustedPortfolioTransaction.investment_income_total, 0.0
            ).label("investment_income_total"),
        )
        .join_from(
            PortfolioAggregate,
            Portfolio,
            Portfolio.portfolio_aggregate_id == PortfolioAggregate.id,
        )
        .join(PortfolioGroup, PortfolioGroup.portfolio_id == Portfolio.id)
        .join(
            PortfolioGroupAsset,
            PortfolioGroupAsset.portfolio_group_id == PortfolioGroup.id,
        )
        .join(
            cte_adjusted_asset_pricings,
            cte_adjusted_asset_pricings.c.asset_id == PortfolioGroupAsset.asset_id,
        )
        .outerjoin(
            AdjustedPortfolioTransaction,
            and_(
                AdjustedPortfolioTransaction.portfolio_id == Portfolio.id,
                AdjustedPortfolioTransaction.asset_id == PortfolioGroupAsset.asset_id,
                AdjustedPortfolioTransaction.date == cte_adjusted_asset_pricings.c.date,
            ),
        )
        .join(
            cte_first_transaction_date,
            and_(
                cte_first_transaction_date.c.portfolio_id == Portfolio.id,
                cte_first_transaction_date.c.asset_id
                == cte_adjusted_asset_pricings.c.asset_id,
            ),
        )
        .where(
            and_(
                PortfolioAggregate.user_id == user_id,
                cte_adjusted_asset_pricings.c.date
                >= func.max(
                    cte_first_transaction_date.c.first_transaction_date,
                    PortfolioAggregate.checkpoint_date,
                ),
            )
        )
        .union_all(
            select(
                PortfolioAssetPerformance.portfolio_id,
                PortfolioAssetPerformance.portfolio_group_id,
                PortfolioAssetPerformance.asset_id,
                PortfolioAggregate.checkpoint_date,
                PortfolioAssetPerformance.date,
                PortfolioAssetPerformance.unit_price,
                PortfolioAssetPerformance.unit_price_adj,
                PortfolioAssetPerformance.quantity,
                PortfolioAssetPerformance.delta_quantity,
                PortfolioAssetPerformance.invested_amount,
                PortfolioAssetPerformance.invested_amount_total,
                PortfolioAssetPerformance.asset_disposal_income,
                PortfolioAssetPerformance.asset_disposal_income_total,
                PortfolioAssetPerformance.asset_holding_income,
                PortfolioAssetPerformance.asset_holding_income_total,
                PortfolioAssetPerformance.investment_income,
                PortfolioAssetPerformance.investment_income_total,
            )
            .join_from(
                PortfolioAssetPerformance,
                Portfolio,
                Portfolio.id == PortfolioAssetPerformance.portfolio_id,
            )
            .join(
                PortfolioAggregate,
                PortfolioAggregate.id == Portfolio.portfolio_aggregate_id,
            )
            .where(
                and_(
                    PortfolioAggregate.user_id == user_id,
                    PortfolioAssetPerformance.date
                    == func.date(PortfolioAggregate.checkpoint_date, "-1 day"),
                )
            )
        )
    ).cte(name="cte_1")

    cte_2 = (
        select(
            cte_1.c.portfolio_id,
            cte_1.c.portfolio_group_id,
            cte_1.c.asset_id,
            cte_1.c.checkpoint_date,
            cte_1.c.date,
            cte_1.c.unit_price,
            cte_1.c.unit_price_adj,
            (
                func.sum(cte_1.c.quantity).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
            ).label("quantity"),
            func.sum(cte_1.c.delta_quantity)
            .over(
                partition_by=[
                    cte_1.c.portfolio_id,
                    cte_1.c.asset_id,
                    cte_1.c.date,
                ],
            )
            .label("delta_quantity"),
            (
                func.sum(cte_1.c.quantity).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
                * cte_1.c.unit_price
            ).label("market_value"),
            (
                func.sum(cte_1.c.quantity).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
                * cte_1.c.unit_price_adj
            ).label("market_value_adj"),
            (
                func.sum(cte_1.c.delta_quantity).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                        cte_1.c.date,
                    ],
                )
                * cte_1.c.unit_price_adj
            ).label("delta_quantity_value_adj"),
            (
                func.sum(cte_1.c.invested_amount).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
            ).label("invested_amount"),
            (
                func.sum(cte_1.c.invested_amount_total).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
            ).label("invested_amount_total"),
            (
                func.sum(cte_1.c.asset_disposal_income).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
            ).label("asset_disposal_income"),
            (
                func.sum(cte_1.c.asset_disposal_income_total).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
            ).label("asset_disposal_income_total"),
            (
                func.sum(cte_1.c.asset_holding_income).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
            ).label("asset_holding_income"),
            (
                func.sum(cte_1.c.asset_holding_income_total).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
            ).label("asset_holding_income_total"),
            (
                func.sum(cte_1.c.investment_income).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
            ).label("investment_income"),
            (
                func.sum(cte_1.c.investment_income_total).over(
                    partition_by=[
                        cte_1.c.portfolio_id,
                        cte_1.c.asset_id,
                    ],
                    order_by=cte_1.c.date,
                )
            ).label("investment_income_total"),
        )
        .distinct()
        .union_all(
            select(
                PortfolioAssetPerformance.portfolio_id,
                PortfolioAssetPerformance.portfolio_group_id,
                PortfolioAssetPerformance.asset_id,
                PortfolioAggregate.checkpoint_date,
                PortfolioAssetPerformance.date,
                PortfolioAssetPerformance.unit_price,
                PortfolioAssetPerformance.unit_price_adj,
                PortfolioAssetPerformance.quantity,
                PortfolioAssetPerformance.delta_quantity,
                PortfolioAssetPerformance.market_value,
                PortfolioAssetPerformance.market_value_adj,
                PortfolioAssetPerformance.delta_quantity_value_adj,
                PortfolioAssetPerformance.invested_amount,
                PortfolioAssetPerformance.invested_amount_total,
                PortfolioAssetPerformance.asset_disposal_income,
                PortfolioAssetPerformance.asset_disposal_income_total,
                PortfolioAssetPerformance.asset_holding_income,
                PortfolioAssetPerformance.asset_holding_income_total,
                PortfolioAssetPerformance.investment_income,
                PortfolioAssetPerformance.investment_income_total,
            )
            .join_from(
                PortfolioAssetPerformance,
                Portfolio,
                Portfolio.id == PortfolioAssetPerformance.portfolio_id,
            )
            .join(
                PortfolioAggregate,
                PortfolioAggregate.id == Portfolio.portfolio_aggregate_id,
            )
            .where(
                PortfolioAssetPerformance.date
                < func.date(PortfolioAggregate.checkpoint_date, "-1 day")
            )
        )
    ).cte(name="cte_2")

    cte_3 = select(
        cte_2,
        (
            cte_2.c.market_value + cte_2.c.invested_amount + cte_2.c.investment_income
        ).label("profit"),
        (
            cte_2.c.market_value
            + cte_2.c.invested_amount_total
            + cte_2.c.investment_income_total
        ).label("profit_total"),
        (
            (cte_2.c.market_value + cte_2.c.invested_amount + cte_2.c.investment_income)
            / func.abs(cte_2.c.invested_amount)
        ).label("profit_percentage"),
        (
            (
                cte_2.c.market_value
                + cte_2.c.invested_amount_total
                + cte_2.c.investment_income_total
            )
            / func.abs(cte_2.c.invested_amount_total)
        ).label("profit_percentage_total"),
        (
            func.max(cte_2.c.market_value + cte_2.c.asset_disposal_income).over(
                partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                order_by=cte_2.c.date,
            )
        ).label("past_maximum_value"),
        (
            func.max(cte_2.c.market_value + cte_2.c.asset_disposal_income_total).over(
                partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                order_by=cte_2.c.date,
            )
        ).label("past_maximum_value_total"),
        (
            func.max(
                cte_2.c.market_value
                + cte_2.c.invested_amount
                + cte_2.c.investment_income
            ).over(
                partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                order_by=cte_2.c.date,
            )
        ).label("past_maximum_profit"),
        (
            func.max(
                cte_2.c.market_value
                + cte_2.c.invested_amount_total
                + cte_2.c.investment_income_total
            ).over(
                partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                order_by=cte_2.c.date,
            )
        ).label("past_maximum_profit_total"),
        func.coalesce(
            (
                (cte_2.c.market_value_adj - cte_2.c.delta_quantity_value_adj)
                / func.lag(cte_2.c.market_value_adj).over(
                    partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                    order_by=cte_2.c.date,
                )
                - 1
            ),
            0.0,
        ).label("hpr"),
        (
            func.row_number().over(
                partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                order_by=cte_2.c.date,
            )
        ).label("row_number"),
        (
            cte_2.c.invested_amount
            - func.lag(cte_2.c.invested_amount, 1, 0.0).over(
                partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                order_by=cte_2.c.date,
            )
            + cte_2.c.investment_income
            - func.lag(cte_2.c.investment_income, 1, 0.0).over(
                partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                order_by=cte_2.c.date,
            )
        ).label("cash_flow"),
        (
            cte_2.c.invested_amount_total
            - func.lag(cte_2.c.invested_amount_total, 1, 0.0).over(
                partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                order_by=cte_2.c.date,
            )
            + cte_2.c.investment_income_total
            - func.lag(cte_2.c.investment_income_total, 1, 0.0).over(
                partition_by=[cte_2.c.portfolio_id, cte_2.c.asset_id],
                order_by=cte_2.c.date,
            )
        ).label("cash_flow_total"),
    ).cte(name="cte_3")

    cte_4 = select(
        cte_3,
        (
            func.exp(
                func.sum(func.ln(1 + cte_3.c.hpr)).over(
                    partition_by=[cte_3.c.portfolio_id, cte_3.c.asset_id],
                    order_by=cte_3.c.date,
                )
            )
        ).label("hpr_cumulative"),
        (cte_3.c.row_number / 365.0).label("years_passed"),
        func.nullif(cte_3.c.hpr, 0.0).label("hpr_non_zero"),
        (
            func.xirr(
                cte_3.c.date,
                cte_3.c.cash_flow,
                cte_3.c.market_value,
                cte_3.c.checkpoint_date,
            ).over(
                partition_by=[cte_3.c.portfolio_id, cte_3.c.asset_id],
                order_by=cte_3.c.date,
            )
        ).label("xirr_rate"),
        (
            func.xirr(
                cte_3.c.date,
                cte_3.c.cash_flow_total,
                cte_3.c.market_value,
                cte_3.c.checkpoint_date,
            ).over(
                partition_by=[cte_3.c.portfolio_id, cte_3.c.asset_id],
                order_by=cte_3.c.date,
            )
        ).label("xirr_rate_total"),
    ).cte(name="cte_4")

    cte_5 = select(
        cte_4,
        (
            func.max(cte_4.c.hpr_cumulative).over(
                partition_by=[cte_4.c.portfolio_id, cte_4.c.asset_id],
                order_by=cte_4.c.date,
            )
        ).label("past_maximum_hpr_cumulative"),
        (
            func.avg(cte_4.c.hpr_non_zero).over(
                partition_by=[cte_4.c.portfolio_id, cte_4.c.asset_id],
                order_by=cte_4.c.date,
            )
        ).label("hpr_non_zero_avg"),
        (
            func.stddev(cte_4.c.hpr_non_zero).over(
                partition_by=[cte_4.c.portfolio_id, cte_4.c.asset_id],
                order_by=cte_4.c.date,
            )
        ).label("hpr_non_zero_stddev"),
        (
            func.stddev(
                func.iif(cte_4.c.hpr_non_zero < 0, cte_4.c.hpr_non_zero, None)
            ).over(
                partition_by=[cte_4.c.portfolio_id, cte_4.c.asset_id],
                order_by=cte_4.c.date,
            )
        ).label("hpr_non_zero_stddev_d"),
        (
            func.count(cte_4.c.hpr_non_zero).over(
                partition_by=[cte_4.c.portfolio_id, cte_4.c.asset_id],
                order_by=cte_4.c.date,
            )
            * 365.0
            / cte_4.c.row_number
        ).label("avg_days_per_year"),
    ).cte(name="cte_5")

    query = select(
        cte_5.c.portfolio_id,
        cte_5.c.portfolio_group_id,
        cte_5.c.asset_id,
        cte_5.c.date,
        cte_5.c.unit_price,
        cte_5.c.unit_price_adj,
        cte_5.c.quantity,
        cte_5.c.delta_quantity,
        cte_5.c.market_value,
        cte_5.c.market_value_adj,
        cte_5.c.delta_quantity_value_adj,
        cte_5.c.invested_amount,
        cte_5.c.invested_amount_total,
        cte_5.c.asset_disposal_income,
        cte_5.c.asset_disposal_income_total,
        cte_5.c.asset_holding_income,
        cte_5.c.asset_holding_income_total,
        cte_5.c.investment_income,
        cte_5.c.investment_income_total,
        cte_5.c.profit,
        cte_5.c.profit_total,
        func.coalesce(cte_5.c.profit_percentage, 0.0).label("profit_percentage"),
        func.coalesce(cte_5.c.profit_percentage_total, 0.0).label(
            "profit_percentage_total"
        ),
        func.coalesce(
            (cte_5.c.market_value + cte_5.c.asset_disposal_income)
            / cte_5.c.past_maximum_value
            - 1,
            0.0,
        ).label("drawdown_value"),
        func.coalesce(
            (cte_5.c.market_value + cte_5.c.asset_disposal_income_total)
            / cte_5.c.past_maximum_value_total
            - 1,
            0.0,
        ).label("drawdown_value_total"),
        func.coalesce(
            (cte_5.c.profit - cte_5.c.past_maximum_profit) / cte_5.c.past_maximum_value,
            0.0,
        ).label("drawdown_profit"),
        func.coalesce(
            (cte_5.c.profit_total - cte_5.c.past_maximum_profit_total)
            / cte_5.c.past_maximum_value_total,
            0.0,
        ).label("drawdown_profit_total"),
        cte_5.c.hpr,
        (cte_5.c.hpr_cumulative / cte_5.c.past_maximum_hpr_cumulative - 1).label(
            "drawdown"
        ),
        (cte_5.c.hpr_cumulative - 1).label("twrr_rate_daily"),
        (func.pow(cte_5.c.hpr_cumulative, 1.0 / cte_5.c.years_passed) - 1).label(
            "twrr_rate_annualized"
        ),
        (cte_5.c.hpr_non_zero_avg / cte_5.c.hpr_non_zero_stddev).label(
            "sharpe_ratio_daily"
        ),
        (
            cte_5.c.hpr_non_zero_avg
            / cte_5.c.hpr_non_zero_stddev
            * func.pow(cte_5.c.avg_days_per_year, 0.5)
        ).label("sharpe_ratio_annualized"),
        (cte_5.c.hpr_non_zero_avg / cte_5.c.hpr_non_zero_stddev_d).label(
            "sortino_ratio_daily"
        ),
        (
            cte_5.c.hpr_non_zero_avg
            / cte_5.c.hpr_non_zero_stddev_d
            * func.pow(cte_5.c.avg_days_per_year, 0.5)
        ).label("sortino_ratio_annualized"),
        cte_5.c.xirr_rate,
        cte_5.c.xirr_rate_total,
    ).where(cte_5.c.date >= cte_5.c.checkpoint_date)

    return insert(PortfolioAssetPerformance).from_select(
        [
            "portfolio_id",
            "portfolio_group_id",
            "asset_id",
            "date",
            "unit_price",
            "unit_price_adj",
            "quantity",
            "delta_quantity",
            "market_value",
            "market_value_adj",
            "delta_quantity_value_adj",
            "invested_amount",
            "invested_amount_total",
            "asset_disposal_income",
            "asset_disposal_income_total",
            "asset_holding_income",
            "asset_holding_income_total",
            "investment_income",
            "investment_income_total",
            "profit",
            "profit_total",
            "profit_percentage",
            "profit_percentage_total",
            "drawdown_value",
            "drawdown_value_total",
            "drawdown_profit",
            "drawdown_profit_total",
            "hpr",
            "drawdown",
            "twrr_rate_daily",
            "twrr_rate_annualized",
            "sharpe_ratio_daily",
            "sharpe_ratio_annualized",
            "sortino_ratio_daily",
            "sortino_ratio_annualized",
            "xirr_rate",
            "xirr_rate_total",
        ],
        query,
    )
