from ...dependencies import get_db
from ...shecemas.auth_shecema import *
from ...table_models.user import User
from ...utitilities import generate_salt, detemenistic_hash, decode_token

from typing import Optional
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from sqlalchemy import select

async def TryGetUserByName(username: str) -> Optional[User]:
    async for session in get_db():
        result = await session.execute(
            select(User)
            .where(User.name == username)
        )
        return result.scalar_one_or_none() 

async def TryGetUserById(user_id: int) -> Optional[User]:
    async for session in get_db():
        result = await session.execute(
            select(User)
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none() 

async def TryCreateNewUser(info: RegistrateModel) -> Optional[User]:
    async for session in get_db():
        if await TryGetUserByName(info.username) is not None:
            return None
        
        salt: str = await generate_salt()
        hashed_password: str = detemenistic_hash(info.password + salt)

        user: User = User(name=info.username, surename=info.surename, hashed_password=hashed_password, salt=salt)

        session.add(user)
        await session.commit()
        return user

async def TryLoginUser(info: LoginModel) -> Optional[User]:
    async for session in get_db():
        potential_user = await TryGetUserByName(info.username)
        if potential_user is None:
            return None
        
        return potential_user if detemenistic_hash(info.password + potential_user.salt) == potential_user.hashed_password else None
    
async def AuthByToken(
    token: str = Depends(HTTPBearer()),
    db = Depends(get_db)
) -> User:

    user = await TryGetUserById(db, decode_token(token.credentials))

    if not user:
        raise HTTPException(401, "Invalid token")
    return user