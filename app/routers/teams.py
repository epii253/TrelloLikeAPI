from ..shecemas.teams_schema import NewTeamModel, InviteUserModel, NewRoleModel
from ..crud.auth.registration import AuthByToken , TryGetUserByName
from ..crud.team.team_actions import TryCreateTeam, TryGetTeamByName, TryAddNewTeamMember, GetTeamsBoards, TryUpdateMemberRole, TryCheckUserInTeam
from ..table_models.user import User
from ..table_models.team import Team, TeamMember, Role
from ..dependencies import get_db

from typing import Optional

from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

teams_route: APIRouter = APIRouter(prefix="/teams", tags=["teams"])

@teams_route.post("/")
async def create_team(
    info: NewTeamModel,
    response: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
):
    result: Team = await TryCreateTeam(db, info, user)

    if not result:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This team-name already exists"
            )
    
    response.status_code = status.HTTP_201_CREATED
    return {"details": "Team has been created", "name": result.name}

@teams_route.post("/{team_name}/invite")
async def add_member(
    team_name: str,
    info: InviteUserModel,
    response: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
):
    team: Optional[Team] = await TryGetTeamByName(db, team_name)
    invited_user: Optional[User] = await TryGetUserByName(db, info.username)

    if team is None or invited_user is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="There is no such User or Team"
            )

    if team.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Only owners cand invite new users"
        )
    
    member: Optional[TeamMember] = await TryAddNewTeamMember(db, invited_user, team, Role.Worker)

    if member is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="User already in this team"
            )
    
    response.status_code = status.HTTP_201_CREATED
    return {"details": "User added"}

@teams_route.patch("/{team_name}/update_role")
async def change_role(
    team_name:str,
    info: NewRoleModel,
    response: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
):
    team: Optional[Team] = await TryGetTeamByName(db, team_name)
    target_user: Optional[User] = await TryGetUserByName(db, info.username)

    if team is None or target_user is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="There is no such User or Team"
            )

    if team.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Only owners cand update roles"
        )
    updated_member: Optional[TeamMember] = await TryUpdateMemberRole(db, target_user, team, info.role)

    if updated_member is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Role update error"
        )
    response.status_code = status.HTTP_200_OK
    return {"details": "role updated", "new_role": updated_member.role}
    

@teams_route.get("/{team_name}/boards")
async def get_boards(
    team_name: str,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
    statust_code=status.HTTP_200_OK
):
    team: Team = await TryGetTeamByName(db, team_name)
    
    member: Optional[TeamMember] = await TryCheckUserInTeam(db, user.id, team.id)
    
    if member is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="You must be team member to get access"
            )

    boards: list[str] = await GetTeamsBoards(db, team=team)

    return {"boards": boards}
