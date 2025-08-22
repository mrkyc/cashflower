import logging

from .extract import extract_data_yfinance
from .transform import transform_data_yfinance
from .load import load_data_yfinance
from src.domain import AssetService, AssetPricingService, AdjustedAssetPricingService


logger = logging.getLogger(__name__)


def assets_etl_yfinance(
    symbols: list[str],
    asset_service: AssetService,
    asset_pricing_service: AssetPricingService,
    adjusted_asset_pricing_service: AdjustedAssetPricingService,
):
    assets = [asset_service.get_one_by_symbol(symbol=symbol) for symbol in symbols]
    assets_info = {
        asset.symbol: {
            "asset_id": asset.id,
            "first_pricing_date": asset.first_pricing_date,
            "last_pricing_date": asset.last_pricing_date,
        }
        for asset in assets
        if asset is not None
    }
    if set(assets_info.keys()) != set(symbols):
        missing_symbols = set(symbols) - set(assets_info.keys())
        logger.warning(
            f" ASSETS - The following symbols are not found in the database: {', '.join(missing_symbols)}"
        )

    start_date = min(asset["last_pricing_date"] for asset in assets_info.values())

    try:
        df_data = extract_data_yfinance(symbols, start_date)
    except Exception as e:
        logger.error(
            f" ASSETS - Error while extracting data for the period starting from {start_date}: {e}"
        )
        return

    if df_data is None or df_data.empty:
        logger.warning(
            f" ASSETS - No data is available for the period starting from {start_date}"
        )
        return

    for symbol, asset in assets_info.items():
        asset_id = asset["asset_id"]
        first_pricing_date = asset["first_pricing_date"]
        last_pricing_date = asset["last_pricing_date"]

        try:
            df_data_symbol = df_data.loc[last_pricing_date:, symbol.upper()].dropna()
        except KeyError:
            logger.error(
                f" Symbol {symbol} - Error while retrieving data from extracted DataFrame for the period starting from {start_date}"
            )
            continue
        if df_data_symbol.empty:
            logger.warning(
                f" Symbol {symbol} - No data available for the period starting from {start_date}"
            )
            continue

        try:
            transformed_df_data = transform_data_yfinance(df_data_symbol, asset_id)
        except Exception as e:
            logger.error(
                f" Symbol {symbol} - Error while transforming data for the period {df_data_symbol.iloc[0].name.date()} - {df_data_symbol.iloc[-1].name.date()}: {e}"
            )
            continue

        first_date = transformed_df_data["date"].iloc[0]
        last_date = transformed_df_data["date"].iloc[-1]

        try:
            load_data_yfinance(asset_pricing_service, transformed_df_data, asset_id)
            logger.info(
                f""" Symbol {symbol} - Loaded data to database for the period {first_date} - {last_date}"""
            )
        except Exception as e:
            logger.error(
                f""" Symbol {symbol} - Error while loading data to database for the period {first_date} - {last_date}: {e}"""
            )
            continue

        try:
            if first_pricing_date == "1900-01-01":
                asset_service.update_one(
                    id=asset_id,
                    first_pricing_date=first_date,
                )
                logger.info(
                    f""" Symbol {symbol} - Updated first pricing date: {first_date}"""
                )
        except Exception as e:
            logger.error(
                f""" Symbol {symbol} - Error while updating first pricing date: {e}"""
            )

        try:
            adjusted_asset_pricing_service.insert_with_select(asset_id)
            logger.info(
                f""" Symbol {symbol} - Processed adjusted data for the period {first_date} - {last_date}"""
            )
        except Exception as e:
            logger.error(
                f""" Symbol {symbol} - Error while processing adjusted data: {e}"""
            )
            continue

        try:
            asset_service.update_one(
                id=asset_id,
                last_pricing_date=last_date,
            )
            logger.info(
                f""" Symbol {symbol} - Updated last pricing date: {last_date}"""
            )
        except Exception as e:
            logger.error(
                f""" Symbol {symbol} - Error while updating last pricing date: {e}"""
            )
