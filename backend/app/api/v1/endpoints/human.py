from fastapi import APIRouter
from .elderly_persons import router as elderly_persons_router
from .reminders import router as reminders_router
from .alerts import router as alerts_router
from .device_services import router as device_services_router

router = APIRouter()

router.include_router(elderly_persons_router, prefix="/elderly-persons", tags=["human"])
router.include_router(reminders_router, prefix="/reminders", tags=["human"])
router.include_router(alerts_router, prefix="/alerts", tags=["human"])
router.include_router(device_services_router, tags=["human"]) 