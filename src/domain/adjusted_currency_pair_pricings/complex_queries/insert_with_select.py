from sqlalchemy import select, insert, and_, func

from src.domain.currency_pairs.currency_pair_model import CurrencyPair
from src.domain.adjusted_currency_pair_pricings.adjusted_currency_pair_pricing_model import (
    AdjustedCurrencyPairPricing,
)
from src.domain.currency_pair_pricings.currency_pair_pricing_model import (
    CurrencyPairPricing,
)


def insert_with_select(currency_pair_id):
    cte_currency_pair_continuous_dates = (
        select(
            CurrencyPair.id.label("currency_pair_id"),
            func.max(
                CurrencyPair.first_pricing_date,
                CurrencyPair.last_pricing_date,
            ).label("date"),
        )
        .where(CurrencyPair.id == currency_pair_id)
        .cte(name="cte_currency_pair_min_dates", recursive=True)
    )

    cte_currency_pair_continuous_dates = cte_currency_pair_continuous_dates.union_all(
        select(
            cte_currency_pair_continuous_dates.c.currency_pair_id,
            func.date(cte_currency_pair_continuous_dates.c.date, "+1 day").label(
                "date"
            ),
        ).where(cte_currency_pair_continuous_dates.c.date < func.date("now"))
    )

    query = select(
        cte_currency_pair_continuous_dates.c.currency_pair_id,
        cte_currency_pair_continuous_dates.c.date,
        func.coalesce(
            CurrencyPairPricing.open_price,
            select(CurrencyPairPricing.open_price)
            .where(
                CurrencyPairPricing.date < cte_currency_pair_continuous_dates.c.date,
                CurrencyPairPricing.currency_pair_id
                == cte_currency_pair_continuous_dates.c.currency_pair_id,
            )
            .order_by(CurrencyPairPricing.date.desc())
            .correlate(cte_currency_pair_continuous_dates)
            .scalar_subquery(),
            0.0,
        ).label("open_price"),
        func.coalesce(
            CurrencyPairPricing.high_price,
            select(CurrencyPairPricing.high_price)
            .where(
                CurrencyPairPricing.date < cte_currency_pair_continuous_dates.c.date,
                CurrencyPairPricing.currency_pair_id
                == cte_currency_pair_continuous_dates.c.currency_pair_id,
            )
            .order_by(CurrencyPairPricing.date.desc())
            .correlate(cte_currency_pair_continuous_dates)
            .scalar_subquery(),
            0.0,
        ).label("high_price"),
        func.coalesce(
            CurrencyPairPricing.low_price,
            select(CurrencyPairPricing.low_price)
            .where(
                CurrencyPairPricing.date < cte_currency_pair_continuous_dates.c.date,
                CurrencyPairPricing.currency_pair_id
                == cte_currency_pair_continuous_dates.c.currency_pair_id,
            )
            .order_by(CurrencyPairPricing.date.desc())
            .correlate(cte_currency_pair_continuous_dates)
            .scalar_subquery(),
            0.0,
        ).label("low_price"),
        func.coalesce(
            CurrencyPairPricing.close_price,
            select(CurrencyPairPricing.close_price)
            .where(
                CurrencyPairPricing.date < cte_currency_pair_continuous_dates.c.date,
                CurrencyPairPricing.currency_pair_id
                == cte_currency_pair_continuous_dates.c.currency_pair_id,
            )
            .order_by(CurrencyPairPricing.date.desc())
            .correlate(cte_currency_pair_continuous_dates)
            .scalar_subquery(),
            0.0,
        ).label("close_price"),
    ).outerjoin_from(
        cte_currency_pair_continuous_dates,
        CurrencyPairPricing,
        and_(
            cte_currency_pair_continuous_dates.c.currency_pair_id
            == CurrencyPairPricing.currency_pair_id,
            cte_currency_pair_continuous_dates.c.date == CurrencyPairPricing.date,
        ),
    )

    return insert(AdjustedCurrencyPairPricing).from_select(
        [
            "currency_pair_id",
            "date",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
        ],
        query,
    )
