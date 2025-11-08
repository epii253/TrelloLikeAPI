import pytest
import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

DATABASE_HOST="localhost"
DATABASE_USER="postgres"
DATABASE_PORT=5432
DATABASE_NAME="async"
POSTGRES_PASSWORD="kqVI7H8069"
DATABASE_URL="postgresql+asyncpg://"

os.environ["DATABASE_HOST"] = "localhost"
os.environ["DATABASE_USER"] = "postgres"
os.environ["DATABASE_PORT"] = str(DATABASE_PORT)
os.environ["DATABASE_NAME"] = "test_trello"
os.environ["POSTGRES_PASSWORD"] = "password"
os.environ["DATABASE_URL"] = "postgresql+asyncpg://" 

FULL_DATABASE_URL = os.environ["DATABASE_URL"] \
                    + os.environ["DATABASE_USER"] \
                    + ":" + os.environ["POSTGRES_PASSWORD"] \
                    + "@" \
                    + os.environ["DATABASE_HOST"] \
                    + ":" + os.environ["DATABASE_PORT"] \
                    + "/" + os.environ["DATABASE_NAME"]

from app.main import app
from app.dependencies import get_db

from app.table_models import Base 

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    engine: AsyncEngine = create_async_engine(FULL_DATABASE_URL, echo=False)
    TestingSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)
    yield

    async with engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)

    app.dependency_overrides.pop(get_db, None)
    await engine.dispose()

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

