import uuid
from datetime import datetime
from functools import lru_cache
from typing import Optional

import grpc
from loguru import logger

from clients.grpc.proto.line_provider import line_provider_pb2
from clients.grpc.proto.line_provider.line_provider_pb2_grpc import LineProviderServicer
from common.exceptions.event import EventNotExists
from db.postgres.models.event import EventStatus
from schemas.response.event import EventResponse
from services.event.abc_event import AbstractEventService
from services.event.event import get_event_service


class LineProviderServicer(LineProviderServicer):
    def __init__(self):
        self.event_service: Optional[AbstractEventService] = None

    async def init_services(self):
        self.event_service = await get_event_service()

    async def GetEvents(self, request, context) -> line_provider_pb2.GetEventsResponse:
        """
        GRPC get events
        Args:
            request: GRPC request object
            context: GRPC context object for response
        Returns:
            CreateUserBalanceResponse
            context INTERNAL if error in service working
        """
        try:
            events = await self.event_service.get_available_events()
            return line_provider_pb2.GetEventsResponse(
                events=[
                    line_provider_pb2.EventResponse(**EventResponse.to_grpc(event))
                    for event in events
                ]
            )
        except Exception as e:
            error_msg = "Error occurred: " + str(e)
            context.set_details(error_msg)
            logger.opt(exception=e).error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)

    async def CheckIfEventExists(
        self, request, context
    ) -> line_provider_pb2.EventResponse:
        """
        GRPC check if event exists
        Args:
            request: GRPC request object
            context: GRPC context object for response
        Returns:
            CreateUserBalanceResponse
            context INTERNAL if error in service working
        """
        try:
            uuid.UUID(request.event_id)
            if (
                event := await self.event_service.check_existing_event(
                    id=request.event_id, status=EventStatus.PENDING
                )
            ) and datetime.utcnow() < event.deadline:
                return line_provider_pb2.EventResponse(**EventResponse.to_grpc(event))
            return line_provider_pb2.EventResponse()
        except ValueError as e:
            error_msg = "Error occurred: " + str(e)
            context.set_details(error_msg)
            logger.opt(exception=e).error(error_msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        except Exception as e:
            error_msg = "Error occurred: " + str(e)
            context.set_details(error_msg)
            logger.opt(exception=e).error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)


@lru_cache
async def get_line_provider_servicer():
    servicer = LineProviderServicer()
    await servicer.init_services()
    return servicer
