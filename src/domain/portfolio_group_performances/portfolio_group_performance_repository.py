from .portfolio_group_performance_model import PortfolioGroupPerformance


class PortfolioGroupPerformanceRepository:
    def __init__(self, session):
        self.session = session

    def get_one(self, id):
        return (
            self.session.query(PortfolioGroupPerformance)
            .filter(PortfolioGroupPerformance.id == id)
            .first()
        )

    def get_many(self, portfolio_group_id):
        return (
            self.session.query(PortfolioGroupPerformance)
            .filter(PortfolioGroupPerformance.portfolio_group_id == portfolio_group_id)
            .all()
        )

    def get_all(self):
        return self.session.query(PortfolioGroupPerformance).all()

    def delete_one(self, portfolio_group_performance):
        self.session.delete(portfolio_group_performance)
        self.session.flush()
        return portfolio_group_performance

    def delete_all(self):
        deleted_count = self.session.query(PortfolioGroupPerformance).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
