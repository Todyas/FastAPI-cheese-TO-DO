from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Модель задачи


class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


# Хранилище задач (в памяти)
tasks: List[Task] = []

# Получение всех задач


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# Добавление новой задачи


@app.post("/tasks", response_model=Task)
def add_task(task: Task):
    # Проверяем, есть ли задача с таким же id
    if any(t.id == task.id for t in tasks):
        raise HTTPException(
            status_code=400, detail="Task with this ID already exists")
    tasks.append(task)
    return task

# Обновление существующей задачи


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# Удаление задачи


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
