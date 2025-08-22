from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.concurrency import run_in_threadpool

from .utils import (
    get_session_id,
    get_db,
    get_user,
    get_upsert_manager,
    get_download_manager,
)
from .utils.db import Database
from .utils.pricings import download_pricings_logic, PricingDownloadError

from src.dto import SettingsDTO
from src.application import UpsertManager, DownloadManager
from src.domain import User

router = APIRouter()


def _init_user_and_settings(
    session_id: str,
    db: Database,
    upsert_manager: UpsertManager,
    settings_dto: SettingsDTO,
) -> User:
    """Creates the database, user, and settings."""
    db.create_database()
    user = upsert_manager.upsert_user(session_id=session_id)
    upsert_manager.upsert_settings(user_id=user.id, settings_dto=settings_dto)
    return user


async def _trigger_pricing_download(
    download_manager: DownloadManager, settings_dto: SettingsDTO
):
    """Downloads all necessary pricings based on user settings."""
    asset_symbols = set(settings_dto.portfolio_group_assets.asset_symbol)
    transaction_file_currencies = set(settings_dto.transaction_files.currency)
    analysis_currency = settings_dto.analysis_currency

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


def _upsert_portfolio_structure(
    upsert_manager: UpsertManager, user_id: int, settings_dto: SettingsDTO
):
    """Upserts all portfolio-related data."""
    portfolio_aggregate = upsert_manager.upsert_portfolio_aggregate(user_id=user_id)
    upsert_manager.upsert_portfolios(
        user_id=user_id,
        portfolio_aggregate_id=portfolio_aggregate.id,
        transaction_files=settings_dto.transaction_files,
    )
    upsert_manager.upsert_portfolio_groups(
        user_id=user_id, portfolio_groups=settings_dto.portfolio_groups
    )
    upsert_manager.upsert_portfolio_group_assets(
        user_id=user_id, portfolio_group_assets=settings_dto.portfolio_group_assets
    )
    upsert_manager.upsert_portfolio_transaction_files(
        user_id=user_id,
        portfolio_transaction_files=settings_dto.transaction_files,
        analysis_currency=settings_dto.analysis_currency,
    )
    upsert_manager.upsert_portfolio_transactions(
        user_id=user_id, list_of_transactions=settings_dto.transactions.items
    )


@router.post(
    "/settings",
    tags=["Settings"],
    summary="Creates or updates settings and all related data",
    description="A comprehensive endpoint that creates a user, settings, portfolios, groups, and transactions based on the provided data.",
    status_code=status.HTTP_201_CREATED,
)
async def upsert_pipeline(
    session_id: str = Depends(get_session_id),
    db: Database = Depends(get_db),
    settings_dto: SettingsDTO = Body(...),
    upsert_manager: UpsertManager = Depends(get_upsert_manager),
    download_manager: DownloadManager = Depends(get_download_manager),
):
    user = await run_in_threadpool(
        _init_user_and_settings, session_id, db, upsert_manager, settings_dto
    )
    await _trigger_pricing_download(download_manager, settings_dto)
    await run_in_threadpool(
        _upsert_portfolio_structure, upsert_manager, user.id, settings_dto
    )

    return {
        "message": "Settings and all related data have been created/updated successfully."
    }


@router.get(
    "/settings",
    tags=["Settings"],
    summary="Gets the current settings",
)
async def get_settings(user: User = Depends(get_user)):
    return await run_in_threadpool(lambda: user.settings)
