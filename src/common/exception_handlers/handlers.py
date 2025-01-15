from fastapi import status

from common.exception_handlers.base_exception_handler import (
    RequestIdJsonExceptionHandler,
)
from common.exceptions import IntegrityDataError
from common.exceptions.base import ObjectAlreadyExists, ObjectDoesNotExist
from common.exceptions.event import EventError
from common.exceptions.grpc import GRPCError


class ValidationExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_400_BAD_REQUEST
    exception = IntegrityDataError


class ObjectAlreadyExistsExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_409_CONFLICT
    exception = ObjectAlreadyExists


class ObjectDoesNotExistExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_404_NOT_FOUND
    exception = ObjectDoesNotExist


class GRPCExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_502_BAD_GATEWAY
    exception = GRPCError


class EventErrorHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_400_BAD_REQUEST
    exception = EventError
