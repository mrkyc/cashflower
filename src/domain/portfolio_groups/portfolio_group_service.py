from .portfolio_group_model import PortfolioGroup
from .portfolio_group_repository import PortfolioGroupRepository


class PortfolioGroupService:
    def __init__(self, portfolio_group_repository: PortfolioGroupRepository):
        self.portfolio_group_repository = portfolio_group_repository

    def create_one(
        self,
        user_id,
        portfolio_id,
        name,
        weight,
    ):
        portfolio_group = PortfolioGroup(
            user_id=user_id,
            portfolio_id=portfolio_id,
            name=name,
            weight=weight,
        )
        return self.portfolio_group_repository.create_one(
            portfolio_group=portfolio_group
        )

    def get_one(self, id):
        return self.portfolio_group_repository.get_one(id=id)

    def get_one_by_portfolio_id_and_name(self, portfolio_id, name):
        return self.portfolio_group_repository.get_one_by_portfolio_id_and_name(
            portfolio_id=portfolio_id, name=name
        )

    def get_all(self):
        return self.portfolio_group_repository.get_all()

    def delete_one(self, id):
        portfolio_group = self.get_one(id=id)
        if portfolio_group is None:
            return None
        else:
            return self.portfolio_group_repository.delete_one(id=id)

    def delete_all(self):
        return self.portfolio_group_repository.delete_all()

    def get_portfolio_groups_by_portfolio_id(self, portfolio_id):
        return self.portfolio_group_repository.get_portfolio_groups_by_portfolio_id(
            portfolio_id=portfolio_id
        )
