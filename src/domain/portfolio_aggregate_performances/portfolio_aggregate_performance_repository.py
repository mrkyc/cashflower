from .portfolio_aggregate_performance_model import PortfolioAggregatePerformance


class PortfolioAggregatePerformanceRepository:
    def __init__(self, session):
        self.session = session

    def get_one(self, id):
        return (
            self.session.query(PortfolioAggregatePerformance)
            .filter(PortfolioAggregatePerformance.id == id)
            .first()
        )

    def get_many(self, portfolio_aggregate_id):
        return (
            self.session.query(PortfolioAggregatePerformance)
            .filter(
                PortfolioAggregatePerformance.portfolio_aggregate_id
                == portfolio_aggregate_id
            )
            .all()
        )

    def get_all(self):
        return self.session.query(PortfolioAggregatePerformance).all()

    def delete_one(self, portfolio_aggregate_performance):
        self.session.delete(portfolio_aggregate_performance)
        self.session.flush()
        return portfolio_aggregate_performance

    def delete_all(self):
        deleted_count = self.session.query(PortfolioAggregatePerformance).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
