from sqlalchemy import delete, exists

from src.domain.asset_pricings.asset_pricing_model import AssetPricing
from src.domain.assets.asset_model import Asset


def delete_many_by_asset_id_and_date(asset_id: int):
    query = delete(AssetPricing).where(
        exists().where(
            (Asset.id == AssetPricing.asset_id)
            & (AssetPricing.asset_id == asset_id)
            & (AssetPricing.date >= Asset.last_pricing_date)
        )
    )

    return query
