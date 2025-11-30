from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth.registration import AuthByToken
from app.extenshions.database.sessions_manager import get_db
from app.extenshions.database.table_models.user import User
from app.schemes.responces.team_responce import (
    BoardsInfoResponceModel,
    InviteResponceModel,
    RoleUpdateResponceModel,
    TeamCreationResponceModel,
)
from app.schemes.teams_schema import InviteUserModel, NewRoleModel, NewTeamModel
from app.use_cases.team_cases import (
    add_member_case,
    change_role_case,
    create_team_case,
    get_boards_case,
)

teams_route: APIRouter = APIRouter(prefix="/teams", tags=["teams"])

@teams_route.post("/")
async def create_team(
    json: NewTeamModel,
    response: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),

) -> TeamCreationResponceModel:
    return await create_team_case(json, response, user, db)

@teams_route.post("/{team_name}/invite")
async def add_member(
    team_name: str,
    json: InviteUserModel,
    response: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),

) -> InviteResponceModel:
    return await add_member_case(team_name, json, response, user, db)

@teams_route.patch("/{team_name}/update_role")
async def change_role(
    team_name:str,
    json: NewRoleModel,
    response: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),

) -> RoleUpdateResponceModel:
    return await change_role_case(team_name, json, response, user, db)
    

@teams_route.get("/{team_name}/boards")
async def get_boards(
    team_name: str,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
    statust_code = status.HTTP_200_OK

) -> BoardsInfoResponceModel:
    return await get_boards_case(team_name, user, db)
