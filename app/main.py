from contextlib import asynccontextmanager
from fastapi import FastAPI
# from dotenv import load_dotenv
from app.database import create_db_if_not_exists
# from app import models
from app.routers import login, register, todos

# load_dotenv()  # .env vars

# first you define the lifespan
"""with lifespan, you’re telling FastAPI: “before you start handling requests, run this first”"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_if_not_exists()  # create the database if not exists
    yield

# then you create the app (you already know lifespan)
app = FastAPI(title="Todo List API", lifespan=lifespan)

app.include_router(register.router)
app.include_router(login.router)
app.include_router(todos.router)

# lastly, the routes (you already know the app)
@app.get("/")
def root():
    return {"message": "Todo List API working"}


# status codes: https://fastapi.tiangolo.com/reference/status/#fastapi.status.WS_1008_POLICY_VIOLATION
# run app: uv run fastapi dev
# stop app: Ctrl + C
