from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.users.user_model import User
    from src.domain.portfolio_transaction_files.portfolio_transaction_file_model import (
        PortfolioTransactionFile,
    )
    from src.domain.adjusted_portfolio_transactions.adjusted_portfolio_transaction_model import (
        AdjustedPortfolioTransaction,
    )
    from src.domain.portfolio_groups.portfolio_group_model import PortfolioGroup
    from src.domain.portfolio_asset_performances.portfolio_asset_performance_model import (
        PortfolioAssetPerformance,
    )
    from src.domain.portfolio_group_performances.portfolio_group_performance_model import (
        PortfolioGroupPerformance,
    )
    from src.domain.portfolio_performances.portfolio_performance_model import (
        PortfolioPerformance,
    )
    from src.domain.portfolio_aggregates.portfolio_aggregate_model import (
        PortfolioAggregate,
    )


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )
    portfolio_aggregate_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("portfolio_aggregates.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="portfolios")
    portfolio_transaction_files: Mapped[list["PortfolioTransactionFile"]] = (
        relationship(
            "PortfolioTransactionFile",
            back_populates="portfolio",
            cascade="all, delete-orphan",
            passive_deletes=True,
        )
    )
    adjusted_portfolio_transactions: Mapped[list["AdjustedPortfolioTransaction"]] = (
        relationship("AdjustedPortfolioTransaction", back_populates="portfolio")
    )
    portfolio_groups: Mapped[list["PortfolioGroup"]] = relationship(
        "PortfolioGroup",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    portfolio_asset_performances: Mapped[list["PortfolioAssetPerformance"]] = (
        relationship("PortfolioAssetPerformance", back_populates="portfolio")
    )
    portfolio_group_performances: Mapped[list["PortfolioGroupPerformance"]] = (
        relationship("PortfolioGroupPerformance", back_populates="portfolio")
    )
    portfolio_performances: Mapped[list["PortfolioPerformance"]] = relationship(
        "PortfolioPerformance",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    portfolio_aggregate: Mapped["PortfolioAggregate"] = relationship(
        "PortfolioAggregate", back_populates="portfolios"
    )

    __table_args__ = (
        UniqueConstraint(
            "portfolio_aggregate_id", "name", name="uix_portfolio_aggregate_id_name"
        ),
    )
