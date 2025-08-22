from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.portfolio_aggregates.portfolio_aggregate_model import (
        PortfolioAggregate,
    )


class PortfolioAggregatePerformance(Base):
    __tablename__ = "portfolio_aggregate_performances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    portfolio_aggregate_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("portfolio_aggregates.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    date: Mapped[str] = mapped_column(String, index=True, nullable=False)
    market_value: Mapped[float] = mapped_column(Float, nullable=False)
    market_value_adj: Mapped[float] = mapped_column(Float, nullable=False)
    delta_quantity_value_adj: Mapped[float] = mapped_column(Float, nullable=False)
    cash_balance: Mapped[float] = mapped_column(Float, nullable=False)
    invested_amount: Mapped[float] = mapped_column(Float, nullable=False)
    invested_amount_total: Mapped[float] = mapped_column(Float, nullable=False)
    asset_disposal_income: Mapped[float] = mapped_column(Float, nullable=False)
    asset_disposal_income_total: Mapped[float] = mapped_column(Float, nullable=False)
    asset_holding_income: Mapped[float] = mapped_column(Float, nullable=False)
    asset_holding_income_total: Mapped[float] = mapped_column(Float, nullable=False)
    interest_income: Mapped[float] = mapped_column(Float, nullable=False)
    interest_income_total: Mapped[float] = mapped_column(Float, nullable=False)
    investment_income: Mapped[float] = mapped_column(Float, nullable=False)
    investment_income_total: Mapped[float] = mapped_column(Float, nullable=False)
    profit: Mapped[float] = mapped_column(Float, nullable=False)
    profit_total: Mapped[float] = mapped_column(Float, nullable=False)
    profit_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    profit_percentage_total: Mapped[float] = mapped_column(Float, nullable=False)
    drawdown_value: Mapped[float] = mapped_column(Float, nullable=False)
    drawdown_value_total: Mapped[float] = mapped_column(Float, nullable=False)
    drawdown_profit: Mapped[float] = mapped_column(Float, nullable=False)
    drawdown_profit_total: Mapped[float] = mapped_column(Float, nullable=False)
    hpr: Mapped[float] = mapped_column(Float, nullable=False)
    drawdown: Mapped[float] = mapped_column(Float, nullable=False)
    twrr_rate_daily: Mapped[float] = mapped_column(Float, nullable=False)
    twrr_rate_annualized: Mapped[float] = mapped_column(Float, nullable=True)
    sharpe_ratio_daily: Mapped[float] = mapped_column(Float, nullable=True)
    sharpe_ratio_annualized: Mapped[float] = mapped_column(Float, nullable=True)
    sortino_ratio_daily: Mapped[float] = mapped_column(Float, nullable=True)
    sortino_ratio_annualized: Mapped[float] = mapped_column(Float, nullable=True)
    xirr_rate: Mapped[float] = mapped_column(Float, nullable=True)
    xirr_rate_total: Mapped[float] = mapped_column(Float, nullable=True)

    portfolio_aggregate: Mapped["PortfolioAggregate"] = relationship(
        "PortfolioAggregate", back_populates="portfolio_aggregate_performances"
    )

    __table_args__ = (
        UniqueConstraint(
            "portfolio_aggregate_id", "date", name="uix_portfolio_aggregate_id_date"
        ),
    )
