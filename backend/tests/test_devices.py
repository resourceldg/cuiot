import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_device_crud(async_client, auth_headers, normalized_catalogs):
    """Test CRUD operations for devices"""
    
    # Get device_type_id from normalized catalogs
    device_type_id = normalized_catalogs["device_type_id"]
    
    # Create device
    device_data = {
        "device_id": "TEST_DEVICE_001",
        "device_type_id": device_type_id,
        "name": "Test Sensor",
        "description": "Test device for unit testing",
        "location": "Room 101",
        "status": "active"
    }
    
    response = await async_client.post("/api/v1/devices/", json=device_data, headers=auth_headers)
    assert response.status_code == 201
    device = response.json()
    
    assert device["name"] == "Test Sensor"
    assert device["device_type_id"] == device_type_id
    assert device["device_id"] == "TEST_DEVICE_001"
    
    # Get device
    response = await async_client.get(f"/api/v1/devices/{device['id']}", headers=auth_headers)
    assert response.status_code == 200
    retrieved_device = response.json()
    assert retrieved_device["id"] == device["id"]
    
    # Update device
    update_data = {"name": "Updated Sensor", "model": "Updated Model"}
    response = await async_client.put(f"/api/v1/devices/{device['id']}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated_device = response.json()
    assert updated_device["name"] == "Updated Sensor"
    assert updated_device["model"] == "Updated Model"
    
    # Delete device
    response = await async_client.delete(f"/api/v1/devices/{device['id']}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify deletion
    response = await async_client.get(f"/api/v1/devices/{device['id']}", headers=auth_headers)
    assert response.status_code == 404 