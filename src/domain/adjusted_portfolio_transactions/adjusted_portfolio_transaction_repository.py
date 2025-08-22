from .adjusted_portfolio_transaction_model import AdjustedPortfolioTransaction


class AdjustedPortfolioTransactionRepository:
    def __init__(self, session):
        self.session = session

    def get_one(self, id):
        return (
            self.session.query(AdjustedPortfolioTransaction)
            .filter(AdjustedPortfolioTransaction.id == id)
            .first()
        )

    def get_all(self):
        return self.session.query(AdjustedPortfolioTransaction).all()

    def delete_one(self, adjusted_portfolio_transaction):
        self.session.delete(adjusted_portfolio_transaction)
        self.session.flush()
        return adjusted_portfolio_transaction

    def delete_all(self):
        deleted_count = self.session.query(AdjustedPortfolioTransaction).delete()
        self.session.flush()
        return deleted_count

    def delete_many_by_user_id(self, user_id: int):
        deleted_count = (
            self.session.query(AdjustedPortfolioTransaction)
            .filter(
                AdjustedPortfolioTransaction.portfolio_transaction_file.user_id
                == user_id
            )
            .delete()
        )
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
