from src.domain.assets.asset_model import Asset


class AssetRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, asset):
        self.session.add(asset)
        self.session.flush()
        self.session.refresh(asset)
        return asset

    def get_one(self, id):
        return self.session.query(Asset).filter(Asset.id == id).first()

    def get_one_by_name(self, name):
        return self.session.query(Asset).filter(Asset.name == name).first()

    def get_one_by_symbol(self, symbol):
        return self.session.query(Asset).filter(Asset.symbol == symbol).first()

    def get_all(self):
        return self.session.query(Asset).all()

    def update_one(self, asset):
        return self.session.merge(asset)

    def delete_one(self, asset):
        self.session.delete(asset)
        self.session.flush()
        return asset

    def delete_all(self):
        deleted_count = self.session.query(Asset).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result

    def get_assets_last_pricing_dates(self):
        return self.session.query(
            Asset.name,
            Asset.symbol,
            Asset.last_pricing_date,
        ).all()
