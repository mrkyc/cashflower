from .asset_pricing_model import AssetPricing


class AssetPricingRepository:
    def __init__(self, session):
        self.session = session

    def create_many(self, asset_pricings):
        self.session.add_all(asset_pricings)
        self.session.flush()
        for asset_pricing in asset_pricings:
            self.session.refresh(asset_pricing)
        return asset_pricings

    def get_one(self, id):
        return self.session.query(AssetPricing).filter(AssetPricing.id == id).first()

    def get_all(self):
        return self.session.query(AssetPricing).all()

    def update_one(self, asset_pricing):
        return self.session.merge(asset_pricing)

    def delete_one(self, asset_pricing):
        self.session.delete(asset_pricing)
        self.session.flush()
        return asset_pricing

    def delete_all(self):
        deleted_count = self.session.query(AssetPricing).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
