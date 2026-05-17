"""
Remove all clients, products, and addresses from a running Catalog server.

Deleting each client cascades to its products and addresses in the API.

Run with pytest:

  $env:BASE_URL = "http://YOUR_EC2_PUBLIC_IP"
  pytest tests/test_clear_data.py -v

Or:

  $env:BASE_URL = "http://YOUR_EC2_PUBLIC_IP"
  python tests/test_clear_data.py

Does NOT run in CI.
"""

import pytest

from seed_helpers import clear_catalog, get_base_url

pytestmark = pytest.mark.seed


def test_clear_all_catalog_data():
    clear_catalog(get_base_url())


if __name__ == "__main__":
    clear_catalog()
