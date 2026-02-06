"""Tasks for OpenAPI schema management."""

from invoke import task


@task
def export(c, output="docs/openapi.json"):
    """
    Export the OpenAPI schema to a JSON file.

    Args:
        output: Path where the OpenAPI JSON will be saved (default: docs/openapi.json)
    """
    print(f"📜 Exporting OpenAPI schema to {output}...")

    # Run the export script with the output path as environment variable
    c.run(f'OUTPUT_PATH="{output}" uv run python scripts/export_openapi.py')


@task
def view(c):
    """Display the OpenAPI schema."""
    print("📜 Generating OpenAPI schema...")
    c.run('uv run python -c "from main import app; import json; print(json.dumps(app.openapi(), indent=2))"')


@task
def docs(c):
    """Open API documentation in browser."""
    print("📖 Opening API docs...")
    print("   Swagger UI: http://localhost:8000/docs")
    print("   ReDoc: http://localhost:8000/redoc")
    c.run("python -m webbrowser http://localhost:8000/docs", warn=True)
