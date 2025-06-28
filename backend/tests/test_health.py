import pytest

@pytest.mark.asyncio
async def test_health_endpoints(async_client):
    for url in [
        "/api/v1/health/",
        "/api/v1/health/db",
        "/api/v1/health/system",
        "/api/v1/health/stats",
        "/api/v1/health/full",
        "/api/v1/health/ping"
    ]:
        response = await async_client.get(url)
        assert response.status_code == 200 or response.status_code == 201 