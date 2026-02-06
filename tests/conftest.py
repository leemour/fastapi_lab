"""
Pytest configuration and fixtures.
This file is automatically loaded by pytest.
"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI application.
    This fixture is function-scoped and creates a new client for each test.
    """
    return TestClient(app)


@pytest.fixture
def sample_item():
    """Sample item data for testing."""
    return {"name": "Test Item", "description": "A test item", "price": 10.99, "tax": 1.10}


@pytest.fixture
def sample_item_no_tax():
    """Sample item data without tax for testing."""
    return {"name": "Test Item", "description": "A test item", "price": 10.99}
