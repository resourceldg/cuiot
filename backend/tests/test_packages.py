import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_package_admin(async_client, admin_auth):
    headers = admin_auth
    package_data = {
        "package_type": "individual",
        "name": "Básico",
        "description": "Paquete básico para individuos",
        "price_monthly": 50000,
        "currency": "ARS",
        "max_users": 1,
        "max_devices": 5,
        "features": {"features": ["monitoreo"]},
        "is_featured": False
    }
    response = await async_client.post("/api/v1/packages/", json=package_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Básico"
    assert data["package_type"] == "individual"

@pytest.mark.asyncio
async def test_list_packages(async_client, auth_headers):
    headers = auth_headers
    response = await async_client.get("/api/v1/packages/", headers=headers)
    assert response.status_code == 200
    packages = response.json()
    assert isinstance(packages, list)

@pytest.mark.asyncio
async def test_get_package_detail(async_client, admin_auth):
    headers = admin_auth
    # Crear paquete primero
    package_data = {
        "package_type": "individual",
        "name": "Premium",
        "description": "Paquete premium",
        "price_monthly": 120000,
        "currency": "ARS",
        "max_users": 1,
        "max_devices": 15,
        "features": {"features": ["agenda"]},
        "is_featured": False
    }
    create_resp = await async_client.post("/api/v1/packages/", json=package_data, headers=headers)
    package_id = create_resp.json()["id"]
    
    # Obtener detalles
    response = await async_client.get(f"/api/v1/packages/{package_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Premium"

@pytest.mark.asyncio
async def test_update_package_admin(async_client, admin_auth):
    headers = admin_auth
    # Crear paquete primero
    package_data = {
        "package_type": "individual",
        "name": "Pro",
        "description": "Paquete profesional",
        "price_monthly": 1200000,
        "currency": "ARS",
        "max_users": 1,
        "max_devices": 15,
        "features": {"features": ["agenda"]},
        "is_featured": False
    }
    create_resp = await async_client.post("/api/v1/packages/", json=package_data, headers=headers)
    package_id = create_resp.json()["id"]
    
    # Actualizar
    update_data = {"name": "Pro Plus", "is_featured": True}
    response = await async_client.put(f"/api/v1/packages/{package_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Pro Plus"
    assert response.json()["is_featured"] is True

@pytest.mark.asyncio
async def test_delete_package_admin(async_client, admin_auth):
    headers = admin_auth
    # Crear paquete
    package_data = {
        "package_type": "institutional",
        "name": "Institucional",
        "description": "Paquete institucional",
        "price_monthly": 5000000,
        "currency": "ARS",
        "max_users": 100,
        "max_devices": 300,
        "features": {"features": ["api", "integración"]},
        "is_featured": False
    }
    create_resp = await async_client.post("/api/v1/packages/", json=package_data, headers=headers)
    package_id = create_resp.json()["id"]
    
    # Eliminar
    response = await async_client.delete(f"/api/v1/packages/{package_id}", headers=headers)
    assert response.status_code == 200
    assert "eliminado" in response.json()["message"].lower()

@pytest.mark.asyncio
async def test_filter_packages_by_type(async_client, auth_headers, admin_auth):
    # Crear un paquete de tipo individual
    headers_admin = admin_auth
    package_data = {
        "package_type": "individual",
        "name": "FiltroTest",
        "description": "Paquete para filtro",
        "price_monthly": 100000,
        "currency": "ARS",
        "max_users": 1,
        "max_devices": 1,
        "features": {"features": ["monitoreo"]},
        "is_featured": False
    }
    await async_client.post("/api/v1/packages/", json=package_data, headers=headers_admin)
    headers = auth_headers
    response = await async_client.get("/api/v1/packages/?package_type=individual", headers=headers)
    assert response.status_code == 200
    for pkg in response.json():
        assert pkg["package_type"] == "individual"

@pytest.mark.asyncio
async def test_filter_packages_by_featured(async_client, auth_headers):
    headers = auth_headers
    response = await async_client.get("/api/v1/packages/?is_featured=true", headers=headers)
    assert response.status_code == 200
    for pkg in response.json():
        assert pkg["is_featured"] is True 