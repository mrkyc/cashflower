from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.currency_pair_pricings.currency_pair_pricing_model import (
        CurrencyPairPricing,
    )
    from src.domain.adjusted_currency_pair_pricings.adjusted_currency_pair_pricing_model import (
        AdjustedCurrencyPairPricing,
    )
    from src.domain.assets.asset_model import Asset
    from src.domain.portfolio_transaction_files.portfolio_transaction_file_model import (
        PortfolioTransactionFile,
    )


class CurrencyPair(Base):
    __tablename__ = "currency_pairs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_currency_name: Mapped[str] = mapped_column(String, nullable=False)
    second_currency_name: Mapped[str] = mapped_column(String, nullable=False)
    first_pricing_date: Mapped[str] = mapped_column(
        String, nullable=False, default="1900-01-01"
    )
    last_pricing_date: Mapped[str] = mapped_column(
        String, nullable=False, default="1900-01-01"
    )

    currency_pair_pricings: Mapped[list["CurrencyPairPricing"]] = relationship(
        "CurrencyPairPricing",
        back_populates="currency_pair",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    adjusted_currency_pair_pricings: Mapped[list["AdjustedCurrencyPairPricing"]] = (
        relationship(
            "AdjustedCurrencyPairPricing",
            back_populates="currency_pair",
            cascade="all, delete-orphan",
            passive_deletes=True,
        )
    )
    portfolio_transaction_files: Mapped[list["PortfolioTransactionFile"]] = (
        relationship("PortfolioTransactionFile", back_populates="currency_pair")
    )

    __table_args__ = (
        UniqueConstraint(
            "first_currency_name", "second_currency_name", name="uix_currency_names"
        ),
    )
