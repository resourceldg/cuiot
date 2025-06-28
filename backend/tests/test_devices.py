import pytest

@pytest.mark.asyncio
async def test_device_crud(async_client, auth_headers):
    # Crear adulto mayor primero
    elderly_person_data = {
        "first_name": "Test",
        "last_name": "Device",
        "age": 70,
        "address": "Test 123"
    }
    resp = await async_client.post("/api/v1/elderly-persons/", json=elderly_person_data, headers=auth_headers)
    elderly_id = resp.json()["id"]

    # Crear dispositivo
    payload = {
        "elderly_person_id": elderly_id,
        "device_id": "esp32-001",
        "name": "Pulsera",
        "location": "Dormitorio"
    }
    resp = await async_client.post("/api/v1/devices/", json=payload, headers=auth_headers)
    assert resp.status_code == 201
    device_id = resp.json()["id"]

    # Editar dispositivo
    resp = await async_client.put(f"/api/v1/devices/{device_id}", json={"name": "Pulsera Editada"}, headers=auth_headers)
    assert resp.status_code == 200

    # Desactivar dispositivo
    resp = await async_client.patch(f"/api/v1/devices/{device_id}/deactivate", headers=auth_headers)
    assert resp.status_code == 200

    # Eliminar dispositivo
    resp = await async_client.delete(f"/api/v1/devices/{device_id}", headers=auth_headers)
    assert resp.status_code == 204 