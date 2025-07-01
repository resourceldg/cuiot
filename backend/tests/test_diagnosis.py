import pytest
import pytest_asyncio
from datetime import datetime

@pytest.mark.asyncio
async def test_diagnosis_crud(async_client, auth_headers):
    # Crear persona bajo cuidado
    cared_person_data = {
        "first_name": "Carlos",
        "last_name": "Ramírez",
        "date_of_birth": "1955-07-20",
        "care_type": "delegated"
    }
    response = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    assert response.status_code == 201
    cared_person = response.json()
    cared_person_id = cared_person["id"]

    # Crear diagnóstico
    diagnosis_data = {
        "diagnosis_text": "Diabetes tipo 2. Hipertensión controlada.",
        "diagnosis_type": "inicial",
        "cared_person_id": cared_person_id,
        "attachments": [],
        "is_active": "active"
    }
    response = await async_client.post("/api/v1/diagnoses/", data=diagnosis_data, headers=auth_headers)
    assert response.status_code == 200 or response.status_code == 201
    diagnosis = response.json()
    assert diagnosis["diagnosis_text"] == "Diabetes tipo 2. Hipertensión controlada."
    diagnosis_id = diagnosis["id"]

    # Listar diagnósticos
    response = await async_client.get(f"/api/v1/diagnoses/?cared_person_id={cared_person_id}", headers=auth_headers)
    assert response.status_code == 200
    diagnoses = response.json()
    assert any(d["id"] == diagnosis_id for d in diagnoses)

    # Obtener diagnóstico
    response = await async_client.get(f"/api/v1/diagnoses/{diagnosis_id}", headers=auth_headers)
    assert response.status_code == 200
    diagnosis_fetched = response.json()
    assert diagnosis_fetched["diagnosis_text"] == "Diabetes tipo 2. Hipertensión controlada."

    # Actualizar diagnóstico
    update_data = {
        "diagnosis_text": "Diabetes tipo 2. Hipertensión controlada. Mejoría reciente.",
        "diagnosis_type": "actualización",
        "cared_person_id": cared_person_id,
        "attachments": [],
        "is_active": "active"
    }
    response = await async_client.put(f"/api/v1/diagnoses/{diagnosis_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated = response.json()
    assert updated["diagnosis_text"] == "Diabetes tipo 2. Hipertensión controlada. Mejoría reciente."

    # Eliminar diagnóstico
    response = await async_client.delete(f"/api/v1/diagnoses/{diagnosis_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["ok"] is True

    # Verificar que ya no existe
    response = await async_client.get(f"/api/v1/diagnoses/{diagnosis_id}", headers=auth_headers)
    assert response.status_code == 404 