# FastAPI Testing Lab

A FastAPI project with RSpec-style testing using pytest-describe, pytest-sugar, pytest-xdist, and more.

## Quick Start

```bash
# Install Task (if not already installed)
# See TASK_INSTALLATION.md for detailed instructions
# macOS: brew install go-task
# Linux: sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin

# Install dependencies
task install

# Run tests with beautiful output
task test

# Run tests in parallel (faster!)
task test-parallel

# Run with coverage report
task test-cov

# Start the application
task run-dev
```

> **Note**: This project uses [Task](https://taskfile.dev/) as a task runner. See [TASK_INSTALLATION.md](TASK_INSTALLATION.md) for installation instructions. You can also run commands directly with `uv run` if you prefer not to install Task.

## Features

### Testing Tools Configured

- **pytest-describe** - Write RSpec-style `describe`/`it` blocks for BDD testing
- **pytest-sugar** - Beautiful progress bars and colored output
- **pytest-xdist** - Run tests in parallel across multiple CPUs
- **pytest-cov** - Code coverage reporting with HTML output
- **pytest-asyncio** - Full async/await support for FastAPI
- **pytest-mock** - Easy mocking and stubbing
- **httpx** - Modern HTTP client for testing FastAPI endpoints

### Test Results

✓ 25 tests passing  
✓ 100% code coverage  
✓ Tests run in ~0.06s (sequential) or ~2.7s with 24 parallel workers  
✓ Beautiful output with pytest-sugar  

## Project Structure

```
fastapi_lab/
├── main.py                    # FastAPI application
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Shared fixtures (client, sample data)
│   ├── test_main.py          # RSpec-style endpoint tests
│   └── test_advanced.py      # Advanced testing patterns
├── docs/
│   └── TESTING_GUIDE.md      # Comprehensive testing guide
├── pyproject.toml            # Dependencies & pytest config
├── Taskfile.yml              # Task runner configuration
├── README.md                 # This file
├── SETUP_SUMMARY.md          # Setup overview
└── TASK_INSTALLATION.md      # Task installation instructions
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

### Advanced Usage

```bash
# Run in parallel (much faster!)
uv run pytest -n auto

# Run with coverage
uv run pytest --cov=. --cov-report=html
open htmlcov/index.html

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

## Example Test

Here's what RSpec-style testing looks like:

```python
def describe_items_api():
    """Group related tests together."""
    
    def describe_create_item():
        """Context: Creating items."""
        
        def describe_with_tax():
            """Context: When item includes tax."""
            
            def it_creates_item_successfully(client, sample_item):
                """It should create the item."""
                response = client.post("/items", json=sample_item)
                assert response.status_code == 200
            
            def it_calculates_price_with_tax(client, sample_item):
                """It should calculate total price."""
                response = client.post("/items", json=sample_item)
                data = response.json()
                expected = sample_item["price"] + sample_item["tax"]
                assert data["price_with_tax"] == expected
        
        def describe_without_tax():
            """Context: When item has no tax."""
            
            def it_creates_item_without_calculation(client, sample_item_no_tax):
                """It should create without tax calculation."""
                response = client.post("/items", json=sample_item_no_tax)
                assert response.status_code == 200
                assert "price_with_tax" not in response.json()
```

## Running the Application

```bash
# Development server with auto-reload
task run-dev

# Or directly
uv run uvicorn main:app --reload

# Production server
task run

# Or directly
uv run python main.py
```

Visit http://localhost:8000/docs for interactive API documentation.

## Documentation

- **SETUP_SUMMARY.md** - Overview of what was installed and configured
- **docs/TESTING_GUIDE.md** - Comprehensive guide with examples and best practices
- **TASK_INSTALLATION.md** - How to install and use Task runner

## Task Commands

```bash
task                  # Show all available commands
task install          # Install all dependencies
task test             # Run all tests
task test-parallel    # Run tests in parallel (alias: tp)
task test-cov         # Run with coverage report (alias: cov)
task test-unit        # Run only unit tests
task test-integration # Run only integration tests
task test-fast        # Fast fail mode (alias: tf)
task test-watch       # Run tests in watch mode (alias: tw)
task clean            # Remove generated files
task run              # Run the FastAPI application
task run-dev          # Run with auto-reload (alias: dev)
task lint             # Run linter
task format           # Format code
task check            # Run all checks (lint + format + test)
task ci               # Run CI pipeline
```

## Why RSpec-Style?

1. **Better Organization** - Tests grouped by context and behavior
2. **Readable Output** - Test names read like natural sentences
3. **Natural Nesting** - Easy context-specific tests without classes
4. **BDD-Friendly** - Encourages behavior-driven development
5. **Flexible Fixtures** - Fixtures can be scoped to any describe block

## Configuration Highlights

### pytest.ini_options in pyproject.toml

- Automatic test discovery with `describe_*` and `it_*` patterns
- Code coverage enabled by default
- Verbose output with short tracebacks
- Custom markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`
- Async test support enabled

### Coverage Settings

- Excludes test files from coverage
- Shows missing lines in reports
- Generates HTML reports
- Requires 80% coverage minimum

## Next Steps

1. Read `TESTING_GUIDE.md` for comprehensive examples
2. Check `PYTEST_CHEATSHEET.md` for quick command reference
3. Write your own tests following the examples in `tests/`
4. Run `make test-parallel` for faster test execution
5. Check coverage with `make test-cov`

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-describe](https://github.com/pytest-dev/pytest-describe)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [RSpec Documentation](https://rspec.info/) (for comparison)

---

Happy Testing! 🚀
