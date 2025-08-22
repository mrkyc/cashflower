from .portfolio_transaction_file_model import PortfolioTransactionFile
from .portfolio_transaction_file_repository import PortfolioTransactionFileRepository


class PortfolioTransactionFileService:
    def __init__(
        self, portfolio_transaction_file_repository: PortfolioTransactionFileRepository
    ):
        self.portfolio_transaction_file_repository = (
            portfolio_transaction_file_repository
        )

    def create_one(self, user_id, portfolio_id, name, currency, currency_pair_id):
        portfolio_transaction_file = PortfolioTransactionFile(
            user_id=user_id,
            portfolio_id=portfolio_id,
            name=name,
            currency=currency,
            currency_pair_id=currency_pair_id,
        )
        return self.portfolio_transaction_file_repository.create_one(
            portfolio_transaction_file=portfolio_transaction_file
        )

    def get_one(self, id):
        return self.portfolio_transaction_file_repository.get_one(id=id)

    def get_one_by_user_id_and_name(self, user_id, name):
        return self.portfolio_transaction_file_repository.get_one_by_user_id_and_name(
            user_id=user_id, name=name
        )

    def get_all(self):
        return self.portfolio_transaction_file_repository.get_all()

    def update_one(
        self,
        id,
        portfolio_id=None,
        currency=None,
        currency_pair_id=None,
    ):
        portfolio_transaction_file = self.get_one(id=id)
        if portfolio_transaction_file is None:
            return None
        else:
            if portfolio_id is not None:
                portfolio_transaction_file.portfolio_id = portfolio_id
            if currency is not None:
                portfolio_transaction_file.currency = currency
            if currency_pair_id is not None:
                portfolio_transaction_file.currency_pair_id = currency_pair_id

            return self.portfolio_transaction_file_repository.update_one(
                portfolio_transaction_file=portfolio_transaction_file
            )

    def upsert_one(self, user_id, portfolio_id, name, currency, currency_pair_id):
        portfolio_transaction_file = self.get_one_by_user_id_and_name(
            user_id=user_id, name=name
        )
        if portfolio_transaction_file:
            return self.update_one(
                id=portfolio_transaction_file.id,
                portfolio_id=portfolio_id,
                currency=currency,
                currency_pair_id=currency_pair_id,
            )
        else:
            return self.create_one(
                user_id=user_id,
                portfolio_id=portfolio_id,
                name=name,
                currency=currency,
                currency_pair_id=currency_pair_id,
            )

    def delete_one(self, id):
        portfolio_transaction_file = self.get_one(id=id)
        if portfolio_transaction_file is None:
            return None
        else:
            return self.portfolio_transaction_file_repository.delete_one(
                portfolio_transaction_file=portfolio_transaction_file
            )

    def delete_all(self):
        return self.portfolio_transaction_file_repository.delete_all()
