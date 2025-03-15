from fastapi import FastAPI

from schemas.TaskSchema import Task, TaskUpdate
from schemas.UserSchema import User
from database import init_db
from repositories import task_repository, user_repository

app = FastAPI() 

init_db()

@app.get("/")
async def read_root():
    return {"message": "Добро пожаловать в FastAPI!"}

@app.post("/register")
async def register_user(user: User):
    return user_repository.register_user(user)

@app.get("/tasks")
async def get_tasks():
    return task_repository.get_all_tasks()

@app.post("/task")
async def create_task(task: Task):
    return task_repository.create_task(task)

@app.put("/task/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    return task_repository.update_task(task_id, task_update)

@app.delete("/task/{task_id}")
async def delete_task(task_id: int):
    return task_repository.delete_task(task_id)