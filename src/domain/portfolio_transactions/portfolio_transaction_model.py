from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.portfolio_transaction_files.portfolio_transaction_file_model import (
        PortfolioTransactionFile,
    )
    from src.domain.assets.asset_model import Asset


class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    portfolio_transaction_file_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("portfolio_transaction_files.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
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

    portfolio_transaction_file: Mapped["PortfolioTransactionFile"] = relationship(
        "PortfolioTransactionFile", back_populates="portfolio_transactions"
    )
    asset: Mapped["Asset"] = relationship(
        "Asset", back_populates="portfolio_transactions"
    )
