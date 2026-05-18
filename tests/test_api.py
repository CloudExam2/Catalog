"""CRUD tests on in-memory SQLite; tables dropped after each test (no AWS, no leftover data)."""

import pytest

pytestmark = pytest.mark.ephemeral

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ---------- Clients ----------

def test_create_and_read_client():
    payload = {"rfc": "GECI950101XX", "razon_social": "Inaki Corp", "email": "inaki@test.com"}
    response = client.post("/clients/", json=payload)
    assert response.status_code == 200, response.text
    client_id = response.json()["id"]

    get_res = client.get(f"/clients/{client_id}")
    assert get_res.status_code == 200
    assert get_res.json()["razon_social"] == "Inaki Corp"


def test_create_client_invalid_rfc():
    payload = {"rfc": "WAY_TOO_LONG_RFC_123456", "razon_social": "Bad", "email": "bad@test.com"}
    response = client.post("/clients/", json=payload)
    assert response.status_code == 422


def test_list_multiple_clients():
    for i in range(3):
        r = client.post(
            "/clients/",
            json={"rfc": f"MULTI00000{i:02d}", "razon_social": f"Client {i}", "email": f"c{i}@t.com"},
        )
        assert r.status_code == 200, r.text

    listed = client.get("/clients/")
    assert listed.status_code == 200
    body = listed.json()
    assert len(body) == 3
    razones = {c["razon_social"] for c in body}
    assert razones == {"Client 0", "Client 1", "Client 2"}


# ---------- Products (independent of clients) ----------

def test_create_standalone_product():
    payload = {"name": "Mechanical Keyboard", "unit": "unit", "base_price": 150.00}
    p_res = client.post("/products/", json=payload)
    assert p_res.status_code == 200, p_res.text
    body = p_res.json()
    assert body["name"] == "Mechanical Keyboard"
    assert "client_id" not in body


def test_get_nonexistent_product():
    response = client.get("/products/9999")
    assert response.status_code == 404


def test_list_multiple_products():
    for i, name in enumerate(["A", "B", "C"]):
        r = client.post("/products/", json={"name": name, "unit": "kg", "base_price": 10.0 + i})
        assert r.status_code == 200, r.text

    listed = client.get("/products/").json()
    assert {p["name"] for p in listed} == {"A", "B", "C"}


# ---------- Addresses (independent of clients; FACTURACIÓN + ENVÍO) ----------

def test_create_facturacion_and_envio_addresses():
    fac = client.post(
        "/addresses/",
        json={"domicilio": "Av. Vallarta 100", "address_type": "FACTURACIÓN"},
    )
    env = client.post(
        "/addresses/",
        json={"domicilio": "Av. Patria 200", "address_type": "ENVÍO"},
    )
    assert fac.status_code == 200, fac.text
    assert env.status_code == 200, env.text

    listed = client.get("/addresses/").json()
    types = {a["address_type"] for a in listed}
    assert types == {"FACTURACIÓN", "ENVÍO"}


def test_create_address_invalid_type():
    payload = {"domicilio": "123 Main St", "address_type": "CASA"}
    response = client.post("/addresses/", json=payload)
    assert response.status_code == 422


def test_delete_address():
    a_res = client.post(
        "/addresses/",
        json={"domicilio": "123 Main St", "address_type": "FACTURACIÓN"},
    )
    aid = a_res.json()["id"]

    del_res = client.delete(f"/addresses/{aid}")
    assert del_res.status_code == 200

    check = client.get(f"/addresses/{aid}")
    assert check.status_code == 404
