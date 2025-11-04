import pytest

@pytest.mark.asyncio
async def test_create_task(client):
    member_name: str = "alice"
    alice_response = await client.post(
        "/auth/register",
        json={
            "username": member_name,
            "password": "secure123",
            "surename": "Алисова"
        }
    )
    
    assert alice_response.status_code == 201
    alice_token: str = alice_response.json()["token"]
    # ----

    owner = await client.post(url="/auth/register", json={
        "username": "owner",
        "password": "password123",
        "surename": "Овнер"
    })
    assert owner.status_code == 201
    owner_token = owner.json()["token"]

    # ---
    team_name: str = "DevOps"
    team_response = await client.post(
        url="/teams/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"name": team_name}
    )

    assert team_response.status_code == 201
    team_data = team_response.json()
    assert team_data["name"] == team_name

    # ---
    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"username": member_name}
    )

    assert invite.status_code == 201

    # ---
    board_name: str = "HDDDD"
    new_board = await client.post(
        url=f"/boards/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "name": board_name,
            "team_name": team_name,
        }
    )

    assert new_board.status_code == 201 

    task_tittle: str = "someOne"
    status: str = "ToDo"
    new_task = await client.post(
        url=f"/tasks/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "status": status,
            "team": team_name,
            "board": board_name,

            "tittle": task_tittle
        }
    )

    assert new_task.status_code == 201

    data = new_task.json()

    assert "task_status" in data
    assert data["task_status"] == status