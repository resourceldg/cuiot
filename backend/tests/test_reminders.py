import pytest
import uuid

@pytest.mark.asyncio
async def test_reminder_crud(async_client, auth_headers):
    # Primero crear un elderly person
    elderly_person_data = {
        "first_name": "María",
        "last_name": "García",
        "age": 80,
        "address": "Avenida Central 456"
    }
    response = await async_client.post("/api/v1/elderly-persons/", json=elderly_person_data, headers=auth_headers)
    assert response.status_code == 201
    elderly_person = response.json()
    elderly_person_id = elderly_person["id"]
    
    # Crear recordatorio
    payload = {
        "elderly_person_id": elderly_person_id,
        "title": "Tomar medicación",
        "description": "Pastilla azul",
        "reminder_type": "medication",
        "scheduled_time": "08:00:00",
        "days_of_week": [1,2,3,4,5]
    }
    response = await async_client.post("/api/v1/reminders/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    reminder = response.json()
    reminder_id = reminder["id"]
    
    # Obtener recordatorio
    response = await async_client.get(f"/api/v1/reminders/{reminder_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Listar recordatorios
    response = await async_client.get("/api/v1/reminders/", headers=auth_headers)
    assert response.status_code == 200
    
    # Actualizar recordatorio
    response = await async_client.put(f"/api/v1/reminders/{reminder_id}", json={"title": "Nuevo título"}, headers=auth_headers)
    assert response.status_code == 200
    
    # Activar recordatorio
    response = await async_client.patch(f"/api/v1/reminders/{reminder_id}/activate", headers=auth_headers)
    assert response.status_code == 200
    
    # Desactivar recordatorio
    response = await async_client.patch(f"/api/v1/reminders/{reminder_id}/deactivate", headers=auth_headers)
    assert response.status_code == 200
    
    # Eliminar recordatorio
    response = await async_client.delete(f"/api/v1/reminders/{reminder_id}", headers=auth_headers)
    assert response.status_code == 204 