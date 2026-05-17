"""Smoke tests: quick health checks (no OpenAI — 'smoke' = shallow sanity test)."""

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.ephemeral


def test_health_endpoint():
    # Import after conftest.pytest_configure set DATABASE_URL
    from main import app

    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body.get("status") == "healthy"
    assert body.get("service") == "catalog"


def test_openapi_available():
    from main import app

    client = TestClient(app)
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    assert spec.get("openapi")
    assert "paths" in spec
    assert "/clients/" in spec["paths"]
    assert "/products/" in spec["paths"]
