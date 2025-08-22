from fastapi.concurrency import run_in_threadpool

from src.application import DownloadManager


__all__ = ["download_pricings_logic", "PricingDownloadError"]


class PricingDownloadError(Exception):
    """Custom exception for errors during pricing download."""

    pass


async def download_pricings_logic(
    download_manager: DownloadManager,
    asset_symbols: set[str],
    transaction_file_currencies: set[str],
    analysis_currency: str,
):
    """
    Core logic for downloading asset and currency prices.
    Can be reused by different endpoints.
    """
    if not asset_symbols and not transaction_file_currencies:
        raise PricingDownloadError(
            "No assets or currencies found in user settings to download prices for."
        )

    await run_in_threadpool(
        download_manager.upsert_assets_and_currencies,
        asset_symbols,
        transaction_file_currencies,
        analysis_currency,
    )
