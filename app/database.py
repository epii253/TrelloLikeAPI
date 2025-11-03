from .settings import env_settings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from typing import Optional

class Datatbase():
    def __init__(self, url: Optional[str] = None):

        self.db_url = url if url else env_settings.DATABASE_URL
        #print("\n\n\n\n\n\n\n\n "+ self.db_url + "\n\n\n\n\n\n\n\n")
        self.connect_args = {"uri": True} if self.db_url.startswith("sqlite") else {}
        self.name = self.db_url.split(":")[0].split("+")[0]

        self.async_engine = create_async_engine(self.db_url, echo=True, connect_args=self.connect_args)

        self.AsyncSessionLocal = sessionmaker(
                bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False
        )
database: Datatbase = Datatbase()

# async_engine: Optional[AsyncEngine] = None

# AsyncSessionLocal: Optional[sessionmaker] = None
# def init_db(url: str | None = None):
#     global async_engine, AsyncSessionLocal
#     if async_engine is None:
#         db_url = url or env_settings.DATABASE_URL
#         connect_args = {"uri": True} if db_url.startswith("sqlite") else {}

#         async_engine = create_async_engine(db_url, echo=True, connect_args=connect_args)

#         AsyncSessionLocal = sessionmaker(
#                 bind=async_engine,
#             class_=AsyncSession,
#             expire_on_commit=False,
#             autoflush=False,
#             autocommit=False
#         )
#     return async_engine, AsyncSessionLocal