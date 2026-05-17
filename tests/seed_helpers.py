"""Shared helpers for seed/clear scripts (live Catalog server over HTTP)."""

import os

import requests

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


def get_base_url() -> str:
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _check_reachable(base_url: str) -> None:
    r = requests.get(f"{base_url}/", timeout=15)
    if r.status_code != 200:
        raise RuntimeError(f"Catalog not reachable at {base_url} (status {r.status_code})")


def seed_catalog(base_url: str | None = None) -> None:
    base_url = (base_url or get_base_url()).rstrip("/")
    _check_reachable(base_url)

    seller = requests.post(
        f"{base_url}/clients/",
        json={
            "rfc": "SEEDSELLER123",
            "razon_social": "Seed Seller Corp",
            "email": "seed@seller.test",
            "telefono": "1234567890",
            "comercial_name": "Seed Seller Corp",
        },
        timeout=15,
    )
    if seller.status_code != 200:
        raise RuntimeError(f"Create seller failed: {seller.status_code} {seller.text}")
    seller_id = seller.json()["id"]

    products = [
        {"name": "Industrial Copper Sulfate", "unit": "kg", "base_price": 45.50, "client_id": seller_id},
        {"name": "Potassium Permanganate", "unit": "kg", "base_price": 32.00, "client_id": seller_id},
        {"name": "ITESO Lab Flask", "unit": "unit", "base_price": 15.00, "client_id": seller_id},
    ]

    created_ids = []
    for item in products:
        res = requests.post(f"{base_url}/products/", json=item, timeout=15)
        if res.status_code != 200:
            raise RuntimeError(f"Create product {item['name']} failed: {res.status_code} {res.text}")
        created_ids.append(res.json()["id"])

    print(f"Seeded at {base_url}")
    print(f"  seller client_id={seller_id}")
    print(f"  product_ids={created_ids}")
    print("  products:", ", ".join(p["name"] for p in products))


def clear_catalog(base_url: str | None = None) -> None:
    """Delete all clients (products and addresses cascade via the API/ORM)."""
    base_url = (base_url or get_base_url()).rstrip("/")
    _check_reachable(base_url)

    clients = requests.get(f"{base_url}/clients/", timeout=15)
    if clients.status_code != 200:
        raise RuntimeError(f"List clients failed: {clients.status_code} {clients.text}")

    deleted_clients = 0
    for row in clients.json():
        r = requests.delete(f"{base_url}/clients/{row['id']}", timeout=15)
        if r.status_code == 200:
            deleted_clients += 1

    products = requests.get(f"{base_url}/products/", timeout=15).json()
    addresses = requests.get(f"{base_url}/addresses/", timeout=15).json()

    print(f"Cleared at {base_url}")
    print(f"  deleted clients: {deleted_clients}")
    print(f"  products remaining: {len(products)}")
    print(f"  addresses remaining: {len(addresses)}")
