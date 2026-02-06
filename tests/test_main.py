"""
RSpec-style tests for FastAPI endpoints using pytest-describe.

Run with:
    pytest                          # Run all tests
    pytest -n auto                  # Run tests in parallel
    pytest -k "describe_root"       # Run specific describe block
    pytest -m unit                  # Run only unit tests
    pytest -v                       # Verbose output
"""

import pytest


def describe_root_endpoint():
    """Tests for the root endpoint."""

    def it_returns_hello_world(client):
        """It should return a hello world message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def it_uses_get_method(client):
        """It should only accept GET requests."""
        response = client.post("/")
        assert response.status_code == 405  # Method Not Allowed


def describe_health_check():
    """Tests for the health check endpoint."""

    def it_returns_healthy_status(client):
        """It should return a healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @pytest.mark.unit
    def it_responds_quickly(client):
        """It should respond within acceptable time."""
        response = client.get("/health")
        assert response.status_code == 200
        # Health checks should be fast
        assert response.elapsed.total_seconds() < 1


def describe_read_item():
    """Tests for reading items."""

    def describe_with_valid_id():
        """When the item ID is valid."""

        def it_returns_item_with_id(client):
            """It should return the item with the given ID."""
            response = client.get("/items/42")
            assert response.status_code == 200
            assert response.json()["item_id"] == 42

        def it_includes_query_parameter(client):
            """It should include query parameters in response."""
            response = client.get("/items/1?q=test")
            assert response.status_code == 200
            data = response.json()
            assert data["item_id"] == 1
            assert data["q"] == "test"

        def it_works_without_query_parameter(client):
            """It should work without query parameters."""
            response = client.get("/items/1")
            assert response.status_code == 200
            data = response.json()
            assert data["item_id"] == 1
            assert data["q"] is None

    def describe_with_invalid_id():
        """When the item ID is invalid."""

        def it_returns_400_for_negative_id(client):
            """It should return 400 for negative IDs."""
            response = client.get("/items/-1")
            assert response.status_code == 400
            assert "Invalid item ID" in response.json()["detail"]

        def it_returns_400_for_zero_id(client):
            """It should return 400 for zero ID."""
            response = client.get("/items/0")
            assert response.status_code == 400


def describe_create_item():
    """Tests for creating items."""

    def describe_with_tax():
        """When the item includes tax."""

        def it_creates_item_successfully(client, sample_item):
            """It should create the item with tax calculation."""
            response = client.post("/items/", json=sample_item)
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == sample_item["name"]
            assert data["price"] == sample_item["price"]
            assert data["tax"] == sample_item["tax"]

        def it_calculates_price_with_tax(client, sample_item):
            """It should calculate the total price including tax."""
            response = client.post("/items/", json=sample_item)
            data = response.json()
            expected_total = sample_item["price"] + sample_item["tax"]
            assert data["price_with_tax"] == pytest.approx(expected_total)

    def describe_without_tax():
        """When the item does not include tax."""

        def it_creates_item_without_tax_calculation(client, sample_item_no_tax):
            """It should create the item without tax calculation."""
            response = client.post("/items/", json=sample_item_no_tax)
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == sample_item_no_tax["name"]
            assert "price_with_tax" not in data

    def describe_with_invalid_data():
        """When the item data is invalid."""

        def it_returns_422_for_missing_required_fields(client):
            """It should return 422 for missing required fields."""
            response = client.post("/items/", json={"name": "Test"})
            assert response.status_code == 422

        def it_returns_422_for_invalid_price_type(client):
            """It should return 422 for invalid price type."""
            response = client.post("/items/", json={"name": "Test", "price": "not-a-number"})
            assert response.status_code == 422
