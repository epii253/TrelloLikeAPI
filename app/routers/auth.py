from fastapi import APIRouter, Response, status, HTTPException
from ..shecemas.auth_shecema import *
from ..crud.auth.registration import *
from ..utitilities import create_access_token
from ..dependencies import get_db

auth_route: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@auth_route.post("/register")
async def register(
    info: RegistrateModel,
    responce: Response,
    db: AsyncSession = Depends(get_db)
):
    new_user: Optional[User] = await TryCreateNewUser(db, info)
    if new_user is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

    responce.status_code = status.HTTP_201_CREATED
    return {"token": await create_access_token(data={"id": new_user.id, "name": new_user.username})}

@auth_route.post("/login")
async def register(
    info: LoginModel,
    responce: Response,
    db: AsyncSession = Depends(get_db)
):
    user: Optional[User] = await TryLoginUser(db, info)

    if user is None:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Unknow user or incorrect password"
            )
    
    responce.status_code = status.HTTP_200_OK
    return {"token": await create_access_token(data={"id": user.id, "name": user.name})}