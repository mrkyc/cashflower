from .adjusted_portfolio_transaction_repository import (
    AdjustedPortfolioTransactionRepository,
)
from .complex_queries import *


class AdjustedPortfolioTransactionService:
    def __init__(
        self,
        adjusted_portfolio_transaction_repository: AdjustedPortfolioTransactionRepository,
    ):
        self.adjusted_portfolio_transaction_repository = (
            adjusted_portfolio_transaction_repository
        )

    def get_one(self, id):
        return self.adjusted_portfolio_transaction_repository.get_one(id=id)

    def get_all(self):
        return self.adjusted_portfolio_transaction_repository.get_all()

    def delete_one(self, id):
        adjusted_portfolio_transaction = self.get_one(id=id)
        if adjusted_portfolio_transaction is None:
            return None
        else:
            return self.adjusted_portfolio_transaction_repository.delete_one(
                adjusted_portfolio_transaction=adjusted_portfolio_transaction
            )

    def delete_all(self):
        return self.adjusted_portfolio_transaction_repository.delete_all()

    def delete_many_by_user_id(self, user_id: int):
        query = delete_many_by_user_id(user_id=user_id)
        return self.adjusted_portfolio_transaction_repository.execute_custom_query(
            query=query
        )

    def insert_with_select(self, user_id: int):
        self.delete_many_by_user_id(user_id)
        query = insert_with_select(user_id)
        return self.adjusted_portfolio_transaction_repository.execute_custom_query(
            query=query
        )
