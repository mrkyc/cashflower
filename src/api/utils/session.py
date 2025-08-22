from fastapi import Header, HTTPException, status
import uuid


__all__ = ["get_session_id"]


def get_session_id(x_session_id: str = Header(...)):
    try:
        uuid.UUID(x_session_id, version=4)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid UUID format",
        )

    return x_session_id
