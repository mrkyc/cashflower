from .portfolio_transaction_model import PortfolioTransaction


class PortfolioTransactionRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, portfolio_transaction):
        self.session.add(portfolio_transaction)
        self.session.flush()
        self.session.refresh(portfolio_transaction)
        return portfolio_transaction

    def get_one(self, id):
        return (
            self.session.query(PortfolioTransaction)
            .filter(PortfolioTransaction.id == id)
            .first()
        )

    def get_all(self):
        return self.session.query(PortfolioTransaction).all()

    def update_one(self, portfolio_transaction):
        return self.session.merge(portfolio_transaction)

    def delete_one(self, portfolio_transaction):
        self.session.delete(portfolio_transaction)
        self.session.flush()
        return portfolio_transaction

    def delete_many_by_file_id(self, transaction_file_id: int):
        deleted_count = (
            self.session.query(PortfolioTransaction)
            .filter(
                PortfolioTransaction.portfolio_transaction_file_id
                == transaction_file_id
            )
            .delete()
        )
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
