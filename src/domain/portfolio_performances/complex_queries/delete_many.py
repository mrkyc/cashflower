from sqlalchemy import delete, exists

from src.domain.portfolio_performances.portfolio_performance_model import (
    PortfolioPerformance,
)
from src.domain.portfolios.portfolio_model import Portfolio
from src.domain.portfolio_aggregates.portfolio_aggregate_model import PortfolioAggregate


def delete_many_by_user_id_and_date(user_id: int):
    query = delete(PortfolioPerformance).where(
        exists().where(
            (Portfolio.id == PortfolioPerformance.portfolio_id)
            & (PortfolioAggregate.id == Portfolio.portfolio_aggregate_id)
            & (PortfolioAggregate.user_id == user_id)
            & (PortfolioPerformance.date >= PortfolioAggregate.checkpoint_date)
        )
    )

    return query
