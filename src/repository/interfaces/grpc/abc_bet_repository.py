from abc import ABC, abstractmethod


class AbstractBetRepository(ABC):
    @abstractmethod
    async def update_event(self, event_id: str, status: str):
        pass
