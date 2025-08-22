from fastapi import Depends

from .services import *

from src.domain import *
from src.application import UpsertManager, DownloadManager, DataProcessingManager


__all__ = [
    "get_upsert_manager",
    "get_download_manager",
    "get_data_processing_manager",
]


def get_upsert_manager(
    user_service: UserService = Depends(get_user_service),
    settings_service: SettingsService = Depends(get_settings_service),
    currency_pair_service: CurrencyPairService = Depends(get_currency_pair_service),
    asset_service: AssetService = Depends(get_asset_service),
    portfolio_aggregate_service: PortfolioAggregateService = Depends(
        get_portfolio_aggregate_service
    ),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
    portfolio_group_service: PortfolioGroupService = Depends(
        get_portfolio_group_service
    ),
    portfolio_group_asset_service: PortfolioGroupAssetService = Depends(
        get_portfolio_group_asset_service
    ),
    portfolio_transaction_file_service: PortfolioTransactionFileService = Depends(
        get_portfolio_transaction_file_service
    ),
    portfolio_transactions_service: PortfolioTransactionService = Depends(
        get_portfolio_transactions_service
    ),
) -> UpsertManager:
    return UpsertManager(
        user_service=user_service,
        settings_service=settings_service,
        currency_pair_service=currency_pair_service,
        asset_service=asset_service,
        portfolio_aggregate_service=portfolio_aggregate_service,
        portfolio_service=portfolio_service,
        portfolio_group_service=portfolio_group_service,
        portfolio_group_asset_service=portfolio_group_asset_service,
        portfolio_transaction_file_service=portfolio_transaction_file_service,
        portfolio_transactions_service=portfolio_transactions_service,
    )


def get_download_manager(
    currency_pair_service: CurrencyPairService = Depends(get_currency_pair_service),
    currency_pair_pricing_service: CurrencyPairPricingService = Depends(
        get_currency_pair_pricing_service
    ),
    asset_service: AssetService = Depends(get_asset_service),
    asset_pricing_service: AssetPricingService = Depends(get_asset_pricing_service),
    adjusted_currency_pair_pricing_service: AdjustedCurrencyPairPricingService = Depends(
        get_adjusted_currency_pair_pricing_service
    ),
    adjusted_asset_pricing_service: AdjustedAssetPricingService = Depends(
        get_adjusted_asset_pricing_service
    ),
) -> DownloadManager:
    return DownloadManager(
        currency_pair_service=currency_pair_service,
        currency_pair_pricing_service=currency_pair_pricing_service,
        asset_service=asset_service,
        asset_pricing_service=asset_pricing_service,
        adjusted_currency_pair_pricing_service=adjusted_currency_pair_pricing_service,
        adjusted_asset_pricing_service=adjusted_asset_pricing_service,
    )


def get_data_processing_manager(
    adjusted_portfolio_transaction_service: AdjustedPortfolioTransactionService = Depends(
        get_adjusted_portfolio_transaction_service
    ),
    portfolio_asset_performance_service: PortfolioAssetPerformanceService = Depends(
        get_portfolio_asset_performance_service
    ),
    portfolio_group_performance_service: PortfolioGroupPerformanceService = Depends(
        get_portfolio_group_performance_service
    ),
    portfolio_performance_service: PortfolioPerformanceService = Depends(
        get_portfolio_performance_service
    ),
    portfolio_aggregate_performance_service: PortfolioAggregatePerformanceService = Depends(
        get_portfolio_aggregate_performance_service
    ),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
    asset_service: AssetService = Depends(get_asset_service),
    portfolio_aggregate_service: PortfolioAggregateService = Depends(
        get_portfolio_aggregate_service
    ),
) -> DataProcessingManager:
    return DataProcessingManager(
        adjusted_portfolio_transaction_service=adjusted_portfolio_transaction_service,
        portfolio_asset_performance_service=portfolio_asset_performance_service,
        portfolio_group_performance_service=portfolio_group_performance_service,
        portfolio_performance_service=portfolio_performance_service,
        portfolio_aggregate_performance_service=portfolio_aggregate_performance_service,
        portfolio_service=portfolio_service,
        asset_service=asset_service,
        portfolio_aggregate_service=portfolio_aggregate_service,
    )
