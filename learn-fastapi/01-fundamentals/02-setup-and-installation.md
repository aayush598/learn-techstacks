# 02 - Setup and Installation

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Virtual Environments](#virtual-environments)
4. [Project Structure](#project-structure)
5. [Main.py Setup](#mainpy-setup)
6. [Running the Application](#running-the-application)
7. [IDE Setup](#ide-setup)
8. [Linting and Type Checking](#linting-and-type-checking)
9. [pyproject.toml Setup](#pyprojecttoml-setup)
10. [Docker Quickstart](#docker-quickstart)
11. [Interview Questions](#interview-questions)

---

## Prerequisites

### Python Version

FastAPI requires **Python 3.7+**, but **Python 3.10+** is strongly recommended for:

```python
# Python 3.9+ (built-in generics)
def get_items() -> list[str]:  # No need for List[str]
    return ["a", "b"]

# Python 3.10+ (Annotated syntax for cleaner type hints)
from typing import Annotated
from fastapi import Query

async def get_items(q: Annotated[str, Query(min_length=3)]):
    return {"q": q}
```

### Check Your Python Version

```bash
python --version
# or
python3 --version
```

---

## Installation Methods

### Basic pip Install

```bash
# Install FastAPI with all standard extras
pip install fastapi[all]

# Or install just the core (recommended for production)
pip install fastapi

# You also need an ASGI server
pip install uvicorn[standard]
```

> **Note:** `fastapi[all]` includes uvicorn, python-multipart, jinja2, and python-dotenv. For production, install only what you need.

### What Gets Installed

```bash
pip install fastapi
```

Core dependencies installed automatically:
- `starlette` - ASGI toolkit
- `pydantic` - Data validation
- `typing-extensions` - Backported typing features
- `anyio` - Async I/O abstraction

Optional extras you may need:
- `uvicorn[standard]` - ASGI server
- `python-multipart` - For form data and file uploads
- `python-jose[cryptography]` - For JWT tokens
- `passlib[bcrypt]` - For password hashing
- `httpx` - For async HTTP client (testing)

---

## Virtual Environments

Virtual environments isolate your project's dependencies from the system Python.

### Method 1: venv (Built-in)

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Verify you're in the venv
which python
# Should show: /path/to/.venv/bin/python

# Install dependencies
pip install fastapi uvicorn[standard]

# Save dependencies
pip freeze > requirements.txt

# Deactivate when done
deactivate
```

### Method 2: Poetry

```bash
# Install poetry
pip install poetry

# Create a new project
poetry new my-fastapi-project
cd my-fastapi-project

# Or add to existing project
poetry init

# Add dependencies
poetry add fastapi
poetry add --group dev uvicorn[standard]
poetry add --group dev ruff mypy

# Run the application
poetry run uvicorn main:app --reload

# Export requirements.txt (if needed)
poetry export -f requirements.txt --output requirements.txt
```

### Method 3: pdm

```bash
# Install pdm
pip install pdm

# Create a new project
pdm init

# Add dependencies
pdm add fastapi
pdm add -d uvicorn[standard]
pdm add -d ruff mypy

# Run the application
pdm run uvicorn main:app --reload
```

### Method 4: uv (Recommended - Fastest)

```bash
# Install uv
pip install uv

# Create a new project with uv
uv init my-fastapi-project
cd my-fastapi-project

# Add dependencies (blazingly fast)
uv add fastapi uvicorn[standard]

# Run the application
uv run uvicorn main:app --reload

# uv is 10-100x faster than pip for dependency resolution
```

### Comparison Table

| Tool | Speed | Lock File | Script Runner | Recommended For |
|------|-------|-----------|---------------|-----------------|
| venv | Slow | No | No | Simple projects |
| Poetry | Medium | poetry.lock | `poetry run` | Medium projects |
| pdm | Medium | pdm.lock | `pdm run` | Medium projects |
| uv | Very fast | uv.lock | `uv run` | All projects |

---

## Project Structure

### Flat Structure (Small Projects)

```
my-api/
├── .venv/
├── main.py
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Layered Structure (Medium Projects)

```
my-api/
├── .venv/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   └── item_repo.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── pyproject.toml
├── Dockerfile
└── .gitignore
```

### Domain-Driven Structure (Large Projects)

```
my-api/
├── .venv/
├── src/
│   └── my_api/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── dependencies.py
│       ├── domains/
│       │   ├── __init__.py
│       │   ├── user/
│       │   │   ├── __init__.py
│       │   │   ├── models.py
│       │   │   ├── schemas.py
│       │   │   ├── router.py
│       │   │   ├── service.py
│       │   │   └── repository.py
│       │   └── item/
│       │       ├── __init__.py
│       │       ├── models.py
│       │       ├── schemas.py
│       │       ├── router.py
│       │       ├── service.py
│       │       └── repository.py
│       ├── shared/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   ├── exceptions.py
│       │   └── middleware.py
│       └── core/
│           ├── __init__.py
│           ├── security.py
│           └── events.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .github/
    └── workflows/
        └── ci.yml
```

### Which Structure to Choose?

| Project Size | Structure | When to Use |
|-------------|-----------|-------------|
| 1-5 endpoints | Flat | Learning, prototypes, small tools |
| 5-20 endpoints | Layered | Most web APIs, small teams |
| 20+ endpoints | Domain-driven | Large teams, complex domains |
| Microservices | Flat or Domain | Depends on service size |

---

## Main.py Setup

### Minimal Setup

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Production Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create DB connection pool, cache, etc.
    print("Starting up...")
    yield
    # Shutdown: close DB connection pool, cleanup, etc.
    print("Shutting down...")

app = FastAPI(
    title="My API",
    description="A production-ready FastAPI application",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.routers import users, items
app.include_router(users.router)
app.include_router(items.router)
```

### Application Factory Pattern

```python
# app/main.py
from fastapi import FastAPI

def create_app() -> FastAPI:
    application = FastAPI(title="My API")
    
    # Add middleware
    # Include routers
    # Set up event handlers
    
    return application

app = create_app()
```

### Config with pydantic-settings

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "My API"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str = "change-me-in-production"
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Running the Application

### Development Mode

```bash
# Basic run
uvicorn main:app --reload

# With host and port
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# With log level
uvicorn main:app --reload --log-level info

# With specific app module path
uvicorn app.main:app --reload

# Using the --app-dir flag for custom paths
uvicorn main:app --reload --app-dir src
```

### The `--reload` Flag

The `--reload` flag watches for file changes and automatically restarts the server. **Never use this in production.**

```bash
# This watches ALL files in the current directory
uvicorn main:app --reload

# Watch specific directories
uvicorn main:app --reload --reload-dir app
uvicorn main:app --reload --reload-dir app --reload-dir lib
```

### Production Mode

```bash
# Single worker (simple production)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Using gunicorn with uvicorn workers (recommended)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# With access logging
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --access-logfile -

# With timeout
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --timeout 120
```

### Using FastAPI CLI

```bash
# Install FastAPI CLI
pip install fastapi-cli

# Run the application
fastapi dev main.py          # Development mode (with --reload)
fastapi run main.py          # Production mode

# Specify host and port
fastapi run main.py --host 0.0.0.0 --port 8000
```

### Production Worker Count

```bash
# Rule of thumb: (2 x CPU cores) + 1
# For a 4-core server:
gunicorn main:app -w 9 -k uvicorn.workers.UvicornWorker

# For async apps with many I/O operations:
# You can use more workers since they're lightweight
gunicorn main:app -w 16 -k uvicorn.workers.UvicornWorker
```

### Environment Variables

```bash
# Set environment variables
export APP_ENV=production
export DEBUG=false
export DATABASE_URL=postgresql://user:pass@localhost/db

# Or use a .env file with python-dotenv
# (FastAPI loads .env automatically with python-dotenv installed)
```

---

## IDE Setup

### VS Code Setup

1. Install the **Python** extension
2. Install **Pylance** (included with Python extension)
3. Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.diagnosticMode": "workspace",
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
        }
    }
}
```

4. Recommended VS Code extensions:

```
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Ruff (charliermarsh.ruff)
- FastAPI Snippets (nicktraz.fastapi-snippets)
- Python Indent (KevinRose.vsc-python-indent)
```

### PyCharm Setup

1. Install the **FastAPI** plugin from JetBrains Marketplace
2. Configure the Python interpreter to use your virtual environment
3. Enable type hints inspection

---

## Linting and Type Checking

### Ruff (Recommended Linter + Formatter)

Ruff is a fast Python linter written in Rust. It replaces flake8, isort, black, and many more.

```bash
# Install
pip install ruff

# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Check with specific rules
ruff check --select E,F,W,I -- .
```

Configuration in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py310"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM", "TCH"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["app"]
```

### mypy (Type Checker)

```bash
# Install
pip install mypy

# Run type checking
mypy .

# Run on specific files
mypy app/main.py

# Strict mode
mypy --strict .
```

Configuration in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [fastapi, pydantic]
```

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## pyproject.toml Setup

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-fastapi-project"
version = "1.0.0"
description = "A FastAPI project"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
authors = [
    { name = "Your Name", email = "you@example.com" }
]
dependencies = [
    "fastapi>=0.115.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "uvicorn[standard]>=0.30.0",
    "python-multipart>=0.0.9",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.4.0",
    "mypy>=1.10.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.27.0",
    "pre-commit>=3.7.0",
]

[tool.ruff]
target-version = "py310"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM"]

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

---

## Docker Quickstart

### Dockerfile

```dockerfile
# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/mydb
      - DEBUG=false
    depends_on:
      - db
    volumes:
      - .:/app  # For development only
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload  # Dev mode

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Running with Docker

```bash
# Build and run
docker compose up --build

# Run in background
docker compose up --build -d

# Stop
docker compose down

# View logs
docker compose logs -f api
```

### .dockerignore

```
__pycache__
*.pyc
.venv
.git
.env
.pytest_cache
.mypy_cache
.ruff_cache
*.md
tests/
```

---

## Interview Questions

### Q1: What is the recommended way to install FastAPI for a new project?

**Answer:** Use `uv` (fastest) or `poetry` for dependency management:

```bash
# Using uv
uv init my-project && cd my-project
uv add fastapi uvicorn[standard]

# Using poetry
poetry new my-project && cd my-project
poetry add fastapi
poetry add --group dev uvicorn[standard]
```

Always use a virtual environment, never install packages system-wide.

### Q2: What is the difference between `--reload` in development and production mode?

**Answer:** `--reload` watches for file changes and automatically restarts the server. It adds overhead and should never be used in production. In production, use `gunicorn` with `uvicorn` workers for process management, automatic restarts on crashes, and worker scaling.

### Q3: How many workers should you run in production?

**Answer:** The general rule is `(2 × number of CPU cores) + 1`. For CPU-bound apps, stick to this. For I/O-bound async apps, you can use more workers since async coroutines are lightweight. Monitor your server's resource usage and adjust accordingly.

### Q4: What's the difference between `pip install fastapi[all]` and `pip install fastapi`?

**Answer:** `fastapi[all]` installs all optional dependencies (uvicorn, python-multipart, jinja2, python-dotenv). `fastapi` installs only the core dependencies (starlette, pydantic). For production, install only what you need to minimize the attack surface and image size.

### Q5: Why would you use a layered project structure instead of putting everything in one file?

**Answer:** Separation of concerns: routers handle HTTP, services handle business logic, repositories handle data access. This makes code testable (mock at any layer), maintainable (changes in one layer don't affect others), and scalable (teams can work on different layers independently).

### Q6: What does `uvicorn main:app` mean?

**Answer:** `main` is the Python module (main.py), and `app` is the variable name of the FastAPI instance within that module. So `main:app` tells uvicorn to import `app` from the `main` module. This is Python's module:attribute notation used for ASGI application discovery.
