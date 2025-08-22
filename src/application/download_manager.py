from src.domain import *
from src.infrastructure.asset_info import fetch_asset_info
from src.infrastructure.currency_pair_pricings import currency_pairs_etl_yfinance
from src.infrastructure.asset_pricings import assets_etl_yfinance


class DownloadManager:
    def __init__(
        self,
        currency_pair_service: CurrencyPairService,
        currency_pair_pricing_service: CurrencyPairPricingService,
        asset_service: AssetService,
        asset_pricing_service: AssetPricingService,
        adjusted_currency_pair_pricing_service: AdjustedCurrencyPairPricingService,
        adjusted_asset_pricing_service: AdjustedAssetPricingService,
    ):
        self.currency_pair_service = currency_pair_service
        self.currency_pair_pricing_service = currency_pair_pricing_service
        self.asset_service = asset_service
        self.asset_pricing_service = asset_pricing_service
        self.adjusted_currency_pair_pricing_service = (
            adjusted_currency_pair_pricing_service
        )
        self.adjusted_asset_pricing_service = adjusted_asset_pricing_service

    def upsert_assets_and_currencies(
        self,
        asset_symbols: set[str],
        transaction_file_currencies: set[str],
        analysis_currency: str,
    ):
        etl_currency_pair_symbols = set()
        etl_asset_symbols = set()

        for asset_symbol in asset_symbols:
            asset_info = fetch_asset_info(symbol=asset_symbol)
            asset_currency = asset_info["currency"]
            asset_full_name = asset_info["full_name"]

            currency_pair_name = f"{asset_currency}{analysis_currency}".lower()
            currency_pair_symbol = f"{currency_pair_name}=x"
            currency_pair = self.currency_pair_service.upsert_one(
                name=currency_pair_name,
                symbol=currency_pair_symbol,
                first_currency_name=asset_currency,
                second_currency_name=analysis_currency,
            )
            if currency_pair:
                etl_currency_pair_symbols.add(currency_pair_symbol)

            asset = self.asset_service.upsert_one(
                symbol=asset_symbol,
                name=asset_full_name,
                currency=asset_currency,
            )
            if asset:
                etl_asset_symbols.add(asset_symbol)

        for currency in transaction_file_currencies:
            currency_pair_name = f"{currency}{analysis_currency}".lower()
            currency_pair_symbol = f"{currency_pair_name}=x"

            if (
                currency_pair_symbol in etl_currency_pair_symbols
                or currency.lower() == analysis_currency.lower()
            ):
                continue

            currency_pair = self.currency_pair_service.upsert_one(
                symbol=currency_pair_symbol,
                name=currency_pair_name,
                first_currency_name=currency,
                second_currency_name=analysis_currency,
            )
            if currency_pair:
                etl_currency_pair_symbols.add(currency_pair_symbol)

        currency_pairs_etl_yfinance(
            symbols=etl_currency_pair_symbols,
            currency_pair_service=self.currency_pair_service,
            currency_pair_pricing_service=self.currency_pair_pricing_service,
            adjusted_currency_pair_pricing_service=self.adjusted_currency_pair_pricing_service,
        )
        assets_etl_yfinance(
            symbols=etl_asset_symbols,
            asset_service=self.asset_service,
            asset_pricing_service=self.asset_pricing_service,
            adjusted_asset_pricing_service=self.adjusted_asset_pricing_service,
        )
