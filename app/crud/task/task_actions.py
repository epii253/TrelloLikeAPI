from typing import Optional
from uuid import UUID

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.extenshions.database.table_models.boards import Board
from app.extenshions.database.table_models.tasks import Status, Task
from app.schemes.responces.board_responce import TaskInfoModel


async def TryGetTaskByName(session: AsyncSession, board_id: UUID, title: str) -> Optional[Task]:
    result: Result = await session.execute(
        select(Task).
        where((Task.tittle == title) & (Task.board_id == board_id))
    )
    return result.scalar_one_or_none()

async def TryGetTaskById(session: AsyncSession, board_id: UUID, id: UUID) -> Optional[Task]:
    result: Result = await session.execute(
        select(Task).
        where((Task.id == id) & (Task.board_id == board_id))
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
    task_id: UUID, 
    new_status: Status
) -> Optional[Task]:
    result: Optional[Task] = await TryGetTaskById(session, board.id, task_id)

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

    info: list[TaskInfoModel] = []
    for row in result.scalars().all():
        description: str = row.description if row.description is not None else ""
        info.append(TaskInfoModel(tittle=row.tittle, status=row.status, description=description, detail=None))

    return info