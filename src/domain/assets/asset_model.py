from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.asset_pricings.asset_pricing_model import AssetPricing
    from src.domain.adjusted_asset_pricings.adjusted_asset_pricing_model import (
        AdjustedAssetPricing,
    )
    from src.domain.portfolio_transactions.portfolio_transaction_model import (
        PortfolioTransaction,
    )
    from src.domain.adjusted_portfolio_transactions.adjusted_portfolio_transaction_model import (
        AdjustedPortfolioTransaction,
    )
    from src.domain.portfolio_group_assets.portfolio_group_asset_model import (
        PortfolioGroupAsset,
    )
    from src.domain.portfolio_asset_performances.portfolio_asset_performance_model import (
        PortfolioAssetPerformance,
    )


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    symbol: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    first_pricing_date: Mapped[str] = mapped_column(
        String, nullable=False, default="1900-01-01"
    )
    last_pricing_date: Mapped[str] = mapped_column(
        String, nullable=False, default="1900-01-01"
    )

    asset_pricings: Mapped[list["AssetPricing"]] = relationship(
        "AssetPricing",
        back_populates="asset",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    adjusted_asset_pricings: Mapped[list["AdjustedAssetPricing"]] = relationship(
        "AdjustedAssetPricing",
        back_populates="asset",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    portfolio_transactions: Mapped[list["PortfolioTransaction"]] = relationship(
        "PortfolioTransaction", back_populates="asset"
    )
    adjusted_portfolio_transactions: Mapped[list["AdjustedPortfolioTransaction"]] = (
        relationship("AdjustedPortfolioTransaction", back_populates="asset")
    )
    portfolio_groups: Mapped[list["PortfolioGroupAsset"]] = relationship(
        "PortfolioGroupAsset", back_populates="asset"
    )
    portfolio_asset_performances: Mapped[list["PortfolioAssetPerformance"]] = (
        relationship("PortfolioAssetPerformance", back_populates="asset")
    )
