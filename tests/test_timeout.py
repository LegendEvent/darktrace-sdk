"""
Test suite for timeout configuration in Darktrace SDK.

Tests verify that timeout is properly passed to requests at:
1. Client level (default timeout)
2. Per-request level (override)
3. Tuple format (connect, read timeouts)
"""
import pytest
from unittest.mock import Mock, patch, call
from darktrace import DarktraceClient, TimeoutType


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock()
    response.raise_for_status = Mock()
    response.json.return_value = {"devices": []}
    return response


class TestClientLevelTimeout:
    """Test client-level timeout configuration."""

    def test_client_with_no_timeout_default(self, mock_response):
        """Client without timeout should pass None to requests (no timeout)."""
        client = DarktraceClient(
            host="https://test.darktrace.com",
            public_token="test_public",
            private_token="test_private",
        )
        assert client.timeout is None

        with patch("darktrace.dt_devices.requests.get", return_value=mock_response) as mock_get:
            client.devices.get()
            
            # Verify timeout=None was passed (no timeout)
            call_kwargs = mock_get.call_args[1]
            assert call_kwargs.get("timeout") is None

    def test_client_with_float_timeout(self, mock_response):
        """Client with float timeout should pass it to all requests."""
        client = DarktraceClient(
            host="https://test.darktrace.com",
            public_token="test_public",
            private_token="test_private",
            timeout=30.0,
        )
        assert client.timeout == 30.0

        with patch("darktrace.dt_devices.requests.get", return_value=mock_response) as mock_get:
            client.devices.get()
            
            call_kwargs = mock_get.call_args[1]
            assert call_kwargs.get("timeout") == 30.0

    def test_client_with_tuple_timeout(self, mock_response):
        """Client with tuple timeout should pass (connect, read) tuple."""
        client = DarktraceClient(
            host="https://test.darktrace.com",
            public_token="test_public",
            private_token="test_private",
            timeout=(5.0, 30.0),
        )
        assert client.timeout == (5.0, 30.0)

        with patch("darktrace.dt_devices.requests.get", return_value=mock_response) as mock_get:
            client.devices.get()
            
            call_kwargs = mock_get.call_args[1]
            assert call_kwargs.get("timeout") == (5.0, 30.0)


class TestPerRequestTimeout:
    """Test per-request timeout override."""

    def test_per_request_override_float(self, mock_response):
        """Per-request timeout should override client default."""
        client = DarktraceClient(
            host="https://test.darktrace.com",
            public_token="test_public",
            private_token="test_private",
            timeout=30.0,  # Client default
        )

        with patch("darktrace.dt_devices.requests.get", return_value=mock_response) as mock_get:
            client.devices.get(timeout=60.0)  # Per-request override
            
            call_kwargs = mock_get.call_args[1]
            assert call_kwargs.get("timeout") == 60.0

    def test_per_request_override_tuple(self, mock_response):
        """Per-request tuple timeout should work."""
        client = DarktraceClient(
            host="https://test.darktrace.com",
            public_token="test_public",
            private_token="test_private",
        )

        with patch("darktrace.dt_devices.requests.get", return_value=mock_response) as mock_get:
            client.devices.get(timeout=(10.0, 60.0))
            
            call_kwargs = mock_get.call_args[1]
            assert call_kwargs.get("timeout") == (10.0, 60.0)

    def test_per_request_none_uses_client_default(self, mock_response):
        """Per-request None should use client default."""
        client = DarktraceClient(
            host="https://test.darktrace.com",
            public_token="test_public",
            private_token="test_private",
            timeout=30.0,
        )

        with patch("darktrace.dt_devices.requests.get", return_value=mock_response) as mock_get:
            # Explicitly passing None should use client default
            client.devices.get(timeout=None)
            
            call_kwargs = mock_get.call_args[1]
            assert call_kwargs.get("timeout") == 30.0


class TestTimeoutType:
    """Test TimeoutType export for type hints."""

    def test_timeout_type_import(self):
        """TimeoutType should be importable from darktrace."""
        from darktrace import TimeoutType
        assert TimeoutType is not None

    def test_timeout_type_annotation(self):
        """TimeoutType should work as type annotation."""
        timeout: TimeoutType = 30.0
        assert timeout == 30.0

        timeout_tuple: TimeoutType = (5.0, 30.0)
        assert timeout_tuple == (5.0, 30.0)

        timeout_none: TimeoutType = None
        assert timeout_none is None


class TestMultipleEndpoints:
    """Test timeout works across different endpoint types."""

    def test_timeout_on_get_request(self, mock_response):
        """Timeout should work on GET requests."""
        client = DarktraceClient(
            host="https://test.darktrace.com",
            public_token="test_public",
            private_token="test_private",
            timeout=45.0,
        )

        with patch("darktrace.dt_devices.requests.get", return_value=mock_response) as mock_get:
            client.devices.get()
            assert mock_get.call_args[1]["timeout"] == 45.0

    def test_timeout_on_post_request(self, mock_response):
        """Timeout should work on POST requests."""
        client = DarktraceClient(
            host="https://test.darktrace.com",
            public_token="test_public",
            private_token="test_private",
            timeout=60.0,
        )
        mock_response.json.return_value = {"tid": 1}

        with patch("darktrace.dt_tags.requests.post", return_value=mock_response) as mock_post:
            client.tags.create(name="test-tag")
            assert mock_post.call_args[1]["timeout"] == 60.0

    def test_timeout_on_delete_request(self, mock_response):
        """Timeout should work on DELETE requests."""
        client = DarktraceClient(
            host="https://test.darktrace.com",
            public_token="test_public",
            private_token="test_private",
            timeout=15.0,
        )
        mock_response.json.return_value = {"deleted": True}

        with patch("darktrace.dt_tags.requests.delete", return_value=mock_response) as mock_delete:
            client.tags.delete(tag_id="123")
            assert mock_delete.call_args[1]["timeout"] == 15.0
