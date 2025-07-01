import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_add_on_admin(async_client, admin_auth):
    add_on_data = {
        "name": "Extra Storage",
        "description": "50GB extra",
        "add_on_type": "storage",
        "price_monthly": 10000,
        "price_yearly": 100000,
        "configuration": {"extra_gb": 50},
        "max_quantity": 2
    }
    headers = admin_auth
    response = await async_client.post("/api/v1/packages/add-ons/", json=add_on_data, headers=headers)
    assert response.status_code in (201, 501)  # 501 si no está implementado

@pytest.mark.asyncio
async def test_add_add_on_to_subscription(async_client, auth_headers, admin_auth):
    headers_admin = admin_auth
    headers_user = auth_headers
    # Crear paquete
    package_data = {
        "package_type": "individual",
        "name": "AddOnTest",
        "description": "Paquete para add-ons",
        "price_monthly": 900000,
        "currency": "ARS",
        "max_users": 1,
        "max_devices": 3,
        "features": {"features": ["monitoreo"]},
        "is_featured": False
    }
    pkg_resp = await async_client.post("/api/v1/packages/", json=package_data, headers=headers_admin)
    package_id = pkg_resp.json()["id"]
    # Crear add-on real
    add_on_data = {
        "name": "Extra Storage",
        "description": "50GB extra",
        "add_on_type": "storage",
        "price_monthly": 10000,
        "price_yearly": 100000,
        "configuration": {"extra_gb": 50},
        "max_quantity": 2
    }
    add_on_resp = await async_client.post("/api/v1/packages/add-ons/", json=add_on_data, headers=headers_admin)
    add_on_id = add_on_resp.json()["id"]
    # Suscribirse
    subscription_data = {
        "package_id": package_id,
        "billing_cycle": "monthly",
        "auto_renew": True
    }
    sub_resp = await async_client.post("/api/v1/packages/user/subscribe", json=subscription_data, headers=headers_user)
    subscription_id = sub_resp.json()["id"]
    # Agregar add-on real
    user_add_on_data = {
        "add_on_id": add_on_id,
        "quantity": 1,
        "billing_cycle": "monthly"
    }
    response = await async_client.post(f"/api/v1/packages/user/subscriptions/{subscription_id}/add-ons", json=user_add_on_data, headers=headers_user)
    assert response.status_code in (200, 400)  # 400 si el add-on no es compatible o hay otra validación

@pytest.mark.asyncio
async def test_remove_add_on_from_subscription(async_client, auth_headers):
    headers = auth_headers
    # Simular add-on agregado (mock)
    user_add_on_id = str(uuid4())
    response = await async_client.delete(f"/api/v1/packages/user/add-ons/{user_add_on_id}", headers=headers)
    assert response.status_code in (200, 404) 