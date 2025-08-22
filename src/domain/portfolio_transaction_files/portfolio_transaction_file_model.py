from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.users.user_model import User
    from src.domain.portfolios.portfolio_model import Portfolio
    from src.domain.currency_pairs.currency_pair_model import CurrencyPair
    from src.domain.portfolio_transactions.portfolio_transaction_model import (
        PortfolioTransaction,
    )
    from src.domain.adjusted_portfolio_transactions.adjusted_portfolio_transaction_model import (
        AdjustedPortfolioTransaction,
    )


class PortfolioTransactionFile(Base):
    __tablename__ = "portfolio_transaction_files"

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
    currency: Mapped[str] = mapped_column(String, nullable=False)
    currency_pair_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("currency_pairs.id", ondelete="RESTRICT"),
        index=True,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="portfolio_transaction_files"
    )
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio", back_populates="portfolio_transaction_files"
    )
    currency_pair: Mapped["CurrencyPair"] = relationship(
        "CurrencyPair", back_populates="portfolio_transaction_files"
    )
    portfolio_transactions: Mapped["PortfolioTransaction"] = relationship(
        "PortfolioTransaction",
        back_populates="portfolio_transaction_file",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    adjusted_portfolio_transactions: Mapped["AdjustedPortfolioTransaction"] = (
        relationship(
            "AdjustedPortfolioTransaction",
            back_populates="portfolio_transaction_file",
            cascade="all, delete-orphan",
            passive_deletes=True,
        )
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id", "portfolio_id", "name", name="uix_user_id_portfolio_id_name"
        ),
    )
