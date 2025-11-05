from .settings import env_settings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from typing import Optional

class Datatbase():
    def __init__(self, url: Optional[str] = None):

        self.db_url = url if url else \
            env_settings.DATABASE_URL \
            + env_settings.DATABASE_USER \
            + (":" + env_settings.POSTGRES_PASSWORD if len(env_settings.POSTGRES_PASSWORD) > 0 else "") \
            + "@" \
            + (env_settings.DATABASE_HOST if len(env_settings.DATABASE_HOST) > 0 else "") \
            + (":" + str(env_settings.DATABASE_PORT) if env_settings.DATABASE_PORT is not None else "") \
            + "/" + env_settings.DATABASE_NAME

        self.name = self.db_url.split(":")[0].split("+")[0]

        self.async_engine = create_async_engine(self.db_url, echo=True)

        self.AsyncSessionLocal = sessionmaker(
                bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False
        )
database: Datatbase = Datatbase()