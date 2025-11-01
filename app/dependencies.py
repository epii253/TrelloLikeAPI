from .database import AsyncSessionLocal
from .utitilities import decode_token
from .crud.auth.registration import UserExists

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_current_user(
    token: str = Depends(HTTPBearer()),
    db: AsyncSession = Depends(get_db)
) -> bool:
    user = decode_token(token)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return UserExists(user)