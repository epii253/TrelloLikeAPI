from fastapi import FastAPI
from .routers import auth, teams

app: FastAPI = FastAPI()
app.include_router(auth.auth_route)
app.include_router(teams.teams_route)
