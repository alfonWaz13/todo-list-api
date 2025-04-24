from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from source.database import get_db
from source.models import ToDos
from source.schemas.todo import ToDoRequest

router = APIRouter(prefix="/todos", tags=["ToDos"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    todos = db.query(ToDos).all()
    return todos

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int):
    todo = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: ToDoRequest):
    todo_to_insert = ToDos(**todo_request.model_dump())
    db.add(todo_to_insert)
    db.commit()

@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_id: int, todo_request: ToDoRequest):
    todo_to_update: ToDos = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if not todo_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    todo_to_update.title = todo_request.title
    todo_to_update.description = todo_request.description
    todo_to_update.priority = todo_request.priority
    todo_to_update.completed = todo_request.completed

    db.add(todo_to_update)
    db.commit()
