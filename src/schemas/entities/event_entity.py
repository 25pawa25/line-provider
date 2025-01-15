from datetime import datetime

from pydantic import Field

from db.postgres.models.event import EventStatus
from schemas.entities.base_entity import BaseEntity


class EventEntity(BaseEntity):
    coefficient: float
    status: EventStatus
    deadline: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
