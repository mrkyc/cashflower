from sqlalchemy import delete, exists

from src.domain.portfolio_aggregate_performances.portfolio_aggregate_performance_model import (
    PortfolioAggregatePerformance,
)
from src.domain.portfolio_aggregates.portfolio_aggregate_model import PortfolioAggregate


def delete_many_by_user_id_and_date(user_id: int):
    query = delete(PortfolioAggregatePerformance).where(
        exists().where(
            (
                PortfolioAggregate.id
                == PortfolioAggregatePerformance.portfolio_aggregate_id
            )
            & (PortfolioAggregate.user_id == user_id)
            & (PortfolioAggregatePerformance.date >= PortfolioAggregate.checkpoint_date)
        )
    )

    return query
