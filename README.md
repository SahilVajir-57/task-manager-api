# Task Manager API

A RESTful API for managing tasks and projects, built with FastAPI and PostgreSQL.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Projects Management**: Create, read, update, delete projects
- **Tasks Management**: Full CRUD with filtering, sorting, and pagination
- **API Documentation**: Interactive Swagger UI and ReDoc

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (async)
- **Authentication**: JWT (python-jose)
- **Validation**: Pydantic
- **Testing**: pytest
- **Containerization**: Docker

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/task-manager-api.git
cd task-manager-api
```

2. Create environment file:

```bash
cp .env.example .env
```

3. Start the application:

```bash
docker-compose up --build
```

4. Access the API:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint         | Description             |
| ------ | ---------------- | ----------------------- |
| POST   | `/auth/register` | Register a new user     |
| POST   | `/auth/login`    | Login and get JWT token |
| GET    | `/auth/me`       | Get current user info   |

### Projects

| Method | Endpoint         | Description                   |
| ------ | ---------------- | ----------------------------- |
| POST   | `/projects`      | Create a project              |
| GET    | `/projects`      | List all projects (paginated) |
| GET    | `/projects/{id}` | Get a project                 |
| PUT    | `/projects/{id}` | Update a project              |
| DELETE | `/projects/{id}` | Delete a project              |

### Tasks

| Method | Endpoint                         | Description                        |
| ------ | -------------------------------- | ---------------------------------- |
| POST   | `/projects/{id}/tasks`           | Create a task                      |
| GET    | `/projects/{id}/tasks`           | List tasks (filterable, paginated) |
| GET    | `/projects/{id}/tasks/{task_id}` | Get a task                         |
| PUT    | `/projects/{id}/tasks/{task_id}` | Update a task                      |
| DELETE | `/projects/{id}/tasks/{task_id}` | Delete a task                      |

## Query Parameters

### Pagination (all list endpoints)

- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)

### Task Filtering

- `status`: Filter by status (`todo`, `in_progress`, `done`)
- `priority`: Filter by priority (`low`, `medium`, `high`)
- `sort_by`: Sort field (`created_at`, `due_date`, `priority`)
- `order`: Sort order (`asc`, `desc`)

## Example Usage

### Register a user

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "full_name": "John Doe"}'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

### Create a project

```bash
curl -X POST http://localhost:8000/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "description": "Project description"}'
```

### Create a task

```bash
curl -X POST http://localhost:8000/projects/PROJECT_ID/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "priority": "high", "status": "todo"}'
```

## Running Tests

```bash
docker-compose exec web pytest -v
```

## Project Structure

```
task-manager-api/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── routers/         # API endpoints
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── utils/           # Utilities
│   ├── config.py        # Settings
│   ├── database.py      # Database setup
│   ├── dependencies.py  # FastAPI dependencies
│   ├── exceptions.py    # Exception handlers
│   └── main.py          # Application entry
├── tests/               # Test files
├── alembic/             # Database migrations
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Environment Variables

| Variable                      | Description                  | Default |
| ----------------------------- | ---------------------------- | ------- |
| `DATABASE_URL`                | PostgreSQL connection string | -       |
| `SECRET_KEY`                  | JWT secret key               | -       |
| `ALGORITHM`                   | JWT algorithm                | HS256   |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration             | 30      |
