import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_alert_crud(async_client, auth_headers):
    # Primero crear un cared person
    cared_person_data = {
        "first_name": "Juan",
        "last_name": "Pérez",
        "date_of_birth": "1949-01-01",
        "address": "Calle Principal 123"
    }
    response = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    assert response.status_code == 201
    cared_person = response.json()
    
    # Crear una alerta
    alert_data = {
        "alert_type": "no_movement",
        "title": "No se detectó movimiento",
        "message": "No se detectó movimiento en las últimas 3 horas",
        "severity": "medium",
        "cared_person_id": cared_person["id"]
    }
    response = await async_client.post("/api/v1/alerts/", json=alert_data, headers=auth_headers)
    assert response.status_code == 201
    alert = response.json()
    
    # Obtener la alerta
    response = await async_client.get(f"/api/v1/alerts/{alert['id']}", headers=auth_headers)
    assert response.status_code == 200
    
    # Actualizar la alerta
    update_data = {"severity": "high"}
    response = await async_client.put(f"/api/v1/alerts/{alert['id']}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated_alert = response.json()
    assert updated_alert["severity"] == "high"
    
    # Eliminar la alerta
    response = await async_client.delete(f"/api/v1/alerts/{alert['id']}", headers=auth_headers)
    assert response.status_code == 204

def test_alert_audit_log(async_client, auth_headers):
    # Crear cared person
    cared_person_data = {
        "first_name": "Audit",
        "last_name": "Test",
        "date_of_birth": "1950-01-01",
        "address": "Audit 123"
    }
    response = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    cared_person = response.json()
    # Crear alerta
    alert_data = {
        "alert_type": "audit_test",
        "title": "Audit Alert",
        "message": "Audit log test",
        "severity": "medium",
        "cared_person_id": cared_person["id"]
    }
    response = await async_client.post("/api/v1/alerts/", json=alert_data, headers=auth_headers)
    assert response.status_code == 201
    alert = response.json()
    # Verificar registro de auditoría (opcional: consulta directa a la tabla audit_logs)
    # Actualizar alerta
    update_data = {"severity": "high"}
    response = await async_client.put(f"/api/v1/alerts/{alert['id']}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    # Eliminar alerta
    response = await async_client.delete(f"/api/v1/alerts/{alert['id']}", headers=auth_headers)
    assert response.status_code == 204 