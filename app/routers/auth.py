from fastapi import APIRouter, Response, status
from typing import Annotated
from ..shecemas.auth_shecema import *
from ..crud.auth.registration import *

auth_route: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@auth_route.post("/register")
async def register(
    info: RegistrateModel,
    responce: Response
):
    succes: bool = TryCreateNewUser(info=info)

    result = {"token": ""}

    if not succes:
        responce.status_code = status.HTTP_401_UNAUTHORIZED
        return result
    
    responce.status_code = status.HTTP_200_OK
    result["token"] = ""
    return result

@auth_route.get("/login")
async def register(info: LoginModel):
    pass