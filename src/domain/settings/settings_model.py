from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, JSON, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.users.user_model import User


class Settings(Base):
    __tablename__ = "settings"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    analysis_currency: Mapped[str] = mapped_column(String, nullable=False)
    ohlc_assets: Mapped[str] = mapped_column(String, nullable=False)
    ohlc_currencies: Mapped[str] = mapped_column(String, nullable=False)
    transaction_files: Mapped[dict] = mapped_column(JSON, nullable=False)
    transactions: Mapped[dict] = mapped_column(JSON, nullable=False)
    portfolio_groups: Mapped[dict] = mapped_column(JSON, nullable=False)
    portfolio_group_assets: Mapped[dict] = mapped_column(JSON, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="settings")
