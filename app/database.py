from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

user: str = "psql"
host: str = "localhost"
port: str = 5432
URL = "postgresql://{user}@{host}:{port}/async"

async_engine = create_async_engine(URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)