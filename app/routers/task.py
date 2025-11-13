from app.schemes.tasks_shema import CreateTaskModel, UpdateTaskStatusModel
from app.schemes.responces.tasks_responce import CreationTaskResponceModel, UpdateStatusResponceModel
from app.crud.auth.registration import AuthByToken
from app.crud.team.team_actions import TryGetUserInTeam, TryGetTeamByName
from app.crud.board.board_actions import TryGetTeamBoardByName
from app.crud.task.task_actions import TryCreatTask, TryUpdateTaskStatus
from app.extenshions.database.table_models.user import User
from app.extenshions.database.table_models.tasks import Task, Status
from app.extenshions.database.table_models.team import Team, TeamMember, Role
from app.extenshions.database.table_models.boards import Board
from app.extenshions.database.sessions_manager import get_db

from typing import Optional

from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

tasks_router: APIRouter = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.post("/")
async def add_task(
    info: CreateTaskModel,
    responce: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
):
    team: Optional[Team] = await TryGetTeamByName(db, info.team)

    if team is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail="No such team")

    member: Optional[TeamMember] = await TryGetUserInTeam(db, user.id, team.id)

    if member is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="There is no such user in this team")
    
    if member.role < Role.Admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="At least admins can create tasks")
    
    board: Optional[Board] = await TryGetTeamBoardByName(db, team.id, info.board)

    if board is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="There is no such board in this team")
    
    task: Optional[Task] = await TryCreatTask(db, board, info.status, info.tittle, info.description)

    if task is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="Task with this tittle is already exists for this team")
    
    responce.status_code = status.HTTP_201_CREATED
    return CreationTaskResponceModel(
                                        detail="task created", 
                                        task_status=task.status,
                                        team=team.name,
                                        board=board.name, 
                                        tittle=task.tittle
                                    )

@tasks_router.patch("/new_status")
async def new_task_status(
    responce: Response,
    info: UpdateTaskStatusModel = Depends(),
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
):
    team: Optional[Team] = await TryGetTeamByName(db, info.team)

    if team is None:
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, 
                    detail="No such team"
            )

    member: Optional[TeamMember] = await TryGetUserInTeam(db, user.id, team.id)

    if member is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="There is no such user in this team")
    
    board: Optional[Board] = await TryGetTeamBoardByName(db, team.id, info.board)
    if board is None:
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, 
                    detail="No such board"
            )



    updated_task: Optional[Task] = await TryUpdateTaskStatus(db, board, info.tittle, info.new_status)

    if updated_task is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="There is no sush task")
    
    responce.status_code = status.HTTP_200_OK
    return UpdateStatusResponceModel(
                                        detail="status updated", 
                                        tittle=updated_task.tittle, 
                                        new_status=updated_task.status
                                    )
