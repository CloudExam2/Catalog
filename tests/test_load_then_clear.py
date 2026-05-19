"""
Bulk data + HTTP stress on live Catalog EC2, then wipe everything.

Uses BASE_URL from .env (Catalog/.env) or environment variable.

  copy .env.example .env   # set your Elastic IP once
  python tests/test_load_then_clear.py

Or: pytest tests/test_load_then_clear.py -v

Does NOT run in CI. Ends with 404/422/500 traffic for HTTP % widgets, then clears data.
"""

import pytest

from seed_helpers import get_base_url, load_test_then_clear

pytestmark = pytest.mark.seed


def test_load_then_clear_catalog():
    load_test_then_clear(get_base_url())


if __name__ == "__main__":
    load_test_then_clear()
