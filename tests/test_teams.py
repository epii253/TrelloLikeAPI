import pytest

@pytest.mark.asyncio
async def test_create_team(client):
    reg = await client.post(url="/auth/register", json={
        "username": "owner",
        "password": "password123",
        "surename": "Овнер"
    })
    assert reg.status_code == 201
    token = reg.json()["token"]
    response = await client.post(
        url="/teams/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "DevOps"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "DevOps"
    #assert data["owner_id"] > 0

@pytest.mark.asyncio
async def test_invite(client):
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

    member_name2: str = "bob"
    bob_response = await client.post(
        "/auth/register",
        json={
            "username": member_name2,
            "password": "isjfljdfkl23",
            "surename": "MCBOBED"
        }
    )
    assert bob_response.status_code == 201

    # ----

    owner = await client.post(url="/auth/register", json={
        "username": "owner",
        "password": "password123",
        "surename": "Овнер"
    })
    assert owner.status_code == 201
    owner_token = owner.json()["token"]

    # ---

    team_response = await client.post(
        url="/teams/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"name": "DevOps"}
    )

    assert team_response.status_code == 201
    team_data = team_response.json()
    assert team_data["name"] == "DevOps"

    # ---
    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"username": member_name}
    )

    assert invite.status_code == 201

    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"username": member_name2}
    )

    assert invite.status_code == 201

@pytest.mark.asyncio
async def test_invite_security(client):
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

    member_name2: str = "bob"
    bob_response = await client.post(
        "/auth/register",
        json={
            "username": member_name2,
            "password": "isjfljdfkl23",
            "surename": "MCBOBED"
        }
    )
    assert bob_response.status_code == 201
    bob_token: str = bob_response.json()["token"]

    # ---

    owner = await client.post(url="/auth/register", json={
        "username": "owner",
        "password": "password123",
        "surename": "Овнер"
    })
    assert owner.status_code == 201
    owner_token = owner.json()["token"]
    team_response = await client.post(
        url="/teams/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"name": "DevOps"}
    )

    assert team_response.status_code == 201
    team_data = team_response.json()
    assert team_data["name"] == "DevOps"

    # ---

    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"username": member_name}
    )

    assert invite.status_code == 201

    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {alice_token}"},
        json = {"username": member_name2}
    )
    assert invite.status_code == 401

@pytest.mark.asyncio
async def test_double_invite(client):
    member_name: str = "bob"
    bob_response = await client.post(
        "/auth/register",
        json={
            "username": member_name,
            "password": "isjfljdfkl23",
            "surename": "MCBOBED"
        }
    )
    assert bob_response.status_code == 201

    # ----

    owner = await client.post(url="/auth/register", json={
        "username": "owner",
        "password": "password123",
        "surename": "Овнер"
    })
    assert owner.status_code == 201
    owner_token = owner.json()["token"]
    team_response = await client.post(
        url="/teams/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"name": "DevOps"}
    )

    assert team_response.status_code == 201
    team_data = team_response.json()
    assert team_data["name"] == "DevOps"

    # ---
    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"username": member_name}
    )

    assert invite.status_code == 201

    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"username": member_name}
    )

    assert invite.status_code == 409

@pytest.mark.asyncio
async def test_update_role(client):
    member_name: str = "bob"
    bob_response = await client.post(
        "/auth/register",
        json={
            "username": member_name,
            "password": "isjfljdfkl23",
            "surename": "MCBOBED"
        }
    )
    assert bob_response.status_code == 201

    # ----

    owner = await client.post(url="/auth/register", json={
        "username": "owner",
        "password": "password123",
        "surename": "Овнер"
    })
    assert owner.status_code == 201
    owner_token = owner.json()["token"]

    # ---

    team_response = await client.post(
        url="/teams/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"name": "DevOps"}
    )

    assert team_response.status_code == 201
    team_data = team_response.json()
    assert team_data["name"] == "DevOps"

    # ---
    invite = await client.post(url=f"/teams/{team_data["name"]}/invite",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"username": member_name}
    )

    assert invite.status_code == 201

    # ---
    to_admin = await client.patch(url=f"/teams/{team_data["name"]}/update_role",
        headers={"Authorization": f"Bearer {owner_token}"},
        json = {"username": member_name, "role": 'admin'}
    )

    assert to_admin.status_code == 200