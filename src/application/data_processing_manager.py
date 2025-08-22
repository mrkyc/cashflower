from src.domain import *


class DataProcessingManager:
    def __init__(
        self,
        adjusted_portfolio_transaction_service: AdjustedPortfolioTransactionService,
        portfolio_asset_performance_service: PortfolioAssetPerformanceService,
        portfolio_group_performance_service: PortfolioGroupPerformanceService,
        portfolio_performance_service: PortfolioPerformanceService,
        portfolio_aggregate_performance_service: PortfolioAggregatePerformanceService,
        portfolio_service: PortfolioService,
        asset_service: AssetService,
        portfolio_aggregate_service: PortfolioAggregateService,
    ):
        self.adjusted_portfolio_transaction_service = (
            adjusted_portfolio_transaction_service
        )
        self.portfolio_asset_performance_service = portfolio_asset_performance_service
        self.portfolio_group_performance_service = portfolio_group_performance_service
        self.portfolio_performance_service = portfolio_performance_service
        self.portfolio_aggregate_performance_service = (
            portfolio_aggregate_performance_service
        )
        self.portfolio_service = portfolio_service
        self.asset_service = asset_service
        self.portfolio_aggregate_service = portfolio_aggregate_service

    def process_adjusted_portfolio_transactions(self, user_id: int) -> None:
        self.adjusted_portfolio_transaction_service.insert_with_select(user_id)

    def process_portfolio_asset_performances(self, user_id: int) -> None:
        self.portfolio_asset_performance_service.insert_with_select(user_id)

    def process_portfolio_group_performances(self, user_id: int) -> None:
        self.portfolio_group_performance_service.insert_with_select(user_id)

    def process_portfolio_performances(self, user_id: int) -> None:
        self.portfolio_performance_service.insert_with_select(user_id)

    def process_portfolio_aggregate_performances(self, user_id: int) -> None:
        self.portfolio_aggregate_performance_service.insert_with_select(user_id)

    def update_checkpoint_date(self, user_id: int) -> None:
        self.portfolio_aggregate_service.update_checkpoint_date(user_id=user_id)
