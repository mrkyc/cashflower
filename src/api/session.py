from fastapi import APIRouter, HTTPException, status, Depends
import uuid

from .utils.db import get_db_validation


router = APIRouter()


@router.get(
    "/session-id",
    tags=["Session"],
    summary="Generates a new session ID",
    description="Returns a unique UUID that can be used to track a user session.",
)
def get_session_id():
    return str(uuid.uuid4())


@router.post(
    "/validate-session-id",
    tags=["Session"],
    summary="Validates a session ID",
    description="Checks if the provided session ID is valid and exists in the system.",
)
def validate_session_id(is_valid: bool = Depends(get_db_validation)):
    if is_valid:
        return {"message": "Session ID is valid"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Session ID is invalid"
        )
