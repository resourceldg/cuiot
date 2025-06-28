from fastapi import APIRouter
from app.api.v1.endpoints import health, human, admin
from app.api.v1.endpoints import debug

api_router = APIRouter()

# Rutas de autenticación y salud
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Routers por dominio
api_router.include_router(human.router, tags=["human"])
api_router.include_router(admin.router, tags=["admin"])
api_router.include_router(debug.router, prefix="/debug", tags=["debug"])

# TODO: Agregar los demás routers cuando estén implementados
# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# api_router.include_router(elderly_persons.router, prefix="/elderly-persons", tags=["elderly-persons"])
# api_router.include_router(events.router, prefix="/events", tags=["events"])
# api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
# api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"]) 