import pytest
import pytest_asyncio

@pytest_asyncio.fixture
def user_data():
    return {
        "email": "minimal_test@example.com",
        "username": "minimal_test",
        "password": "testpass123",
        "first_name": "Minimal",
        "last_name": "User"
    }

@pytest.mark.asyncio
async def test_create_user_minimal(async_client, user_data):
    response = await async_client.post("/api/v1/users/", json=user_data)
    try:
        detail = response.json()
    except Exception:
        detail = response.text
    assert response.status_code == 201, f"Status: {response.status_code}, Body: {detail}, Payload: {user_data}" 