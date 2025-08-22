from .portfolio_aggregate_model import PortfolioAggregate
from .portfolio_aggregate_repository import PortfolioAggregateRepository
from .complex_queries import *


class PortfolioAggregateService:
    def __init__(self, portfolio_aggregate_repository: PortfolioAggregateRepository):
        self.portfolio_aggregate_repository = portfolio_aggregate_repository

    def create_one(self, user_id):
        portfolio_aggregate = PortfolioAggregate(user_id=user_id)
        return self.portfolio_aggregate_repository.create_one(
            portfolio_aggregate=portfolio_aggregate
        )

    def get_one(self, id):
        return self.portfolio_aggregate_repository.get_one(id=id)

    def get_one_by_user_id(self, user_id):
        return self.portfolio_aggregate_repository.get_one_by_user_id(user_id=user_id)

    def get_all(self):
        return self.portfolio_aggregate_repository.get_all()

    def update_one(self, id, checkpoint_date=None):
        portfolio_aggregate = self.get_one(id=id)
        if portfolio_aggregate is None:
            return None
        else:
            if checkpoint_date is not None:
                portfolio_aggregate.checkpoint_date = checkpoint_date
            return self.portfolio_aggregate_repository.update_one(
                portfolio_aggregate=portfolio_aggregate
            )

    def update_checkpoint_date(self, user_id):
        query = update_checkpoint_date(user_id=user_id)
        return self.portfolio_aggregate_repository.execute_custom_query(query=query)

    def delete_one(self, id):
        portfolio_aggregate = self.get_one(id=id)
        if portfolio_aggregate is None:
            return None
        else:
            return self.portfolio_aggregate_repository.delete_one(
                portfolio_aggregate=portfolio_aggregate
            )

    def delete_all(self):
        return self.portfolio_aggregate_repository.delete_all()

    def get_portfolio_variants(self, user_id: int):
        query = get_portfolio_variants(user_id)
        return (
            self.portfolio_aggregate_repository.execute_custom_query(query=query)
            .mappings()
            .all()
        )
