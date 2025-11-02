from fastapi import APIRouter, Response, status, HTTPException
from ..shecemas.auth_shecema import *
from ..crud.auth.registration import *
from ..utitilities import create_access_token, decode_token

auth_route: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@auth_route.post("/register")
async def register(
    info: RegistrateModel,
    responce: Response
):
    new_user: Optional[User] = await TryCreateNewUser(info)
    if new_user is None:
        responce.status_code = status.HTTP_409_CONFLICT
        return {"detail": "User already exists"}
    
    responce.status_code = status.HTTP_201_CREATED
    return {"token": await create_access_token(data={"id": new_user.id, "name": new_user.username})}

@auth_route.post("/login")
async def register(
    info: LoginModel,
    responce: Response
):
    user: Optional[User] = await TryLoginUser(info)

    if user is None:
        responce.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Unknow user or incorrect password"}
    
    responce.status_code = status.HTTP_200_OK
    return {"token": await create_access_token(data={"id": user.id, "name": user.name})}