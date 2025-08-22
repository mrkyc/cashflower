from sqlalchemy import delete, exists

from src.domain.currency_pair_pricings.currency_pair_pricing_model import (
    CurrencyPairPricing,
)
from src.domain.currency_pairs.currency_pair_model import CurrencyPair


def delete_many_by_currency_pair_id_and_date(currency_pair_id: int):
    query = delete(CurrencyPairPricing).where(
        exists().where(
            (CurrencyPair.id == CurrencyPairPricing.currency_pair_id)
            & (CurrencyPairPricing.currency_pair_id == currency_pair_id)
            & (CurrencyPairPricing.date >= CurrencyPair.last_pricing_date)
        )
    )

    return query
