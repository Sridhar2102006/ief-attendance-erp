from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.core.config import get_settings


class DatabaseConfigurationError(RuntimeError):
    """Raised when the database URL has not been configured."""


@lru_cache
def get_engine() -> Engine:
    database_url = get_settings().database_url
    if database_url is None:
        raise DatabaseConfigurationError("DATABASE_URL is not configured.")

    return create_engine(str(database_url), pool_pre_ping=True)
