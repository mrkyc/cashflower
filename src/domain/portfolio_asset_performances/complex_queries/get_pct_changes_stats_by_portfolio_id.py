from sqlalchemy import select, and_, func, true

from src.domain.portfolio_groups.portfolio_group_model import PortfolioGroup
from src.domain.portfolio_group_assets.portfolio_group_asset_model import (
    PortfolioGroupAsset,
)
from src.domain.adjusted_asset_pricings.adjusted_asset_pricing_model import (
    AdjustedAssetPricing,
)


def get_pct_changes_stats_by_portfolio_id(portfolio_id):
    cte_1 = (
        select(
            AdjustedAssetPricing.asset_id,
            func.min(AdjustedAssetPricing.date).label("min_date"),
        )
        .group_by(AdjustedAssetPricing.asset_id)
        .cte("cte_1")
    )

    cte_2 = (
        select(func.max(cte_1.c.min_date).label("first_common_date"))
        .join_from(
            cte_1,
            PortfolioGroupAsset,
            PortfolioGroupAsset.asset_id == cte_1.c.asset_id,
        )
        .join(
            PortfolioGroup,
            PortfolioGroup.id == PortfolioGroupAsset.portfolio_group_id,
        )
        .where(PortfolioGroup.portfolio_id == portfolio_id)
        .cte("cte_2")
    )

    cte_3 = (
        select(
            PortfolioGroupAsset.portfolio_group_id,
            func.count(PortfolioGroupAsset.asset_id).label("group_asset_count"),
        ).group_by(
            PortfolioGroupAsset.portfolio_group_id,
        )
    ).cte("cte_3")

    cte_4 = (
        select(
            AdjustedAssetPricing.asset_id,
            PortfolioGroupAsset.portfolio_group_id,
            PortfolioGroup.portfolio_id,
            PortfolioGroup.weight,
            AdjustedAssetPricing.date,
            (
                (
                    AdjustedAssetPricing.adj_close_price
                    - func.lag(AdjustedAssetPricing.adj_close_price).over(
                        partition_by=[AdjustedAssetPricing.asset_id],
                        order_by=AdjustedAssetPricing.date,
                    )
                )
                / func.lag(AdjustedAssetPricing.adj_close_price).over(
                    partition_by=[AdjustedAssetPricing.asset_id],
                    order_by=AdjustedAssetPricing.date,
                )
                * PortfolioGroup.weight
                / 100
                / cte_3.c.group_asset_count
            ).label("pct_change"),
        )
        .join_from(
            AdjustedAssetPricing,
            PortfolioGroupAsset,
            PortfolioGroupAsset.asset_id == AdjustedAssetPricing.asset_id,
        )
        .join(
            PortfolioGroup,
            PortfolioGroup.id == PortfolioGroupAsset.portfolio_group_id,
        )
        .join(
            cte_3,
            cte_3.c.portfolio_group_id == PortfolioGroupAsset.portfolio_group_id,
        )
        .where(
            and_(
                PortfolioGroup.portfolio_id == portfolio_id,
                AdjustedAssetPricing.date >= cte_2.c.first_common_date,
            )
        )
    ).cte("cte_4")

    cte_5 = (
        select(
            cte_4.c.date,
            func.nullif(func.sum(cte_4.c.pct_change), 0.0).label("pct_change"),
        ).group_by(
            cte_4.c.date,
        )
    ).cte("cte_5")

    cte_6 = (select(func.avg(cte_5.c.pct_change).label("pct_change_avg"))).cte("cte_6")

    query = select(
        cte_6.c.pct_change_avg,
        func.sqrt(
            func.avg(func.pow(cte_5.c.pct_change - cte_6.c.pct_change_avg, 2))
        ).label("pct_change_std"),
    ).join(cte_6, true())

    return query
