from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timezone
from app.database import get_db
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.security import get_current_user
from app.models import User

router = APIRouter(prefix="/todos", tags=["todos"])


# create a todo
@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.id:
        raise HTTPException(status_code=500, detail="Error interno")
    todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        user_id=current_user.id
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


# get all todos for the current user
@router.get("/")
def get_todos(page: int = 1, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = select(Todo).where(Todo.user_id == current_user.id)
    total = len(db.exec(query).all())
    todos = db.exec(query.offset((page - 1) * limit).limit(limit)).all()
    return {"data": todos, "page": page, "limit": limit, "total": total}


# get a single todo by id
@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return todo


# update a todo
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.exec(select(Todo).where(Todo.id == todo_id)).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # only update fields that were sent
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.done is not None:
        todo.done = todo_data.done

    todo.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(todo)
    return todo


# delete a todo
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.exec(select(Todo).where(Todo.id == todo_id)).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db.delete(todo)
    db.commit()
