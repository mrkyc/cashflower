from .portfolio_group_asset_model import PortfolioGroupAsset


class PortfolioGroupAssetRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, portfolio_group_asset):
        self.session.add(portfolio_group_asset)
        self.session.flush()
        self.session.refresh(portfolio_group_asset)
        return portfolio_group_asset

    def get_one(self, portfolio_group_id, asset_id):
        return (
            self.session.query(PortfolioGroupAsset)
            .filter(
                PortfolioGroupAsset.portfolio_group_id == portfolio_group_id,
                PortfolioGroupAsset.asset_id == asset_id,
            )
            .first()
        )

    def get_all(self):
        return self.session.query(PortfolioGroupAsset).all()

    def delete_one(self, portfolio_group_asset):
        self.session.delete(portfolio_group_asset)
        self.session.flush()
        return portfolio_group_asset

    def delete_all(self):
        deleted_count = self.session.query(PortfolioGroupAsset).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
