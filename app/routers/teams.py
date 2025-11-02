from ..shecemas.teams_schema import NewTeamModel 
from ..crud.auth.registration import AuthByToken , TryGetUserByName
from ..crud.team.team_actions import TryCreateTeam, TryGetTeamByName, TryAddNewTeamMember, GetTeamsBoards
from ..table_models.user import User
from ..table_models.team import Team, TeamMember, Role

from typing import Optional

from fastapi import APIRouter, Response, Depends, status

teams: APIRouter = APIRouter(prefix="/teams", tags=["teams"])

@teams.post("/")
async def create_team(
    info: NewTeamModel,
    response: Response,
    user: User = Depends(AuthByToken)
):
    result: Team = await TryCreateTeam(info, user)

    if not result:
        response.status_code = status.HTTP_409_CONFLICT
        return {"details": "This team-name already exists"}
    
    response.status_code = status.HTTP_201_CREATED
    return {"details": "Team has been created"}

@teams.post("/{team_name}/invite/{user_name}")
async def add_member(
    team_name: str,
    user_name: str,
    response: Response,
    user: User = Depends(AuthByToken)
):
    team: Optional[Team] = await TryGetTeamByName(team_name)
    invited_user: Optional[User] = await TryGetUserByName(user_name)

    if team.owner_id != user.id:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"details": "Only owners cand invite new users"}

    if team is None or invited_user is None:
        response.status_code = status.HTTP_409_CONFLICT
        return {"details": "There is no such User or Team"}
    
    member: Optional[TeamMember] = await TryAddNewTeamMember(invited_user, team, Role.Worker)

    if member is None:
        response.status_code = status.HTTP_409_CONFLICT
        return {"details": "User already in this team"}
    
    response.status_code = status.HTTP_201_CREATED
    return {"details": "User added"}

@teams.get("/{team_name}/boards")
async def get_boards(
    team_name: str,
    response: Response,
    user: User = Depends(AuthByToken)
):
    team: Team = await TryGetTeamByName(team_name)
    
    if user not in team.members:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"details": "You must be team member to get access"}

    boards: list[str] = await GetTeamsBoards(team=team)

    response.status_code = status.HTTP_200_OK
    return {"boards": boards}