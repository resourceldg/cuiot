import pytest
import pytest_asyncio
from datetime import datetime

@pytest.mark.asyncio
async def test_event_crud(async_client, auth_headers, normalized_catalogs):
    # Crear cared person primero
    cared_person_data = {
        "first_name": "Test",
        "last_name": "Event",
        "date_of_birth": "1952-01-01",
        "care_type_id": normalized_catalogs["care_type_id"]
    }
    resp = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    cared_person = resp.json()
    
    # Inicializar event types por defecto
    await async_client.post("/api/v1/event-types/initialize-defaults", headers=auth_headers)
    
    # Obtener event_type_id para "sensor_event"
    response = await async_client.get("/api/v1/event-types/", headers=auth_headers)
    assert response.status_code == 200
    event_types = response.json()
    sensor_type = next((et for et in event_types if et["name"] == "sensor_event"), None)
    assert sensor_type is not None, "Event type 'sensor_event' not found"
    
    # Crear evento con event_type_id normalizado
    event_data = {
        "event_type_id": sensor_type["id"],
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