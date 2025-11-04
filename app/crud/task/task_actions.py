from ...table_models.team import Team, TeamMember, Role
from ...table_models.user import User
from ...table_models.boards import Board
from ...table_models.tasks import Task, Status
from ...shecemas.teams_schema import NewTeamModel
from ...dependencies import get_db 

from typing import Optional
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

async def TryGetTaskByName(session: AsyncSession, board_id: int, title: str) -> Optional[Task]:
    result: Result = await session.execute(
        select(Task).
        where((Task.title == title) & (Task.board_id == board_id))
    )
    return result.scalar_one_or_none()

async def TryCreatTask(
    session: AsyncSession, 
    board: Board, 
    status: Status, 
    title: str, 
    description: Optional[str]
) -> Optional[Task]:
    
    result: Optional[Task] = await TryGetTaskByName(session, board.id, title)

    if result is not None:
        return None
    
    new_task: Task = Task(board_id=board.id, status=status, title=title, description=description)

    session.add(new_task)
    await session.commit()

    await session.refresh(new_task)
    return new_task
