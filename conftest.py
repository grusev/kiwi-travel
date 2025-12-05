import pytest
from pathlib import Path

# Import fixtures to make them available to all tests
pytest_plugins = ["fixtures.fixtures"]


def pytest_configure(config):
    """Create reports directory if it doesn't exist"""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
