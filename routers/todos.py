from fastapi import APIRouter, Depends, Path, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from source.database import get_db
from source.models import ToDos

router = APIRouter(prefix="/todos", tags=["ToDos"])

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: Session = Depends(get_db)):
    todos = db.query(ToDos).all()
    return todos

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    todo = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
