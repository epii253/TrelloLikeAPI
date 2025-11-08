import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name",
    ["alice", "bob"]
)    
async def test_register_user(client, name):
    response = await client.post(
        "/auth/register",
        json={
            "username": name,
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

    response = await client.post("/auth/register", json={"username": "bob", "password": "passMCBOB"})
    assert response.status_code == 409

    response = await client.post("/auth/register", json={"username": "alice", "password": "passMCBOB"})
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_register_login(client):
    response = await client.post("/auth/register", json={"username": "bob", "password": "passMCBOB"})
    assert response.status_code == 201

    response = await client.post("/auth/login", json={"username": "bob", "password": "passMCBOB"})
    assert response.status_code == 200

    data = response.json()
    assert "token" in data
    assert data["token"].startswith("ey")