# schemas/TaskSchema.py
from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    is_completed: bool = False

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None