import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, TIMESTAMP, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped

from db.postgres.models.base_model import BaseModel, Column
from db.postgres.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


@enum.unique
class EventStatus(enum.Enum):
    PENDING = "pending"
    FIRST_WIN = "first_win"
    SECOND_WIN = "second_win"


class Event(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for event db table."""

    __tablename__ = "event"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="event_pkey"),
        CheckConstraint("coefficient > 0", name="check_coefficient_positive"),
    )
    coefficient: Mapped[Decimal] = Column(DECIMAL(precision=7, scale=2), nullable=False)
    deadline: Mapped[datetime] = Column(
        TIMESTAMP(timezone=False),
        nullable=False,
    )
    status: Mapped[str] = Column(
        ENUM(EventStatus, name="event_status"),
        nullable=False,
        default=EventStatus.PENDING,
    )

    def __repr__(self):
        return (
            f"Event(id={self.id}, coefficient={self.coefficient}, deadline={self.deadline}, "
            f"status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})"
        )
