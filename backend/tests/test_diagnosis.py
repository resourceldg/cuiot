import pytest
import pytest_asyncio
from datetime import datetime
from io import BytesIO

@pytest.mark.asyncio
async def test_diagnosis_crud(async_client, auth_headers, normalized_catalogs):
    # Crear persona bajo cuidado
    cared_person_data = {
        "first_name": "Carlos",
        "last_name": "Ramírez",
        "date_of_birth": "1955-07-20",
        "care_type_id": normalized_catalogs["care_type_id"]
    }
    response = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    assert response.status_code == 201
    cared_person = response.json()
    cared_person_id = cared_person["id"]

    # Simular archivo adjunto
    file_content = b"PDF data or image data"
    files = [
        ("files", ("diagnosis_report.pdf", BytesIO(file_content), "application/pdf")),
    ]

    # Crear diagnóstico con adjunto
    data = {
        "diagnosis_name": "Diabetes tipo 2",
        "description": "Diabetes tipo 2. Hipertensión controlada.",
        "severity_level": "moderate",
        "doctor_name": "Dr. House",
        "cared_person_id": cared_person_id,
        "is_active": "true"
    }
    response = await async_client.post(
        "/api/v1/diagnoses/",
        data=data,
        files=files,
        headers=auth_headers
    )
    assert response.status_code in (200, 201)
    diagnosis = response.json()
    assert diagnosis["diagnosis_name"] == "Diabetes tipo 2"
    assert diagnosis["description"] == "Diabetes tipo 2. Hipertensión controlada."
    assert diagnosis["attachments"]
    assert diagnosis["attachments"][0]["filename"] == "diagnosis_report.pdf"
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
    assert diagnosis_fetched["diagnosis_name"] == "Diabetes tipo 2"
    assert diagnosis_fetched["description"] == "Diabetes tipo 2. Hipertensión controlada."

    # Actualizar diagnóstico (sin adjunto)
    update_data = {
        "diagnosis_name": "Diabetes tipo 2",
        "description": "Diabetes tipo 2. Hipertensión controlada. Mejoría reciente.",
        "severity_level": "moderate",
        "doctor_name": "Dr. House",
        "cared_person_id": cared_person_id,
        "is_active": "true"
    }
    response = await async_client.put(f"/api/v1/diagnoses/{diagnosis_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated = response.json()
    assert updated["description"] == "Diabetes tipo 2. Hipertensión controlada. Mejoría reciente."

    # Eliminar diagnóstico
    response = await async_client.delete(f"/api/v1/diagnoses/{diagnosis_id}", headers=auth_headers)
    assert response.status_code in (200, 204)
    # Verificar que ya no existe
    response = await async_client.get(f"/api/v1/diagnoses/{diagnosis_id}", headers=auth_headers)
    assert response.status_code == 404 