from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.currency_pairs.currency_pair_model import CurrencyPair


class AdjustedCurrencyPairPricing(Base):
    __tablename__ = "adjusted_currency_pair_pricings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    currency_pair_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("currency_pairs.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    date: Mapped[str] = mapped_column(String, index=True, nullable=False)
    open_price: Mapped[float] = mapped_column(Float, nullable=False)
    high_price: Mapped[float] = mapped_column(Float, nullable=False)
    low_price: Mapped[float] = mapped_column(Float, nullable=False)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)

    currency_pair: Mapped["CurrencyPair"] = relationship(
        "CurrencyPair", back_populates="adjusted_currency_pair_pricings"
    )

    __table_args__ = (
        UniqueConstraint("currency_pair_id", "date", name="uix_currency_pair_id_date"),
    )
