from pydantic import BaseModel, Field

class ToDoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str
    priority: int = Field(gt=0, lt=3)
    completed: bool
