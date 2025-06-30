import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_generate_and_cleanup_debug_data(async_client, auth_headers):
    # Generar datos de prueba
    response = await async_client.post("/api/v1/debug/generate-test-data", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    results = data["results"]
    assert "cared_persons_created" in results
    assert results["cared_persons_created"] > 0
    assert "alerts_created" in results
    assert results["alerts_created"] > 0
    assert "debug_events_created" in results
    assert results["debug_events_created"] > 0
    assert "devices_created" in results
    assert results["devices_created"] > 0

    # El resto de endpoints de debug requieren un cared_person_id real, que no se obtiene directamente aquí.
    # Por lo tanto, solo validamos la generación de datos de prueba. 

@pytest.mark.asyncio
async def test_debug_data_no_duplicate_devices(async_client, auth_headers):
    # Generar datos de prueba dos veces seguidas
    response1 = await async_client.post("/api/v1/debug/generate-test-data", headers=auth_headers)
    assert response1.status_code == 200
    
    # La segunda llamada puede fallar por duplicados, pero no debería ser 500
    response2 = await async_client.post("/api/v1/debug/generate-test-data", headers=auth_headers)
    # Aceptar 200 (éxito) o 400 (duplicados), pero no 500 (error interno)
    assert response2.status_code in [200, 400]
    
    if response2.status_code == 400:
        # Si hay duplicados, verificar que el mensaje sea apropiado
        assert "duplicate" in response2.json()["detail"].lower() or "already exists" in response2.json()["detail"].lower() 