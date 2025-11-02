from ..shecemas.teams_schema import NewTeamModel 
from ..crud.auth.registration import AuthByToken 
from ..crud.team.team_actions import CreateTeam
from ..table_models.user import User
from ..table_models.team import Team

from fastapi import APIRouter, Response, Depends, status

teams: APIRouter = APIRouter(prefix="/teams", tags=["teams"])

@teams.post("/")
async def create_team(
    info: NewTeamModel,
    response: Response,
    user: User = Depends(AuthByToken)
):
    result: Team = await CreateTeam(info, user)

    if not result:
        response.status_code = status.HTTP_409_CONFLICT
        return {"detail": "This team-name already exists"}
    
    response.status_code = status.HTTP_201_CREATED
    return {"detail": "Team has been created"}