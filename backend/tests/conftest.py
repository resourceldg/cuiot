import os
# Use PostgreSQL for tests (development database)
os.environ["DATABASE_URL"] = "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_db"

import pytest
import pytest_asyncio
from httpx import AsyncClient
from main import app
from app.core.database import get_db, engine, SessionLocal
from app.models.base import Base
from sqlalchemy import text

# Create all tables in the test database
@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables in the test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Fixture para obtener una sesión de base de datos y cerrarla correctamente."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def clean_db():
    """Clean database before each test using PostgreSQL"""
    db = next(get_db())
    try:
        db.execute(text("SET session_replication_role = replica;"))
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;"))
        db.execute(text("SET session_replication_role = DEFAULT;"))
        db.commit()
    except Exception as e:
        print(f"Warning: Could not clean database: {e}")
        db.rollback()
    finally:
        db.close()
    yield

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest_asyncio.fixture
async def auth_headers(async_client, db_session):
    """Create a test user and return authentication headers"""
    # Registrar usuario primero
    register_response = await async_client.post("/api/v1/auth/register", json={
        "email": "testuser@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "phone": "123456789"
    })
    
    # Verificar que el registro fue exitoso
    if register_response.status_code != 201:
        print(f"Warning: User registration failed with status {register_response.status_code}")
        print(f"Response: {register_response.text}")
    
    # Create basic role and assign it
    db = db_session
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole
    import json
    from datetime import datetime
    
    # Find the user
    db_user = db.query(User).filter_by(email="testuser@example.com").first()
    
    # Create basic role if it doesn't exist
    basic_role = db.query(Role).filter_by(name="basic").first()
    if not basic_role:
        basic_role = Role(
            name="basic",
            description="Basic user role",
            permissions=json.dumps({
                "users": {"read": True},
                "profile": {"read": True, "write": True},
                "devices": {"read": True},
                "alerts": {"read": True}
            }),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(basic_role)
        db.commit()
        db.refresh(basic_role)
    
    # Assign role to user
    user_role = UserRole(
        user_id=db_user.id,
        role_id=basic_role.id,
        created_at=datetime.now()
    )
    db.add(user_role)
    db.commit()
    
    # Login para obtener token
    login_response = await async_client.post("/api/v1/auth/login", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    
    # Verificar que el login fue exitoso
    if login_response.status_code != 200:
        print(f"Warning: User login failed with status {login_response.status_code}")
        print(f"Response: {login_response.text}")
        # Si falla, intentar con credenciales alternativas
        login_response = await async_client.post("/api/v1/auth/login", json={
            "email": "testuser@example.com",
            "password": "testpassword"
        })
    
    try:
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    except (KeyError, ValueError) as e:
        print(f"Error extracting token from response: {e}")
        print(f"Response status: {login_response.status_code}")
        print(f"Response body: {login_response.text}")
        # Retornar headers vacíos si falla
        return {"Authorization": "Bearer invalid_token"}

@pytest_asyncio.fixture
async def admin_auth(async_client, db_session):
    """Create an admin user and return authentication headers"""
    # Registrar usuario admin primero
    register_response = await async_client.post("/api/v1/auth/register", json={
        "email": "admin@example.com",
        "password": "adminpassword",
        "first_name": "Admin",
        "last_name": "User",
        "phone": "987654321",
        "username": "adminuser"
    })
    
    # Verificar que el registro fue exitoso
    if register_response.status_code != 201:
        print(f"Warning: Admin registration failed with status {register_response.status_code}")
        print(f"Response: {register_response.text}")
    
    # Create admin role and assign it
    db = db_session
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole
    import json
    from datetime import datetime
    
    # Find the admin user
    db_user = db.query(User).filter_by(email="admin@example.com").first()
    
    # Crear rol admin si no existe
    admin_role = db.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(
            name="admin",
            description="Administrator role",
            permissions=json.dumps({
                "users": {"read": True, "write": True, "delete": True},
                "profile": {"read": True, "write": True},
                "devices": {"read": True, "write": True, "delete": True},
                "alerts": {"read": True, "write": True},
                "packages": {"read": True, "write": True, "delete": True},
                "cared_persons": {"read": True, "write": True, "delete": True},
                "institutions": {"read": True, "write": True, "delete": True},
                "protocols": {"read": True, "write": True, "delete": True},
                "reports": {"read": True, "write": True},
                "system": {"read": True, "write": True, "delete": True}
            }),
            is_system=False,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)
    
    # Asignar rol admin al usuario
    user_role = UserRole(
        user_id=db_user.id,
        role_id=admin_role.id,
        is_active=True,
        created_at=datetime.now()
    )
    db.add(user_role)
    db.commit()
    
    # Login para obtener token
    login_response = await async_client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    
    # Verificar que el login fue exitoso
    if login_response.status_code != 200:
        print(f"Warning: Admin login failed with status {login_response.status_code}")
        print(f"Response: {login_response.text}")
    
    try:
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    except (KeyError, ValueError) as e:
        print(f"Error extracting admin token from response: {e}")
        print(f"Response status: {login_response.status_code}")
        print(f"Response body: {login_response.text}")
        # Retornar headers vacíos si falla
        return {"Authorization": "Bearer invalid_token"} 