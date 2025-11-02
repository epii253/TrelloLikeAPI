from ...table_models.team import Team, TeamMember, Role
from ...table_models.user import User
from ...table_models.boards import Board
from ...shecemas.teams_schema import NewTeamModel
from ...dependencies import get_db 

from typing import Optional
from sqlalchemy import select, Result

async def TryGetTeamByName(name: str) -> Optional[Team]:
    async for session in get_db():
        result = await session.execute(
            select(Team)
            .where(Team.name == name)
        )
        return result.scalar_one_or_none()
    
async def TryGetTeamById(id: int) -> Optional[Team]:
    async for session in get_db():
        result: Result = await session.execute(
            select(Team)
            .where(Team.id == id)
        )
        return result.scalar_one_or_none()

async def TryAddNewTeamMember(user: User, team: Team, role: Role) -> Optional[TeamMember]:
    async for session in get_db():

        member: TeamMember = TeamMember(member_id=user.id, team_id=team.id, role=role)

        session.add(member)
        await session.execute()

        #await session.refresh(member)
        return member

async def TryUpdateMemberRole(user: User, team: Team, new_role: Role) -> Optional[TeamMember]:
    async for session in get_db():
        result: Result = await session.execute(
            select(TeamMember)
            .where(TeamMember.member_id == user.id and TeamMember.team_id == team.id)
        )
        member: TeamMember = result.scalar_one_or_none()
        
        if member is None or member.role == Role.Owner or new_role == Role.Owner:
            return None
        
        member.role = new_role
        await session.execute()

        #await session.refresh(member)
        return member


async def TryCreateTeam(team_info: NewTeamModel, owner: User) -> Optional[Team]:
    async for session in get_db():
        result: Result = await TryGetTeamByName(team_info.name)

        if result is not None:
            return None

        new_team: Team = Team(owner=owner.id, name=team_info.name)
        session.add(new_team)
        await session.execute()

        #await session.refresh(new_team)
        return new_team

async def GetTeamsBoards(team: Team) -> list[str]:
    async for session in get_db():
        result: Result = await session.execute(
            select(Board.name).
            where(Board.team_id == team.id)
        )

        return list(result.scalars().all())