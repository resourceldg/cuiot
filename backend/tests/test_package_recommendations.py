import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_package_recommendation_individual(async_client, auth_headers):
    headers = auth_headers
    request = {
        "user_type": "individual",
        "needs": ["monitoreo"],
        "budget_monthly": 1000000
    }
    response = await async_client.post("/api/v1/packages/recommendations", json=request, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "recommended_package" in data

@pytest.mark.asyncio
async def test_package_recommendation_professional(async_client, auth_headers):
    headers = auth_headers
    request = {
        "user_type": "professional",
        "needs": ["agenda"],
        "budget_monthly": 2000000
    }
    response = await async_client.post("/api/v1/packages/recommendations", json=request, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "recommended_package" in data 