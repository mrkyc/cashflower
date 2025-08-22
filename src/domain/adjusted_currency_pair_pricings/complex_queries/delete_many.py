from sqlalchemy import delete, exists

from src.domain.currency_pairs.currency_pair_model import CurrencyPair
from src.domain.adjusted_currency_pair_pricings.adjusted_currency_pair_pricing_model import (
    AdjustedCurrencyPairPricing,
)


def delete_many_by_currency_pair_id_and_date(currency_pair_id):
    query = delete(AdjustedCurrencyPairPricing).where(
        exists().where(
            (CurrencyPair.id == AdjustedCurrencyPairPricing.currency_pair_id)
            & (AdjustedCurrencyPairPricing.currency_pair_id == currency_pair_id)
            & (AdjustedCurrencyPairPricing.date >= CurrencyPair.last_pricing_date)
        )
    )

    return query
