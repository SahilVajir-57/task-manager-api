from fastapi import FastAPI
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Task Manager API",
    description="A RESTful API for managing tasks and projects",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Task Manager API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}