from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.infrastructure.db import Base

if TYPE_CHECKING:
    from src.domain.settings.settings_model import Settings
    from src.domain.portfolio_aggregates.portfolio_aggregate_model import (
        PortfolioAggregate,
    )
    from src.domain.portfolios.portfolio_model import Portfolio
    from src.domain.portfolio_groups.portfolio_group_model import PortfolioGroup
    from src.domain.portfolio_transaction_files.portfolio_transaction_file_model import (
        PortfolioTransactionFile,
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String, unique=True, index=True)

    settings: Mapped["Settings"] = relationship("Settings", back_populates="user")
    portfolio_aggregate: Mapped["PortfolioAggregate"] = relationship(
        "PortfolioAggregate",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    portfolios: Mapped[list["Portfolio"]] = relationship(
        "Portfolio", back_populates="user"
    )
    portfolio_groups: Mapped[list["PortfolioGroup"]] = relationship(
        "PortfolioGroup", back_populates="user"
    )
    portfolio_transaction_files: Mapped[list["PortfolioTransactionFile"]] = (
        relationship("PortfolioTransactionFile", back_populates="user")
    )
