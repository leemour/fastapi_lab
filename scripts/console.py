#!/usr/bin/env python3
"""
Interactive Python console with FastAPI application context loaded.
Similar to Rails console - provides access to the app, models, and utilities.

Usage:
    task console              # Run locally with uv
    task docker-console       # Run in Docker container
    python scripts/console.py # Direct execution
"""

import sys
from pathlib import Path

# Add project root and src to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Import app and commonly used modules
from main import app, logger  # noqa: E402
from src.core.config import settings  # noqa: E402

# Import any models or utilities here as they're created
# from src.models import User, Item  # Example
# from src.core.database import get_db  # Example

# Color codes for pretty output
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


def print_banner():
    """Print welcome banner with available objects."""
    banner = f"""
{CYAN}╔════════════════════════════════════════════════════════════╗
║  FastAPI Lab - Interactive Console                         ║
╚════════════════════════════════════════════════════════════╝{RESET}

{GREEN}Available objects:{RESET}
  {YELLOW}app{RESET}      - FastAPI application instance
  {YELLOW}settings{RESET} - Application settings
  {YELLOW}logger{RESET}   - Application logger

{GREEN}Examples:{RESET}
  >>> app.routes                    # List all routes
  >>> settings.app_name             # Get app name
  >>> logger.info("Test message")   # Test logging
  >>> [route.path for route in app.routes]  # List route paths

{GREEN}Tips:{RESET}
  - Use dir(app) to see all app attributes
  - Use help(object) for documentation
  - Press Ctrl+D or type exit() to quit
"""
    print(banner)


def start_console():
    """Start interactive Python console with app context."""
    import code
    import readline
    import rlcompleter

    # Enable tab completion
    readline.set_completer(rlcompleter.Completer(locals()).complete)
    readline.parse_and_bind("tab: complete")

    # Print banner
    print_banner()

    # Prepare console namespace
    console_namespace = {
        "app": app,
        "settings": settings,
        "logger": logger,
        # Add more objects here as needed
        # "User": User,
        # "Item": Item,
        # "get_db": get_db,
    }

    # Start interactive console
    console = code.InteractiveConsole(locals=console_namespace)
    console.interact(banner="", exitmsg=f"\n{GREEN}Goodbye!{RESET}\n")


if __name__ == "__main__":
    try:
        start_console()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}\n")
        sys.exit(0)
