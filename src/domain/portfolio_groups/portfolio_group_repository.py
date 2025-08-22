from .portfolio_group_model import PortfolioGroup


class PortfolioGroupRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, portfolio_group):
        self.session.add(portfolio_group)
        self.session.flush()
        self.session.refresh(portfolio_group)
        return portfolio_group

    def get_one(self, id):
        return (
            self.session.query(PortfolioGroup).filter(PortfolioGroup.id == id).first()
        )

    def get_one_by_portfolio_id_and_name(self, portfolio_id, name):
        return (
            self.session.query(PortfolioGroup)
            .filter(
                PortfolioGroup.portfolio_id == portfolio_id, PortfolioGroup.name == name
            )
            .first()
        )

    def get_all(self):
        return self.session.query(PortfolioGroup).all()

    def update_one(self, portfolio_group):
        return self.session.merge(portfolio_group)

    def delete_one(self, portfolio_group):
        self.session.delete(portfolio_group)
        self.session.flush()
        return portfolio_group

    def delete_all(self):
        deleted_count = self.session.query(PortfolioGroup).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result

    def get_portfolio_groups_by_portfolio_id(self, portfolio_id):
        return (
            self.session.query(PortfolioGroup.name, PortfolioGroup.weight)
            .filter(PortfolioGroup.portfolio_id == portfolio_id)
            .all()
        )
