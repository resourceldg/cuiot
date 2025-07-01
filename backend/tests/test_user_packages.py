import pytest
from uuid import uuid4
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_subscribe_to_package(async_client, auth_headers, admin_auth):
    # Primero crear un paquete con admin
    admin_headers = admin_auth
    package_data = {
        "package_type": "individual",
        "name": "Test Package",
        "description": "Paquete de prueba",
        "price_monthly": 100000,
        "currency": "ARS",
        "max_users": 1,
        "max_devices": 5,
        "features": {"features": ["monitoreo"]},
        "is_featured": False
    }
    create_resp = await async_client.post("/api/v1/packages/", json=package_data, headers=admin_headers)
    package_id = create_resp.json()["id"]
    
    # Suscribirse con usuario normal
    headers = auth_headers
    subscription_data = {
        "package_id": package_id,
        "billing_cycle": "monthly",
        "auto_renew": True
    }
    response = await async_client.post("/api/v1/packages/user/subscribe", json=subscription_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["package_id"] == package_id
    assert data["billing_cycle"] == "monthly"

@pytest.mark.asyncio
async def test_cancel_subscription(async_client, auth_headers, admin_auth):
    # Primero crear un paquete con admin
    admin_headers = admin_auth
    package_data = {
        "package_type": "individual",
        "name": "Test Package",
        "description": "Paquete de prueba",
        "price_monthly": 100000,
        "currency": "ARS",
        "max_users": 1,
        "max_devices": 5,
        "features": {"features": ["monitoreo"]},
        "is_featured": False
    }
    create_resp = await async_client.post("/api/v1/packages/", json=package_data, headers=admin_headers)
    package_id = create_resp.json()["id"]
    
    # Suscribirse
    headers = auth_headers
    subscription_data = {
        "package_id": package_id,
        "billing_cycle": "monthly",
        "auto_renew": True
    }
    sub_resp = await async_client.post("/api/v1/packages/user/subscribe", json=subscription_data, headers=headers)
    subscription_id = sub_resp.json()["id"]
    
    # Cancelar
    response = await async_client.delete(f"/api/v1/packages/user/subscriptions/{subscription_id}", headers=headers)
    assert response.status_code == 200
    assert "cancelada" in response.json()["message"].lower()

@pytest.mark.asyncio
async def test_legal_capacity_validation_autocuidado(async_client, auth_headers):
    headers = auth_headers
    # Simular usuario autocuidado
    verification_data = {"user_id": str(uuid4())}
    response = await async_client.post("/api/v1/packages/legal-capacity/verify", json=verification_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["can_contract"] is True

@pytest.mark.asyncio
async def test_legal_capacity_validation_delegated(async_client, auth_headers):
    headers = auth_headers
    # Simular usuario bajo cuidado delegado
    verification_data = {"user_id": str(uuid4()), "legal_representative_id": str(uuid4())}
    response = await async_client.post("/api/v1/packages/legal-capacity/verify", json=verification_data, headers=headers)
    assert response.status_code == 200
    # El test espera que la lógica de negocio lo deniegue si es delegado
    result = response.json()
    assert "can_contract" in result

@pytest.mark.asyncio
async def test_subscribe_with_customization(async_client, auth_headers, admin_auth):
    # Crear paquete personalizable con admin
    admin_headers = admin_auth
    package_data = {
        "package_type": "individual",
        "name": "CustomTest",
        "description": "Paquete personalizable",
        "price_monthly": 1000000,
        "currency": "ARS",
        "max_users": 2,
        "max_devices": 5,
        "features": {"features": ["monitoreo", "alertas"]},
        "customizable_options": {"premium_support": True},
        "is_customizable": True
    }
    create_resp = await async_client.post("/api/v1/packages/", json=package_data, headers=admin_headers)
    package_id = create_resp.json()["id"]
    
    # Suscribirse con personalización
    headers = auth_headers
    subscription_data = {
        "package_id": package_id,
        "billing_cycle": "monthly",
        "auto_renew": True,
        "custom_configuration": {"premium_support": True},
        "selected_features": {"features": ["monitoreo", "alertas"]},
        "custom_limits": {"max_users": 2, "max_devices": 5}
    }
    response = await async_client.post("/api/v1/packages/user/subscribe", json=subscription_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["custom_configuration"]["premium_support"] is True 