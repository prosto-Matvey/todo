from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None