import pytest

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/auth/register",
        json={
            "username": "alice",
            "password": "secure123",
            "surename": "Алисова"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert data["token"].startswith("ey")

@pytest.mark.asyncio
async def test_register_duplicate(client):
    response = await client.post("/auth/register", json={"username": "bob", "password": "passMCBOB"})
    assert response.status_code == 201

    response = await client.post("/auth/register", json={"username": "bob", "password": "passMCBOB"})
    assert response.status_code == 409