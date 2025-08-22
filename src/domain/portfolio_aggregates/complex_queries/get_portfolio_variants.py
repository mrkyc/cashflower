from sqlalchemy import select

from src.domain.portfolio_aggregates.portfolio_aggregate_model import PortfolioAggregate
from src.domain.portfolios.portfolio_model import Portfolio
from src.domain.portfolio_groups.portfolio_group_model import PortfolioGroup
from src.domain.portfolio_group_assets.portfolio_group_asset_model import (
    PortfolioGroupAsset,
)
from src.domain.assets.asset_model import Asset


def get_portfolio_variants(user_id: int):
    query = (
        select(
            Portfolio.portfolio_aggregate_id,
            Portfolio.id.label("portfolio_id"),
            Portfolio.name.label("portfolio_name"),
            PortfolioGroup.id.label("portfolio_group_id"),
            PortfolioGroup.name.label("portfolio_group_name"),
            Asset.id.label("asset_id"),
            Asset.name.label("asset_name"),
            Asset.symbol.label("asset_symbol"),
        )
        .join_from(
            PortfolioAggregate,
            Portfolio,
            Portfolio.portfolio_aggregate_id == PortfolioAggregate.id,
        )
        .join(
            PortfolioGroup,
            PortfolioGroup.portfolio_id == Portfolio.id,
        )
        .join(
            PortfolioGroupAsset,
            PortfolioGroupAsset.portfolio_group_id == PortfolioGroup.id,
        )
        .join(
            Asset,
            Asset.id == PortfolioGroupAsset.asset_id,
        )
        .where(PortfolioAggregate.user_id == user_id)
    )

    return query
