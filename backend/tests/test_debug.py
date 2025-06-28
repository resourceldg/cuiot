import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Utilidad para obtener un usuario de prueba (o crear uno dummy)
def get_test_user_id():
    # En un entorno real, deberías consultar la base de datos o usar un fixture
    # Aquí simplemente generamos un UUID aleatorio para pruebas aisladas
    return str(uuid.uuid4())


def test_generate_and_cleanup_debug_data():
    user_id = get_test_user_id()

    # Generar datos de prueba
    response = client.post(f"/api/v1/debug/generate-test-data?user_id={user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "cared_person_id" in data
    cared_person_id = data["cared_person_id"]
    assert len(data["geofences"]) > 0
    assert len(data["events"]) > 0
    assert len(data["locations"]) > 0
    assert "protocol_id" in data

    # Listar eventos de debug
    response = client.get(f"/api/v1/debug/debug-events?cared_person_id={cared_person_id}")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    assert len(events) > 0
    assert "event_type" in events[0]

    # Listar ubicaciones de debug
    response = client.get(f"/api/v1/debug/locations?cared_person_id={cared_person_id}")
    assert response.status_code == 200
    locations = response.json()
    assert isinstance(locations, list)
    assert len(locations) > 0
    assert "latitude" in locations[0]

    # Listar geofences de debug
    response = client.get(f"/api/v1/debug/geofences?cared_person_id={cared_person_id}")
    assert response.status_code == 200
    geofences = response.json()
    assert isinstance(geofences, list)
    assert len(geofences) > 0
    assert "name" in geofences[0]

    # Obtener resumen de debug
    response = client.get(f"/api/v1/debug/summary?cared_person_id={cared_person_id}")
    assert response.status_code == 200
    summary = response.json()
    assert summary["cared_person_id"] == cared_person_id
    assert summary["location_count"] > 0
    assert summary["geofence_count"] > 0
    assert summary["event_count"] > 0

    # Limpiar datos de prueba
    response = client.post(f"/api/v1/debug/cleanup-test-data?cared_person_id={cared_person_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Datos de prueba eliminados" 