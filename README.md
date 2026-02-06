# FastAPI Lab

A production-ready FastAPI project template with comprehensive testing, Docker support, CI/CD pipeline, structured logging, and modern development practices.

## ✨ Features

### Core Framework
- **FastAPI** - Modern, fast Python web framework with automatic API documentation
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server
- **Structured Logging** - JSON logging with correlation IDs using Loguru
- **Exception Handling** - Centralized error handling with custom handlers

### Development Tools
- **UV** - Ultra-fast Python package manager (10-100x faster than pip)
- **Task** - Task runner for common operations
- **Ruff** - Extremely fast Python linter and formatter
- **MyPy** - Static type checking
- **Pre-commit hooks** - Automated code quality checks
- **Invoke** - Python task automation framework

### Testing Stack
- **pytest** - Modern testing framework
- **pytest-describe** - BDD-style testing (RSpec-like syntax)
- **pytest-sugar** - Beautiful test output with progress bars
- **pytest-xdist** - Parallel test execution
- **pytest-cov** - Code coverage reporting (80% minimum)
- **pytest-asyncio** - Async test support
- **httpx** - Modern HTTP client for API testing

### Infrastructure
- **Docker** - Multi-stage containerization with non-root user
- **Docker Compose** - Local development environment
- **PostgreSQL** - Primary database (ready to integrate)
- **Redis** - Caching and sessions (ready to integrate)
- **GitHub Actions** - Complete CI/CD pipeline

### API Features
- **Versioning** - URL-based API versioning (`/v1/`)
- **Authentication** - API key authentication (extensible to JWT/OAuth2)
- **Middleware** - Request logging, correlation IDs, custom error handling
- **Auto-generated docs** - OpenAPI/Swagger UI and ReDoc
- **Hot reload** - Automatic server restart on code changes

### Automation Models (NEW!)
- **Webhook Inbox** - Universal webhook receiver for testing integrations
- **Scheduled Tasks** - Task scheduling with execution tracking
- **Workflows** - Multi-step automation pipelines
- **API Logs** - Request/response logging and analytics
- **SQLModel** - Modern ORM combining SQLAlchemy + Pydantic

## 🚀 Quick Start

### Prerequisites

