# Contributing Guide

Welcome to the FastAPI Lab project! This guide will help you set up your development environment and contribute to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Creating New Features](#creating-new-features)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Git Workflow](#git-workflow)
- [Debugging](#debugging)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Python 3.13+
- [UV](https://docs.astral.sh/uv/) - Fast Python package manager
- [Task](https://taskfile.dev/) - Task runner
- Docker & Docker Compose (optional, for local services)

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi_lab
   ```

2. **Install dependencies**
   ```bash
   task install
   # or
   uv sync --extra test
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Install pre-commit hooks**
   ```bash
   uv run pre-commit install
   ```

### Running the Application

#### Local Development (without Docker)

```bash
# Run with hot reload
task dev
# or
uv run uvicorn main:app --reload

# Access the app
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

#### With Docker Compose

```bash
# Start all services (app, postgres, redis)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

#### Development Mode with Docker

```bash
# Uses docker-compose.override.yml automatically
docker-compose up

# Includes: pgAdmin, Redis Commander, MailHog
# - pgAdmin: http://localhost:5050
# - Redis Commander: http://localhost:8081
# - MailHog: http://localhost:8025
```

## Development Workflow

### 1. Create a New Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Write Code

Follow the project conventions:
- Keep functions small and focused
- Write docstrings for public functions
- Use type hints everywhere
- Follow REST conventions for APIs

### 3. Run Tests

```bash
# Run all tests
task test

# Run with coverage
task test-cov

# Run specific tests
uv run pytest tests/unit/test_auth.py

# Run in watch mode
task test-watch
```

### 4. Lint and Format

```bash
# Check linting
task lint

# Auto-fix linting issues
task lint-fix

# Format code
task format

# Run all checks
task check
```

### 5. Commit Changes

```bash
# Stage changes
git add .

# Commit (pre-commit hooks will run automatically)
git commit -m "feat: add user authentication"

# If pre-commit fails, fix issues and try again
git add .
git commit -m "feat: add user authentication"
```

### 6. Push and Create PR

```bash
git push origin feature/my-new-feature
# Create PR on GitHub
```

## Creating New Features

### Creating API Endpoints

#### Manual Method

1. **Create the schema** (`src/schemas/user.py`)
   ```python
   from pydantic import BaseModel, Field
   
   class UserCreate(BaseModel):
       email: str
       username: str = Field(..., min_length=3)
   
   class UserResponse(BaseModel):
       id: int
       email: str
       username: str
   ```

2. **Create the endpoint** (`src/api/v1/users.py`)
   ```python
   from fastapi import APIRouter, Depends
   from src.core.auth import require_api_key
   
   router = APIRouter()
   
   @router.post("/users", dependencies=[Depends(require_api_key)])
   def create_user(user: UserCreate):
       return {"message": "User created"}
   ```

3. **Register the router** (`src/api/v1/router.py`)
   ```python
   from src.api.v1 import users
   
   api_router.include_router(users.router, tags=["users"])
   ```

#### Using Invoke (Automated)

```bash
# Create a basic route
task route-create -- --name=users

# Create a route with authentication
task route-create -- --name=posts --auth
```

### Task Commands

#### Running the App
```bash
task run          # Run the app
task dev          # Run with hot reload
```

#### Testing
```bash
task test                # Run all tests
task test-cov            # Run tests with coverage
task test-parallel       # Run tests in parallel
task test-unit           # Run only unit tests
task test-integration    # Run only integration tests
task test-watch          # Run tests in watch mode
task test-fast           # Fast fail mode
task test-debug          # Run with debugger
```

#### Code Quality
```bash
task lint                # Check linting
task lint-fix            # Fix linting issues
task format              # Format code
task format-check        # Check formatting
task check               # Run all checks
```

#### Invoke Tasks
```bash
task inv-list            # List invoke tasks
task route-list          # List API routes
task route-create -- --name=users  # Create new route
task openapi-export      # Export OpenAPI schema
```

#### Cleanup
```bash
task clean               # Remove generated files
```

## Testing

### RSpec-Style Testing with pytest-describe

We use `pytest-describe` for BDD-style testing.

#### Basic Test Structure

```python
def describe_endpoint():
    """Top-level describe block."""
    
    def it_does_something(client):
        """Test case with descriptive name."""
        # Arrange
        data = {"key": "value"}
        
        # Act
        response = client.post("/endpoint", json=data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["key"] == "value"
```

#### Testing FastAPI Endpoints

```python
def describe_items_api():
    
    def describe_get_items():
        """GET /items tests."""
        
        def it_returns_list_of_items(client):
            response = client.get("/items")
            assert response.status_code == 200
            assert isinstance(response.json(), list)
        
        def it_filters_by_query_parameter(client):
            response = client.get("/items?category=electronics")
            assert response.status_code == 200
            items = response.json()
            assert all(item["category"] == "electronics" for item in items)
```

#### Fixtures

Define reusable fixtures in `tests/conftest.py`:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Test client for API requests."""
    return TestClient(app)

@pytest.fixture
def api_headers():
    """Headers with valid API key."""
    return {"X-API-Key": "test-api-key"}
```

#### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_main.py

# Run specific describe block
uv run pytest -k "describe_root"

# Run in parallel (faster!)
uv run pytest -n auto

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run only unit tests
uv run pytest -m unit

# Stop at first failure
uv run pytest -x
```

#### Test Best Practices

1. **Descriptive Names** - Use clear names that explain what the test does
2. **One Assertion Per Test** - When possible, focus on a single behavior
3. **Use Fixtures for Setup** - Reuse setup code with fixtures
4. **Test Edge Cases** - Cover boundary conditions
5. **Mark Slow Tests** - Use `@pytest.mark.slow` for long-running tests
6. **Group Related Tests** - Organize with nested describe blocks

## Code Quality

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Line length: 110 characters
- Use type hints
- Write docstrings for public functions
- Ruff handles formatting and linting

### Imports

```python
# Standard library
import os
from typing import Optional

# Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local
from src.core.config import settings
from src.api.v1 import router
```

### Naming Conventions

- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

### Pre-commit Hooks

Our pre-commit hooks automatically check:
- Ruff linting and formatting
- Type checking with mypy
- Security issues with bandit
- YAML/JSON/TOML validation
- Trailing whitespace
- File size limits
- Private key detection

## Git Workflow

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add tests for auth module
refactor: simplify config loading
chore: update dependencies
```

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

## Debugging

### VS Code / Cursor

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload", "--port", "8000"],
      "jinja": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      }
    }
  ]
}
```

### Python Debugger

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint()
breakpoint()
```

### Docker Logs

```bash
# View app logs
docker-compose logs -f app

# View all service logs
docker-compose logs -f

# View postgres logs
docker-compose logs postgres
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Make sure PYTHONPATH includes src/
export PYTHONPATH="${PYTHONPATH}:./src"

# Or use task commands which set this automatically
task run
```

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

#### Docker Issues
```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

#### Database Migrations
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
uv run alembic upgrade head
```

## Environment Variables

### Development (.env)

```bash
APP_NAME=fastapi_lab
ENVIRONMENT=development
API_KEY=dev-api-key

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_lab
REDIS_URL=redis://localhost:6379/0
```

### Production

Set environment variables through your deployment platform:
- Heroku: `heroku config:set API_KEY=xxx`
- Docker: Use `.env` file or `environment` in docker-compose
- Kubernetes: Use ConfigMaps and Secrets

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)
- [UV Documentation](https://docs.astral.sh/uv/)

## Getting Help

1. Check the documentation in `docs/`
2. Search existing issues on GitHub
3. Ask in team chat
4. Create a new issue with detailed description

---

**Happy coding!** 🚀
