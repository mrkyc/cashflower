from fastapi import Depends

from .session import get_session_id
from ..constants import DB_EXTENSIONS

from src.infrastructure import Database


__all__ = ["get_db", "get_db_session", "get_db_validation", "load_db_extensions"]


def get_db(session_id: str = Depends(get_session_id)):
    return Database(session_id)


def get_db_session(db: Database = Depends(get_db)):
    yield from db.get_db_session()


def get_db_validation(session_id: str = Depends(get_session_id)):
    db = Database(session_id)
    return db.path_exists


def load_db_extensions(db: Database = Depends(get_db)):
    """Dependency to load required database extensions."""
    db.load_extensions(DB_EXTENSIONS)
