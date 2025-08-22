from .portfolio_group_asset_model import PortfolioGroupAsset
from .portfolio_group_asset_repository import PortfolioGroupAssetRepository


class PortfolioGroupAssetService:
    def __init__(self, portfolio_group_asset_repository: PortfolioGroupAssetRepository):
        self.portfolio_group_asset_repository = portfolio_group_asset_repository

    def create_one(
        self,
        portfolio_group_id,
        asset_id,
    ):
        portfolio_group_asset = PortfolioGroupAsset(
            portfolio_group_id=portfolio_group_id,
            asset_id=asset_id,
        )
        return self.portfolio_group_asset_repository.create_one(
            portfolio_group_asset=portfolio_group_asset
        )

    def get_one(self, portfolio_group_id, asset_id):
        return self.portfolio_group_asset_repository.get_one(
            portfolio_group_id=portfolio_group_id, asset_id=asset_id
        )

    def get_all(self):
        return self.portfolio_group_asset_repository.get_all()

    def delete_one(self, portfolio_group_id, asset_id):
        portfolio_group_asset = self.get_one(
            portfolio_group_id=portfolio_group_id, asset_id=asset_id
        )
        if portfolio_group_asset is None:
            return None
        else:
            return self.portfolio_group_asset_repository.delete_one(
                portfolio_group_asset=portfolio_group_asset
            )

    def delete_all(self):
        return self.portfolio_group_asset_repository.delete_all()
