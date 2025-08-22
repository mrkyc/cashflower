from fastapi import APIRouter, Depends, status, HTTPException

from .utils import get_user, get_download_manager
from .utils.pricings import download_pricings_logic, PricingDownloadError

from src.domain import User
from src.application import DownloadManager


router = APIRouter()


@router.post(
    "/download-pricings",
    tags=["Pricings"],
    summary="Starts downloading asset and currency prices",
    description="Triggers the process of downloading and updating prices for all assets and currency pairs defined in the user's settings.",
)
async def download_pricings(
    user: User = Depends(get_user),
    download_manager: DownloadManager = Depends(get_download_manager),
):
    analysis_currency = user.settings.analysis_currency
    asset_symbols = set(user.settings.portfolio_group_assets["asset_symbol"])
    transaction_file_currencies = set(user.settings.transaction_files["currency"])

    try:
        await download_pricings_logic(
            download_manager=download_manager,
            asset_symbols=asset_symbols,
            transaction_file_currencies=transaction_file_currencies,
            analysis_currency=analysis_currency,
        )
    except (ValueError, PricingDownloadError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to download pricings: {e}",
        )

    return {"message": "Pricings downloaded."}
