"""Fast checks that do not use RDS, SQS, or API Gateway — only the app process + local SQLite."""

from fastapi.testclient import TestClient


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
