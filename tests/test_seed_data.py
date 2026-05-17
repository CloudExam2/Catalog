"""
Add demo products on a running Catalog server (data stays on the server).

Run with pytest (recommended):

  $env:BASE_URL = "http://YOUR_EC2_PUBLIC_IP"
  pytest tests/test_seed_data.py -v

Or:

  $env:BASE_URL = "http://YOUR_EC2_PUBLIC_IP"
  python tests/test_seed_data.py

Does NOT run in CI.
"""

import pytest

from seed_helpers import get_base_url, seed_catalog

pytestmark = pytest.mark.seed


def test_seed_seller_and_products():
    seed_catalog(get_base_url())


if __name__ == "__main__":
    seed_catalog()
