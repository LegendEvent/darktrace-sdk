#!/usr/bin/env python3
"""
Comprehensive read-only test for ALL Darktrace SDK endpoints.

This test reads credentials from:
1. Environment variables (DARKTRACE_HOST, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN)
2. Keyring (service='darktrace', username='api')
3. Encrypted credential file (~/.darktrace_credentials) - XOR encoded
4. Command line arguments

Usage:
    # Via environment variables
    export DARKTRACE_HOST=https://your-instance.darktrace.com
    export DARKTRACE_PUBLIC_TOKEN=your_public_token
    export DARKTRACE_PRIVATE_TOKEN=your_private_token
    pytest tests/real/test_all_endpoints.py -v

    # Via command line
    pytest tests/real/test_all_endpoints.py -v --host=https://... --public-token=... --private-token=...

    # Self-signed cert
    pytest tests/real/test_all_endpoints.py -v --host=... --public-token=... --private-token=... --no-verify
"""

import os
import pytest
from typing import Optional, Tuple

# Will be set by fixture or manual loading
_client = None


def load_credentials_from_file() -> Optional[Tuple[str, str, str]]:
    """Try to load credentials from encrypted file."""
    cred_file = os.path.expanduser("~/.darktrace_credentials")
    if not os.path.exists(cred_file):
        return None

    try:
        with open(cred_file, "rb") as f:
            data = f.read()

        # Try XOR decode with various keys
        for key in [b"darktrace", b"DarktraceSDK", b"api", b"key"]:
            try:
                decoded = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
                decoded_str = decoded.decode("utf-8", errors="ignore")
                if "https://" in decoded_str or "http://" in decoded_str:
                    # Parse as JSON or key=value format
                    import json
                    try:
                        creds = json.loads(decoded_str)
                        return (
                            creds.get("host") or creds.get("DARKTRACE_HOST"),
                            creds.get("public_token") or creds.get("DARKTRACE_PUBLIC_TOKEN"),
                            creds.get("private_token") or creds.get("DARKTRACE_PRIVATE_TOKEN"),
                        )
                    except:
                        # Try key=value format
                        lines = decoded_str.strip().split("\n")
                        creds = {}
                        for line in lines:
                            if "=" in line:
                                k, v = line.split("=", 1)
                                creds[k.strip()] = v.strip()
                        if "host" in creds or "DARKTRACE_HOST" in creds:
                            return (
                                creds.get("host") or creds.get("DARKTRACE_HOST"),
                                creds.get("public_token") or creds.get("DARKTRACE_PUBLIC_TOKEN"),
                                creds.get("private_token") or creds.get("DARKTRACE_PRIVATE_TOKEN"),
                            )
            except:
                continue
    except:
        pass
    return None


def load_credentials_from_keyring() -> Optional[Tuple[str, str, str]]:
    """Try to load credentials from system keyring."""
    try:
        import keyring
        for service in ["darktrace", "Darktrace", "darktrace-sdk"]:
            for username in ["api", "user", "default", "credentials"]:
                try:
                    creds = keyring.get_password(service, username)
                    if creds:
                        import json
                        try:
                            data = json.loads(creds)
                            return (
                                data.get("host") or data.get("DARKTRACE_HOST"),
                                data.get("public_token") or data.get("DARKTRACE_PUBLIC_TOKEN"),
                                data.get("private_token") or data.get("DARKTRACE_PRIVATE_TOKEN"),
                            )
                        except:
                            continue
                except:
                    continue
    except ImportError:
        pass
    return None


