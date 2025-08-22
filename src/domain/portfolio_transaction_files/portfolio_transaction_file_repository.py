from .portfolio_transaction_file_model import PortfolioTransactionFile


class PortfolioTransactionFileRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, portfolio_transaction_file):
        self.session.add(portfolio_transaction_file)
        self.session.flush()
        self.session.refresh(portfolio_transaction_file)
        return portfolio_transaction_file

    def get_one(self, id):
        return (
            self.session.query(PortfolioTransactionFile)
            .filter(PortfolioTransactionFile.id == id)
            .first()
        )

    def get_one_by_user_id_and_name(self, user_id, name):
        return (
            self.session.query(PortfolioTransactionFile)
            .filter(
                PortfolioTransactionFile.user_id == user_id,
                PortfolioTransactionFile.name == name,
            )
            .first()
        )

    def get_all(self):
        return self.session.query(PortfolioTransactionFile).all()

    def update_one(self, portfolio_transaction_file):
        return self.session.merge(portfolio_transaction_file)

    def delete_one(self, portfolio_transaction_file):
        self.session.delete(portfolio_transaction_file)
        self.session.flush()
        return portfolio_transaction_file

    def delete_all(self):
        deleted_count = self.session.query(PortfolioTransactionFile).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
