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
    responce: Response,
    json: RegistrateModel,
    db: AsyncSession = Depends(get_db)
) -> AuthResponceModel:
    new_user: Optional[User] = await TryCreateNewUser(db, json)
    if new_user is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
    new_user.id.__str__
    responce.status_code = status.HTTP_201_CREATED
    return AuthResponceModel(token=create_access_token(data={"id": str(new_user.id), "name": new_user.username}), id=new_user.id, detail=None)

@auth_route.post("/login")
async def login(
    responce: Response,
    json: LoginModel,
    db: AsyncSession = Depends(get_db)
) -> AuthResponceModel:
    user: Optional[User] = await TryLoginUser(db, json)

    if user is None:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Unknow user or incorrect password"
            )
    
    responce.status_code = status.HTTP_200_OK
    return AuthResponceModel(token=create_access_token(data={"id": str(user.id), "name": user.username}), id=user.id, detail=None)