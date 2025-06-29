import pytest
import pytest_asyncio
from datetime import datetime

@pytest.mark.asyncio
async def test_event_crud(async_client, auth_headers):
    # Crear cared person primero
    cared_person_data = {
        "first_name": "Test",
        "last_name": "Event",
        "date_of_birth": "1952-01-01",
        "address": "Test 456"
    }
    resp = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    cared_person = resp.json()
    
    # Crear evento
    event_data = {
        "event_type": "movement",
        "event_time": datetime.now().isoformat(),
        "severity": "info",
        "message": "Test event description",
        "cared_person_id": cared_person["id"]
    }
    response = await async_client.post("/api/v1/events/", json=event_data, headers=auth_headers)
    assert response.status_code == 201
    event = response.json()
    
    # Obtener evento
    response = await async_client.get(f"/api/v1/events/{event['id']}", headers=auth_headers)
    assert response.status_code == 200
    
    # Actualizar evento
    update_data = {"message": "Updated Event"}
    response = await async_client.put(f"/api/v1/events/{event['id']}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated_event = response.json()
    assert updated_event["message"] == "Updated Event"
    
    # Eliminar evento
    response = await async_client.delete(f"/api/v1/events/{event['id']}", headers=auth_headers)
    assert response.status_code == 204 