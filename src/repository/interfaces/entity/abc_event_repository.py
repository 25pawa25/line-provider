from abc import abstractmethod
from typing import List, Optional

from repository.base.abc_entity_repository import BaseRepository
from schemas.entities.base_entity import BaseEntity


class AbstractEventRepository(BaseRepository):
    @abstractmethod
    async def create_event(self, **fields) -> BaseEntity:
        pass

    @abstractmethod
    async def update_event(self, event_id: str, **fields) -> Optional[BaseEntity]:
        pass

    @abstractmethod
    async def delete_event(self, event_id: str):
        pass

    @abstractmethod
    async def get_event_by(
        self, raise_if_notfound: bool = True, **kwargs
    ) -> Optional[BaseEntity]:
        pass

    @abstractmethod
    async def get_events_by(
        self, page: int = 1, page_size: int = 10, **fields
    ) -> List[BaseEntity]:
        pass
