from sqlalchemy import select, func

from src.domain.portfolio_group_performances.portfolio_group_performance_model import (
    PortfolioGroupPerformance,
)
from src.domain.portfolio_groups.portfolio_group_model import PortfolioGroup


def get_weights_by_portfolio_id(portfolio_id):
    cte = (
        select(
            PortfolioGroupPerformance.portfolio_group_id,
            PortfolioGroupPerformance.date,
            (
                PortfolioGroupPerformance.market_value
                / func.sum(PortfolioGroupPerformance.market_value).over(
                    partition_by=[PortfolioGroupPerformance.date],
                )
                * 100
            ).label("weight"),
        )
        .where(PortfolioGroupPerformance.portfolio_id == portfolio_id)
        .cte("cte")
    )

    query = select(
        PortfolioGroup.name.label("portfolio_group_name"),
        PortfolioGroup.weight.label("model_weight"),
        cte.c.date,
        cte.c.weight,
        (cte.c.weight - PortfolioGroup.weight).label("weight_deviation"),
    ).join_from(cte, PortfolioGroup, PortfolioGroup.id == cte.c.portfolio_group_id)

    return query
