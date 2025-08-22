from .asset_pricing_model import AssetPricing
from .asset_pricing_repository import AssetPricingRepository

from .complex_queries import *


class AssetPricingService:
    def __init__(self, asset_pricing_repository: AssetPricingRepository):
        self.asset_pricing_repository = asset_pricing_repository

    def create_many(
        self,
        asset_ids,
        dates,
        open_prices,
        high_prices,
        low_prices,
        close_prices,
        adjusted_close_prices,
    ):
        asset_pricing_data = zip(
            asset_ids,
            dates,
            open_prices,
            high_prices,
            low_prices,
            close_prices,
            adjusted_close_prices,
        )

        asset_pricings = [
            AssetPricing(
                asset_id=int(id),
                date=date,
                open_price=op,
                high_price=hp,
                low_price=lp,
                close_price=cp,
                adjusted_close_price=acp,
            )
            for id, date, op, hp, lp, cp, acp in asset_pricing_data
        ]

        return self.asset_pricing_repository.create_many(asset_pricings=asset_pricings)

    def get_one(self, id):
        return self.asset_pricing_repository.get_one(id=id)

    def get_all(self):
        return self.asset_pricing_repository.get_all()

    def update_one(
        self,
        id,
        date=None,
        open_price=None,
        high_price=None,
        low_price=None,
        close_price=None,
        adjusted_close_price=None,
    ):
        asset_pricing = self.get_one(id=id)
        if asset_pricing is None:
            return None
        else:
            if date is not None:
                asset_pricing.date = date
            if open_price is not None:
                asset_pricing.open_price = open_price
            if high_price is not None:
                asset_pricing.high_price = high_price
            if low_price is not None:
                asset_pricing.low_price = low_price
            if close_price is not None:
                asset_pricing.close_price = close_price
            if adjusted_close_price is not None:
                asset_pricing.adjusted_close_price = adjusted_close_price
            return self.asset_pricing_repository.update_one(asset_pricing=asset_pricing)

    def delete_one(self, id):
        asset_pricing = self.get_one(id=id)
        if asset_pricing is None:
            return None
        else:
            return self.asset_pricing_repository.delete_one(asset_pricing=asset_pricing)

    def delete_all(self):
        return self.asset_pricing_repository.delete_all()

    def delete_many_by_asset_id_and_date(self, asset_id):
        query = delete_many_by_asset_id_and_date(asset_id)
        return self.asset_pricing_repository.execute_custom_query(query)
