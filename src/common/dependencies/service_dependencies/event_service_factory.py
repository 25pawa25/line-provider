from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.dependencies.registrator import add_factory_to_mapper
from db.postgres.connection import get_async_session
from repository.grpc_implementation.bet_repository import get_grpc_bet_repository
from repository.postgres_implementation.event_repository import SQLEventRepository
from services import EventService
from services.event.abc_event import AbstractEventService


@add_factory_to_mapper(AbstractEventService)
def create_event_service(
    session: AsyncSession = Depends(get_async_session),
):
    return EventService(
        event_repository=SQLEventRepository(session=session),
        bet_repository=get_grpc_bet_repository(),
    )
