from .portfolio_asset_performance_model import PortfolioAssetPerformance


class PortfolioAssetPerformanceRepository:
    def __init__(self, session):
        self.session = session

    def get_one(self, id):
        return (
            self.session.query(PortfolioAssetPerformance)
            .filter(PortfolioAssetPerformance.id == id)
            .first()
        )

    def get_many(self, portfolio_id, asset_id):
        return (
            self.session.query(PortfolioAssetPerformance)
            .filter(
                PortfolioAssetPerformance.portfolio_id == portfolio_id,
                PortfolioAssetPerformance.asset_id == asset_id,
            )
            .all()
        )

    def get_all(self):
        return self.session.query(PortfolioAssetPerformance).all()

    def delete_one(self, portfolio_asset_performance):
        self.session.delete(portfolio_asset_performance)
        self.session.flush()
        return portfolio_asset_performance

    def delete_all(self):
        deleted_count = self.session.query(PortfolioAssetPerformance).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
