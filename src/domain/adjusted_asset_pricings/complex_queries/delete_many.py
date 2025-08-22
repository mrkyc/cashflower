from sqlalchemy import delete, exists

from src.domain.assets.asset_model import Asset
from src.domain.adjusted_asset_pricings.adjusted_asset_pricing_model import (
    AdjustedAssetPricing,
)


def delete_many_by_asset_id_and_date(asset_id):
    query = delete(AdjustedAssetPricing).where(
        exists().where(
            (Asset.id == AdjustedAssetPricing.asset_id)
            & (AdjustedAssetPricing.asset_id == asset_id)
            & (AdjustedAssetPricing.date >= Asset.last_pricing_date)
        )
    )

    return query
