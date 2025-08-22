from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool

from .utils import get_user, get_data_processing_manager
from .utils.db import load_db_extensions

from src.domain import User
from src.application import DataProcessingManager


router = APIRouter()


def process_data(data_processing_manager: DataProcessingManager, user_id: int):
    """A synchronous function that runs all data processing steps."""
    data_processing_manager.process_adjusted_portfolio_transactions(user_id)
    data_processing_manager.process_portfolio_asset_performances(user_id)
    data_processing_manager.process_portfolio_group_performances(user_id)
    data_processing_manager.process_portfolio_performances(user_id)
    data_processing_manager.process_portfolio_aggregate_performances(user_id)
    data_processing_manager.update_checkpoint_date(user_id)


@router.post(
    "/run-processing",
    tags=["Processing"],
    summary="Starts data processing",
    description="Starts the full data processing pipeline for the user, including performance calculation for all portfolio levels.",
    dependencies=[Depends(load_db_extensions)],
)
async def run_processing(
    user: User = Depends(get_user),
    data_processing_manager: DataProcessingManager = Depends(
        get_data_processing_manager
    ),
):
    user_id = user.id
    await run_in_threadpool(process_data, data_processing_manager, user_id)
    return {"message": "Data processing finished."}
