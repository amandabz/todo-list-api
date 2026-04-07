from sqlmodel import SQLModel
from datetime import datetime

# auth
class UserRegister(SQLModel):  # what the API receives when registering
    email: str
    name: str
    password: str

class UserLogin(SQLModel):  # what the API receives when logging in
    email: str
    password: str

class UserResponseToken(SQLModel):  # what the API returns (never the password)
    token: str

class Token(SQLModel):  # the JWT returned by the login
    token: str

# todo
class TodoCreate(SQLModel):  # data to create a task
    title: str
    description: str | None = None

class TodoUpdate(SQLModel):  # optional fields
    title: str | None = None
    description: str | None = None
    done: bool | None = None

class TodoResponse(SQLModel):  # what the API returns
    id: int
    title: str
    description: str | None
    done: bool
    created_at: datetime
    updated_at: datetime
