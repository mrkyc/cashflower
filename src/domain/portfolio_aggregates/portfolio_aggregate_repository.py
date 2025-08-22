from .portfolio_aggregate_model import PortfolioAggregate


class PortfolioAggregateRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, portfolio_aggregate):
        self.session.add(portfolio_aggregate)
        self.session.flush()
        self.session.refresh(portfolio_aggregate)
        return portfolio_aggregate

    def get_one(self, id):
        return (
            self.session.query(PortfolioAggregate)
            .filter(PortfolioAggregate.id == id)
            .first()
        )

    def get_one_by_user_id(self, user_id):
        return (
            self.session.query(PortfolioAggregate)
            .filter(PortfolioAggregate.user_id == user_id)
            .first()
        )

    def get_all(self):
        return self.session.query(PortfolioAggregate).all()

    def update_one(self, portfolio_aggregate):
        return self.session.merge(portfolio_aggregate)

    def delete_one(self, portfolio_aggregate):
        self.session.delete(portfolio_aggregate)
        self.session.flush()
        return portfolio_aggregate

    def delete_all(self):
        deleted_count = self.session.query(PortfolioAggregate).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
