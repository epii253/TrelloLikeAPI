from typing import Optional
from uuid import UUID

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.extenshions.database.table_models.boards import Board
from app.extenshions.database.table_models.team import Role, Team, TeamMember
from app.extenshions.database.table_models.user import User
from app.schemes.teams_schema import NewTeamModel


async def TryGetTeamByName(session: AsyncSession, name: str) -> Optional[Team]:
    result = await session.execute(
        select(Team)
        .where(Team.name == name)
    )
    return result.scalar_one_or_none()
    
async def TryGetTeamById(session: AsyncSession, id: UUID) -> Optional[Team]:
    result: Result = await session.execute(
        select(Team)
        .where(Team.id == id)
    )
    return result.scalar_one_or_none()

async def TryGetUserInTeam(session: AsyncSession, id: UUID, team_id: UUID) -> Optional[TeamMember]:
    result: Result = await session.execute(
        select(TeamMember)
        .where((TeamMember.team_id == team_id) & (TeamMember.member_id == id))
    )
    return result.scalar_one_or_none()

async def TryCheckUserInTeam(session: AsyncSession, user_id: UUID, team_id: UUID) -> Optional[TeamMember]:
    result: Result = await session.execute(
        select(TeamMember)
        .where((TeamMember.team_id == team_id) & (TeamMember.member_id == user_id))
    )
    return result.scalar_one_or_none()

async def TryAddNewTeamMember(session: AsyncSession, user: User, team: Team, role: Role) -> Optional[TeamMember]:
    result: Optional[TeamMember] = await TryCheckUserInTeam(session, user_id=user.id, team_id=team.id)
    
    if result is not None:
        return None

    member: TeamMember = TeamMember(member_id=user.id, team_id=team.id, role=role)

    session.add(member)

    await session.commit()

    await session.refresh(member)
    return member

async def TryUpdateMemberRole(session: AsyncSession, user: User, team: Team, new_role: Role) -> Optional[TeamMember]:
    result: Result = await session.execute(
        select(TeamMember)
        .where(TeamMember.member_id == user.id and TeamMember.team_id == team.id)
    )
    member: Optional[TeamMember] = result.scalar_one_or_none()
    
    if member is None or member.role == Role.Owner or new_role == Role.Owner:
        return None
    
    member.role = new_role
    await session.commit()

    await session.refresh(member)
    return member


async def TryCreateTeam(session: AsyncSession, team_info: NewTeamModel, owner: User) -> Optional[Team]:
    result: Optional[Team] = await TryGetTeamByName(session, team_info.name)

    if result is not None:
        return None

    new_team: Team = Team(owner_id=owner.id, name=team_info.name)

    session.add(new_team)
    await session.commit()

    await session.refresh(new_team)

    new_team_member: TeamMember = TeamMember(member_id=owner.id, team_id=new_team.id, role=Role.Owner)
    session.add(new_team_member)
    await session.commit()

    return new_team

async def GetTeamsBoards(session: AsyncSession, team: Team) -> list[str]:
    result: Result = await session.execute(
        select(Board.name).
        where(Board.team_id == team.id)
    )

    return list(result.scalars().all())