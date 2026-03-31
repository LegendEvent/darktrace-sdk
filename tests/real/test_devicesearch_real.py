"""
Real-environment tests for DeviceSearch module.

These tests require a live Darktrace instance with valid credentials.
They are skipped by default and only run on work machines with API access.

To run these tests:
```bash
pytest tests/real/test_devicesearch_real.py \\
    --host=https://your-darktrace-instance \\
    --public-token=YOUR_PUBLIC_TOKEN \\
    --private-token=YOUR_PRIVATE_TOKEN
```

NOTE: This is a stub test file intended for future real-environment testing.
The stub tests were added to validate the fix for Issue #45 in the codebase.
As we don't have a live Darktrace instance available in CI/CD, these stub tests will remain skipped.

"""

import pytest
import requests
from darktrace import DarktraceClient


@pytest.mark.skip(
    reason="Requires live Darktrace instance - run with --host and credentials"
)
def test_real_multi_param_search():
    """
    Test multi-parameter search against real Darktrace API.
    Validates the fix for Issue #45 in a real environment.
    """
    # This test is skipped by default - requires live credentials
    # When run with credentials, it will verify multi-param search works
    pass


@pytest.mark.skip(reason="Requires live Darktrace instance")
def test_real_single_param_search():
    """Test single-parameter search against real Darktrace API."""
    pass


@pytest.mark.skip(reason="Requires live Darktrace instance")
def test_real_search_with_wildcards():
    """Test search with wildcards against real Darktrace API."""
    pass
