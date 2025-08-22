from .portfolio_model import Portfolio


class PortfolioRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, portfolio):
        self.session.add(portfolio)
        self.session.flush()
        self.session.refresh(portfolio)
        return portfolio

    def get_one(self, id):
        return self.session.query(Portfolio).filter(Portfolio.id == id).first()

    def get_one_by_user_id_and_name(self, user_id, name):
        return (
            self.session.query(Portfolio)
            .filter(Portfolio.user_id == user_id, Portfolio.name == name)
            .first()
        )

    def get_all(self):
        return self.session.query(Portfolio).all()

    def update_one(self, portfolio):
        return self.session.merge(portfolio)

    def delete_one(self, portfolio):
        self.session.delete(portfolio)
        self.session.flush()
        return portfolio

    def delete_all(self):
        deleted_count = self.session.query(Portfolio).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
