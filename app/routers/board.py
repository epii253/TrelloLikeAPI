from ..shecemas.board_schema import CreateBoardModel, DeleteBoardModel
from ..crud.auth.registration import AuthByToken
from ..crud.team.team_actions import TryGetUserInTeam, TryGetTeamByName
from ..crud.board.board_actions import TryCreateBoard, TryDeleteBoard
from ..table_models.user import User
from ..table_models.team import Team, TeamMember, Role
from ..table_models.boards import Board
from ..dependencies import get_db

from typing import Optional

from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

board_router: APIRouter = APIRouter(prefix="/boards", tags=["boards"])

@board_router.post("/")
async def create_board(
    info: CreateBoardModel,
    responce: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
):
    team: Optional[Team] = await TryGetTeamByName(db, info.team_name)

    if team is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No such team")
    
    member: Optional[TeamMember] = await TryGetUserInTeam(db, user.id, team.id)

    if member is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="No such user in this team")
    if member.role < Role.Admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="At least admins can create boards")

    board: Optional[Board] = await TryCreateBoard(db, user, team, info.name)

    if board is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="There is board-name for this time")
    
    responce.status_code = status.HTTP_201_CREATED
    return {"detail": "Board Created"}

@board_router.delete("/delete") # TODO json is not allowed - remove
async def delete_board(
    info: DeleteBoardModel,
    responce: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
):
    team: Optional[Team] = await TryGetTeamByName(db, info.team_name)

    if team is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No such team")
    
    member: Optional[TeamMember] = await TryGetUserInTeam(db, user.id, team.id)

    if member is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="No such user in this team")
    if member.role < Role.Admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="At least admins can delete boards")

    deleted: bool = await TryDeleteBoard(db, team, info.name)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="Delete is fail")
    
    responce.status_code = status.HTTP_200_OK
    return {"detail": "Board Deleted"}