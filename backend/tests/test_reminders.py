import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_reminder_crud(async_client, auth_headers):
    # Primero crear un cared person
    cared_person_data = {
        "first_name": "María",
        "last_name": "García",
        "date_of_birth": "1944-01-01",
        "address": "Avenida Central 456"
    }
    response = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    assert response.status_code == 201
    cared_person = response.json()
    
    # Crear recordatorio
    reminder_data = {
        "reminder_type": "medication",
        "title": "Tomar medicamento",
        "description": "Tomar pastilla para la presión",
        "scheduled_time": "2024-07-01T08:00:00",
        "cared_person_id": cared_person["id"]
    }
    response = await async_client.post("/api/v1/reminders/", json=reminder_data, headers=auth_headers)
    assert response.status_code == 201
    reminder = response.json()
    
    # Obtener recordatorio
    response = await async_client.get(f"/api/v1/reminders/{reminder['id']}", headers=auth_headers)
    assert response.status_code == 200
    
    # Actualizar recordatorio
    update_data = {"title": "Medicamento actualizado"}
    response = await async_client.put(f"/api/v1/reminders/{reminder['id']}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated_reminder = response.json()
    assert updated_reminder["title"] == "Medicamento actualizado"
    
    # Eliminar recordatorio
    response = await async_client.delete(f"/api/v1/reminders/{reminder['id']}", headers=auth_headers)
    assert response.status_code == 204 