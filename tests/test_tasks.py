from uuid import UUID

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_tittle, status",
    [
        ("PASS_ППА2", "ToDo"), 
        ("PASS_ППА", "Done"), 
        ("Lab3_charrp", "InProcess")
    ]
)
async def test_create_task(client, task_tittle, status):
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
    alice_response = alice_response.json()
    assert "id" in alice_response
    alice_id: UUID = alice_response["id"]
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
    assert "team_id" in team_data
    team_id: UUID = team_data["team_id"]

    # ---
    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"user_id": alice_id}
    )

    assert invite.status_code == 201

    # ---
    board_name: str = "HDDDD"
    new_board = await client.post(
        url="/boards/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "name": board_name,
            "team_id": team_id,
        }
    )

    assert new_board.status_code == 201
    new_board = new_board.json() 
    assert "board_id" in new_board
    board_id: UUID = new_board["board_id"]

    new_task = await client.post(
        url="/tasks/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "status": status,
            "team_id": team_id,
            "board_id": board_id,

            "tittle": task_tittle
        }
    )

    assert new_task.status_code == 201

    data = new_task.json()

    assert "task_status" in data
    assert data["task_status"] == status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_tittle, status, task_tittle2, status2, description2",
    [
        ("someOne", "ToDo", "SomeTwo", "Done", "bombom"),
        ("First", "InProcess", "Second", "ToDo", "bimbam"),
        ("heGonna", "ToDo", "findYou", "InProcess", ""),
        ("youGonna", "ToDo", "devovuryourslef", "Done", "..")
    ]
)
async def test_get_task(client, task_tittle: str, status: str, task_tittle2: str, status2: str, description2: str):
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
    alice_id: UUID = alice_response.json()["id"]
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
    assert "team_id" in team_data
    team_id: UUID = team_data["team_id"]

    # ---
    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"user_id": alice_id}
    )

    assert invite.status_code == 201

    # ---
    board_name: str = "HDDDD"
    new_board = await client.post(
        url="/boards/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "name": board_name,
            "team_id": team_id,
        }
    )
    assert new_board.status_code == 201
    board_data: dict = new_board.json()
    assert "board_id" in board_data
    board_id: UUID = board_data["board_id"]


    # ---
    new_task = await client.post(
        url="/tasks/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "status": status,
            "team_id": team_id,
            "board_id": board_id,

            "tittle": task_tittle
        }
    )

    assert new_task.status_code == 201

    data = new_task.json()

    assert "task_status" in data
    assert data["task_status"] == status

    # --- 
    new_task2 = await client.post(
        url="/tasks/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "status": status2,
            "team_id": team_id,
            "board_id": board_id,

            "tittle": task_tittle2,
            "description": description2
        }
    )

    assert new_task2.status_code == 201

    data2 = new_task2.json()

    assert "task_status" in data2
    assert data2["task_status"] == status2


    # ---
    all_tasks = await client.get(
        url=f"/boards/{board_name}/tasks?team_id={team_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert all_tasks.status_code == 200
    tasks_js = all_tasks.json()
    assert "tasks" in tasks_js

    assert tasks_js["tasks"] == [{"tittle": task_tittle, "status": status, "description": "", "detail": None}, 
                                   {"tittle": task_tittle2, "status": status2, "description": description2, "detail": None}]


@pytest.mark.asyncio
@pytest.mark.parametrize (
    "task_tittle, status, description, new_status",
    [
        ("Huh", "ToDo", "", "Done"),
        ("You", "Done", "justTired", "InProcess"),
        ("Iam", "Done", "justforgetme", "Done"),
        ("IhaveNo", "Done", "enemies", "ToDo")
    ]
)
async def test_update_task_status(client, task_tittle: str, status: str, description: str, new_status: str):
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
    alice_id: UUID = alice_response.json()["id"]
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
    team_data: dict = team_response.json()
    assert team_data["name"] == team_name
    assert "team_id" in team_data
    team_id: UUID = team_data["team_id"]

    # ---
    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"user_id": alice_id}
    )

    assert invite.status_code == 201

    # ---
    board_name: str = "HDDDD"
    new_board = await client.post(
        url="/boards/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "name": board_name,
            "team_id": team_id,
        }
    )

    assert new_board.status_code == 201 
    board_data: dict = new_board.json()
    assert "board_id" in board_data
    board_id: UUID = board_data["board_id"]

    # ---
    new_task2 = await client.post(
        url="/tasks/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "status": status,
            "team_id": team_id,
            "board_id": board_id,

            "tittle": task_tittle,
            "description": description
        }
    )

    assert new_task2.status_code == 201

    data: dict = new_task2.json()

    assert "task_status" in data
    assert data["task_status"] == status
    assert "task_id" in data
    task_id: UUID = data["task_id"]

    # ---
    all_tasks = await client.get(
        url=f"/boards/{board_name}/tasks?team_id={team_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert all_tasks.status_code == 200
    tasks_js = all_tasks.json()
    assert "tasks" in tasks_js

    assert tasks_js["tasks"] == [{"tittle": task_tittle, "status": status, "description": description, "detail": None}]
    
    upd_tasks = await client.patch(
        url=f"/tasks/new_status?team_id={team_id}&board_id={board_id}&task_id={task_id}&new_status={new_status}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert upd_tasks.status_code == 200

    # ---
    all_tasks = await client.get(
        url=f"/boards/{board_name}/tasks?team_id={team_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert all_tasks.status_code == 200
    tasks_js = all_tasks.json()
    assert "tasks" in tasks_js

    assert tasks_js["tasks"] == [{"tittle": task_tittle, "status": new_status, "description": description, "detail": None}]
