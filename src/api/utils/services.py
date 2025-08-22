from fastapi import Depends
from sqlalchemy.orm import Session

from .db import get_db_session
from src.domain import *


def _camel_to_snake(name: str) -> str:
    """Converts CamelCase to snake_case."""
    return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_")


def _create_service_dependency(service_class, repository_class):
    """Creates a FastAPI dependency for a service."""

    def dependency(session: Session = Depends(get_db_session)):
        repo = repository_class(session=session)
        repo_arg_name = _camel_to_snake(repository_class.__name__)
        return service_class(**{repo_arg_name: repo})

    return dependency


get_adjusted_asset_pricing_service = _create_service_dependency(
    AdjustedAssetPricingService, AdjustedAssetPricingRepository
)
get_adjusted_currency_pair_pricing_service = _create_service_dependency(
    AdjustedCurrencyPairPricingService, AdjustedCurrencyPairPricingRepository
)
get_adjusted_portfolio_transaction_service = _create_service_dependency(
    AdjustedPortfolioTransactionService, AdjustedPortfolioTransactionRepository
)
get_asset_pricing_service = _create_service_dependency(
    AssetPricingService, AssetPricingRepository
)
get_asset_service = _create_service_dependency(AssetService, AssetRepository)
get_currency_pair_pricing_service = _create_service_dependency(
    CurrencyPairPricingService, CurrencyPairPricingRepository
)
get_currency_pair_service = _create_service_dependency(
    CurrencyPairService, CurrencyPairRepository
)
get_portfolio_aggregate_performance_service = _create_service_dependency(
    PortfolioAggregatePerformanceService, PortfolioAggregatePerformanceRepository
)
get_portfolio_aggregate_service = _create_service_dependency(
    PortfolioAggregateService, PortfolioAggregateRepository
)
get_portfolio_asset_performance_service = _create_service_dependency(
    PortfolioAssetPerformanceService, PortfolioAssetPerformanceRepository
)
get_portfolio_group_asset_service = _create_service_dependency(
    PortfolioGroupAssetService, PortfolioGroupAssetRepository
)
get_portfolio_group_performance_service = _create_service_dependency(
    PortfolioGroupPerformanceService, PortfolioGroupPerformanceRepository
)
get_portfolio_group_service = _create_service_dependency(
    PortfolioGroupService, PortfolioGroupRepository
)
get_portfolio_performance_service = _create_service_dependency(
    PortfolioPerformanceService, PortfolioPerformanceRepository
)
get_portfolio_service = _create_service_dependency(
    PortfolioService, PortfolioRepository
)
get_portfolio_transaction_file_service = _create_service_dependency(
    PortfolioTransactionFileService, PortfolioTransactionFileRepository
)
get_portfolio_transactions_service = _create_service_dependency(
    PortfolioTransactionService, PortfolioTransactionRepository
)
get_settings_service = _create_service_dependency(SettingsService, SettingsRepository)
get_user_service = _create_service_dependency(UserService, UserRepository)


__all__ = [
    "get_adjusted_asset_pricing_service",
    "get_adjusted_currency_pair_pricing_service",
    "get_adjusted_portfolio_transaction_service",
    "get_asset_pricing_service",
    "get_asset_service",
    "get_currency_pair_pricing_service",
    "get_currency_pair_service",
    "get_portfolio_aggregate_performance_service",
    "get_portfolio_aggregate_service",
    "get_portfolio_asset_performance_service",
    "get_portfolio_group_asset_service",
    "get_portfolio_group_performance_service",
    "get_portfolio_group_service",
    "get_portfolio_performance_service",
    "get_portfolio_service",
    "get_portfolio_transaction_file_service",
    "get_portfolio_transactions_service",
    "get_settings_service",
    "get_user_service",
]
