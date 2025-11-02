from ...table_models.team import Team, TeamMembers
from ...table_models.user import User
from ...shecemas.teams_schema import NewTeamModel
from ...dependencies import get_db 

from typing import Optional
from sqlalchemy import select

async def GetTeamByName(name: str) -> Optional[Team]:
    async for session in get_db():
        result = await session.execute(
            select(Team)
            .where(Team.name == name)
        )
        return result.scalar_one_or_none()

async def CreateTeam(team_info: NewTeamModel, owner: User) -> Optional[Team]:
    async for session in get_db():
        result = await GetTeamByName(team_info.name)

        if result is not None:
            return None

        new_team: Team = Team(owner=owner.id, name=team_info.name)
        session.add(new_team)
        await session.execute()
        return new_team