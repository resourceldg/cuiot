import pytest
import pytest_asyncio
from httpx import AsyncClient
from main import app
from app.core.database import get_db
from sqlalchemy import text

@pytest.fixture(autouse=True)
def clean_db():
    # Limpia todas las tablas principales antes de cada test
    db = next(get_db())
    # Desactiva restricciones de clave foránea temporalmente
    db.execute(text('''
        DO $$ DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
            END LOOP;
        END $$;
    '''))
    db.commit()
    yield

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest_asyncio.fixture
async def auth_headers(async_client):
    # Registrar usuario primero
    response = await async_client.post("/api/v1/auth/register", json={
        "email": "testuser@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "phone": "123456789"
    })
    
    # Login para obtener token
    response = await async_client.post("/api/v1/auth/login", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"} 