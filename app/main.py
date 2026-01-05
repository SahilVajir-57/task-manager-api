from fastapi import FastAPI
from app.config import get_settings
from app.routers import auth, projects, tasks

settings = get_settings()

app = FastAPI(
    title="Task Manager API",
    description="A RESTful API for managing tasks and projects",
    version="1.0.0",
)

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "Task Manager API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}