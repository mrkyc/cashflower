from .adjusted_asset_pricing_repository import AdjustedAssetPricingRepository
from .complex_queries import *


class AdjustedAssetPricingService:
    def __init__(
        self, adjusted_asset_pricing_repository: AdjustedAssetPricingRepository
    ):
        self.adjusted_asset_pricing_repository = adjusted_asset_pricing_repository

    def get_one(self, id):
        return self.adjusted_asset_pricing_repository.get_one(id=id)

    def get_all(self):
        return self.adjusted_asset_pricing_repository.get_all()

    def delete_one(self, id):
        adjusted_asset_pricing = self.get_one(id=id)
        if adjusted_asset_pricing is None:
            return None
        else:
            return self.adjusted_asset_pricing_repository.delete_one(id=id)

    def delete_all(self):
        return self.adjusted_asset_pricing_repository.delete_all()

    def delete_many_by_asset_id_and_date(self, asset_id):
        query = delete_many_by_asset_id_and_date(asset_id)
        return self.adjusted_asset_pricing_repository.execute_custom_query(query=query)

    def insert_with_select(self, asset_id):
        self.delete_many_by_asset_id_and_date(asset_id)
        query = insert_with_select(asset_id)
        return self.adjusted_asset_pricing_repository.execute_custom_query(query=query)
