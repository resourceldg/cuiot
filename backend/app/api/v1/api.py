from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, debug, health, cared_persons, devices, alerts, events, reminders, reports

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(cared_persons.router, prefix="/cared-persons", tags=["cared-persons"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
