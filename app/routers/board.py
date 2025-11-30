from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth.registration import AuthByToken
from app.extenshions.database.sessions_manager import get_db
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
from app.use_cases.board_cases import (
    create_board_case,
    delete_board_case,
    get_board_tasks_case,
)

board_router: APIRouter = APIRouter(prefix="/boards", tags=["boards"])

@board_router.post("/")
async def create_board(
    json: CreateBoardModel,
    responce: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),

) -> BoardCreationResponceModel:
    return await create_board_case(json, user, db, responce)

@board_router.get("/{board_name}/tasks")
async def get_board_tasks(
    board_name: str,
    query: GetBoardTasksdModel = Depends(),
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
    statust_code: int =status.HTTP_200_OK
    
) -> TasksInfoResponceModel:
    return await get_board_tasks_case(board_name, query, user, db)


@board_router.delete("/delete")
async def delete_board(
    responce: Response,
    query: DeleteBoardModel = Depends(),
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),

) -> Informative: 
    return await delete_board_case(responce, query, user, db)