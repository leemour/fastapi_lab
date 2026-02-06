"""Script to export OpenAPI schema to a JSON file."""

import json
import os
import sys
from pathlib import Path

from main import app

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def export_openapi(output_path: str = "docs/openapi.json"):
    """
    Export the OpenAPI schema to a JSON file.

    Args:
        output_path: Path where the OpenAPI JSON will be saved
    """
    # Get the OpenAPI schema from the app
    openapi_schema = app.openapi()

    # Ensure the output directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the schema to a file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)

    print(f"✅ OpenAPI schema exported to: {output_file}")
    print(f"   Title: {openapi_schema.get('info', {}).get('title')}")
    print(f"   Version: {openapi_schema.get('info', {}).get('version')}")
    print(f"   Endpoints: {len(openapi_schema.get('paths', {}))}")


if __name__ == "__main__":
    # Get output path from environment variable or use default
    output_path = os.environ.get("OUTPUT_PATH", "docs/openapi.json")
    export_openapi(output_path)
