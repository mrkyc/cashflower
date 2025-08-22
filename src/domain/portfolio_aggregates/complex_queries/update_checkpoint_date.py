from sqlalchemy import update, select, func, and_

from src.domain.assets.asset_model import Asset
from src.domain.currency_pairs.currency_pair_model import CurrencyPair
from src.domain.portfolios.portfolio_model import Portfolio
from src.domain.portfolio_groups.portfolio_group_model import PortfolioGroup
from src.domain.portfolio_group_assets.portfolio_group_asset_model import (
    PortfolioGroupAsset,
)
from src.domain.portfolio_aggregates.portfolio_aggregate_model import PortfolioAggregate
from src.domain.settings.settings_model import Settings


def update_checkpoint_date(user_id: int):
    subquery = (
        select(
            func.min(
                func.coalesce(
                    func.min(
                        Asset.last_pricing_date,
                        CurrencyPair.last_pricing_date,
                    ),
                    Asset.last_pricing_date,
                    "1900-01-01",
                )
            ).label("date")
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
        .join(Asset, Asset.id == PortfolioGroupAsset.asset_id)
        .join(Settings, Settings.user_id == PortfolioAggregate.user_id)
        .outerjoin(
            CurrencyPair,
            and_(
                CurrencyPair.first_currency_name == Asset.currency,
                CurrencyPair.second_currency_name == Settings.analysis_currency,
            ),
        )
        .where(PortfolioAggregate.user_id == user_id)
        .scalar_subquery()
    )

    query = update(PortfolioAggregate).values(checkpoint_date=subquery)

    return query
