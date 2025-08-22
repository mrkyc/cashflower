from src.domain import *
from src.dto import (
    SettingsDTO,
    TransactionFilesModel,
    TransactionsModel,
    PortfolioGroupsModel,
    PortfolioGroupAssetsModel,
)


class UpsertManager:
    def __init__(
        self,
        user_service: UserService,
        settings_service: SettingsService,
        currency_pair_service: CurrencyPairService,
        asset_service: AssetService,
        portfolio_aggregate_service: PortfolioAggregateService,
        portfolio_service: PortfolioService,
        portfolio_group_service: PortfolioGroupService,
        portfolio_group_asset_service: PortfolioGroupAssetService,
        portfolio_transaction_file_service: PortfolioTransactionFileService,
        portfolio_transactions_service: PortfolioTransactionService,
    ):
        self.user_service = user_service
        self.settings_service = settings_service
        self.currency_pair_service = currency_pair_service
        self.asset_service = asset_service
        self.portfolio_aggregate_service = portfolio_aggregate_service
        self.portfolio_service = portfolio_service
        self.portfolio_group_service = portfolio_group_service
        self.portfolio_group_asset_service = portfolio_group_asset_service
        self.portfolio_transaction_file_service = portfolio_transaction_file_service
        self.portfolio_transactions_service = portfolio_transactions_service

    def upsert_user(self, session_id: str):
        return self.user_service.upsert_one(session_id=session_id)

    def upsert_settings(self, user_id: int, settings_dto: SettingsDTO):
        return self.settings_service.upsert_one(
            user_id=user_id,
            analysis_currency=settings_dto.analysis_currency,
            ohlc_assets=settings_dto.ohlc_assets,
            ohlc_currencies=settings_dto.ohlc_currencies,
            transaction_files=settings_dto.transaction_files.model_dump(),
            transactions=settings_dto.transactions.model_dump(),
            portfolio_groups=settings_dto.portfolio_groups.model_dump(),
            portfolio_group_assets=settings_dto.portfolio_group_assets.model_dump(),
        )

    def upsert_portfolio_aggregate(self, user_id: int):
        portfolio_aggregate = self.portfolio_aggregate_service.get_one_by_user_id(
            user_id=user_id
        )
        if portfolio_aggregate:
            return portfolio_aggregate
        else:
            return self.portfolio_aggregate_service.create_one(user_id=user_id)

    def upsert_portfolios(
        self,
        user_id: int,
        portfolio_aggregate_id: int,
        transaction_files: TransactionFilesModel,
    ):
        for name in set(transaction_files.portfolio_name):
            portfolio = self.portfolio_service.get_one_by_user_id_and_name(
                user_id=user_id, name=name
            )
            if not portfolio:
                portfolio = self.portfolio_service.create_one(
                    user_id=user_id,
                    portfolio_aggregate_id=portfolio_aggregate_id,
                    name=name,
                )

        return None

    def upsert_portfolio_groups(
        self, user_id: int, portfolio_groups: PortfolioGroupsModel
    ):
        portfolio_names = portfolio_groups.portfolio_name
        group_names = portfolio_groups.group_name
        group_weights = portfolio_groups.group_weight

        for portfolio_name, group_name, group_weight in zip(
            portfolio_names, group_names, group_weights
        ):
            portfolio = self.portfolio_service.get_one_by_user_id_and_name(
                user_id=user_id, name=portfolio_name
            )
            if portfolio:
                portfolio_group = (
                    self.portfolio_group_service.get_one_by_portfolio_id_and_name(
                        portfolio_id=portfolio.id, name=group_name
                    )
                )
                if not portfolio_group:
                    portfolio_group = self.portfolio_group_service.create_one(
                        user_id=user_id,
                        portfolio_id=portfolio.id,
                        name=group_name,
                        weight=group_weight,
                    )

        return None

    def upsert_portfolio_group_assets(
        self, user_id: int, portfolio_group_assets: PortfolioGroupAssetsModel
    ):
        portfolio_names = portfolio_group_assets.portfolio_name
        asset_symbols = portfolio_group_assets.asset_symbol
        group_names = portfolio_group_assets.group_name

        for portfolio_name, asset_symbol, group_name in zip(
            portfolio_names, asset_symbols, group_names
        ):
            portfolio = self.portfolio_service.get_one_by_user_id_and_name(
                user_id=user_id, name=portfolio_name
            )

            if portfolio:
                asset = self.asset_service.get_one_by_symbol(symbol=asset_symbol)
                portfolio_group = (
                    self.portfolio_group_service.get_one_by_portfolio_id_and_name(
                        portfolio_id=portfolio.id,
                        name=group_name,
                    )
                )

                if asset and portfolio_group:
                    portfolio_group_asset = self.portfolio_group_asset_service.get_one(
                        portfolio_group_id=portfolio_group.id,
                        asset_id=asset.id,
                    )
                    if not portfolio_group_asset:
                        portfolio_group_asset = (
                            self.portfolio_group_asset_service.create_one(
                                portfolio_group_id=portfolio_group.id,
                                asset_id=asset.id,
                            )
                        )

        return None

    def upsert_portfolio_transaction_files(
        self,
        user_id: int,
        portfolio_transaction_files: TransactionFilesModel,
        analysis_currency: str,
    ):
        file_names = portfolio_transaction_files.file_name
        currencies = portfolio_transaction_files.currency
        portfolio_names = portfolio_transaction_files.portfolio_name

        for file_name, currency, portfolio_name in zip(
            file_names, currencies, portfolio_names
        ):
            currency_pair_name = currency + analysis_currency
            currency_pair = (
                self.currency_pair_service.get_one_by_name(name=currency_pair_name)
                if currency != analysis_currency
                else None
            )
            currency_pair_id = currency_pair.id if currency_pair else None

            portfolio = self.portfolio_service.get_one_by_user_id_and_name(
                user_id=user_id, name=portfolio_name
            )
            if portfolio:
                portfolio_transaction_file = (
                    self.portfolio_transaction_file_service.upsert_one(
                        user_id=user_id,
                        portfolio_id=portfolio.id,
                        name=file_name,
                        currency=currency,
                        currency_pair_id=currency_pair_id,
                    )
                )
                if not portfolio_transaction_file:
                    return None

        return None

    def upsert_portfolio_transactions(
        self, user_id: int, list_of_transactions: list[TransactionsModel]
    ):
        for transactions in list_of_transactions:
            file_name = transactions.file_name
            transaction_data = transactions.transaction_data
            portfolio_transaction_file = (
                self.portfolio_transaction_file_service.get_one_by_user_id_and_name(
                    user_id=user_id, name=file_name
                )
            )
            portfolio_transaction_file_id = (
                portfolio_transaction_file.id if portfolio_transaction_file else None
            )
            self.portfolio_transactions_service.delete_many_by_file_id(
                portfolio_transaction_file_id
            )
            transaction_data_zipped = zip(
                transaction_data.date,
                transaction_data.asset_symbol,
                transaction_data.transaction_type,
                transaction_data.quantity,
                transaction_data.transaction_value,
                transaction_data.fee_amount,
                transaction_data.tax_amount,
            )

            for (
                date,
                asset_symbol,
                transaction_type,
                quantity,
                transaction_value,
                fee_amount,
                tax_amount,
            ) in transaction_data_zipped:
                asset = (
                    self.asset_service.get_one_by_symbol(symbol=asset_symbol)
                    if asset_symbol
                    else None
                )
                asset_id = asset.id if asset else None

                self.portfolio_transactions_service.create_one(
                    portfolio_transaction_file_id=portfolio_transaction_file_id,
                    asset_id=asset_id,
                    date=date,
                    transaction_type=transaction_type,
                    quantity=quantity,
                    transaction_value=transaction_value,
                    fee_amount=fee_amount,
                    tax_amount=tax_amount,
                )
