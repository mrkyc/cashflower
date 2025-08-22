from sqlalchemy import (
    select,
    and_,
    func,
)

from src.domain.portfolio_asset_performances.portfolio_asset_performance_model import (
    PortfolioAssetPerformance,
)
from src.domain.assets.asset_model import Asset
from src.domain.portfolio_groups.portfolio_group_model import PortfolioGroup


def get_assets_status_by_portfolio_id(portfolio_id):
    cte = select(func.max(PortfolioAssetPerformance.date).label("max_date")).cte("cte")

    query = (
        select(
            PortfolioGroup.name.label("portfolio_group_name"),
            PortfolioGroup.weight.label("model_weight"),
            Asset.name.label("asset_name"),
            PortfolioAssetPerformance.unit_price,
            PortfolioAssetPerformance.quantity,
            PortfolioAssetPerformance.market_value,
        )
        .join_from(
            PortfolioAssetPerformance,
            Asset,
            Asset.id == PortfolioAssetPerformance.asset_id,
        )
        .join(
            PortfolioGroup,
            PortfolioGroup.id == PortfolioAssetPerformance.portfolio_group_id,
        )
        .where(
            and_(
                PortfolioAssetPerformance.portfolio_id == portfolio_id,
                PortfolioAssetPerformance.date == cte.c.max_date,
            )
        )
    )

    return query
