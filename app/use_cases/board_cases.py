from typing import Optional

from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.board.board_actions import (
    TryCreateBoard,
    TryDeleteBoard,
    TryGetTeamBoardByName,
)
from app.crud.task.task_actions import GetBoardTasks
from app.crud.team.team_actions import (
    TryCheckUserInTeam,
    TryGetTeamById,
    TryGetUserInTeam,
)
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


async def create_board_case(
    json: CreateBoardModel,
    user: User,
    db: AsyncSession,
    responce: Response,
) -> BoardCreationResponceModel:
    team: Optional[Team] = await TryGetTeamById(db, json.team_id)

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

    board: Optional[Board] = await TryCreateBoard(db, user, team, json.name)

    if board is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is board-name for this time"
            )
    
    responce.status_code = status.HTTP_201_CREATED
    return BoardCreationResponceModel(
                                        detail="Board created", 
                                        board_name=board.name,
                                        board_id=board.id, 
                                        team_id=team.id,
                                        owner_id=user.id,
                                    )

async def get_board_tasks_case(
    board_name: str,
    query: GetBoardTasksdModel,
    user: User,
    db: AsyncSession,
) -> TasksInfoResponceModel:
    team: Optional[Team] = await TryGetTeamById(db, query.team_id)

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
    
    return TasksInfoResponceModel(
                                    board_name=board.name, 
                                    board_id=board.id,
                                    team_name=team.name,
                                    team_id=team.id, 
                                    tasks= await GetBoardTasks(db, board), 
                                    detail=None,
                                )

async def delete_board_case(
    responce: Response,
    query: DeleteBoardModel,
    user: User,
    db: AsyncSession ,

) -> Informative:
    team: Optional[Team] = await TryGetTeamById(db, query.team_id)

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

    deleted: bool = await TryDeleteBoard(session=db, team=team, id=query.board_id)

    if not deleted:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Delete is fail"
            )
    
    responce.status_code = status.HTTP_200_OK
    return Informative(detail="Board deleted") 