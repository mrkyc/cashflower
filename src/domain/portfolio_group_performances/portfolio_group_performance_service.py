from .portfolio_group_performance_repository import PortfolioGroupPerformanceRepository
from .complex_queries import *


class PortfolioGroupPerformanceService:
    def __init__(
        self,
        portfolio_group_performance_repository: PortfolioGroupPerformanceRepository,
    ):
        self.portfolio_group_performance_repository = (
            portfolio_group_performance_repository
        )

    def get_one(self, id):
        return self.portfolio_group_performance_repository.get_one(id=id)

    def get_all(self):
        return self.portfolio_group_performance_repository.get_all()

    def delete_one(self, id):
        portfolio_group_performance = self.get_one(id=id)
        if portfolio_group_performance is None:
            return None
        else:
            return self.portfolio_group_performance_repository.delete_one(
                portfolio_group_performance=portfolio_group_performance
            )

    def delete_all(self):
        return self.portfolio_group_performance_repository.delete_all()

    def delete_many_by_user_id_and_date(self, user_id: int):
        query = delete_many_by_user_id_and_date(user_id)
        return self.portfolio_group_performance_repository.execute_custom_query(
            query=query
        )

    def insert_with_select(self, user_id: int):
        self.delete_many_by_user_id_and_date(user_id)
        query = insert_with_select(user_id)
        return self.portfolio_group_performance_repository.execute_custom_query(
            query=query
        )

    def get_performance_by_portfolio_group_id(self, portfolio_group_id):
        return self.portfolio_group_performance_repository.get_many(
            portfolio_group_id=portfolio_group_id
        )

    def get_performance_status(self, portfolio_group_id, status_date):
        query = get_performance_status(
            portfolio_group_id=portfolio_group_id, status_date=status_date
        )
        return (
            self.portfolio_group_performance_repository.execute_custom_query(
                query=query
            )
            .mappings()
            .all()
        )

    def get_weights_by_portfolio_id(self, portfolio_id):
        query = get_weights_by_portfolio_id(portfolio_id=portfolio_id)
        return (
            self.portfolio_group_performance_repository.execute_custom_query(
                query=query
            )
            .mappings()
            .all()
        )
