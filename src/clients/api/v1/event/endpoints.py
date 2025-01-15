import uuid

from fastapi import APIRouter, Depends, status
from loguru import logger

from schemas.request.event import CreateEventSchema, UpdateEventSchema
from schemas.response.event import EventResponse
from services.event.abc_event import AbstractEventService

router = APIRouter(prefix="/line_provider", tags=["Event actions"])


@router.post(
    "",
    summary="Create event",
    description="Create event",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    request: CreateEventSchema,
    event_service: AbstractEventService = Depends(),
) -> EventResponse:
    """
    Create an event
    Args:
        request: CreateEventSchema
        event_service: EventService
    Returns:
        EventResponse
    """
    logger.info("Create event")
    return await event_service.create_event(request)


@router.get(
    "", summary="Get event", description="Get event by id", response_model=EventResponse
)
async def get_event_by_id(
    event_id: uuid.UUID,
    event_service: AbstractEventService = Depends(),
) -> EventResponse:
    """
    Get event by id
    Args:
        event_id: id of the event
        event_service: EventService
    Returns:
        EventResponse
    """
    logger.info(f"Get event by id: {event_id}")
    return await event_service.get_event_by_id(event_id=event_id)


@router.patch(
    "", summary="Update event", description="Update event", response_model=EventResponse
)
async def update_event(
    event_id: str,
    request: UpdateEventSchema,
    event_service: AbstractEventService = Depends(),
) -> EventResponse:
    """
    Update event
    Args:
        event_id: id of the event
        request: UpdateEventSchema
        event_service: EventService
    Returns:
        EventResponse
    """
    logger.info(f"Update event: {event_id}")
    return await event_service.update_event(event_id=event_id, schema=request)


@router.delete(
    "",
    summary="Delete event",
    description="Delete event",
    status_code=status.HTTP_200_OK,
)
async def delete_event(
    event_id: str,
    event_service: AbstractEventService = Depends(),
):
    """
    Delete an event
    Args:
        event_id: id of the event
        event_service: EventService
    Returns:
        EventResponse
    """
    logger.info("Delete event")
    await event_service.delete_event(event_id=event_id)
