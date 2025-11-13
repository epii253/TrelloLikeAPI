from __future__ import annotations

from ...settings import env_settings
from .table_models.base import Base

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
#from sqlalchemy.orm import sessionmaker, Session
from typing import Optional

class DatabaseUrlBuilder():
    def __init__(self) -> None:
        self.preffix: Optional[str] = None
        self.user: Optional[str] = None
        self.password: Optional[str] = None
        self.host: Optional[str] = None
        self.port: Optional[int] = None
        self.name: Optional[str] = None

    def WithPrefix(self, preffix: str) -> DatabaseUrlBuilder:
        self.preffix = preffix

        return self

    def WithUser(self, user: str) -> DatabaseUrlBuilder:
        self.user = user

        return self

    def WithPassword(self, password: Optional[str]) -> DatabaseUrlBuilder:
        self.password = password

        return self

    def WithHost(self, host: Optional[str]) -> DatabaseUrlBuilder:
        self.host = host

        return self

    def WithPort(self, port: Optional[int]) -> DatabaseUrlBuilder:
        self.port = port

        return self
    
    def WithName(self, name: str) -> DatabaseUrlBuilder:
        self.name = name

        return self

    def Build(self) -> str:
        if self.preffix is None:
            raise ValueError("Database prefix (e.g., 'postgresql://') is required.")
        
        if self.user is None:
            raise ValueError("Database user is required.")
        
        if self.name is None:
            raise ValueError("Database name is required.")

        return self.preffix \
                + self.user \
                + (":" + self.password if self.password is not None and len(self.password) > 0 else "") \
                + "@" \
                + (self.host if self.host is not None and len(self.host) > 0 else "") \
                + (":" + str(self.port) if self.port is not None else "") \
                + "/" + self.name


class Datatbase():
    def __init__(self, url: Optional[str] = None):

        self.db_url: str = url if url else \
            DatabaseUrlBuilder() \
            .WithPrefix(env_settings.DATABASE_URL) \
            .WithUser(env_settings.DATABASE_USER) \
            .WithPassword(env_settings.POSTGRES_PASSWORD) \
            .WithHost(env_settings.DATABASE_HOST) \
            .WithPort(env_settings.DATABASE_PORT) \
            .WithName(env_settings.DATABASE_NAME) \
            .Build()
        
        self.name: str = self.db_url.split(":")[0].split("+")[0]

        self.async_engine: AsyncEngine = create_async_engine(self.db_url, echo=True)

        self.AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
                bind=self.async_engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
                autocommit=False
        )
    async def migrate_models(self) -> None:
        async with self.async_engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    
database: Datatbase = Datatbase()
