from .adjusted_asset_pricing_model import AdjustedAssetPricing


class AdjustedAssetPricingRepository:
    def __init__(self, session):
        self.session = session

    def get_one(self, id):
        return (
            self.session.query(AdjustedAssetPricing)
            .filter(AdjustedAssetPricing.id == id)
            .first()
        )

    def get_all(self):
        return self.session.query(AdjustedAssetPricing).all()

    def delete_one(self, adjusted_asset_pricing):
        self.session.delete(adjusted_asset_pricing)
        self.session.flush()
        return adjusted_asset_pricing

    def delete_all(self):
        deleted_count = self.session.query(AdjustedAssetPricing).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
