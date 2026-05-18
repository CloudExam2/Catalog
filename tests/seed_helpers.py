"""Shared helpers for seed/clear scripts (live Catalog server over HTTP).

Clients, addresses and products are independent entities; a sale (in Sales)
picks ids from each list.
"""

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


# Demo data — three independent buyers, two addresses per buyer (FAC + ENV),
# plus a flat catalog of products with no owner.
DEMO_CLIENTS = [
    {"rfc": "BUYRONE12345", "razon_social": "Buyer One Corp", "email": "one@buyer.test"},
    {"rfc": "BUYRTWO12345", "razon_social": "Buyer Two Corp", "email": "two@buyer.test"},
    {"rfc": "BUYRTHREE123", "razon_social": "Buyer Three Corp", "email": "three@buyer.test"},
]

DEMO_PRODUCTS = [
    {"name": "Industrial Copper Sulfate", "unit": "kg", "base_price": 45.50},
    {"name": "Potassium Permanganate", "unit": "kg", "base_price": 32.00},
    {"name": "ITESO Lab Flask", "unit": "unit", "base_price": 15.00},
    {"name": "Sodium Chloride", "unit": "kg", "base_price": 5.25},
    {"name": "Distilled Water", "unit": "L", "base_price": 8.00},
]


def _addresses_for(client_idx: int) -> list[dict]:
    return [
        {
            "domicilio": f"Av. Vallarta {100 + client_idx}",
            "colonia": "Centro",
            "municipio": "Guadalajara",
            "estado": "Jalisco",
            "address_type": "FACTURACIÓN",
        },
        {
            "domicilio": f"Av. Patria {200 + client_idx}",
            "colonia": "Providencia",
            "municipio": "Guadalajara",
            "estado": "Jalisco",
            "address_type": "ENVÍO",
        },
    ]


def seed_catalog(base_url: str | None = None) -> dict:
    """Create clients, addresses (2 per client) and products. Returns ids for callers."""
    base_url = (base_url or get_base_url()).rstrip("/")
    _check_reachable(base_url)

    client_ids: list[int] = []
    for body in DEMO_CLIENTS:
        res = requests.post(f"{base_url}/clients/", json=body, timeout=15)
        if res.status_code != 200:
            raise RuntimeError(f"Create client {body['rfc']} failed: {res.status_code} {res.text}")
        client_ids.append(res.json()["id"])

    address_ids: list[tuple[int, int]] = []  # (fac_id, env_id) per client
    for idx, _cid in enumerate(client_ids):
        fac, env = _addresses_for(idx)
        fac_res = requests.post(f"{base_url}/addresses/", json=fac, timeout=15)
        env_res = requests.post(f"{base_url}/addresses/", json=env, timeout=15)
        for r in (fac_res, env_res):
            if r.status_code != 200:
                raise RuntimeError(f"Create address failed: {r.status_code} {r.text}")
        address_ids.append((fac_res.json()["id"], env_res.json()["id"]))

    product_ids: list[int] = []
    for body in DEMO_PRODUCTS:
        res = requests.post(f"{base_url}/products/", json=body, timeout=15)
        if res.status_code != 200:
            raise RuntimeError(f"Create product {body['name']} failed: {res.status_code} {res.text}")
        product_ids.append(res.json()["id"])

    print(f"Seeded at {base_url}")
    print(f"  client_ids  = {client_ids}")
    print(f"  address_ids = {address_ids}  # [(fac, env), ...] per client")
    print(f"  product_ids = {product_ids}")

    return {
        "client_ids": client_ids,
        "address_ids": address_ids,
        "product_ids": product_ids,
    }


def _delete_all(base_url: str, path: str) -> int:
    items = requests.get(f"{base_url}{path}", timeout=15).json()
    deleted = 0
    for row in items:
        r = requests.delete(f"{base_url}{path}{row['id']}", timeout=15)
        if r.status_code == 200:
            deleted += 1
    return deleted


def clear_catalog(base_url: str | None = None) -> None:
    """Delete every client, address and product (each list is independent)."""
    base_url = (base_url or get_base_url()).rstrip("/")
    _check_reachable(base_url)

    deleted_clients = _delete_all(base_url, "/clients/")
    deleted_products = _delete_all(base_url, "/products/")
    deleted_addresses = _delete_all(base_url, "/addresses/")

    print(f"Cleared at {base_url}")
    print(f"  deleted clients:   {deleted_clients}")
    print(f"  deleted products:  {deleted_products}")
    print(f"  deleted addresses: {deleted_addresses}")


def load_test_then_clear(base_url: str | None = None) -> None:
    """Create many independent clients/products + parallel GETs to raise CPU, then clear."""
    base_url = (base_url or get_base_url()).rstrip("/")
    num_clients = _env_int("LOAD_CLIENTS", 25)
    num_products = _env_int("LOAD_PRODUCTS_PER_CLIENT", 8) * num_clients
    http_rounds = _env_int("LOAD_HTTP_ROUNDS", 400)
    workers = _env_int("LOAD_WORKERS", 16)

    _check_reachable(base_url)
    print(f"Load test at {base_url}")
    print(f"  clients={num_clients}, products={num_products}, http_rounds={http_rounds}, workers={workers}")
    print("  Watch EC2 CPU in CloudWatch (AWS/EC2 → your instance id) for 1–5 min.")

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

    for i in range(num_products):
        res = requests.post(
            f"{base_url}/products/",
            json={"name": f"Load product {i}", "unit": "kg", "base_price": 10.0 + (i % 50)},
            timeout=30,
        )
        if res.status_code != 200:
            raise RuntimeError(f"Product {i} failed: {res.status_code} {res.text}")

    print(f"  inserted {num_clients} clients, {num_products} products")
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
