from fastapi import APIRouter
from .devices import router as devices_router
from .events import router as events_router

router = APIRouter()

router.include_router(devices_router, prefix="/devices", tags=["devices"])
router.include_router(events_router, prefix="/events", tags=["devices"]) 