"""
Hammer Catalog EC2 CPU (parallel GETs). Watch Exam2-EC2-Overview + CPU alarm email.

  python tests/test_cpu_spike.py

One-liner (PowerShell, from Catalog folder with .env set):

  python -c "import os;from dotenv import load_dotenv;load_dotenv();import requests;u=os.environ.get('BASE_URL','http://127.0.0.1:8000').rstrip('/');[requests.get(f'{u}/products/',timeout=60) or requests.get(f'{u}/clients/',timeout=60) for _ in range(500)]"
"""

import os
from concurrent.futures import ThreadPoolExecutor

import pytest
import requests

pytestmark = pytest.mark.seed

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ROUNDS = int(os.getenv("CPU_SPIKE_ROUNDS", "500"))
WORKERS = int(os.getenv("CPU_SPIKE_WORKERS", "32"))


def _hit(_: int) -> None:
    requests.get(f"{BASE}/products/", timeout=60)
    requests.get(f"{BASE}/clients/", timeout=60)
    requests.get(f"{BASE}/", timeout=60)


def spike_catalog_cpu() -> None:
    print(f"CPU spike on {BASE} — {ROUNDS} rounds, {WORKERS} workers")
    print("  Watch CloudWatch dashboard + email if CPU > 70% for 2 minutes.")
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(_hit, range(ROUNDS)))
    print("  Done.")


def test_spike_catalog_cpu():
    spike_catalog_cpu()


if __name__ == "__main__":
    spike_catalog_cpu()
