from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import uvicorn
import pandas

# Database Connection
async def get_db():
    conn = await asyncpg.connect(user='user', password='password',
                                 database='database', host='127.0.0.1')
    return conn

app = FastAPI()

class TaskCreate(BaseModel):
    name: str
    urgency: str
    assigned_to: int

class UserCreate(BaseModel):
    name: str

@app.post("/tasks/")
async def create_task(task: TaskCreate):
    conn = await get_db()
    await conn.execute('''
        INSERT INTO tasks (name, urgency, assigned_to) VALUES ($1, $2, $3)
    ''', task.name, task.urgency, task.assigned_to)
    await conn.close()
    return {"status": "task created"}

@app.post("/users/")
async def create_user(user: UserCreate):
    conn = await get_db()
    await conn.execute('''
        INSERT INTO users (name) VALUES ($1)
    ''', user.name)
    await conn.close()
    return {"status": "user created"}

# Add more endpoints as needed
