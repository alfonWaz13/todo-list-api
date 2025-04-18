from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from source.database import get_db
from source.models import ToDos

router = APIRouter(prefix="/todos", tags=["ToDos"])

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: Session = Depends(get_db)):
    todos = db.query(ToDos).all()
    return todos
