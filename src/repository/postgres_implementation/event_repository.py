import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select

from common.exceptions.event import EventNotExists
from db.postgres.models.event import Event
from repository.interfaces.entity.abc_event_repository import AbstractEventRepository
from repository.postgres_implementation.base_repository import SQLRepository
from schemas.entities.event_entity import EventEntity


class SQLEventRepository(SQLRepository, AbstractEventRepository):
    class_model = Event
    entity_class = EventEntity

    async def create_event(self, **fields) -> EventEntity:
        """
        Creating an event
        Args:
            **fields: fields of event
        Returns:
            EventEntity
        """
        return await self.add(self.entity_class(**fields))

    async def update_event(self, event_id: str, **fields) -> EventEntity:
        """
        Updating an event
        Args:
            event_id: event id
            **fields: fields of event
        Returns:
            EventEntity
        """
        return await self.update(
            self_id=uuid.UUID(event_id), updated_at=datetime.utcnow(), **fields
        )

    async def delete_event(self, event_id: str):
        """
        Deleting an event
        Args:
            event_id: id of the event
        """
        await self.remove(self_id=uuid.UUID(event_id))

    async def get_event_by(
        self, raise_if_notfound: bool = True, **kwargs
    ) -> Optional[EventEntity]:
        """
        Get event by fields
        Args:
            raise_if_notfound: raise exception if not found
        Returns:
            EventEntity
        """
        if instance := await self.get_by(**kwargs):
            return self.to_entity(instance)
        if raise_if_notfound:
            raise EventNotExists("Event not found", **kwargs)

    async def get_events_by(
        self, page: int = 1, page_size: int = 10, **fields
    ) -> List[EventEntity]:
        """
        Get events by fields
        Args:
            page: number of the page
            page_size: size of the page
            **fields: fields to filter
        Returns:
            EventEntity
        """
        filters = []
        if deadline := fields.pop("deadline", None):
            filters.append(self.class_model.deadline > deadline)
        stmt = (
            select(self.class_model)
            .where(and_(*filters))
            .filter_by(**fields)
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        result = await self.session.execute(stmt)
        return [self.to_entity(instance) for instance in result.scalars().all()]
