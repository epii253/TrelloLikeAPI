from ...dependencies import get_db
from ...shecemas.auth_shecema import *
from ...table_models.user import User
from ...security.core import generate_salt, detemenistic_hash, decode_token

from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

async def TryGetUserByName(session: AsyncSession, username: str) -> Optional[User]:
    result: Result = await session.execute(
        select(User)
        .where(User.username == username)
    )
    return result.scalar_one_or_none() 

async def TryGetUserById(session: AsyncSession,user_id: int) -> Optional[User]:
    result: Result = await session.execute(
        select(User)
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none() 

async def TryCreateNewUser(session: AsyncSession, info: RegistrateModel) -> Optional[User]:
    if await TryGetUserByName(session, info.username) is not None:
        return None
    
    salt: str = await generate_salt()
    hashed_password: str = detemenistic_hash(info.password + salt)

    user: User = User(
        username=info.username, 
        surename=info.surename, 
        hashed_password=hashed_password, 
        salt=salt
    )

    session.add(user)
    await session.commit()

    result: Result = await session.execute(
        select(User)
        .where(User.username == user.username)
    )

    await session.refresh(user)

    return user

async def TryLoginUser(session: AsyncSession, info: LoginModel) -> Optional[User]:
    potential_user: Optional[User] = await TryGetUserByName(session, info.username)
    if potential_user is None:
        return None
    
    return potential_user if detemenistic_hash(info.password + potential_user.salt) == potential_user.hashed_password else None

security = HTTPBearer(auto_error=True) 

async def AuthByToken(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
) -> User:
    
    decoded_id: int = decode_token(credentials.credentials)
    
    user: Optional[User] = await TryGetUserById(db, decoded_id)

    if not user:
        raise HTTPException(401, "Invalid token")
    
    return user