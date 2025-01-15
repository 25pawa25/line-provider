from fastapi import APIRouter

from clients.api.v1.event import event_routers

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(event_routers)
