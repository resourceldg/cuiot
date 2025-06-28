import pytest
import uuid

@pytest.mark.asyncio
async def test_alert_crud(async_client, auth_headers):
    # Primero crear un elderly person
    elderly_person_data = {
        "first_name": "Juan",
        "last_name": "Pérez",
        "age": 75,
        "address": "Calle Principal 123"
    }
    response = await async_client.post("/api/v1/elderly-persons/", json=elderly_person_data, headers=auth_headers)
    assert response.status_code == 201
    elderly_person = response.json()
    elderly_person_id = elderly_person["id"]
    
    # Crear alerta
    payload = {
        "elderly_person_id": elderly_person_id,
        "alert_type": "sos",
        "message": "Test alerta",
        "severity": "high"
    }
    response = await async_client.post("/api/v1/alerts/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    alert = response.json()
    alert_id = alert["id"]
    
    # Obtener alerta
    response = await async_client.get(f"/api/v1/alerts/{alert_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Listar alertas
    response = await async_client.get("/api/v1/alerts/", headers=auth_headers)
    assert response.status_code == 200

    # Actualizar alerta
    response = await async_client.put(f"/api/v1/alerts/{alert_id}", json={"message": "Actualizado"}, headers=auth_headers)
    assert response.status_code == 200

    # Marcar como resuelta
    response = await async_client.patch(f"/api/v1/alerts/{alert_id}/resolve", headers=auth_headers)
    assert response.status_code == 200

    # Eliminar alerta
    response = await async_client.delete(f"/api/v1/alerts/{alert_id}", headers=auth_headers)
    assert response.status_code == 204 