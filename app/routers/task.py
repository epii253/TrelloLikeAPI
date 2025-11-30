from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth.registration import AuthByToken
from app.extenshions.database.sessions_manager import get_db
from app.extenshions.database.table_models.user import User
from app.schemes.responces.tasks_responce import (
    CreationTaskResponceModel,
    UpdateTaskStatusResponceModel,
)
from app.schemes.tasks_shema import CreateTaskModel, UpdateTaskStatusModel
from app.use_cases.task_cases import add_task_case, new_task_status_case

tasks_router: APIRouter = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.post("/")
async def add_task(
    json: CreateTaskModel,
    responce: Response,
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),

) -> CreationTaskResponceModel:
    return await add_task_case(json, responce, user, db)

@tasks_router.patch("/new_status")
async def new_task_status(
    responce: Response,
    query: UpdateTaskStatusModel = Depends(),
    user: User = Depends(AuthByToken),
    db: AsyncSession = Depends(get_db),
    
) -> UpdateTaskStatusResponceModel:
    return await new_task_status_case(responce, query, user, db)
