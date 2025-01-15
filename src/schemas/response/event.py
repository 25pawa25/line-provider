import uuid
from datetime import datetime

from pydantic import BaseModel

from db.postgres.models.event import EventStatus


class EventResponse(BaseModel):
    id: uuid.UUID
    coefficient: float
    status: EventStatus
    deadline: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @staticmethod
    def to_grpc(instance: "EventResponse"):
        return dict(
            id=str(instance.id),
            coefficient=instance.coefficient,
            status=instance.status.value,
            deadline=str(instance.deadline),
            created_at=str(instance.created_at),
            updated_at=str(instance.updated_at),
        )
