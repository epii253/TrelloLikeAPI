from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.extenshions.database.sessions_manager import get_db
from app.schemes.auth_shecema import LoginModel, RegistrateModel
from app.schemes.responces.auth_responce import AuthResponceModel
from app.use_cases.auth_cases import login_user_case, registrate_user_case

auth_route: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@auth_route.post("/register")
async def register(
    responce: Response,
    json: RegistrateModel,
    db: AsyncSession = Depends(get_db)

) -> AuthResponceModel:
    return await registrate_user_case(responce, json, db)

@auth_route.post("/login")
async def login(
    responce: Response,
    json: LoginModel,
    db: AsyncSession = Depends(get_db)

) -> AuthResponceModel:
    return await login_user_case(responce, json, db)