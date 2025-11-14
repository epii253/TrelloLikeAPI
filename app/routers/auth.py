from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth.registration import TryCreateNewUser, TryLoginUser
from app.extenshions.database.sessions_manager import get_db
from app.extenshions.database.table_models.user import User
from app.schemes.auth_shecema import LoginModel, RegistrateModel
from app.schemes.responces.auth_responce import AuthResponceModel
from app.security.core import create_access_token

auth_route: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@auth_route.post("/register")
async def register(
    query: RegistrateModel,
    responce: Response,
    db: AsyncSession = Depends(get_db)
) -> AuthResponceModel:
    new_user: Optional[User] = await TryCreateNewUser(db, query)
    if new_user is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

    responce.status_code = status.HTTP_201_CREATED
    return AuthResponceModel(token=create_access_token(data={"id": new_user.id, "name": new_user.username}), detail=None)

@auth_route.post("/login")
async def login(
    query: LoginModel,
    responce: Response,
    db: AsyncSession = Depends(get_db)
) -> AuthResponceModel:
    user: Optional[User] = await TryLoginUser(db, query)

    if user is None:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Unknow user or incorrect password"
            )
    
    responce.status_code = status.HTTP_200_OK
    return AuthResponceModel(token=create_access_token(data={"id": user.id, "name": user.username}), detail=None)