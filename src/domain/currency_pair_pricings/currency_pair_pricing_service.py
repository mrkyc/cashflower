from .currency_pair_pricing_model import CurrencyPairPricing
from .currency_pair_pricing_repository import CurrencyPairPricingRepository

from .complex_queries import *


class CurrencyPairPricingService:
    def __init__(self, currency_pair_pricing_repository: CurrencyPairPricingRepository):
        self.currency_pair_pricing_repository = currency_pair_pricing_repository

    def create_many(
        self,
        currency_pair_ids,
        dates,
        open_prices,
        high_prices,
        low_prices,
        close_prices,
    ):
        currency_pair_pricing_data = zip(
            currency_pair_ids, dates, open_prices, high_prices, low_prices, close_prices
        )

        currency_pair_pricings = [
            CurrencyPairPricing(
                currency_pair_id=int(id),
                date=date,
                open_price=op,
                high_price=hp,
                low_price=lp,
                close_price=cp,
            )
            for id, date, op, hp, lp, cp in currency_pair_pricing_data
        ]

        return self.currency_pair_pricing_repository.create_many(
            currency_pair_pricings=currency_pair_pricings
        )

    def get_one(self, id):
        return self.currency_pair_pricing_repository.get_one(id=id)

    def get_all(self):
        return self.currency_pair_pricing_repository.get_all()

    def update_one(
        self,
        id,
        date=None,
        open_price=None,
        high_price=None,
        low_price=None,
        close_price=None,
    ):
        currency_pair_pricing = self.get_one(id=id)
        if currency_pair_pricing is None:
            return None
        else:
            if date is not None:
                currency_pair_pricing.date = date
            if open_price is not None:
                currency_pair_pricing.open_price = open_price
            if high_price is not None:
                currency_pair_pricing.high_price = high_price
            if low_price is not None:
                currency_pair_pricing.low_price = low_price
            if close_price is not None:
                currency_pair_pricing.close_price = close_price
            return self.currency_pair_pricing_repository.update_one(
                currency_pair_pricing=currency_pair_pricing
            )

    def delete_one(self, id):
        currency_pair_pricing = self.get_one(id=id)
        if currency_pair_pricing is None:
            return None
        else:
            return self.currency_pair_pricing_repository.delete_one(
                currency_pair_pricing=currency_pair_pricing
            )

    def delete_all(self):
        return self.currency_pair_pricing_repository.delete_all()

    def delete_many_by_currency_pair_id_and_date(self, currency_pair_id):
        query = delete_many_by_currency_pair_id_and_date(currency_pair_id)
        return self.currency_pair_pricing_repository.execute_custom_query(query)
