from datetime import datetime, timedelta
from typing import Any, Optional

from pydantic import BaseModel, Field, validator

from db.postgres.models.event import EventStatus


class CreateEventSchema(BaseModel):
    coefficient: float = Field(example=1.25, gt=1)
    deadline: datetime = Field(
        example=(datetime.utcnow() + timedelta(days=3)).isoformat()
    )
    status: EventStatus = EventStatus.PENDING

    @validator("deadline", pre=True)
    def make_naive(cls, v: Any) -> datetime:
        dt = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
        return dt.replace(tzinfo=None)


class UpdateEventSchema(BaseModel):
    coefficient: Optional[float] = Field(example=1.25, gt=1)
    status: EventStatus


class GetEventSchema(BaseModel):
    deadline: datetime
