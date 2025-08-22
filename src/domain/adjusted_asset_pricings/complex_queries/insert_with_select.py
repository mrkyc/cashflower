from sqlalchemy import select, insert, and_, func

from src.domain.adjusted_asset_pricings.adjusted_asset_pricing_model import (
    AdjustedAssetPricing,
)
from src.domain.assets.asset_model import Asset
from src.domain.asset_pricings.asset_pricing_model import AssetPricing


def insert_with_select(asset_id):
    cte_asset_continuous_dates = (
        select(
            Asset.id.label("asset_id"),
            func.max(
                Asset.first_pricing_date,
                Asset.last_pricing_date,
            ).label("date"),
        )
        .where(Asset.id == asset_id)
        .cte(name="cte_asset_continuous_dates", recursive=True)
    )

    cte_asset_continuous_dates = cte_asset_continuous_dates.union_all(
        select(
            cte_asset_continuous_dates.c.asset_id,
            func.date(cte_asset_continuous_dates.c.date, "+1 day").label("date"),
        ).where(cte_asset_continuous_dates.c.date < func.date("now"))
    )

    query = (
        select(
            cte_asset_continuous_dates.c.asset_id,
            cte_asset_continuous_dates.c.date,
            (
                func.coalesce(
                    AssetPricing.open_price,
                    select(AssetPricing.open_price)
                    .where(
                        AssetPricing.date < cte_asset_continuous_dates.c.date,
                        AssetPricing.asset_id == cte_asset_continuous_dates.c.asset_id,
                    )
                    .order_by(AssetPricing.date.desc())
                    .correlate(cte_asset_continuous_dates)
                    .scalar_subquery(),
                    0.0,
                )
            ).label("open_price"),
            (
                func.coalesce(
                    AssetPricing.high_price,
                    select(AssetPricing.high_price)
                    .where(
                        AssetPricing.date < cte_asset_continuous_dates.c.date,
                        AssetPricing.asset_id == cte_asset_continuous_dates.c.asset_id,
                    )
                    .order_by(AssetPricing.date.desc())
                    .correlate(cte_asset_continuous_dates)
                    .scalar_subquery(),
                    0.0,
                )
            ).label("high_price"),
            (
                func.coalesce(
                    AssetPricing.low_price,
                    select(AssetPricing.low_price)
                    .where(
                        AssetPricing.date < cte_asset_continuous_dates.c.date,
                        AssetPricing.asset_id == cte_asset_continuous_dates.c.asset_id,
                    )
                    .order_by(AssetPricing.date.desc())
                    .correlate(cte_asset_continuous_dates)
                    .scalar_subquery(),
                    0.0,
                )
            ).label("low_price"),
            (
                func.coalesce(
                    AssetPricing.close_price,
                    select(AssetPricing.close_price)
                    .where(
                        AssetPricing.date < cte_asset_continuous_dates.c.date,
                        AssetPricing.asset_id == cte_asset_continuous_dates.c.asset_id,
                    )
                    .order_by(AssetPricing.date.desc())
                    .correlate(cte_asset_continuous_dates)
                    .scalar_subquery(),
                    0.0,
                )
            ).label("close_price"),
            (
                func.coalesce(
                    AssetPricing.adjusted_close_price,
                    select(AssetPricing.adjusted_close_price)
                    .where(
                        AssetPricing.date < cte_asset_continuous_dates.c.date,
                        AssetPricing.asset_id == cte_asset_continuous_dates.c.asset_id,
                    )
                    .order_by(AssetPricing.date.desc())
                    .correlate(cte_asset_continuous_dates)
                    .scalar_subquery(),
                    0.0,
                )
            ).label("adj_close_price"),
        )
        .join_from(
            cte_asset_continuous_dates,
            Asset,
            Asset.id == cte_asset_continuous_dates.c.asset_id,
        )
        .outerjoin(
            AssetPricing,
            and_(
                cte_asset_continuous_dates.c.asset_id == AssetPricing.asset_id,
                cte_asset_continuous_dates.c.date == AssetPricing.date,
            ),
        )
    )

    return insert(AdjustedAssetPricing).from_select(
        [
            "asset_id",
            "date",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "adj_close_price",
        ],
        query,
    )
