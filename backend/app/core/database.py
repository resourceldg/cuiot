from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Crear engine de base de datos usando la URL según el entorno
engine = create_engine(
    settings.get_database_url,
    connect_args={"check_same_thread": False} if settings.get_database_url.startswith("sqlite") else {},
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.environment == "development"
)

# Crear sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 