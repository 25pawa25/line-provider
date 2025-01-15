import uuid
from datetime import datetime
from typing import List, Optional, Union

from db.postgres.connection import get_postgres_session
from db.postgres.models.event import EventStatus
from repository.grpc_implementation.bet_repository import get_grpc_bet_repository
from repository.interfaces.entity.abc_event_repository import AbstractEventRepository
from repository.interfaces.grpc.abc_bet_repository import AbstractBetRepository
from repository.postgres_implementation.event_repository import SQLEventRepository
from schemas.request.event import CreateEventSchema, UpdateEventSchema
from schemas.response.event import EventResponse
from services.event.abc_event import AbstractEventService


class EventService(AbstractEventService):
    def __init__(
        self,
        event_repository: AbstractEventRepository,
        bet_repository: AbstractBetRepository,
    ) -> None:
        self.event_repository = event_repository
        self.bet_repository = bet_repository

    async def create_event(self, schema: CreateEventSchema) -> EventResponse:
        """
        Create event
        Args:
            schema: CreateEventSchema
        Returns:
            EventResponse
        """
        event = await self.event_repository.create_event(**schema.dict())
        return EventResponse.from_orm(event)

    async def update_event(
        self, event_id: str, schema: UpdateEventSchema
    ) -> EventResponse:
        """
        Update event
        Args:
            event_id: id of the event
            schema: UpdateEventSchema
        Returns:
            EventResponse
        """
        await self.bet_repository.update_event(
            event_id=event_id, status=schema.status.value
        )
        event = await self.event_repository.update_event(
            event_id=event_id,
            updated_at=datetime.utcnow(),
            **schema.dict(exclude_none=True),
        )
        return EventResponse.from_orm(event)

    async def delete_event(self, event_id: str):
        """
        Delete event
        Args:
            event_id: id of the event
        """
        await self.event_repository.delete_event(event_id=event_id)

    async def get_event_by_id(
        self, event_id: Union[uuid.UUID, str], **kwargs
    ) -> EventResponse:
        """
        Get event by user_id
        Args:
            event_id: id of the event
        Returns:
            EventResponse
        """
        event_db = await self.event_repository.get_event_by(id=event_id, **kwargs)
        return EventResponse.from_orm(event_db)

    async def check_existing_event(self, **kwargs) -> Optional[EventResponse]:
        if event_db := await self.event_repository.get_event_by(
            raise_if_notfound=False, **kwargs
        ):
            return EventResponse.from_orm(event_db)

    async def get_available_events(self, **kwargs) -> List[EventResponse]:
        """
        Get available events
        Returns:
            List of the available events
        """
        events_db = await self.event_repository.get_events_by(
            deadline=datetime.utcnow(), status=EventStatus.PENDING, **kwargs
        )
        return [EventResponse.from_orm(event) for event in events_db]


async def get_event_service():
    session = await get_postgres_session()
    return EventService(
        event_repository=SQLEventRepository(session=session),
        bet_repository=get_grpc_bet_repository(),
    )
