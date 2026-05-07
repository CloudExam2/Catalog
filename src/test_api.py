import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Internal imports - adjust paths if your 'src' structure differs
from main import app
from database import Base, get_db

# 1. Setup an isolated Test Database (In-Memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite://" # Memory-only
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Dependency Override
# This replaces the real DB with the test DB during testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    """Creates tables before each test and drops them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- CLIENT TESTS ---

def test_create_and_read_client():
    # Test Create
    payload = {"rfc": "GECI950101XXX", "razon_social": "Inaki Corp", "email": "inaki@test.com"}
    response = client.post("/clients/", json=payload)
    assert response.status_code == 200
    client_id = response.json()["id"]

    # Test Read
    get_res = client.get(f"/clients/{client_id}")
    assert get_res.status_code == 200
    assert get_res.json()["razon_social"] == "Inaki Corp"

def test_create_client_invalid_rfc():
    # Testing Pydantic validation (RFC too long)
    payload = {"rfc": "WAY_TOO_LONG_RFC_123456", "razon_social": "Bad", "email": "bad@test.com"}
    response = client.post("/clients/", json=payload)
    assert response.status_code == 422 # Unprocessable Entity

# --- PRODUCT TESTS (With Relationship) ---

def test_create_product_for_client():
    # 1. First create a client (The Seller)
    c_res = client.post("/clients/", json={
        "rfc": "SELLER1234567", 
        "razon_social": "Seller", 
        "email": "s@t.com"
    })
    assert c_res.status_code == 200
    seller_id = c_res.json()["id"]

    # 2. Create product linked to that client
    p_payload = {
        "name": "Mechanical Keyboard",
        "unit": "unit",
        "base_price": 150.00,
        "client_id": seller_id
    }
    p_res = client.post("/products/", json=p_payload)
    assert p_res.status_code == 200
    assert p_res.json()["name"] == "Mechanical Keyboard"
    assert p_res.json()["client_id"] == seller_id

def test_get_nonexistent_product():
    response = client.get("/products/9999")
    assert response.status_code == 404

# --- ADDRESS TESTS ---

def test_delete_address():
    # 1. Create client
    c_res = client.post("/clients/", json={
        "rfc": "ADDRESS123456", 
        "razon_social": "User", 
        "email": "u@t.com"
    })
    assert c_res.status_code == 200
    uid = c_res.json()["id"]

    # 2. Create address
    a_res = client.post("/addresses/", json={
        "domicilio": "123 Main St",
        "client_id": uid,
        "address_type": "FACTURACIÓN"
    })
    aid = a_res.json()["id"]

    # 3. Delete
    del_res = client.delete(f"/addresses/{aid}")
    assert del_res.status_code == 200
    
    # 4. Verify gone
    check = client.get(f"/addresses/{aid}")
    assert check.status_code == 404

def test_create_address_invalid_type():
    # 1. Create client
    c_res = client.post("/clients/", json={
        "rfc": "VALIDRFC12345", 
        "razon_social": "User", 
        "email": "u@t.com"
    })
    uid = c_res.json()["id"]

    # 2. Try to create address with invalid type (Home)
    payload = {
        "domicilio": "123 Main St",
        "client_id": uid,
        "address_type": "CASA" # This should fail
    }
    response = client.post("/addresses/", json=payload)
    assert response.status_code == 422

def test_create_address_valid_type():
    uid = 1 # Assume client 1 exists
    payload = {
        "domicilio": "123 Main St",
        "client_id": uid,
        "address_type": "FACTURACIÓN" # Must match exactly
    }
    response = client.post("/addresses/", json=payload)
    assert response.status_code == 200