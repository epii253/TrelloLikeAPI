import pytest

@pytest.mark.asyncio
async def test_create_team(client):
    reg = await client.post("/auth/register", json={
        "username": "owner",
        "password": "pass",
        "surename": "Овнер"
    })
    token = reg.json()["token"]
    response = await client.post(
        "/teams/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "DevOps"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "DevOps"
    assert data["owner_id"] > 0