from .portfolio_transaction_model import PortfolioTransaction
from .portfolio_transaction_repository import PortfolioTransactionRepository


class PortfolioTransactionService:
    def __init__(
        self, portfolio_transaction_repository: PortfolioTransactionRepository
    ):
        self.portfolio_transaction_repository = portfolio_transaction_repository

    def create_one(
        self,
        portfolio_transaction_file_id,
        asset_id,
        date,
        transaction_type,
        quantity,
        transaction_value,
        fee_amount,
        tax_amount,
    ):
        portfolio_transaction = PortfolioTransaction(
            portfolio_transaction_file_id=portfolio_transaction_file_id,
            asset_id=asset_id,
            date=date,
            transaction_type=transaction_type,
            quantity=quantity,
            transaction_value=transaction_value,
            fee_amount=fee_amount,
            tax_amount=tax_amount,
        )

        return self.portfolio_transaction_repository.create_one(
            portfolio_transaction=portfolio_transaction
        )

    def get_one(self, id):
        return self.portfolio_transaction_repository.get_one(id=id)

    def get_all(self):
        return self.portfolio_transaction_repository.get_all()

    def delete_one(self, id):
        portfolio_transaction = self.get_one(id=id)
        if portfolio_transaction is None:
            return None
        else:
            return self.portfolio_transaction_repository.delete_one(
                portfolio_transaction=portfolio_transaction
            )

    def delete_many_by_file_id(self, transaction_file_id: int):
        return self.portfolio_transaction_repository.delete_many_by_file_id(
            transaction_file_id
        )
