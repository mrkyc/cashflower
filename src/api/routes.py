from fastapi import APIRouter

from .settings import router as settings_router
from .download_pricings import router as download_pricings_router
from .run_processing import router as run_processing_router
from .session import router as session_router
from .performance import router as performance_router
from .reset import router as reset_checkpoint_date_router


router = APIRouter()

router.include_router(settings_router)
router.include_router(download_pricings_router)
router.include_router(run_processing_router)
router.include_router(session_router)
router.include_router(performance_router)
router.include_router(reset_checkpoint_date_router)
