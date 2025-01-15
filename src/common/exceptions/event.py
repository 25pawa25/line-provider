from common.exceptions import AppException
from common.exceptions.base import ObjectDoesNotExist


class EventError(AppException):
    """Base Event Exception"""


class EventNotExists(ObjectDoesNotExist):
    """Event not exists"""
