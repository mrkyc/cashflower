from .settings_model import Settings
from .settings_repository import SettingsRepository


class SettingsService:
    def __init__(self, settings_repository: SettingsRepository):
        self.settings_repository = settings_repository

    def create_one(
        self,
        user_id,
        analysis_currency,
        ohlc_assets,
        ohlc_currencies,
        transaction_files,
        transactions,
        portfolio_groups,
        portfolio_group_assets,
    ):
        settings = Settings(
            user_id=user_id,
            analysis_currency=analysis_currency,
            ohlc_assets=ohlc_assets,
            ohlc_currencies=ohlc_currencies,
            transaction_files=transaction_files,
            transactions=transactions,
            portfolio_groups=portfolio_groups,
            portfolio_group_assets=portfolio_group_assets,
        )
        return self.settings_repository.create_one(settings=settings)

    def get_one(self, user_id) -> Settings | None:
        return self.settings_repository.get_one(user_id=user_id)

    def get_all(self):
        return self.settings_repository.get_all()

    def update_one(
        self,
        user_id,
        analysis_currency=None,
        ohlc_assets=None,
        ohlc_currencies=None,
        transaction_files=None,
        transactions=None,
        portfolio_groups=None,
        portfolio_group_assets=None,
    ):
        settings = self.get_one(user_id=user_id)
        if settings is None:
            return None
        else:
            if analysis_currency is not None:
                settings.analysis_currency = analysis_currency
            if ohlc_assets is not None:
                settings.ohlc_assets = ohlc_assets
            if ohlc_currencies is not None:
                settings.ohlc_currencies = ohlc_currencies
            if transaction_files is not None:
                settings.transaction_files = transaction_files
            if transactions is not None:
                settings.transactions = transactions
            if portfolio_groups is not None:
                settings.portfolio_groups = portfolio_groups
            if portfolio_group_assets is not None:
                settings.portfolio_group_assets = portfolio_group_assets
            return self.settings_repository.update_one(settings=settings)

    def upsert_one(
        self,
        user_id,
        analysis_currency,
        ohlc_assets,
        ohlc_currencies,
        transaction_files,
        transactions,
        portfolio_groups,
        portfolio_group_assets,
    ):
        settings = self.get_one(user_id=user_id)
        if settings:
            return self.update_one(
                user_id=settings.user_id,
                analysis_currency=analysis_currency,
                ohlc_assets=ohlc_assets,
                ohlc_currencies=ohlc_currencies,
                transaction_files=transaction_files,
                transactions=transactions,
                portfolio_groups=portfolio_groups,
                portfolio_group_assets=portfolio_group_assets,
            )
        else:
            return self.create_one(
                user_id=user_id,
                analysis_currency=analysis_currency,
                ohlc_assets=ohlc_assets,
                ohlc_currencies=ohlc_currencies,
                transaction_files=transaction_files,
                transactions=transactions,
                portfolio_groups=portfolio_groups,
                portfolio_group_assets=portfolio_group_assets,
            )

    def delete_one(self, user_id):
        settings = self.get_one(user_id=user_id)
        if settings is None:
            return None
        else:
            return self.settings_repository.delete_one(settings=settings)

    def delete_all(self):
        return self.settings_repository.delete_all()
