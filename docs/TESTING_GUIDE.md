# RSpec-Style Testing Guide for FastAPI

This guide explains how to write RSpec-style tests using pytest-describe for your FastAPI application.

## Table of Contents

- [Quick Start](#quick-start)
- [RSpec-Style Syntax](#rspec-style-syntax)
- [Writing Tests](#writing-tests)
- [Fixtures](#fixtures)
- [Running Tests](#running-tests)
- [Best Practices](#best-practices)

## Quick Start

```bash
# Install dependencies
task install

# Run tests
task test

# Run tests in parallel (faster!)
task test-parallel

# Run with coverage
task test-cov
```

## RSpec-Style Syntax

### describe_* Functions (Like RSpec's `describe`)

Use `describe_*` functions to group related tests:

```python
def describe_user_authentication():
    """Group all authentication-related tests."""
    
    def describe_login():
        """Nested group for login-specific tests."""
        pass
```

### it_* Functions (Like RSpec's `it`)

Use `it_*` functions for individual test cases:

```python
def describe_user_authentication():
    
    def it_allows_valid_credentials(client):
        """Should allow login with valid credentials."""
        response = client.post("/login", json={"username": "user", "password": "pass"})
        assert response.status_code == 200
    
    def it_rejects_invalid_credentials(client):
        """Should reject login with invalid credentials."""
        response = client.post("/login", json={"username": "user", "password": "wrong"})
        assert response.status_code == 401
```

### Context Blocks (Nested describes)

Use nested `describe_*` functions to create contexts:

```python
def describe_shopping_cart():
    
    def describe_when_empty():
        """Context: When the cart is empty."""
        
        def it_shows_zero_items(client):
            assert client.get("/cart").json()["count"] == 0
    
    def describe_when_has_items():
        """Context: When the cart has items."""
        
        @pytest.fixture
        def cart_with_items(client):
            client.post("/cart", json={"item_id": 1})
            return client
        
        def it_shows_correct_count(cart_with_items):
            assert cart_with_items.get("/cart").json()["count"] == 1
```

## Writing Tests

### Basic Test Structure

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

### Testing FastAPI Endpoints

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
    
    def describe_create_item():
        """POST /items tests."""
        
        def it_creates_valid_item(client, sample_item):
            response = client.post("/items", json=sample_item)
            assert response.status_code == 201
            assert response.json()["id"] is not None
        
        def it_validates_required_fields(client):
            response = client.post("/items", json={})
            assert response.status_code == 422
```

### Testing with Pydantic Models

```python
def describe_item_model():
    
    def describe_validation():
        
        def it_accepts_valid_data():
            from main import Item
            item = Item(name="Widget", price=9.99)
            assert item.name == "Widget"
            assert item.price == 9.99
        
        def it_rejects_invalid_price():
            from main import Item
            from pydantic import ValidationError
            
            with pytest.raises(ValidationError):
                Item(name="Widget", price="not-a-number")
```

### Testing Async Endpoints

```python
def describe_async_operations():
    
    @pytest.mark.asyncio
    async def it_handles_async_request(client):
        """Test async endpoint."""
        response = client.get("/async-endpoint")
        assert response.status_code == 200
```

## Fixtures

### Shared Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)

@pytest.fixture
def authenticated_client(client):
    """Client with authentication."""
    client.headers = {"Authorization": "Bearer token"}
    return client
```

### Local Fixtures (in test file)

```python
def describe_user_operations():
    
    @pytest.fixture
    def sample_user():
        """Sample user data."""
        return {
            "username": "testuser",
            "email": "test@example.com"
        }
    
    def it_creates_user(client, sample_user):
        response = client.post("/users", json=sample_user)
        assert response.status_code == 201
```

## Running Tests

### Basic Commands

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_main.py

# Run specific describe block
uv run pytest -k "describe_root"

# Run specific test
uv run pytest -k "it_returns_hello_world"
```

### Advanced Commands

```bash
# Run in parallel (faster!)
uv run pytest -n auto

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration

# Skip slow tests
uv run pytest -m "not slow"

# Stop at first failure
uv run pytest -x

# Run last failed tests
uv run pytest --lf

# Show local variables in tracebacks
uv run pytest -l

# Show print statements
uv run pytest -s
```

### Using Task Commands

```bash
task test              # Run all tests
task test-parallel     # Run tests in parallel
task test-cov          # Run with coverage report
task test-unit         # Run only unit tests
task test-integration  # Run only integration tests
task test-fast         # Run with fast-fail options
```

## Best Practices

### 1. Descriptive Names

Use clear, descriptive names that explain what the test does:

```python
# Good
def it_returns_404_when_item_not_found(client):
    pass

# Bad
def test_item(client):
    pass
```

### 2. One Assertion Per Test (When Possible)

```python
# Good - focused test
def it_creates_user_with_correct_username(client, user_data):
    response = client.post("/users", json=user_data)
    assert response.json()["username"] == user_data["username"]

def it_creates_user_with_correct_email(client, user_data):
    response = client.post("/users", json=user_data)
    assert response.json()["email"] == user_data["email"]

# Acceptable - related assertions
def it_creates_user_with_valid_response(client, user_data):
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    assert "id" in response.json()
```

### 3. Use Fixtures for Setup

```python
# Good - reusable setup
@pytest.fixture
def created_user(client):
    response = client.post("/users", json={"username": "test"})
    return response.json()

def it_can_retrieve_created_user(client, created_user):
    response = client.get(f"/users/{created_user['id']}")
    assert response.status_code == 200
```

### 4. Test Edge Cases

```python
def describe_pagination():
    
    def it_handles_first_page(client):
        response = client.get("/items?page=1")
        assert response.status_code == 200
    
    def it_handles_last_page(client):
        response = client.get("/items?page=999")
        assert response.status_code == 200
    
    def it_handles_invalid_page_number(client):
        response = client.get("/items?page=-1")
        assert response.status_code == 400
```

### 5. Mark Slow Tests

```python
@pytest.mark.slow
def it_processes_large_dataset(client):
    """This test takes a while."""
    # Long-running test
    pass

# Run without slow tests:
# pytest -m "not slow"
```

### 6. Use Markers for Test Organization

```python
@pytest.mark.unit
def it_validates_input():
    """Unit test - no external dependencies."""
    pass

@pytest.mark.integration
def it_saves_to_database(client):
    """Integration test - uses database."""
    pass

# Run specific markers:
# pytest -m unit
# pytest -m integration
```

### 7. Group Related Tests

```python
def describe_user_api():
    
    def describe_registration():
        # All registration tests
        pass
    
    def describe_authentication():
        # All auth tests
        pass
    
    def describe_profile_management():
        # All profile tests
        pass
```

## Common Patterns

### Testing Error Responses

```python
def describe_error_handling():
    
    def it_returns_400_for_invalid_input(client):
        response = client.post("/items", json={"invalid": "data"})
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def it_returns_404_for_missing_resource(client):
        response = client.get("/items/999999")
        assert response.status_code == 404
```

### Testing with Mocks

```python
def describe_external_api_calls():
    
    def it_handles_third_party_api(client, mocker):
        mock_api = mocker.patch('main.external_api.fetch_data')
        mock_api.return_value = {"data": "mocked"}
        
        response = client.get("/external-data")
        assert response.status_code == 200
        mock_api.assert_called_once()
```

### Testing Authentication

```python
def describe_protected_endpoints():
    
    def describe_when_authenticated():
        
        @pytest.fixture
        def auth_client(client):
            client.headers = {"Authorization": "Bearer valid-token"}
            return client
        
        def it_allows_access(auth_client):
            response = auth_client.get("/protected")
            assert response.status_code == 200
    
    def describe_when_not_authenticated():
        
        def it_returns_401(client):
            response = client.get("/protected")
            assert response.status_code == 401
```

## pytest-sugar Features

pytest-sugar provides beautiful output:

- ✓ Green checkmarks for passing tests
- ✗ Red X for failing tests
- Progress bar showing test completion
- Instant feedback on failures
- Cleaner, more readable output

## Coverage Reports

After running tests with coverage:

```bash
task test-cov
```

Open the HTML report:

```bash
# Linux
xdg-open htmlcov/index.html

# macOS
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-describe](https://github.com/pytest-dev/pytest-describe)
- [FastAPI testing docs](https://fastapi.tiangolo.com/tutorial/testing/)
- [RSpec documentation](https://rspec.info/) (for comparison)