- Python 3.14+
- [UV](https://docs.astral.sh/uv/) - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Task](https://taskfile.dev/) - Install with: `brew install go-task` (macOS) or `snap install task` (Linux)
- Docker & Docker Compose (optional)

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd fastapi_lab

# 2. Install dependencies
task install

# 3. Set up environment
cp .env.example .env
# Edit .env with your settings (API_KEY, DATABASE_URL, etc.)

# 4. Install pre-commit hooks (optional but recommended)
uv run pre-commit install

# 5. Run the application
task dev

# 6. Open your browser
open http://localhost:8000/docs
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🤖 Automation Models

This project includes comprehensive automation models for testing typical automation tasks:

### Quick Setup
```bash
# Setup automation models (install deps, start DB, create tables)
./scripts/setup_automation.sh

# Test the endpoints
./scripts/test_automation.sh
```

### Available Models

#### 🪝 Webhook Inbox
Universal webhook receiver for testing integrations.

```bash
# Receive a webhook
curl -X POST http://localhost:8000/v1/webhooks/inbox/github \
  -H "Content-Type: application/json" \
  -d '{"event": "push", "repo": "my-repo"}'

# List webhooks
curl http://localhost:8000/v1/webhooks/inbox
```

**Use cases**: Testing webhooks, debugging payloads, building webhook-triggered automations

#### ⏰ Scheduled Tasks
Task scheduling system with execution tracking.

```bash
# Create a task
curl -X POST http://localhost:8000/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daily Backup",
    "task_type": "cron",
    "schedule": "0 2 * * *",
    "enabled": true,
    "config": {}
  }'
```

**Use cases**: Cron-like scheduled jobs, recurring API calls, periodic data sync

#### 🔄 Workflows
Multi-step automation pipelines with step execution.

```bash
# Create a workflow
curl -X POST http://localhost:8000/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "User Onboarding",
    "trigger_type": "webhook",
    "steps": [
      {"type": "email", "config": {"template": "welcome"}},
      {"type": "api_call", "config": {"url": "https://api.example.com/setup"}}
    ]
  }'
```

**Use cases**: Complex automation pipelines, event-driven workflows, integration orchestration

#### 📊 API Logs
Request/response logging and analytics.

```bash
# Get API statistics
curl http://localhost:8000/v1/api-logs/stats/summary

# List recent logs
curl http://localhost:8000/v1/api-logs
```

**Use cases**: API monitoring, performance analysis, audit trails

📖 **Full documentation**: See [AUTOMATION_SUMMARY.md](./AUTOMATION_SUMMARY.md) and [docs/AUTOMATION_MODELS.md](./docs/AUTOMATION_MODELS.md)

## 📁 Project Structure

```
fastapi_lab/
├── src/                    # Application source code
│   ├── api/               # API endpoints
│   │   └── v1/           # API version 1
│   │       ├── health.py  # Health check endpoint
│   │       ├── items.py   # Example items endpoints
│   │       ├── examples.py # Example endpoints for testing
│   │       ├── webhooks.py # Webhook inbox endpoints
│   │       ├── tasks.py   # Scheduled tasks endpoints
│   │       ├── workflows.py # Workflow automation endpoints
│   │       ├── api_logs.py # API logging endpoints
│   │       └── router.py  # Main API router
│   ├── core/             # Core functionality
│   │   ├── auth.py       # Authentication (API key)
│   │   ├── config.py     # Configuration management
│   │   ├── logging.py    # Structured logging setup
│   │   └── exception_handlers.py # Global exception handlers
│   ├── db/               # Database configuration
│   │   └── base.py       # SQLModel setup & session management
│   ├── models/           # SQLModel models (ORM + schemas)
│   │   ├── webhook.py    # Webhook inbox models
│   │   ├── task.py       # Task scheduling models
│   │   ├── workflow.py   # Workflow automation models
│   │   └── api_log.py    # API logging models
│   ├── middleware/       # Custom middleware
│   │   ├── correlation.py # Correlation ID tracking
│   │   └── request_logging.py # Request/response logging
│   └── services/         # Business logic
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── conftest.py      # Pytest configuration & fixtures
├── docs/                 # Documentation
│   ├── DESIGN.md        # Architecture & API conventions
│   └── CONTRIBUTING.md  # Development & testing guide
├── tasks/                # Invoke automation tasks
│   ├── routes.py        # Route management tasks
│   └── openapi.py       # OpenAPI schema tasks
├── scripts/              # Utility scripts
├── .github/              # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml       # CI/CD pipeline
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Container orchestration
├── main.py              # Application entry point
├── pyproject.toml       # Project configuration
├── Taskfile.yml         # Task runner configuration
└── .pre-commit-config.yaml # Pre-commit hooks
```

## 🛠️ Development

### Running the Application

#### Local Development (Recommended)

```bash
# Run with hot reload (development mode)
task dev

# Or run without hot reload
task run

# Or use uvicorn directly
uv run uvicorn main:app --reload
```

#### With Docker

```bash
# Start all services (app, postgres, redis)
docker compose up -d

# Development mode with additional tools
# Includes: pgAdmin, Redis Commander, MailHog
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d

# View logs
docker compose logs -f app

# Stop services
docker compose down

# Open shell in running container (requires services to be up)
task docker-shell        # or task dsh

# Open Python console in running container (requires services to be up)
task docker-console      # or task dc

# OR create standalone containers (doesn't require services to be up)
task docker-shell-standalone
task docker-console-standalone
```

**Note:** Docker services use non-conflicting ports to work alongside local services:
- **Postgres**: Host port 5433 → Container port 5432 (local Postgres usually uses 5432)
- **Redis**: Host port 6380 → Container port 6379 (local Redis usually uses 6379)
- App containers communicate with Postgres/Redis via Docker's internal network

Development services:
- **pgAdmin**: http://localhost:5050
- **Redis Commander**: http://localhost:8081
- **MailHog**: http://localhost:8025

### Interactive Python Console

Like Rails console, you can open an interactive Python REPL with your FastAPI app loaded:

```bash
# Local console (uses uv) - runs without Docker
task console  # or task c

# Docker console (runs in container)
task docker-console  # or task dc
```

The console loads your FastAPI app, settings, logger, and other commonly used objects:

```python
>>> app.routes  # Access all routes
>>> settings.app_name  # Get configuration
>>> logger.info("Test message")  # Use the logger
>>> [route.path for route in app.routes]  # List all route paths
```

This is perfect for:
- Testing API endpoints without starting the server
- Debugging application logic
- Exploring the app structure
- Running one-off scripts or database operations

### Common Tasks

```bash
# Show all available tasks
task --list

# Development
task dev                 # Run with hot reload
task run                 # Run normally
task console             # Open local Python REPL with app loaded (like Rails console)
task c                   # Alias for console

# Docker (fast - no database/redis startup)
task docker-shell        # Open shell in app container (alias: dsh)
task docker-console      # Open Python console in app container (alias: dc)

# Docker with services (if you need database/redis access)
task docker-shell-full   # Open shell with postgres/redis running
task docker-console-full # Open console with postgres/redis running

# Testing
task test                # Run all tests
task test-cov            # Run tests with coverage
task test-parallel       # Run tests in parallel (faster!)
task test-watch          # Run tests in watch mode

# Code Quality
task lint                # Check linting
task lint-fix            # Fix linting issues
task format              # Format code
task check               # Run all checks (lint + format + test)

# API Management
task route-list          # List all API routes
task route-create -- --name=users  # Create new route
task openapi-export      # Export OpenAPI schema to JSON

# Cleanup
task clean               # Remove generated files
```

## 🧪 Testing

We use pytest with BDD-style testing (RSpec-like syntax):

```bash
# Run all tests
task test

# Run with coverage report
task test-cov

# Run tests in parallel (much faster!)
task test-parallel

# Run specific test types
task test-unit           # Unit tests only
task test-integration    # Integration tests only

# Watch mode (auto-rerun on file changes)
task test-watch

# Fast fail mode (stop on first failure)
task test-fast

# Debug mode
task test-debug
```

### Writing Tests

We use `pytest-describe` for BDD-style testing:

```python
# tests/test_example.py

def describe_user_api():
    """Test suite for user API."""

    def describe_get_users():
        """Tests for GET /users endpoint."""

        def it_returns_list_of_users(client):
            """Should return a list of users."""
            response = client.get("/v1/users")
            assert response.status_code == 200
            assert isinstance(response.json(), list)

        def it_filters_by_query_params(client):
            """Should filter users by query parameters."""
            response = client.get("/v1/users?is_active=true")
            assert response.status_code == 200
```

Coverage requirements:
- Minimum 80% code coverage enforced
- HTML coverage report generated in `htmlcov/`
- Coverage shown in terminal output

## 🔧 Code Quality

### Pre-commit Hooks

Automatically run on every commit:

```bash
# Install hooks
uv run pre-commit install

# Run manually on all files
uv run pre-commit run --all-files

# Update hooks to latest versions
uv run pre-commit autoupdate
```

Pre-commit checks:
- ✅ Ruff linting and formatting
- ✅ MyPy type checking
- ✅ Bandit security checks
- ✅ YAML/JSON/TOML validation
- ✅ Trailing whitespace removal
- ✅ Private key detection
- ✅ Dockerfile linting

### Manual Code Quality Checks

```bash
# Linting
task lint                # Check with Ruff
task lint-fix            # Auto-fix issues

# Formatting
task format              # Format with Ruff
task format-check        # Check formatting

# Type checking
uv run mypy .            # Type check with MyPy

# Run all checks
task check               # Lint + format + test
```

## 🐳 Docker

### Build and Run

```bash
# Build production image
docker build -t fastapi-lab:latest .

# Run container
docker run -p 8000:8000 --env-file .env fastapi-lab:latest

# Using docker-compose
docker-compose up -d
```

### Multi-stage Build

Our Dockerfile uses multi-stage builds for:
- Smaller final image size
- Security (non-root user)
- Separate build and runtime dependencies
- Health check support

## 🔐 Authentication

### API Key Authentication

Include API key in request header:

```bash
# Using curl
curl -H "X-API-Key: your-api-key" http://localhost:8000/v1/items

# Using httpie
http GET localhost:8000/v1/items X-API-Key:your-api-key
```

Set your API key in `.env`:

```bash
API_KEY=your-secure-api-key
```

**Note**: The project is designed to be easily extended to JWT, OAuth2, or other authentication methods.

## 🌐 API Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/docs (interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (beautiful API documentation)
- **OpenAPI JSON**: http://localhost:8000/openapi.json (raw schema)

Export OpenAPI schema:

```bash
task openapi-export
# Output: docs/openapi.json
```

## 🚢 CI/CD

GitHub Actions workflow automatically runs on push/PR:

1. ✅ Dependency installation (with UV)
2. ✅ Linting (Ruff)
3. ✅ Formatting check (Ruff)
4. ✅ Type checking (MyPy)
5. ✅ Tests with coverage (pytest)
6. ✅ Docker image build

See `.github/workflows/ci.yml` for details.

## 📊 Logging & Observability

### Structured Logging

We use Loguru for structured logging:

```python
from src.core.logging import get_logger

logger = get_logger()

logger.info("Processing request", user_id=123, action="create")
logger.error("Failed to connect to database", error=str(e))
```

Features:
- JSON format in production
- Pretty format in development
- Correlation IDs for request tracking
- Context variables for request-specific data
- Automatic request/response logging via middleware

### Correlation IDs

Every request gets a unique correlation ID:
- Automatically generated or from `X-Correlation-ID` header
- Propagated through all log messages
- Useful for distributed tracing and debugging

## ⚙️ Configuration

Configuration is managed via Pydantic Settings:

```python
# src/core/config.py
class Settings(BaseSettings):
    app_name: str = "fastapi_lab"
    environment: str = "development"
    api_key: str
    # ... more settings
```

Environment variables (`.env`):

```bash
APP_NAME=fastapi_lab
ENVIRONMENT=development
API_KEY=your-api-key

# Database (Docker uses 5433 on host, 5432 internally)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5433/db

# Redis (Docker uses 6380 on host, 6379 internally)
REDIS_URL=redis://localhost:6380/0
```

## 📚 Documentation

- **[DESIGN.md](docs/DESIGN.md)** - Architecture, API conventions, and design principles
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Development guide, testing, and workflows

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for:
- Development setup
- Coding standards
- Testing guidelines
- Git workflow
- Pull request process

### Quick Contributing Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`task check`)
5. Commit with conventional commits (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add tests for auth module
refactor: simplify config loading
chore: update dependencies
```

## 🛣️ Roadmap

### Planned Features

- [ ] Database integration (PostgreSQL with SQLAlchemy + Alembic)
- [ ] JWT authentication
- [ ] User management endpoints
- [ ] WebSocket support for real-time features
- [ ] Background job processing (Celery/ARQ)
- [ ] Rate limiting
- [ ] Caching with Redis
- [ ] Metrics and monitoring (Prometheus)
- [ ] Distributed tracing (OpenTelemetry)
- [ ] API documentation versioning
- [ ] GraphQL endpoint

## 🐛 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure PYTHONPATH includes src/
export PYTHONPATH="${PYTHONPATH}:./src"

# Or use task commands (they set PYTHONPATH automatically)
task dev
```

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

#### Pre-commit Hook Failures
```bash
# Fix formatting issues
task format

# Fix linting issues
task lint-fix

# Run all checks
task check

# Then commit again
git add .
git commit -m "your message"
```

For more troubleshooting tips, see [CONTRIBUTING.md](docs/CONTRIBUTING.md#troubleshooting).

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [UV](https://docs.astral.sh/uv/) - Fast Python package manager
- [Ruff](https://docs.astral.sh/ruff/) - Fast Python linter and formatter
- [Task](https://taskfile.dev/) - Task runner
- [Loguru](https://github.com/Delgan/loguru) - Python logging made simple

## 📞 Support

- 📖 Check the [documentation](docs/)
- 🐛 Report issues on [GitHub Issues](../../issues)
- 💬 Ask questions in [GitHub Discussions](../../discussions)

---

**Made with ❤️ using FastAPI and modern Python tools**

**Happy coding!** 🚀
