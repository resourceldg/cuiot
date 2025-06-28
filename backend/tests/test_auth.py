import pytest
import uuid

@pytest.mark.asyncio
async def test_register_and_login(async_client):
    # Usar email único para evitar conflictos
    unique_email = f"test_{uuid.uuid4().hex[:8]}@ejemplo.com"
    
    # Registro
    response = await async_client.post("/api/v1/auth/register", json={
        "email": unique_email,
        "password": "testpassword",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "phone": "123456789"
    })
    assert response.status_code in (200, 201)
    
    # Login
    response = await async_client.post("/api/v1/auth/login", json={
        "email": unique_email,
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer" 