
from typing import Optional

from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth.registration import TryCreateNewUser, TryLoginUser
from app.extenshions.database.table_models.user import User
from app.schemes.auth_shecema import LoginModel, RegistrateModel
from app.schemes.responces.auth_responce import AuthResponceModel
from app.security.core import create_access_token


async def registrate_user_case(
    responce: Response,
    json: RegistrateModel,
    db: AsyncSession,

) -> AuthResponceModel:
    new_user: Optional[User] = await TryCreateNewUser(db, json)
    if new_user is None:
        raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

    responce.status_code = status.HTTP_201_CREATED
    return AuthResponceModel(token=create_access_token(data={"id": str(new_user.id), "name": new_user.username}), id=new_user.id, detail=None)

async def login_user_case(
    responce: Response,
    json: LoginModel,
    db: AsyncSession,

)-> AuthResponceModel:
    user: Optional[User] = await TryLoginUser(db, json)

    if user is None:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Unknow user or incorrect password"
            )
    
    responce.status_code = status.HTTP_200_OK
    return AuthResponceModel(token=create_access_token(data={"id": str(user.id), "name": user.username}), id=user.id, detail=None)