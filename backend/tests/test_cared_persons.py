import pytest
import pytest_asyncio
from datetime import datetime

@pytest.mark.asyncio
async def test_cared_person_crud(async_client, auth_headers):
    """Test CRUD operations for cared persons"""
    # Create cared person
    cared_person_data = {
        "first_name": "María",
        "last_name": "González",
        "date_of_birth": "1945-03-15",
        "address": "Av. Corrientes 1234, CABA",
        "phone": "+54 11 1234-5678",
        "care_type": "delegated",
        "care_level": "medium",
        "mobility_level": "assisted"
    }
    
    response = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    assert response.status_code == 201
    cared_person = response.json()
    
    # Get cared person
    response = await async_client.get(f"/api/v1/cared-persons/{cared_person['id']}", headers=auth_headers)
    assert response.status_code == 200
    retrieved_person = response.json()
    assert retrieved_person["first_name"] == "María"
    assert retrieved_person["last_name"] == "González"
    
    # Update cared person
    update_data = {"care_level": "high", "mobility_level": "wheelchair"}
    response = await async_client.put(f"/api/v1/cared-persons/{cared_person['id']}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated_person = response.json()
    assert updated_person["care_level"] == "high"
    assert updated_person["mobility_level"] == "wheelchair"
    
    # Delete cared person
    response = await async_client.delete(f"/api/v1/cared-persons/{cared_person['id']}", headers=auth_headers)
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_cared_person_list(async_client, auth_headers):
    """Test listing cared persons"""
    # Create multiple cared persons
    cared_persons_data = [
        {
            "first_name": "Juan",
            "last_name": "Pérez",
            "date_of_birth": "1940-01-01",
            "address": "Calle 1, 123",
            "care_type": "delegated",
            "care_level": "low"
        },
        {
            "first_name": "Ana",
            "last_name": "López",
            "date_of_birth": "1950-05-10",
            "address": "Calle 2, 456",
            "care_type": "delegated",
            "care_level": "high"
        }
    ]
    
    for data in cared_persons_data:
        response = await async_client.post("/api/v1/cared-persons/", json=data, headers=auth_headers)
        assert response.status_code == 201
    
    # List cared persons
    response = await async_client.get("/api/v1/cared-persons/", headers=auth_headers)
    assert response.status_code == 200
    cared_persons = response.json()
    assert len(cared_persons) >= 2

@pytest.mark.asyncio
async def test_cared_person_validation(async_client, auth_headers):
    """Test validation for cared person data"""
    # Test missing required fields
    invalid_data = {
        "first_name": "Test",
        # Missing last_name
    }
    
    response = await async_client.post("/api/v1/cared-persons/", json=invalid_data, headers=auth_headers)
    assert response.status_code == 422
    
    # Test invalid care_type (should still work as it has default value)
    valid_data = {
        "first_name": "Test",
        "last_name": "User",
        "care_type": "delegated"  # Valid value
    }
    
    response = await async_client.post("/api/v1/cared-persons/", json=valid_data, headers=auth_headers)
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_cared_person_not_found(async_client, auth_headers):
    """Test handling of non-existent cared person"""
    import uuid
    fake_id = str(uuid.uuid4())
    
    response = await async_client.get(f"/api/v1/cared-persons/{fake_id}", headers=auth_headers)
    assert response.status_code == 404
    
    response = await async_client.put(f"/api/v1/cared-persons/{fake_id}", json={"first_name": "Test"}, headers=auth_headers)
    assert response.status_code == 404
    
    response = await async_client.delete(f"/api/v1/cared-persons/{fake_id}", headers=auth_headers)
    assert response.status_code == 404 