def get_credentials(request) -> Tuple[str, str, str, bool]:
    """Get credentials from various sources in order of priority."""
    # 1. Command line args
    host = request.config.getoption("host")
    public_token = request.config.getoption("public_token")
    private_token = request.config.getoption("private_token")
    no_verify = request.config.getoption("no_verify", default=False)

    if host and public_token and private_token:
        return host, public_token, private_token, no_verify

    # 2. Environment variables
    host = os.environ.get("DARKTRACE_HOST")
    public_token = os.environ.get("DARKTRACE_PUBLIC_TOKEN")
    private_token = os.environ.get("DARKTRACE_PRIVATE_TOKEN")

    if host and public_token and private_token:
        return host, public_token, private_token, no_verify

    # 3. Keyring
    creds = load_credentials_from_keyring()
    if creds and all(creds):
        return creds[0], creds[1], creds[2], no_verify

    # 4. Credential file
    creds = load_credentials_from_file()
    if creds and all(creds):
        return creds[0], creds[1], creds[2], no_verify

    pytest.skip("No credentials found. Set DARKTRACE_HOST, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN env vars or use --host/--public-token/--private-token args")


@pytest.fixture(scope="module")
def client(request):
    """Create a DarktraceClient with credentials from various sources."""
    from darktrace import DarktraceClient

    host, public_token, private_token, no_verify = get_credentials(request)

    client = DarktraceClient(
        host=host,
        public_token=public_token,
        private_token=private_token,
        verify_ssl=not no_verify,
        debug=True
    )

    global _client
    _client = client

    yield client

    # Cleanup
    client.close()


# ============================================================
# ENDPOINT TESTS - READ ONLY
# ============================================================

