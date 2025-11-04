import pytest

@pytest.mark.asyncio
async def test_create_board(client):
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

    new_board = await client.post(
        url=f"/boards/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "name": "HDDDD",
            "team_name": team_name,
        }
    )

    assert new_board.status_code == 201 

@pytest.mark.asyncio
async def test_create_board_security(client):
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

    new_board = await client.post(
        url=f"/boards/",
        headers={"Authorization": f"Bearer {alice_token}"},
        json = {
            "name": "HDDDD",
            "team_name": team_name,
        }
    )

    assert new_board.status_code == 401

@pytest.mark.asyncio
async def test_get_team_boards(client):
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

    board_name2: str = "KEKWEED"
    new_board = await client.post(
        url=f"/boards/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {
            "name": board_name2,
            "team_name": team_name,
        }
    )

    assert new_board.status_code == 201 

    # ---

    result = await client.get(
        url=f"/teams/{team_name}/boards",
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    assert result.status_code == 200
    data = result.json()
    assert "boards" in data

    boards: list[str] = data["boards"]

    assert boards[0] == board_name
    assert boards[1] == board_name2

# @pytest.mark.asyncio
# async def test_delete_board(client):
#     member_name: str = "alice"
#     alice_response = await client.post(
#         "/auth/register",
#         json={
#             "username": member_name,
#             "password": "secure123",
#             "surename": "Алисова"
#         }
#     )
    
#     assert alice_response.status_code == 201
#     alice_token: str = alice_response.json()["token"]
#     # ----

#     owner = await client.post(url="/auth/register", json={
#         "username": "owner",
#         "password": "password123",
#         "surename": "Овнер"
#     })
#     assert owner.status_code == 201
#     owner_token = owner.json()["token"]

#     # ---
#     team_name: str = "DevOps"
#     team_response = await client.post(
#         url="/teams/",
#         headers={"Authorization": f"Bearer {owner_token}"},
#         json={"name": team_name}
#     )

#     assert team_response.status_code == 201
#     team_data = team_response.json()
#     assert team_data["name"] == team_name

#     # ---
#     invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
#         headers={"Authorization": f"Bearer {owner_token}"},
#         json = {"username": member_name}
#     )

#     assert invite.status_code == 201

#     # ---

#     new_board = await client.delete(
#         url=f"/boards/delete",
#         headers={"Authorization": f"Bearer {owner_token}"},
#         json = {
#             "name": "HDDDD",
#             "team_name": team_name,
#         }
#     )

#     assert new_board.status_code == 200