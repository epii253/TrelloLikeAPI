from ...extenshions.database.table_models.team import Team, TeamMember, Role
from ...extenshions.database.table_models.user import User
from ...extenshions.database.table_models.boards import Board
from ...extenshions.database.table_models.tasks import Task, Status
from ...schemes.teams_schema import NewTeamModel
from ...schemes.responces.board_responce import TaskInfoModel
from ...extenshions.database.sessions_manager import get_db 

from typing import Optional
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

async def TryGetTaskByName(session: AsyncSession, board_id: int, title: str) -> Optional[Task]:
    result: Result = await session.execute(
        select(Task).
        where((Task.tittle == title) & (Task.board_id == board_id))
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
    
    new_task: Task = Task(board_id=board.id, status=status, tittle=title, description=description)

    session.add(new_task)
    await session.commit()

    await session.refresh(new_task)
    return new_task

async def TryUpdateTaskStatus(
    session: AsyncSession, 
    board: Board, 
    title: str, 
    new_status: Status
) -> Optional[Task]:
    result: Optional[Task] = await TryGetTaskByName(session, board.id, title)

    if result is None:
        return None
    
    result.status = new_status

    await session.commit()

    await session.refresh(result)
    return result
    

async def GetBoardTasks(
    session: AsyncSession, 
    board: Board,
) -> list[TaskInfoModel]:
    result: Result = await session.execute(
        select(Task)
        .where((Task.board_id == board.id))
    )

    info: list[dict[str, list[dict[str, str]]]] = []
    for row in result.scalars().all():
        description: str = row.description if row.description is not None else ""
        info.append(TaskInfoModel(tittle=row.tittle, status=row.status, description=description))

    return info