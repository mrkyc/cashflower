from typing import TYPE_CHECKING
from sqlalchemy import Integer, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.users.user_model import User
    from src.domain.portfolios.portfolio_model import Portfolio
    from src.domain.portfolio_group_assets.portfolio_group_asset_model import (
        PortfolioGroupAsset,
    )
    from src.domain.portfolio_group_performances.portfolio_group_performance_model import (
        PortfolioGroupPerformance,
    )
    from src.domain.portfolio_asset_performances.portfolio_asset_performance_model import (
        PortfolioAssetPerformance,
    )


class PortfolioGroup(Base):
    __tablename__ = "portfolio_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )
    portfolio_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="portfolio_groups")
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio", back_populates="portfolio_groups"
    )
    assets: Mapped[list["PortfolioGroupAsset"]] = relationship(
        "PortfolioGroupAsset",
        back_populates="portfolio_group",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    portfolio_group_performances: Mapped[list["PortfolioGroupPerformance"]] = (
        relationship(
            "PortfolioGroupPerformance",
            back_populates="portfolio_group",
            cascade="all, delete-orphan",
            passive_deletes=True,
        )
    )
    portfolio_asset_performances: Mapped[list["PortfolioAssetPerformance"]] = (
        relationship(
            "PortfolioAssetPerformance",
            back_populates="portfolio_group",
            cascade="all, delete-orphan",
            passive_deletes=True,
        )
    )

    __table_args__ = (
        UniqueConstraint("portfolio_id", "name", name="uix_portfolio_id_name"),
    )
