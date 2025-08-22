from sqlalchemy import delete, exists

from src.domain.adjusted_portfolio_transactions.adjusted_portfolio_transaction_model import (
    AdjustedPortfolioTransaction,
)
from src.domain.portfolio_transaction_files.portfolio_transaction_file_model import (
    PortfolioTransactionFile,
)


def delete_many_by_user_id(user_id: int):
    query = delete(AdjustedPortfolioTransaction).where(
        exists().where(
            (
                PortfolioTransactionFile.id
                == AdjustedPortfolioTransaction.portfolio_transaction_file_id
            )
            & (PortfolioTransactionFile.user_id == user_id)
        )
    )

    return query
