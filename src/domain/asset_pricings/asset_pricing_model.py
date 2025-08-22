from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.assets.asset_model import Asset


class AssetPricing(Base):
    __tablename__ = "asset_pricings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assets.id", ondelete="CASCADE"), index=True, nullable=False
    )
    date: Mapped[str] = mapped_column(String, index=True, nullable=False)
    open_price: Mapped[float] = mapped_column(Float, nullable=False)
    high_price: Mapped[float] = mapped_column(Float, nullable=False)
    low_price: Mapped[float] = mapped_column(Float, nullable=False)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)
    adjusted_close_price: Mapped[float] = mapped_column(Float, nullable=False)

    asset: Mapped["Asset"] = relationship("Asset", back_populates="asset_pricings")

    __table_args__ = (UniqueConstraint("asset_id", "date", name="uix_asset_id_date"),)
