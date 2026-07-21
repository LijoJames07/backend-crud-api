from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Task API")

# This defines what a "Task" data object must look like
class Task(BaseModel):
    id: int
    title: str
    done: bool
tasks_db: List[Task] = [
    Task(id=1, title="Learn FastAPI basics", done=True),
    Task(id=2, title="Build a CRUD API", done=False),
    Task(id=3, title="Push code to GitHub", done=False),
]
id_counter = 3 
@app.get("/")
def get_root():
    return {"name": "Task API", "version": "1.0"}
@app.get("/health")
def get_health():
    return {"status": "ok"}
@app.get("/tasks")
def get_all_tasks():
    return tasks_db
@app.get("/tasks/{id}")
def get_single_task(id: int):
    for task in tasks_db:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")

class CreateTaskPayload(BaseModel):
    title: str

@app.post("/tasks", status_code=201)
def create_task(payload: CreateTaskPayload):
    global id_counter
    # Validation: If the user provides an empty string or spaces, error out
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    id_counter += 1
    new_task = Task(id=id_counter, title=payload.title, done=False)
    tasks_db.append(new_task)
    return new_task
class UpdateTaskPayload(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.put("/tasks/{id}")
def update_task(id: int, payload: UpdateTaskPayload):
    for task in tasks_db:
        if task.id == id:
            if payload.title is not None:
                if not payload.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task.title = payload.title
            if payload.done is not None:
                task.done = payload.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")
@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    global tasks_db
    for index, task in enumerate(tasks_db):
        if task.id == id:
            tasks_db.pop(index)
            return 
    raise HTTPException(status_code=404, detail=f"Task {id} not found")