from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.users.user_model import User
    from src.domain.portfolios.portfolio_model import Portfolio
    from src.domain.portfolio_aggregate_performances.portfolio_aggregate_performance_model import (
        PortfolioAggregatePerformance,
    )


class PortfolioAggregate(Base):
    __tablename__ = "portfolio_aggregates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    checkpoint_date: Mapped[str] = mapped_column(
        String, nullable=False, default="1900-01-01"
    )

    user: Mapped["User"] = relationship("User", back_populates="portfolio_aggregate")
    portfolios: Mapped[list["Portfolio"]] = relationship(
        "Portfolio",
        back_populates="portfolio_aggregate",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    portfolio_aggregate_performances: Mapped[list["PortfolioAggregatePerformance"]] = (
        relationship(
            "PortfolioAggregatePerformance",
            back_populates="portfolio_aggregate",
            cascade="all, delete-orphan",
            passive_deletes=True,
        )
    )
