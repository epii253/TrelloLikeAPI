from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.extenshions.database.database import database


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with database.AsyncSessionLocal() as session:
        yield session