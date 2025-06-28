import pytest

@pytest.mark.asyncio
async def test_event_crud(async_client, auth_headers):
    # Crear adulto mayor primero
    elderly_person_data = {
        "first_name": "Test",
        "last_name": "Event",
        "age": 72,
        "address": "Test 456"
    }
    resp = await async_client.post("/api/v1/elderly-persons/", json=elderly_person_data, headers=auth_headers)
    elderly_id = resp.json()["id"]

    # Obtener el ID del usuario actual (del token)
    resp = await async_client.get("/api/v1/users/me", headers=auth_headers)
    user_id = resp.json()["id"]

    # Crear evento
    payload = {
        "elderly_person_id": elderly_id,
        "event_type": "medical",
        "title": "Turno médico",
        "description": "Chequeo general",
        "start_datetime": "2024-07-01T10:00:00",
        "end_datetime": "2024-07-01T11:00:00",
        "location": "Hospital Central",
        "created_by_id": user_id
    }
    resp = await async_client.post("/api/v1/events/", json=payload, headers=auth_headers)
    assert resp.status_code == 201
    event_id = resp.json()["id"]

    # Editar evento
    resp = await async_client.put(f"/api/v1/events/{event_id}", json={"title": "Turno actualizado"}, headers=auth_headers)
    assert resp.status_code == 200

    # Listar eventos
    resp = await async_client.get("/api/v1/events/", headers=auth_headers)
    assert resp.status_code == 200
    assert any(e["id"] == event_id for e in resp.json())

    # Eliminar evento
    resp = await async_client.delete(f"/api/v1/events/{event_id}", headers=auth_headers)
    assert resp.status_code == 204 