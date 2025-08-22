from fastapi import APIRouter, status, Depends
from fastapi.concurrency import run_in_threadpool

from .utils.services import (
    get_portfolio_aggregate_service,
    get_asset_service,
    get_currency_pair_service,
)
from .utils import get_user
from .constants import RESET_DATE

from src.domain import *

router = APIRouter()


def _manage_pricings(
    user: User,
    asset_service: AssetService,
    currency_pair_service: CurrencyPairService,
    reset: bool = False,
):
    """Helper to reset or delete pricings."""
    currencies = set()
    asset_ids = set()
    currency_ids = set()

    asset_symbols = set(user.settings.portfolio_group_assets["asset_symbol"])
    for asset_symbol in asset_symbols:
        asset = asset_service.get_one_by_symbol(asset_symbol)
        if asset:
            asset_ids.add(asset.id)
            currencies.add(asset.currency)

    currencies.update(user.settings.transaction_files["currency"])
    analysis_currency = user.settings.analysis_currency

    for currency in currencies:
        currency = currency.lower()
        if currency == analysis_currency:
            continue

        currency_pair = currency_pair_service.get_one_by_name(
            currency + analysis_currency
        )
        if currency_pair:
            currency_ids.add(currency_pair.id)

    # TODO: Use a bulk update or delete operation
    if reset:
        for asset_id in asset_ids:
            asset_service.update_one(asset_id, last_pricing_date=RESET_DATE)
        for currency_id in currency_ids:
            currency_pair_service.update_one(currency_id, last_pricing_date=RESET_DATE)
    else:
        for asset_id in asset_ids:
            asset_service.delete_one(asset_id)
        for currency_id in currency_ids:
            currency_pair_service.delete_one(currency_id)


@router.post(
    "/reset-checkpoint-date",
    tags=["Reset"],
    summary="Resets the last processing date (checkpoint)",
    description=f"Sets the last processing date to '{RESET_DATE}', which forces data to be reprocessed from the beginning. It also resets the price download dates.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def reset_checkpoint_date(
    user: User = Depends(get_user),
    portfolio_aggregate_service: PortfolioAggregateService = Depends(
        get_portfolio_aggregate_service
    ),
    asset_service: AssetService = Depends(get_asset_service),
    currency_pair_service: CurrencyPairService = Depends(get_currency_pair_service),
):
    await run_in_threadpool(
        portfolio_aggregate_service.update_one,
        id=user.portfolio_aggregate.id,
        checkpoint_date=RESET_DATE,
    )
    await run_in_threadpool(
        _manage_pricings, user, asset_service, currency_pair_service, reset=True
    )


@router.post(
    "/reset-user",
    tags=["Reset"],
    summary="Resets all user data",
    description="Deletes all data associated with the user, including portfolios, transactions, and downloaded prices. Use with caution!",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def reset_user(
    user: User = Depends(get_user),
    portfolio_aggregate_service: PortfolioAggregateService = Depends(
        get_portfolio_aggregate_service
    ),
    asset_service: AssetService = Depends(get_asset_service),
    currency_pair_service: CurrencyPairService = Depends(get_currency_pair_service),
):
    await run_in_threadpool(
        portfolio_aggregate_service.delete_one, id=user.portfolio_aggregate.id
    )
    await run_in_threadpool(
        _manage_pricings, user, asset_service, currency_pair_service, reset=False
    )
