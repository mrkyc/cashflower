from fastapi import APIRouter, Depends, Query
from fastapi.concurrency import run_in_threadpool

from .utils.user import (
    get_user,
    validate_portfolio_for_user,
    validate_portfolio_group_for_user,
    validate_asset_in_portfolio,
)
from .utils.services import *

from src.domain import *


router = APIRouter()


@router.get(
    "/portfolio-variants",
    tags=["Performance"],
    summary="Gets portfolio variants",
)
async def get_portfolio_variants(
    user: User = Depends(get_user),
    service: PortfolioAggregateService = Depends(get_portfolio_aggregate_service),
):
    return await run_in_threadpool(service.get_portfolio_variants, user.id)


@router.get(
    "/portfolio-aggregate-performance",
    tags=["Performance"],
    summary="Gets aggregate portfolio performance",
)
async def get_portfolio_aggregate_performance(
    user: User = Depends(get_user),
    service: PortfolioAggregatePerformanceService = Depends(
        get_portfolio_aggregate_performance_service
    ),
):
    return await run_in_threadpool(
        service.get_performance_by_id,
        portfolio_aggregate_id=user.portfolio_aggregate.id,
    )


@router.get(
    "/portfolio-aggregate-performance-status",
    tags=["Performance"],
    summary="Gets the status of aggregate portfolio performance for a given date",
)
async def get_portfolio_aggregate_performance_status(
    status_date: str = Query(None),
    user: User = Depends(get_user),
    service: PortfolioAggregatePerformanceService = Depends(
        get_portfolio_aggregate_performance_service
    ),
):
    return await run_in_threadpool(
        service.get_performance_status,
        portfolio_aggregate_id=user.portfolio_aggregate.id,
        status_date=status_date,
    )


@router.get(
    "/portfolio-performance/{portfolio_id}",
    tags=["Performance"],
    summary="Gets performance for a specific portfolio",
)
async def get_portfolio_performance(
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    service: PortfolioPerformanceService = Depends(get_portfolio_performance_service),
):
    return await run_in_threadpool(
        service.get_performance_by_portfolio_id, portfolio_id=portfolio.id
    )


@router.get(
    "/portfolio-performance-status/{portfolio_id}",
    tags=["Performance"],
    summary="Gets the performance status for a specific portfolio on a given date",
)
async def get_portfolio_performance_status(
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    status_date: str = Query(None),
    service: PortfolioPerformanceService = Depends(get_portfolio_performance_service),
):
    return await run_in_threadpool(
        service.get_performance_status,
        portfolio_id=portfolio.id,
        status_date=status_date,
    )


@router.get(
    "/portfolio-group-performance/{portfolio_group_id}",
    tags=["Performance"],
    summary="Gets performance for a portfolio group",
)
async def get_portfolio_group_performance(
    portfolio_group: PortfolioGroup = Depends(validate_portfolio_group_for_user),
    service: PortfolioGroupPerformanceService = Depends(
        get_portfolio_group_performance_service
    ),
):
    return await run_in_threadpool(
        service.get_performance_by_portfolio_group_id,
        portfolio_group_id=portfolio_group.id,
    )


@router.get(
    "/portfolio-group-performance-status/{portfolio_group_id}",
    tags=["Performance"],
    summary="Gets the performance status for a portfolio group on a given date",
)
async def get_portfolio_group_performance_status(
    portfolio_group: PortfolioGroup = Depends(validate_portfolio_group_for_user),
    status_date: str = Query(None),
    service: PortfolioGroupPerformanceService = Depends(
        get_portfolio_group_performance_service
    ),
):
    return await run_in_threadpool(
        service.get_performance_status,
        portfolio_group_id=portfolio_group.id,
        status_date=status_date,
    )


@router.get(
    "/portfolio-asset-performance/{portfolio_id}/{asset_id}",
    tags=["Performance"],
    summary="Gets performance for a specific asset within a given portfolio",
)
async def get_portfolio_asset_performance(
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    asset: Asset = Depends(validate_asset_in_portfolio),
    service: PortfolioAssetPerformanceService = Depends(
        get_portfolio_asset_performance_service
    ),
):
    return await run_in_threadpool(
        service.get_performance_by_portfolio_id_and_asset_id,
        portfolio_id=portfolio.id,
        asset_id=asset.id,
    )


@router.get(
    "/portfolio-asset-performance-status/{portfolio_id}/{asset_id}",
    tags=["Performance"],
    summary="Gets the performance status for an asset in a portfolio on a given date",
)
async def get_portfolio_asset_performance_status(
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    asset: Asset = Depends(validate_asset_in_portfolio),
    status_date: str = Query(None),
    service: PortfolioAssetPerformanceService = Depends(
        get_portfolio_asset_performance_service
    ),
):
    return await run_in_threadpool(
        service.get_performance_status,
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        status_date=status_date,
    )


@router.get(
    "/portfolio-group-weights/{portfolio_id}",
    tags=["Performance"],
    summary="Gets group weights in a given portfolio",
)
async def get_portfolio_group_weights(
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    service: PortfolioGroupPerformanceService = Depends(
        get_portfolio_group_performance_service
    ),
):
    return await run_in_threadpool(
        service.get_weights_by_portfolio_id, portfolio_id=portfolio.id
    )


@router.get(
    "/portfolio-assets-status/{portfolio_id}",
    tags=["Performance"],
    summary="Gets the status of assets in a given portfolio",
)
async def get_portfolio_assets_status(
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    service: PortfolioAssetPerformanceService = Depends(
        get_portfolio_asset_performance_service
    ),
):
    return await run_in_threadpool(
        service.get_assets_status_by_portfolio_id, portfolio_id=portfolio.id
    )


@router.get(
    "/portfolio-groups/{portfolio_id}",
    tags=["Performance"],
    summary="Gets groups for a given portfolio",
)
async def get_portfolio_groups(
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    service: PortfolioGroupService = Depends(get_portfolio_group_service),
):
    results = await run_in_threadpool(
        service.get_portfolio_groups_by_portfolio_id, portfolio_id=portfolio.id
    )
    return [dict(row._mapping) for row in results]


@router.get(
    "/model-portfolio-stats/{portfolio_id}",
    tags=["Performance"],
    summary="Gets statistics for the model portfolio",
)
async def get_model_portfolio_stats(
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    service: PortfolioAssetPerformanceService = Depends(
        get_portfolio_asset_performance_service
    ),
):
    return await run_in_threadpool(
        service.get_pct_changes_stats_by_portfolio_id, portfolio_id=portfolio.id
    )


@router.get(
    "/portfolio-market-values/{portfolio_id}",
    tags=["Performance"],
    summary="Gets market values for a given portfolio",
)
async def get_portfolio_market_values(
    portfolio: Portfolio = Depends(validate_portfolio_for_user),
    service: PortfolioPerformanceService = Depends(get_portfolio_performance_service),
):
    results = await run_in_threadpool(
        service.get_market_values_by_portfolio_id, portfolio_id=portfolio.id
    )
    return [dict(row._mapping) for row in results]
