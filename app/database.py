from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

user: str = "postgres"
host: str = "localhost"
port: int = 5432
URL = f"postgresql+asyncpg://{user}@{host}:{port}/async"

async_engine = create_async_engine(URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
) # Sessions generator