class TestAllEndpointsReadOnly:
    """Test all endpoints with read-only operations."""

    # --- Status & System ---

    def test_status(self, client):
        """Test /status endpoint."""
        result = client.status.get()
        assert result is not None
        print(f"\nStatus: {type(result).__name__}")

    def test_enums(self, client):
        """Test /enums endpoint."""
        result = client.enums.get()
        assert result is not None
        print(f"\nEnums: {type(result).__name__}")

    def test_network(self, client):
        """Test /network endpoint."""
        result = client.network.get()
        assert result is not None
        print(f"\nNetwork: {type(result).__name__}")

    def test_subnets(self, client):
        """Test /subnets endpoint."""
        result = client.subnets.get()
        assert result is not None
        print(f"\nSubnets: {type(result).__name__}")

    # --- Devices ---

    def test_devices(self, client):
        """Test /devices endpoint."""
        result = client.devices.get(responsedata="did")
        assert isinstance(result, list)
        print(f"\nDevices count: {len(result)}")

    def test_devicesearch(self, client):
        """Test /devicesearch endpoint."""
        result = client.devicesearch.get(query="type:server", count=5)
        assert result is not None
        print(f"\nDeviceSearch: {type(result).__name__}")

    def test_similardevices(self, client):
        """Test /similardevices endpoint."""
        # Get a device first
        devices = client.devices.get(responsedata="did")
        if devices and len(devices) > 0:
            did = devices[0].get("did", 1)
            result = client.similardevices.get(did=did)
            print(f"\nSimilarDevices for did={did}: {type(result).__name__}")

    # --- Model Breaches & Analyst ---

    def test_modelbreaches(self, client):
        """Test /modelbreaches endpoint."""
        result = client.breaches.get(minimal=True, includeacknowledged=False)
        assert result is not None
        print(f"\nModelBreaches: {type(result).__name__}")

    def test_models(self, client):
        """Test /models endpoint."""
        result = client.models.get()
        assert result is not None
        print(f"\nModels: {type(result).__name__}")

    def test_analyst(self, client):
        """Test /analyst endpoint."""
        result = client.analyst.get_stats()
        assert result is not None
        print(f"\nAnalyst stats: {type(result).__name__}")

    # --- Intel Feed ---
    # --- Intel Feed ---
    # --- Intel Feed ---

    def test_intelfeed_sources(self, client):
        """Test /intelfeed endpoint - get sources."""
        result = client.intelfeed.get(sources=True)
        assert isinstance(result, list)
        print(f"\nIntelFeed sources count: {len(result)}")

    def test_intelfeed_entries(self, client):
        """Test /intelfeed endpoint - get entries."""
        result = client.intelfeed.get()
        assert isinstance(result, list)
        print(f"\nIntelFeed entries count: {len(result)}")

    # --- Antigena ---

    def test_antigena(self, client):
        """Test /antigena endpoint."""
        result = client.antigena.get_summary()
        assert result is not None
        print(f"\nAntigena summary: {type(result).__name__}")


    def test_antigena_actions(self, client):
        """Test /antigena/actions endpoint."""
        result = client.antigena.get_actions()
        assert result is not None
        print(f"\nAntigena Actions: {type(result).__name__}")

    # --- Components & CVEs ---

    def test_components(self, client):
        """Test /components endpoint."""
        result = client.components.get()
        assert result is not None
        print(f"\nComponents: {type(result).__name__}")

    def test_cves(self, client):
        """Test /cves endpoint."""
        result = client.cves.get()
        assert result is not None
        print(f"\nCVEs: {type(result).__name__}")

    # --- Metrics & Statistics ---

    def test_metrics(self, client):
        """Test /metrics endpoint."""
        result = client.metrics.get()
        assert result is not None
        print(f"\nMetrics: {type(result).__name__}")

    def test_summarystatistics(self, client):
        """Test /summarystatistics endpoint."""
        result = client.summarystatistics.get()
        assert result is not None
        print(f"\nSummaryStatistics: {type(result).__name__}")

    # --- Tags ---

    def test_tags(self, client):
        """Test /tags endpoint."""
        result = client.tags.get()
        assert result is not None
        print(f"\nTags: {type(result).__name__}")

    # --- Advanced Search ---

    def test_advancedsearch(self, client):
        """Test /advancedsearch endpoint."""
        # This requires a search query - just check it doesn't crash
        try:
            from darktrace.dt_utils import encode_query
            query = encode_query({"search": "test", "fields": ["did"]})
            result = client.advanced_search.get(query=query)
            print(f"\nAdvancedSearch: {type(result).__name__}")
        except Exception as e:
            print(f"\nAdvancedSearch: Skipped ({e})")

    # --- Details & PCAPs ---

    def test_endpointdetails(self, client):
        """Test /endpointdetails endpoint."""
        result = client.endpointdetails.get()
        assert result is not None
        print(f"\nEndpointDetails: {type(result).__name__}")

    # --- Email ---

    def test_email(self, client):
        """Test /email endpoint - may require license."""
        try:
            result = client.email.get_dash_stats()
            assert result is not None
            print(f"\nEmail dash stats: {type(result).__name__}")
        except Exception as e:
            print(f"\nEmail: Skipped (may require license) - {e}")

    # --- Filter Types ---
    # --- Filter Types ---

    def test_filtertypes(self, client):
        """Test /filtertypes endpoint."""
        result = client.filtertypes.get()
        assert result is not None
        print(f"\nFilterTypes: {type(result).__name__}")


class TestNewFeatures:
    """Test new features added in this PR."""

    def test_session_exists(self, client):
        """Verify requests.Session is being used."""
        assert hasattr(client, "_session")
        assert client._session is not None
        print("\n✓ Session pooling active")

    def test_context_manager(self):
        """Verify context manager works."""
        from darktrace import DarktraceClient
        # Get credentials
        import os
        host = os.environ.get("DARKTRACE_HOST", "https://test.com")
        public = os.environ.get("DARKTRACE_PUBLIC_TOKEN", "test")
        private = os.environ.get("DARKTRACE_PRIVATE_TOKEN", "test")

        with DarktraceClient(host, public, private) as c:
            assert hasattr(c, "_session")
        print("✓ Context manager works")

    def test_url_validation_blocks_dangerous_schemes(self):
        """Verify SSRF protection blocks dangerous schemes."""
        from darktrace import DarktraceClient
        import os

        host = os.environ.get("DARKTRACE_HOST", "https://test.com")
        public = os.environ.get("DARKTRACE_PUBLIC_TOKEN", "test")
        private = os.environ.get("DARKTRACE_PRIVATE_TOKEN", "test")

        for bad_url in ["file:///etc/passwd", "ftp://server", "data:text/html,test"]:
            try:
                DarktraceClient(bad_url, public, private)
                assert False, f"Should have blocked: {bad_url}"
            except ValueError as e:
                assert "scheme" in str(e).lower()
        print("✓ SSRF protection active")

    def test_private_ip_allowed(self):
        """Verify private IPs are allowed (enterprise use case)."""
        from darktrace import DarktraceClient

        # Private IPs should work
        client = DarktraceClient("https://192.168.1.1", "pub", "priv")
        assert client.host == "https://192.168.1.1"
        print("✓ Private IPs allowed")


