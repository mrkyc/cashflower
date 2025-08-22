from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.portfolio_groups.portfolio_group_model import PortfolioGroup
    from src.domain.assets.asset_model import Asset


class PortfolioGroupAsset(Base):
    __tablename__ = "portfolio_groups_assets"

    portfolio_group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("portfolio_groups.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    asset_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assets.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    )

    portfolio_group: Mapped["PortfolioGroup"] = relationship(
        "PortfolioGroup", back_populates="assets"
    )
    asset: Mapped["Asset"] = relationship("Asset", back_populates="portfolio_groups")
