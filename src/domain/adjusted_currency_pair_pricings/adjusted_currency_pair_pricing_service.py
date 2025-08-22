from .adjusted_currency_pair_pricing_repository import (
    AdjustedCurrencyPairPricingRepository,
)
from .complex_queries import *


class AdjustedCurrencyPairPricingService:
    def __init__(
        self,
        adjusted_currency_pair_pricing_repository: AdjustedCurrencyPairPricingRepository,
    ):
        self.adjusted_currency_pair_pricing_repository = (
            adjusted_currency_pair_pricing_repository
        )

    def get_one(self, id):
        return self.adjusted_currency_pair_pricing_repository.get_one(id=id)

    def get_all(self):
        return self.adjusted_currency_pair_pricing_repository.get_all()

    def delete_one(self, id):
        adjusted_currency_pair_pricing = self.get_one(id=id)
        if adjusted_currency_pair_pricing:
            return self.adjusted_currency_pair_pricing_repository.delete_one(
                adjusted_currency_pair_pricing=adjusted_currency_pair_pricing
            )
        else:
            return None

    def delete_all(self):
        return self.adjusted_currency_pair_pricing_repository.delete_all()

    def delete_many_by_currency_pair_id_and_date(self, currency_pair_id):
        query = delete_many_by_currency_pair_id_and_date(currency_pair_id)
        return self.adjusted_currency_pair_pricing_repository.execute_custom_query(
            query=query
        )

    def insert_with_select(self, currency_pair_id):
        self.delete_many_by_currency_pair_id_and_date(currency_pair_id)
        query = insert_with_select(currency_pair_id)
        return self.adjusted_currency_pair_pricing_repository.execute_custom_query(
            query=query
        )