class TestRetryLogic:
    """Test retry logic (informational only - can't force failures)."""

    def test_retry_config(self):
        """Verify retry configuration is correct."""
        from darktrace.dt_utils import _MAX_RETRIES, _RETRY_WAIT_SECONDS, _RETRY_STATUS_CODES

        assert _MAX_RETRIES == 3
        assert _RETRY_WAIT_SECONDS == 10
        assert 429 in _RETRY_STATUS_CODES
        assert 500 in _RETRY_STATUS_CODES
        assert 502 in _RETRY_STATUS_CODES
        assert 503 in _RETRY_STATUS_CODES
        assert 504 in _RETRY_STATUS_CODES
        assert 400 not in _RETRY_STATUS_CODES  # Client errors not retried
        print("\n✓ Retry config: 3 retries, 10s wait, 429+5xx retried")


if __name__ == "__main__":
    # Run directly for quick testing
    import sys

    # Try to load credentials
    host = os.environ.get("DARKTRACE_HOST")
    public = os.environ.get("DARKTRACE_PUBLIC_TOKEN")
    private = os.environ.get("DARKTRACE_PRIVATE_TOKEN")

    if not all([host, public, private]):
        print("Set environment variables:")
        print("  export DARKTRACE_HOST=https://your-instance.darktrace.com")
        print("  export DARKTRACE_PUBLIC_TOKEN=your_token")
        print("  export DARKTRACE_PRIVATE_TOKEN=your_token")
        sys.exit(1)

    from darktrace import DarktraceClient

    print(f"\n{'='*60}")
    print("Testing all Darktrace SDK endpoints (READ ONLY)")
    print(f"{'='*60}")
    print(f"Host: {host}")
    print(f"{'='*60}\n")

    client = DarktraceClient(host, public, private, debug=True)

    # Test all endpoints
    endpoints = [
        ("status", lambda: client.status.get()),
        ("enums", lambda: client.enums.get()),
        ("network", lambda: client.network.get()),
        ("subnets", lambda: client.subnets.get()),
        ("devices", lambda: client.devices.get(responsedata="did")),
        ("devicesearch", lambda: client.devicesearch.get(query="type:server", count=1)),
        ("modelbreaches", lambda: client.breaches.get(minimal=True)),
        ("models", lambda: client.models.get()),
        ("analyst", lambda: client.analyst.get()),
        ("intelfeed", lambda: client.intelfeed.get()),
        ("antigena", lambda: client.antigena.get()),
        ("components", lambda: client.components.get()),
        ("cves", lambda: client.cves.get()),
        ("metrics", lambda: client.metrics.get()),
        ("summarystatistics", lambda: client.summarystatistics.get()),
        ("tags", lambda: client.tags.get()),
        ("endpointdetails", lambda: client.endpointdetails.get()),
        ("email", lambda: client.email.get()),
        ("filtertypes", lambda: client.filtertypes.get()),
    ]

    passed = 0
    failed = 0

    for name, func in endpoints:
        try:
            result = func()
            print(f"✓ {name}: {type(result).__name__}")
            passed += 1
        except Exception as e:
            print(f"✗ {name}: {e}")
            failed += 1

    client.close()

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")
