from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.assets.asset_model import Asset
    from src.domain.portfolios.portfolio_model import Portfolio
    from src.domain.portfolio_transaction_files.portfolio_transaction_file_model import (
        PortfolioTransactionFile,
    )


class AdjustedPortfolioTransaction(Base):
    __tablename__ = "adjusted_portfolio_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    portfolio_transaction_file_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("portfolio_transaction_files.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    portfolio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("portfolios.id"), index=True, nullable=False
    )
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assets.id", ondelete="RESTRICT"), index=True, nullable=True
    )
    date: Mapped[str] = mapped_column(String, index=True, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_value: Mapped[float] = mapped_column(Float, nullable=False)
    fee_amount: Mapped[float] = mapped_column(Float, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Float, nullable=False)
    cash_flow: Mapped[float] = mapped_column(Float, nullable=False)
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

    portfolio_transaction_file: Mapped["PortfolioTransactionFile"] = relationship(
        "PortfolioTransactionFile", back_populates="adjusted_portfolio_transactions"
    )
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio", back_populates="adjusted_portfolio_transactions"
    )
    asset: Mapped["Asset"] = relationship(
        "Asset", back_populates="adjusted_portfolio_transactions"
    )
