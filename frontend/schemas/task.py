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



