"""
Seed a running Catalog server with demo data for Sales testing.

Does NOT run in CI (see conftest.py). Run locally against EC2 or uvicorn:

  set BASE_URL=http://YOUR_EC2_PUBLIC_IP
  pytest tests/ -m seed -v

Data is left on the server on purpose.
"""

import os

import pytest
import requests

pytestmark = pytest.mark.seed

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def test_seed_seller_and_products():
    health = requests.get(f"{BASE_URL}/", timeout=15)
    assert health.status_code == 200, f"Catalog not reachable at {BASE_URL}"

    seller = requests.post(
        f"{BASE_URL}/clients/",
        json={
            "rfc": "SEEDSELLER1234",
            "razon_social": "Seed Seller Corp",
            "email": "seed@seller.test",
        },
        timeout=15,
    )
    assert seller.status_code == 200, seller.text
    seller_id = seller.json()["id"]

    products = [
        {"name": "Industrial Copper Sulfate", "unit": "kg", "base_price": 45.50, "client_id": seller_id},
        {"name": "Potassium Permanganate", "unit": "kg", "base_price": 32.00, "client_id": seller_id},
        {"name": "ITESO Lab Flask", "unit": "unit", "base_price": 15.00, "client_id": seller_id},
    ]

    created_ids = []
    for item in products:
        res = requests.post(f"{BASE_URL}/products/", json=item, timeout=15)
        assert res.status_code == 200, res.text
        created_ids.append(res.json()["id"])

    listed = requests.get(f"{BASE_URL}/products/", timeout=15)
    assert listed.status_code == 200
    names = {p["name"] for p in listed.json()}
    for item in products:
        assert item["name"] in names

    print(f"\nSeeded seller client_id={seller_id}, product_ids={created_ids} at {BASE_URL}\n")
