import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_device_crud(async_client, auth_headers):
    # Crear cared person primero
    cared_person_data = {
        "first_name": "Test",
        "last_name": "Device",
        "date_of_birth": "1954-01-01",
        "address": "Test 123"
    }
    resp = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    cared_person = resp.json()
    
    # Crear dispositivo
    device_data = {
        "device_id": "TEST_DEVICE_001",
        "name": "Test Device",
        "device_type": "sensor",
        "model": "Test Model",
        "manufacturer": "Test Manufacturer",
        "status": "active",
        "cared_person_id": cared_person["id"]
    }
    response = await async_client.post("/api/v1/devices/", json=device_data, headers=auth_headers)
    assert response.status_code == 201
    device = response.json()
    
    # Obtener dispositivo
    response = await async_client.get(f"/api/v1/devices/{device['id']}", headers=auth_headers)
    assert response.status_code == 200
    
    # Actualizar dispositivo
    update_data = {"model": "Updated Model"}
    response = await async_client.put(f"/api/v1/devices/{device['id']}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated_device = response.json()
    assert updated_device["model"] == "Updated Model"
    
    # Eliminar dispositivo
    response = await async_client.delete(f"/api/v1/devices/{device['id']}", headers=auth_headers)
    assert response.status_code == 204 