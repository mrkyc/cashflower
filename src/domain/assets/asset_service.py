from .asset_model import Asset
from .asset_repository import AssetRepository


class AssetService:
    def __init__(self, asset_repository: AssetRepository):
        self.asset_repository = asset_repository

    def create_one(self, symbol, name, currency):
        asset = Asset(
            symbol=symbol,
            name=name,
            currency=currency,
        )
        return self.asset_repository.create_one(asset=asset)

    def get_one(self, id):
        return self.asset_repository.get_one(id=id)

    def get_one_by_symbol(self, symbol):
        return self.asset_repository.get_one_by_symbol(symbol=symbol)

    def get_one_by_name(self, name):
        return self.asset_repository.get_one_by_name(name=name)

    def get_all(self):
        return self.asset_repository.get_all()

    def update_one(
        self,
        id,
        name=None,
        currency=None,
        first_pricing_date=None,
        last_pricing_date=None,
    ):
        asset = self.get_one(id=id)
        if asset is None:
            return None
        else:
            if name is not None:
                asset.name = name
            if currency is not None:
                asset.currency = currency
            if first_pricing_date is not None:
                asset.first_pricing_date = first_pricing_date
            if last_pricing_date is not None:
                asset.last_pricing_date = last_pricing_date
            return self.asset_repository.update_one(asset=asset)

    def upsert_one(self, symbol, name, currency):
        asset = self.get_one_by_symbol(symbol=symbol)
        if asset:
            return asset
        else:
            return self.create_one(
                symbol=symbol,
                name=name,
                currency=currency,
            )

    def delete_one(self, id):
        asset = self.get_one(id=id)
        if asset is None:
            return None
        else:
            return self.asset_repository.delete_one(asset=asset)

    def delete_all(self):
        return self.asset_repository.delete_all()

    def get_assets_last_pricing_dates(self):
        return self.asset_repository.get_assets_last_pricing_dates()
