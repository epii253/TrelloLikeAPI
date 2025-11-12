from fastapi import FastAPI
from contextlib import asynccontextmanager
from .extenshions.database.database import database
from .routers import auth, teams, board, task

# migration on start-up
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.migrate_models()

    try:
        yield
    finally:
        await database.async_engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(auth.auth_route)
app.include_router(teams.teams_route)
app.include_router(board.board_router)
app.include_router(task.tasks_router)

