from .portfolio_performance_model import PortfolioPerformance


class PortfolioPerformanceRepository:
    def __init__(self, session):
        self.session = session

    def get_one(self, id):
        return (
            self.session.query(PortfolioPerformance)
            .filter(PortfolioPerformance.id == id)
            .first()
        )

    def get_many(self, portfolio_id):
        return (
            self.session.query(PortfolioPerformance)
            .filter(PortfolioPerformance.portfolio_id == portfolio_id)
            .all()
        )

    def get_all(self):
        return self.session.query(PortfolioPerformance).all()

    def delete_one(self, portfolio_performance):
        self.session.delete(portfolio_performance)
        self.session.flush()
        return portfolio_performance

    def delete_all(self):
        deleted_count = self.session.query(PortfolioPerformance).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result

    def get_market_values_by_portfolio_id(self, portfolio_id):
        return (
            self.session.query(
                PortfolioPerformance.date,
                PortfolioPerformance.market_value,
            )
            .filter(PortfolioPerformance.portfolio_id == portfolio_id)
            .all()
        )
