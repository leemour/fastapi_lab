# Design & Architecture

This document covers the system architecture, API design conventions, and best practices for the FastAPI Lab project.

## Table of Contents

- [Project Structure](#project-structure)
- [Design Principles](#design-principles)
- [Technology Stack](#technology-stack)
- [API Design Conventions](#api-design-conventions)
- [Database Strategy](#database-strategy)
- [Error Handling](#error-handling)
- [Logging & Observability](#logging--observability)
- [Security](#security)
- [Performance](#performance)

## Project Structure

```
fastapi_lab/
├── src/                    # Application source code
│   ├── api/               # API endpoints
│   │   └── v1/           # API version 1
│   │       ├── health.py  # Health check endpoint
│   │       ├── items.py   # Items endpoints
│   │       ├── examples.py # Example endpoints
│   │       └── router.py  # Main API router
│   ├── core/             # Core functionality
│   │   ├── auth.py       # Authentication & authorization
│   │   ├── config.py     # Configuration management
│   │   ├── logging.py    # Structured logging
│   │   └── exception_handlers.py # Global exception handlers
│   ├── middleware/       # Custom middleware
│   │   ├── correlation.py # Correlation ID tracking
│   │   └── request_logging.py # Request/response logging
│   ├── db/               # Database models & sessions
│   ├── models/           # Business models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── conftest.py      # Pytest configuration
├── docs/                 # Documentation
├── tasks/                # Invoke automation tasks
├── scripts/              # Utility scripts
├── main.py              # Application entry point
└── docker-compose.yml   # Container orchestration
```

## Design Principles

### 1. Separation of Concerns

- **API Layer** (`src/api/`): HTTP request/response handling
- **Business Logic** (`src/services/`): Core application logic
- **Data Layer** (`src/models/`, `src/db/`): Data persistence
- **Schemas** (`src/schemas/`): Data validation and serialization

### 2. Configuration Management

- Environment-based configuration using Pydantic Settings
- `.env` files for local development
- Environment variables for production
- Never commit secrets to version control

### 3. API Versioning

- URL-based versioning: `/v1/`, `/v2/`
- Allows backward compatibility
- Clear migration path for clients

### 4. Authentication & Authorization

- API Key authentication for service-to-service communication
- Easily extendable to JWT, OAuth2, etc.
- Centralized auth logic in `src/core/auth.py`

### 5. Middleware-Based Cross-Cutting Concerns

- Request logging via middleware
- Correlation ID tracking for distributed tracing
- Exception handling at application level

## Technology Stack

### Core Framework

- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation using Python type annotations

### Development Tools

- **UV**: Fast Python package manager
- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checker
- **Pytest**: Testing framework with pytest-describe for BDD-style tests

### Infrastructure

- **Docker**: Containerization
- **PostgreSQL**: Primary database (ready to integrate)
- **Redis**: Caching and sessions (ready to integrate)
- **GitHub Actions**: CI/CD pipeline

## API Design Conventions

### RESTful Design

Follow REST principles for API design:
- Use nouns for resources, not verbs
- Use HTTP methods appropriately
- Keep URLs hierarchical and logical
- Use plural names for collections

### URL Structure

```
/v{version}/{resource}[/{id}][/{sub-resource}]
```

Examples:
- `/v1/users` - Collection of users
- `/v1/users/123` - Specific user
- `/v1/users/123/posts` - User's posts

### HTTP Methods

#### GET - Retrieve Resources

```python
@router.get("/users")
async def get_users(skip: int = 0, limit: int = 100):
    """Get a list of users."""
    return await user_service.get_users(skip=skip, limit=limit)

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get a specific user by ID."""
    return await user_service.get_user(user_id)
```

#### POST - Create Resources

```python
@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user."""
    return await user_service.create_user(user)
```

#### PUT - Full Update

```python
@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    """Fully update a user."""
    return await user_service.update_user(user_id, user)
```

#### PATCH - Partial Update

```python
@router.patch("/users/{user_id}")
async def patch_user(user_id: int, user: UserPatch):
    """Partially update a user."""
    return await user_service.patch_user(user_id, user)
```

#### DELETE - Remove Resource

```python
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete a user."""
    await user_service.delete_user(user_id)
```

### Request/Response Format

#### Request Body

Use Pydantic models for validation:

```python
class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str | None = None
    is_active: bool = True
```

#### Success Response

```json
{
  "id": 123,
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### List Response (with pagination)

```json
{
  "items": [...],
  "total": 150,
  "skip": 0,
  "limit": 20,
  "has_more": true
}
```

#### Error Response

```json
{
  "detail": "User not found",
  "error_code": "USER_NOT_FOUND",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Query Parameters

#### Pagination

```python
@router.get("/users")
async def get_users(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max items to return")
):
    pass
```

#### Filtering & Sorting

```python
@router.get("/users")
async def get_users(
    is_active: bool | None = None,
    role: str | None = None,
    search: str | None = Query(None, min_length=1),
    sort_by: str = Query("created_at", regex="^(created_at|username|email)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$")
):
    pass
```

### Status Codes

#### Success (2xx)
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `202 Accepted` - Request accepted for async processing
- `204 No Content` - Successful DELETE

#### Client Errors (4xx)
- `400 Bad Request` - Invalid request format or data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Resource conflict
- `422 Unprocessable Entity` - Validation error
- `429 Too Many Requests` - Rate limit exceeded

#### Server Errors (5xx)
- `500 Internal Server Error` - Unexpected server error
- `502 Bad Gateway` - Invalid response from upstream
- `503 Service Unavailable` - Server temporarily unavailable

### API Versioning & Deprecation

When deprecating an endpoint:
1. Add deprecation warning in documentation
2. Include `Deprecation` header in response
3. Maintain for at least one major version
4. Provide migration guide

```python
@router.get("/old-endpoint", deprecated=True)
async def old_endpoint(response: Response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Sun, 01 Jan 2025 00:00:00 GMT"
    return {"message": "Use /v2/new-endpoint instead"}
```

### Documentation

Always document endpoints comprehensively:

```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information",
    response_description="The created user",
    tags=["users"]
)
async def create_user(user: UserCreate):
    """
    Create a new user with the following information:

    - **email**: A valid email address (required)
    - **username**: 3-50 characters (required)
    - **full_name**: User's full name (optional)
    - **is_active**: Whether the user is active (default: true)
    """
    pass
```

## Database Strategy

### Migrations (Coming Soon)

- Use Alembic for database migrations
- Version controlled migration scripts
- Separate migrations for schema changes and data migrations

### Connection Pooling

- Use asyncpg for PostgreSQL (async support)
- Configure appropriate pool sizes
- Connection health checks

## Error Handling

### Principles

- Catch exceptions at the appropriate level
- Log errors with context
- Return user-friendly error messages
- Never expose internal details in production

### Custom Exception Handlers

We have centralized exception handlers in `src/core/exception_handlers.py`:

```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": "HTTP_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

## Logging & Observability

### Structured Logging

We use `loguru` for structured logging with:
- JSON formatting in production
- Pretty formatting in development
- Correlation IDs for request tracking
- Context variables for request-specific data

### Log Levels

- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical failures

### Request Logging

Automatic request/response logging via middleware:
- Request method, path, query parameters
- Response status code and processing time
- User agent and client IP
- Correlation ID for distributed tracing

### Correlation IDs

Every request gets a unique correlation ID:
- Automatically generated or from header
- Propagated through all log messages
- Useful for distributed tracing

## Security

### Best Practices

1. **Input Validation**: Always validate user input using Pydantic
2. **SQL Injection**: Use parameterized queries (SQLAlchemy)
3. **Authentication**: Secure API keys, extendable to JWT
4. **HTTPS**: Always use HTTPS in production
5. **CORS**: Configure appropriate CORS policies
6. **Rate Limiting**: Implement for public APIs
7. **Secrets Management**: Use environment variables, never commit secrets

### Security Checks

Pre-commit hooks include:
- Bandit for security issue detection
- Private key detection
- Debug statement detection

### Dependencies

- Regular dependency updates
- Security scanning in CI/CD
- Pin dependency versions in production

## Performance

### Optimization Strategies

1. **Database Indexing**: Index frequently queried columns
2. **Query Optimization**: Use eager loading, avoid N+1 queries
3. **Caching**: Cache expensive computations and API responses
4. **Connection Pooling**: Reuse database connections
5. **Async Operations**: Use async/await for I/O operations

### Monitoring (Ready to Integrate)

- Response time tracking
- Error rate monitoring
- Resource utilization
- Database query performance

## Deployment

### Docker

Multi-stage builds for:
- Smaller images
- Non-root user for security
- Health checks for container orchestration

### Environment-Specific Configuration

- **Development**: Debug mode, verbose logging, hot reload
- **Staging**: Production-like, with test data
- **Production**: Optimized, minimal logging, monitoring

## Future Enhancements

### Planned Features

- Database integration (PostgreSQL with SQLAlchemy)
- User authentication (JWT)
- WebSocket support for real-time features
- Background job processing (Celery/ARQ)
- API documentation versioning
- GraphQL endpoint
- Metrics and monitoring (Prometheus)
- Distributed tracing (OpenTelemetry)

## API Best Practices Summary

1. **Use Pydantic models** for all request/response data
2. **Include examples** in schema definitions
3. **Document all endpoints** with clear descriptions
4. **Use appropriate status codes**
5. **Implement proper error handling**
6. **Version your API** from the start
7. **Paginate list endpoints**
8. **Use query parameters** for filtering/sorting
9. **Include timestamps** in responses
10. **Log all API calls** for debugging

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [The Twelve-Factor App](https://12factor.net/)
- [REST API Design Best Practices](https://restfulapi.net/)

---

**Need help?** Check out [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.
