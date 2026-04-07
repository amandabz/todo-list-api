import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
engine = create_engine(DATABASE_URL, echo=True)  # echo=True shows the queries in the console

def create_db_if_not_exists():  # this function is used in main.py
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

# get_db()
