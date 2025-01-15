import contextlib
from typing import AsyncIterator

from fastapi import FastAPI

from core.config import settings
from db.postgres.session_manager import db_manager


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_manager.init(settings.postgres.database_url)
    yield
    await db_manager.close()
