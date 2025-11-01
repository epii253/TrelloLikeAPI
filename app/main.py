from fastapi import FastAPI
from .routers import auth

app: FastAPI = FastAPI()

app.include_router(auth.auth_route)