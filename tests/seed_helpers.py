"""Shared helpers for seed/clear scripts (live Catalog server over HTTP)."""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    catalog_root = Path(__file__).resolve().parents[1]
    load_dotenv(catalog_root / ".env")


_load_dotenv()


def get_base_url() -> str:
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return int(raw)


def _check_reachable(base_url: str) -> None:
    try:
        r = requests.get(f"{base_url}/", timeout=15)
    except requests.ConnectionError as e:
        hint = ""
        if "127.0.0.1" in base_url or "localhost" in base_url:
            hint = (
                " Nothing is listening on your PC at that address. "
                "For EC2, set BASE_URL to the Catalog Elastic IP (port 80), e.g. "
                "$env:BASE_URL='http://YOUR_CATALOG_EIP'"
            )
        raise RuntimeError(f"Catalog not reachable at {base_url}.{hint}") from e
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


def load_test_then_clear(base_url: str | None = None) -> None:
    """
    Create many clients/products, hammer the API (raises EC2 CPU), then clear all data.
    Tune with env: LOAD_CLIENTS, LOAD_PRODUCTS_PER_CLIENT, LOAD_HTTP_ROUNDS, LOAD_WORKERS.
    """
    base_url = (base_url or get_base_url()).rstrip("/")
    num_clients = _env_int("LOAD_CLIENTS", 25)
    products_per_client = _env_int("LOAD_PRODUCTS_PER_CLIENT", 8)
    http_rounds = _env_int("LOAD_HTTP_ROUNDS", 400)
    workers = _env_int("LOAD_WORKERS", 16)

    _check_reachable(base_url)
    print(f"Load test at {base_url}")
    print(
        f"  clients={num_clients}, products/client={products_per_client}, "
        f"http_rounds={http_rounds}, workers={workers}"
    )
    print("  Watch EC2 CPU in CloudWatch (AWS/EC2 → your instance id) for 1–5 min.")

    client_ids: list[int] = []
    for i in range(num_clients):
        res = requests.post(
            f"{base_url}/clients/",
            json={
                "rfc": f"LOAD{i:08d}",
                "razon_social": f"Load Test Client {i}",
                "email": f"load{i}@loadtest.test",
            },
            timeout=30,
        )
        if res.status_code != 200:
            raise RuntimeError(f"Client {i} failed: {res.status_code} {res.text}")
        client_ids.append(res.json()["id"])

    product_count = 0
    for cid in client_ids:
        for p in range(products_per_client):
            res = requests.post(
                f"{base_url}/products/",
                json={
                    "name": f"Load product {cid}-{p}",
                    "unit": "kg",
                    "base_price": 10.0 + (p % 50),
                    "client_id": cid,
                },
                timeout=30,
            )
            if res.status_code != 200:
                raise RuntimeError(f"Product failed: {res.status_code} {res.text}")
            product_count += 1

    print(f"  inserted {len(client_ids)} clients, {product_count} products")
    print(f"  HTTP stress ({http_rounds} rounds, {workers} workers)...")

    def _one_round(_: int) -> None:
        requests.get(f"{base_url}/products/", timeout=60)
        requests.get(f"{base_url}/clients/", timeout=60)
        requests.get(f"{base_url}/", timeout=60)

    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_one_round, n) for n in range(http_rounds)]
        for fut in as_completed(futures):
            fut.result()
            done += 1
            if done % 50 == 0:
                print(f"    ... {done}/{http_rounds} rounds")

    print("  stress done — clearing all catalog data...")
    clear_catalog(base_url)
    print("  load test finished (data cleared).")
