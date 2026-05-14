"""Ensure DATABASE_URL is set before any `src` modules load (pytest imports tests after configure)."""

import os
import tempfile


def pytest_configure(config):
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    # Windows-safe URL for SQLAlchemy
    db_url = f"sqlite:///{path.replace(os.sep, '/')}"
    os.environ["DATABASE_URL"] = db_url
    config._catalog_sqlite_path = path


def pytest_unconfigure(config):
    path = getattr(config, "_catalog_sqlite_path", None)
    if path and os.path.isfile(path):
        try:
            os.unlink(path)
        except OSError:
            pass
