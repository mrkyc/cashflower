from .portfolio_model import Portfolio
from .portfolio_repository import PortfolioRepository


class PortfolioService:
    def __init__(self, portfolio_repository: PortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def create_one(self, user_id, portfolio_aggregate_id, name):
        portfolio = Portfolio(
            user_id=user_id, portfolio_aggregate_id=portfolio_aggregate_id, name=name
        )
        return self.portfolio_repository.create_one(portfolio=portfolio)

    def get_one(self, id):
        return self.portfolio_repository.get_one(id=id)

    def get_one_by_user_id_and_name(self, user_id, name):
        return self.portfolio_repository.get_one_by_user_id_and_name(
            user_id=user_id, name=name
        )

    def get_all(self):
        return self.portfolio_repository.get_all()

    def update_one(self, id, name=None):
        portfolio = self.get_one(id=id)
        if portfolio is None:
            return None
        else:
            if name is not None:
                portfolio.name = name
            return self.portfolio_repository.update_one(portfolio=portfolio)

    def delete_one(self, id):
        portfolio = self.get_one(id=id)
        if portfolio is None:
            return None
        else:
            return self.portfolio_repository.delete_one(portfolio=portfolio)

    def delete_all(self):
        return self.portfolio_repository.delete_all()
