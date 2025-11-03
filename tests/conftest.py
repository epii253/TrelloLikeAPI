import pytest
import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:password@localhost:5433/test_trello" 
DATABASE_URL = os.environ["DATABASE_URL"]

from app.main import app
from app.dependencies import get_db

from app.table_models import Base 

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
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

# @pytest_asyncio.fixture(scope="session")
# async def engine_session():
#     engine = create_async_engine(DATABASE_URL, echo=False)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield engine
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     await engine.dispose()

# @pytest_asyncio.fixture
# async def dbsession(engine_session):
#     # подключение и начало транзакции на уровне connection
#     async with engine_session.connect() as conn:
#         trans = await conn.begin()       # открытая транзакция
#         TestingSessionLocal = async_sessionmaker(bind=conn, class_=AsyncSession)

#         async with TestingSessionLocal() as session:
#             yield session

#         # откатываем всю транзакцию (всё что делал тест) и закрываем
#         await trans.rollback()

