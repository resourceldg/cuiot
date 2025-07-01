import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_package_statistics_admin(async_client, admin_auth):
    # Crear un paquete si no existe
    package_data = {
        "package_type": "individual",
        "name": "EstadísticaTest",
        "description": "Paquete para estadísticas",
        "price_monthly": 100000,
        "currency": "ARS",
        "max_users": 1,
        "max_devices": 1,
        "features": {"features": ["monitoreo"]},
        "is_featured": False
    }
    create_resp = await async_client.post("/api/v1/packages/", json=package_data, headers=admin_auth)
    # 201 creado, 409 si ya existe
    assert create_resp.status_code in (201, 409, 422)

    # Suscribir al admin al paquete para asegurar una suscripción activa
    package_id = create_resp.json().get("id") if create_resp.status_code == 201 else None
    if not package_id:
        # Obtener el id del paquete existente
        list_resp = await async_client.get("/api/v1/packages/", headers=admin_auth)
        assert list_resp.status_code == 200
        for pkg in list_resp.json():
            if pkg["name"] == "EstadísticaTest":
                package_id = pkg["id"]
                break
    assert package_id is not None

    subscription_data = {
        "package_id": package_id,
        "billing_cycle": "monthly"
    }
    sub_resp = await async_client.post("/api/v1/packages/user/subscribe", json=subscription_data, headers=admin_auth)
    assert sub_resp.status_code in (201, 409, 400)

    # Ahora sí, pedir estadísticas
    response = await async_client.get("/api/v1/packages/statistics", headers=admin_auth)
    if response.status_code != 200:
        raise Exception(f"Status: {response.status_code}, Body: {response.text}")
    data = response.json()
    assert "total_packages" in data
    assert "total_subscriptions" in data
    assert "total_revenue_ars" in data 