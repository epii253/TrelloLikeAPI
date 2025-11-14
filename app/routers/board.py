from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth.registration import AuthByToken
from app.crud.board.board_actions import (
    TryCreateBoard,
    TryDeleteBoard,
    TryGetTeamBoardByName,
)
from app.crud.task.task_actions import GetBoardTasks
from app.crud.team.team_actions import (
    TryCheckUserInTeam,
    TryGetTeamByName,
    TryGetUserInTeam,
)
from app.extenshions.database.sessions_manager import get_db
from app.extenshions.database.table_models.boards import Board
from app.extenshions.database.table_models.team import Role, Team, TeamMember
from app.extenshions.database.table_models.user import User
from app.schemes.board_schema import (
    CreateBoardModel,
    DeleteBoardModel,
    GetBoardTasksdModel,
)
from app.schemes.responces.base_responce import Informative
from app.schemes.responces.board_responce import (
    BoardCreationResponceModel,
    TasksInfoResponceModel,
)

board_router: APIRouter = APIRouter(prefix="/boards", tags=["boards"])

@board_router.post("/")
async def create_board(
    query: CreateBoardModel,
    responce: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
) -> BoardCreationResponceModel:
    team: Optional[Team] = await TryGetTeamByName(db, query.team_name)

    if team is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="There is no such team"
            )
    
    member: Optional[TeamMember] = await TryGetUserInTeam(db, user.id, team.id)

    if member is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No such user in this team"
            )
    if member.role < Role.Admin:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="At least admins can create boards"
            )

    board: Optional[Board] = await TryCreateBoard(db, user, team, query.name)

    if board is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is board-name for this time"
            )
    
    responce.status_code = status.HTTP_201_CREATED
    return BoardCreationResponceModel(
                                        detail="Board created", 
                                        board_name=board.name, 
                                        team_name=team.name,
                                        owner_name=user.username
                                    )

@board_router.get("/{board_name}/tasks")
async def get_board_tasks(
    board_name: str,
    query: GetBoardTasksdModel = Depends(),
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
    statust_code: int =status.HTTP_200_OK
) -> TasksInfoResponceModel:
    team: Optional[Team] = await TryGetTeamByName(db, query.team_name)

    if team is None:
       raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="There is no such team"
            )

    board: Optional[Board] = await TryGetTeamBoardByName(db, team.id, board_name)

    if board is None:
       raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="There is no such team's board"
            )
    
    member: Optional[TeamMember] = await TryCheckUserInTeam(db, user.id, team.id)
    if member is None:
       raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="There is no such member in this team"
            )
    
    return TasksInfoResponceModel(board_name=board.name, team_name=team.name, tasks= await GetBoardTasks(db, board), detail=None)


@board_router.delete("/delete")
async def delete_board(
    responce: Response,
    query: DeleteBoardModel = Depends(),
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
) -> Informative: 
    team: Optional[Team] = await TryGetTeamByName(db, query.team_name)

    if team is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No such team"
            )
    
    member: Optional[TeamMember] = await TryGetUserInTeam(db, user.id, team.id)

    if member is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No such user in this team"
            )
    if member.role < Role.Admin:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="At least admins can delete boards"
            )

    deleted: bool = await TryDeleteBoard(db, team, query.name)

    if not deleted:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Delete is fail"
            )
    
    responce.status_code = status.HTTP_200_OK
    return Informative(detail="Board deleted") 