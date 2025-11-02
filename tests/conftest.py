import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///file:memdb1?mode=memory&cache=shared"
DATABASE_URL = os.environ["DATABASE_URL"]

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import inspect

from app.table_models.base import Base
from app.table_models.user import *
from app.table_models.team import *

import app.database as db
from app.main import app
from app.dependencies import get_db

engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"uri": True})
TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

db.AsyncSessionLocal = TestingSessionLocal

async def override_get_db():
    async with TestingSessionLocal() as session:
        print("override_get_db: session.bind ->", getattr(session, "bind", None))
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        print("registered in Base.metadata:", list(Base.metadata.tables.keys()))

        await conn.run_sync(Base.metadata.create_all)
        
        real = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        print("real tables in DB after create_all:", real)
    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
