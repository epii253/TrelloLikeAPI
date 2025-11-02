from fastapi import FastAPI
from app.routers import auth
# from app.database import init_db

# init_db()

app: FastAPI = FastAPI()
app.include_router(auth.auth_route)
