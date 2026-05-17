"""Pytest hooks: temp SQLite for imports, marker registration."""

import os
import tempfile

import pytest


def pytest_configure(config):
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db_url = f"sqlite:///{path.replace(os.sep, '/')}"
    os.environ.setdefault("DATABASE_URL", db_url)
    config._catalog_sqlite_path = path


def pytest_unconfigure(config):
    path = getattr(config, "_catalog_sqlite_path", None)
    if path and os.path.isfile(path):
        try:
            os.unlink(path)
        except OSError:
            pass


def pytest_collection_modifyitems(config, items):
    """In CI, never run seed tests (they persist data on the real server)."""
    if os.getenv("CI") == "true":
        skip_seed = pytest.mark.skip(reason="seed tests are manual only (set CI=false locally to run)")
        for item in items:
            if "seed" in item.keywords:
                item.add_marker(skip_seed)
