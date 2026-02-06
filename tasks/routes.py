"""Tasks for generating and managing API routes."""

from invoke import task


@task
def list(c):
    """List all registered API routes."""
    print("📋 Listing all FastAPI routes...")
    c.run(
        'uv run python -c "'
        "from main import app; "
        "from fastapi.routing import APIRoute; "
        "routes = [route for route in app.routes if isinstance(route, APIRoute)]; "
        "[print(f'{route.methods} {route.path}') for route in routes]"
        '"'
    )


@task
def create(c, name, prefix="v1", auth=False):
    """
    Create a new API route module.

    Args:
        name: Name of the route (e.g., 'users', 'posts')
        prefix: API version prefix (default: v1)
        auth: Whether to require authentication (default: False)
    """
    print(f"🚀 Creating new route: {name}")

    # Create the route file
    route_file = f"src/api/{prefix}/{name}.py"
    auth_import = "from src.core.auth import require_api_key\n" if auth else ""
    auth_depends = ", dependencies=[Depends(require_api_key)]" if auth else ""

    content = f'''from fastapi import APIRouter{", Depends" if auth else ""}
{auth_import}
router = APIRouter()


@router.get("/{name}"{auth_depends})
def get_{name}():
    """Get all {name}."""
    return {{"{name}": []}}


@router.get("/{name}/{{item_id}}"{auth_depends})
def get_{name.rstrip('s')}(item_id: int):
    """Get a specific {name.rstrip('s')} by ID."""
    return {{"id": item_id, "name": "Example {name.rstrip('s')}"}}


@router.post("/{name}"{auth_depends})
def create_{name.rstrip('s')}(item: dict):
    """Create a new {name.rstrip('s')}."""
    return {{"message": "{name.rstrip('s').capitalize()} created", "data": item}}
'''

    with open(route_file, "w") as f:
        f.write(content)

    print(f"✅ Created {route_file}")
    print("\n📝 Next steps:")
    print(f"   1. Add 'from src.api.{prefix} import {name}' to src/api/{prefix}/router.py")
    print(f"   2. Add 'api_router.include_router({name}.router, tags=[\"{name}\"])' to the router")


@task
def openapi(c):
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
