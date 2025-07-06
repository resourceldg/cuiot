import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_reminder_crud(async_client, auth_headers, normalized_catalogs):
    """Test CRUD operations for reminders"""
    
    # Create a cared person first
    cared_person_data = {
        "first_name": "María",
        "last_name": "García",
        "date_of_birth": "1944-01-01",
        "address": "Avenida Central 456"
    }
    response = await async_client.post("/api/v1/cared-persons/", json=cared_person_data, headers=auth_headers)
    assert response.status_code == 201
    cared_person = response.json()
    
    # Get reminder_type_id from normalized catalogs
    reminder_type_id = normalized_catalogs["reminder_type_id"]
    
    # Create reminder
    reminder_data = {
        "reminder_type_id": reminder_type_id,
        "cared_person_id": cared_person["id"],
        "title": "Test Reminder",
        "description": "Test reminder for unit testing",
        "scheduled_time": "2024-12-25T10:00:00Z",
        "is_active": True
    }
    
    response = await async_client.post("/api/v1/reminders/", json=reminder_data, headers=auth_headers)
    assert response.status_code == 201
    reminder = response.json()
    
    assert reminder["title"] == "Test Reminder"
    assert reminder["is_active"] == True
    
    # Get reminder
    response = await async_client.get(f"/api/v1/reminders/{reminder['id']}", headers=auth_headers)
    assert response.status_code == 200
    retrieved_reminder = response.json()
    assert retrieved_reminder["id"] == reminder["id"]
    
    # Update reminder
    update_data = {"title": "Updated Reminder", "is_active": False}
    response = await async_client.put(f"/api/v1/reminders/{reminder['id']}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated_reminder = response.json()
    assert updated_reminder["title"] == "Updated Reminder"
    assert updated_reminder["is_active"] == False
    
    # Delete reminder
    response = await async_client.delete(f"/api/v1/reminders/{reminder['id']}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify deletion
    response = await async_client.get(f"/api/v1/reminders/{reminder['id']}", headers=auth_headers)
    assert response.status_code == 404 