import uuid
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from schemas.request.event import CreateEventSchema, UpdateEventSchema
from schemas.response.event import EventResponse


class AbstractEventService(ABC):
    @abstractmethod
    async def create_event(self, schema: CreateEventSchema) -> EventResponse:
        ...

    @abstractmethod
    async def update_event(
        self, event_id: str, schema: UpdateEventSchema
    ) -> EventResponse:
        ...

    @abstractmethod
    async def delete_event(self, event_id: str):
        ...

    @abstractmethod
    async def get_event_by_id(
        self, event_id: Union[uuid.UUID, str], **kwargs
    ) -> EventResponse:
        ...

    @abstractmethod
    async def check_existing_event(self, **kwargs) -> Optional[EventResponse]:
        ...

    @abstractmethod
    async def get_available_events(self, **kwargs) -> List[EventResponse]:
        ...
