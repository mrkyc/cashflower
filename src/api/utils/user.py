from fastapi import HTTPException, status, Depends
from fastapi.concurrency import run_in_threadpool

from .session import get_session_id
from .services import get_user_service

from src.domain import User, UserService, Portfolio, PortfolioGroup, Asset


__all__ = [
    "get_user",
    "validate_portfolio_for_user",
    "validate_portfolio_group_for_user",
    "validate_asset_in_portfolio",
]


async def get_user(
    session_id: str = Depends(get_session_id),
    user_service: UserService = Depends(get_user_service),
):
    user = await run_in_threadpool(user_service.get_one_by_session_id, session_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif not user.settings:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User settings not found. Please create a user with valid settings.",
        )
    elif not user.portfolio_aggregate:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Portfolio aggregate not found for the user. Please run data processing.",
        )
    else:
        return user


def _validate_portfolio_sync(portfolio_id: int, user: User) -> Portfolio | None:
    return next((p for p in user.portfolios if p.id == portfolio_id), None)


async def validate_portfolio_for_user(
    portfolio_id: int, user: User = Depends(get_user)
) -> Portfolio:
    """
    Dependency that checks if the portfolio belongs to the user and returns it.
    """
    portfolio = await run_in_threadpool(_validate_portfolio_sync, portfolio_id, user)
    if portfolio:
        return portfolio

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Portfolio not found or user does not have access.",
    )


def _validate_portfolio_group_sync(
    portfolio_group_id: int, user: User
) -> PortfolioGroup | None:
    return next(
        (pg for pg in user.portfolio_groups if pg.id == portfolio_group_id), None
    )


async def validate_portfolio_group_for_user(
    portfolio_group_id: int, user: User = Depends(get_user)
) -> PortfolioGroup:
    """
    Dependency that checks if the portfolio group belongs to the user and returns it.
    """
    portfolio_group = await run_in_threadpool(
        _validate_portfolio_group_sync, portfolio_group_id, user
    )
    if portfolio_group:
        return portfolio_group

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Portfolio group not found or user does not have access.",
    )


def _validate_asset_in_portfolio_sync(
    asset_id: int, portfolio: Portfolio, user: User
) -> Asset | None:
    found_asset_gen = (
        asset
        for pg in user.portfolio_groups
        if pg.portfolio_id == portfolio.id
        for asset in pg.assets
        if asset.asset_id == asset_id
    )
    found_asset = next(found_asset_gen, None)
    if found_asset:
        return found_asset.asset
    return None


async def validate_asset_in_portfolio(
    asset_id: int,
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    user: User = Depends(get_user),
) -> Asset:
    """
    Dependency that checks if an asset exists within a given portfolio and returns it.
    Relies on `validate_portfolio_for_user` to ensure portfolio access is allowed.
    """
    asset = await run_in_threadpool(
        _validate_asset_in_portfolio_sync, asset_id, portfolio, user
    )
    if asset:
        return asset

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The combination of portfolio and asset IDs not found or user does not have access.",
    )
