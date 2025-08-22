import logging

from .extract import extract_data_yfinance
from .transform import transform_data_yfinance
from .load import load_data_yfinance
from src.domain import (
    CurrencyPairService,
    CurrencyPairPricingService,
    AdjustedCurrencyPairPricingService,
)


logger = logging.getLogger(__name__)


def currency_pairs_etl_yfinance(
    symbols: list[str],
    currency_pair_service: CurrencyPairService,
    currency_pair_pricing_service: CurrencyPairPricingService,
    adjusted_currency_pair_pricing_service: AdjustedCurrencyPairPricingService,
):
    currency_pairs = [
        currency_pair_service.get_one_by_symbol(symbol=symbol) for symbol in symbols
    ]
    currency_pairs_info = {
        currency_pair.symbol: {
            "currency_pair_id": currency_pair.id,
            "first_pricing_date": currency_pair.first_pricing_date,
            "last_pricing_date": currency_pair.last_pricing_date,
        }
        for currency_pair in currency_pairs
        if currency_pair is not None
    }
    if set(currency_pairs_info.keys()) != set(symbols):
        missing_symbols = set(symbols) - set(currency_pairs_info.keys())
        logger.warning(
            f" CURRENCIES - The following symbols are not found in the database: {', '.join(missing_symbols)}"
        )

    start_date = min(
        currency_pair["last_pricing_date"]
        for currency_pair in currency_pairs_info.values()
    )

    try:
        df_data = extract_data_yfinance(symbols, start_date)
    except Exception as e:
        logger.error(
            f" CURRENCIES - Error while extracting data for the period starting from {start_date}: {e}"
        )
        return

    if df_data is None or df_data.empty:
        logger.warning(
            f" CURRENCIES - No data is available for the period starting from {start_date}"
        )
        return

    for symbol, currency_pair in currency_pairs_info.items():
        currency_pair_id = currency_pair["currency_pair_id"]
        first_pricing_date = currency_pair["first_pricing_date"]
        last_pricing_date = currency_pair["last_pricing_date"]

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
            transformed_df_data = transform_data_yfinance(
                df_data_symbol, currency_pair_id
            )
        except Exception as e:
            logger.error(
                f" Symbol {symbol} - Error while transforming data for the period {df_data_symbol.iloc[0].name.date()} - {df_data_symbol.iloc[-1].name.date()}: {e}"
            )
            continue

        first_date = transformed_df_data["date"].iloc[0]
        last_date = transformed_df_data["date"].iloc[-1]

        try:
            load_data_yfinance(
                currency_pair_pricing_service, transformed_df_data, currency_pair_id
            )
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
                currency_pair_service.update_one(
                    id=currency_pair_id,
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
            adjusted_currency_pair_pricing_service.insert_with_select(currency_pair_id)
            logger.info(
                f""" Symbol {symbol} - Processed adjusted data for the period {first_date} - {last_date}"""
            )
        except Exception as e:
            logger.error(
                f""" Symbol {symbol} - Error while processing adjusted data: {e}"""
            )
            continue

        try:
            currency_pair_service.update_one(
                id=currency_pair_id,
                last_pricing_date=last_date,
            )
            logger.info(
                f""" Symbol {symbol} - Updated last pricing date: {last_date}"""
            )
        except Exception as e:
            logger.error(
                f""" Symbol {symbol} - Error while updating last pricing date: {e}"""
            )
