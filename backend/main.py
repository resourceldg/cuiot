from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import structlog
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.api import api_router

# Configurar logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema Integral de Monitoreo API",
    description="API para sistema de acompañamiento de personas bajo cuidado",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Incluir rutas de la API
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "Sistema Integral de Monitoreo API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "database": "connected",
        "mqtt": "connected"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejador global de excepciones HTTP"""
    logger.error(
        "HTTP Exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# --- Utilidad para decodificar bytes en dicts, listas, etc. ---
def decode_bytes(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='replace')
    if isinstance(obj, dict):
        return {k: decode_bytes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decode_bytes(i) for i in obj]
    return obj

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    error_obj = decode_bytes(exc)
    error_str = str(error_obj)
    logger.error(
        "General Exception",
        error=error_str,
        path=request.url.path,
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": error_str}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Decodifica el body y los errores si contienen bytes
    errors = decode_bytes(exc.errors())
    
    # Manejar el body de forma segura
    try:
        body = decode_bytes(exc.body)
        # Si el body es FormData, convertirlo a string
        if hasattr(body, '__class__') and 'FormData' in str(body.__class__):
            body = str(body)
        elif not isinstance(body, (str, dict, list, int, float, bool, type(None))):
            body = str(body)
    except Exception:
        body = "Unable to serialize body"
    
    logger.error(
        "Validation Error (422)",
        errors=errors,
        body=body,
        path=request.url.path
    )
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 