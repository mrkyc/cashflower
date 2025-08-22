from .portfolio_performance_repository import PortfolioPerformanceRepository
from .complex_queries import *


class PortfolioPerformanceService:
    def __init__(
        self, portfolio_performance_repository: PortfolioPerformanceRepository
    ):
        self.portfolio_performance_repository = portfolio_performance_repository

    def get_one(self, id):
        return self.portfolio_performance_repository.get_one(id=id)

    def get_all(self):
        return self.portfolio_performance_repository.get_all()

    def delete_one(self, id):
        portfolio_performance = self.get_one(id=id)
        if portfolio_performance is None:
            return None
        else:
            return self.portfolio_performance_repository.delete_one(
                portfolio_performance=portfolio_performance
            )

    def delete_all(self):
        return self.portfolio_performance_repository.delete_all()

    def delete_many_by_user_id_and_date(self, user_id: int):
        query = delete_many_by_user_id_and_date(user_id)
        return self.portfolio_performance_repository.execute_custom_query(query=query)

    def insert_with_select(self, user_id: int):
        self.delete_many_by_user_id_and_date(user_id)
        query = insert_with_select(user_id)
        return self.portfolio_performance_repository.execute_custom_query(query=query)

    def get_performance_by_portfolio_id(self, portfolio_id):
        return self.portfolio_performance_repository.get_many(portfolio_id=portfolio_id)

    def get_performance_status(self, portfolio_id, status_date):
        query = get_performance_status(
            portfolio_id=portfolio_id, status_date=status_date
        )
        return (
            self.portfolio_performance_repository.execute_custom_query(query=query)
            .mappings()
            .all()
        )

    def get_market_values_by_portfolio_id(self, portfolio_id):
        return self.portfolio_performance_repository.get_market_values_by_portfolio_id(
            portfolio_id=portfolio_id
        )
