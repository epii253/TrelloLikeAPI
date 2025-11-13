from app.extenshions.database.table_models.team import Team, TeamMember, Role
from app.extenshions.database.table_models.user import User
from app.extenshions.database.table_models.boards import Board
from app.extenshions.database.sessions_manager import get_db

from typing import Optional
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

async def TryGetTeamBoardByName(session: AsyncSession, team_id: int, tittle: str) -> Optional[Board]:
    result: Result = await session.execute(
        select(Board)
        .where((Board.team_id == team_id) & (Board.name == tittle))
    )
    return result.scalar_one_or_none()

async def TryCreateBoard(session: AsyncSession, creator: User, team: Team, tittle: str) -> Optional[Board]:
    result: Optional[Board] = await TryGetTeamBoardByName(session, team_id=team.id, tittle=tittle)

    if result is not None:
        return None
    
    new_board: Board = Board(owner=creator.id, team_id=team.id, name=tittle)

    session.add(new_board)
    await session.commit()

    await session.refresh(new_board)
    return new_board 

async def TryDeleteBoard(session: AsyncSession, team: Team, tittle: str) -> bool:
    result: Optional[Board] = await TryGetTeamBoardByName(session, team_id=team.id, tittle=tittle)

    if result is None:
        return False
    
    await session.delete(result)

    await session.commit()

    return True 