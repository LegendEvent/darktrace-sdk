#!/usr/bin/env python3
"""
Exception wiring tests for darktrace SDK.

Tests that HTTP errors and network failures are properly mapped
to the typed SDK exception hierarchy defined in darktrace.exceptions.

Run: pytest tests/test_exceptions.py -v
"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from darktrace import DarktraceClient
from darktrace.exceptions import (
    AuthenticationError,
    BadRequestError,
    DarktraceError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from darktrace.exceptions import (
    ConnectionError as DarktraceConnectionError,
)


@pytest.fixture
def client():
    """Create a DarktraceClient instance for testing."""
    return DarktraceClient(
        host="https://test.example.com",
        public_token="test_public",
        private_token="test_private",
    )


def _error_response(status_code, reason="Error", url="https://test.example.com/endpoint", headers=None):
    """Create a mock HTTP error response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.reason = reason
    resp.url = url
    resp.headers = headers or {"Content-Type": "application/json"}
    resp.json.return_value = {}
    return resp


# ==============================================================================
# Connection & Timeout Error Wrapping
# ==============================================================================


class TestConnectionErrorWrapping:
    """Test that requests.ConnectionError and Timeout are wrapped in SDK ConnectionError."""

    def test_connection_error_wrapping(self, client):
        """requests.ConnectionError is wrapped in SDK ConnectionError after retries."""
        with patch.object(client._session, "request", side_effect=requests.ConnectionError("DNS failure")):
            with patch("darktrace.dt_utils.time.sleep"):
                with pytest.raises(DarktraceConnectionError, match="Connection failed"):
                    client.devices.get()

    def test_timeout_error_wrapping(self, client):
        """requests.Timeout is wrapped in SDK ConnectionError after retries."""
        with patch.object(client._session, "request", side_effect=requests.Timeout("timed out")):
            with patch("darktrace.dt_utils.time.sleep"):
                with pytest.raises(DarktraceConnectionError, match="Connection failed"):
                    client.devices.get()

    def test_exception_chaining_preserves_cause(self, client):
        """The original requests exception is set as __cause__ on the SDK exception."""
        original = requests.ConnectionError("DNS failure")
        with patch.object(client._session, "request", side_effect=original):
            with patch("darktrace.dt_utils.time.sleep"):
                with pytest.raises(DarktraceConnectionError) as exc_info:
                    client.devices.get()
                assert exc_info.value.__cause__ is original


# ==============================================================================
# HTTP Status Error Mapping
# ==============================================================================


class TestHTTPStatusMapping:
    """Test that HTTP status codes are mapped to specific SDK exceptions."""

    def test_analyst_not_found_error(self, client):
        """404 from analyst.get_groups() raises NotFoundError with correct attributes."""
        resp = _error_response(404, reason="Not Found", url="https://test.example.com/aianalyst/groups")
        with patch.object(client._session, "request", return_value=resp):
            with pytest.raises(NotFoundError) as exc_info:
                client.analyst.get_groups()
            assert exc_info.value.status_code == 404
            assert exc_info.value.method == "GET"

    def test_pcaps_unauthorized_error(self, client):
        """401 from pcaps.get() raises AuthenticationError."""
        resp = _error_response(401, reason="Unauthorized", url="https://test.example.com/pcaps")
        with patch.object(client._session, "request", return_value=resp):
            with pytest.raises(AuthenticationError) as exc_info:
                client.pcaps.get()
            assert exc_info.value.status_code == 401

    def test_bad_request_error(self, client):
        """400 raises BadRequestError."""
        resp = _error_response(400, reason="Bad Request")
        with patch.object(client._session, "request", return_value=resp):
            with pytest.raises(BadRequestError) as exc_info:
                client.devices.get()
            assert exc_info.value.status_code == 400

    def test_rate_limit_captures_retry_after(self, client):
        """429 raises RateLimitError and captures Retry-After header."""
        resp = _error_response(
            429,
            reason="Too Many Requests",
            headers={"Content-Type": "application/json", "Retry-After": "30"},
        )
        with patch.object(client._session, "request", return_value=resp):
            with patch("darktrace.dt_utils.time.sleep"):
                with pytest.raises(RateLimitError) as exc_info:
                    client.devices.get()
                assert exc_info.value.retry_after == "30"
                assert exc_info.value.status_code == 429

    def test_server_error_500(self, client):
        """500 raises ServerError after retries exhausted."""
        resp = _error_response(500, reason="Internal Server Error")
        with patch.object(client._session, "request", return_value=resp):
            with patch("darktrace.dt_utils.time.sleep"):
                with pytest.raises(ServerError) as exc_info:
                    client.devices.get()
                assert exc_info.value.status_code == 500

    def test_forbidden_error_403(self, client):
        """403 raises ForbiddenError."""
        resp = _error_response(403, reason="Forbidden")
        with patch.object(client._session, "request", return_value=resp):
            with pytest.raises(ForbiddenError) as exc_info:
                client.devices.get()
            assert exc_info.value.status_code == 403


# ==============================================================================
# Backward Compatibility & Attributes
# ==============================================================================


class TestBackwardCompatibility:
    """Test that all SDK exceptions are backward compatible with requests.HTTPError."""

    def test_darktrace_error_backward_compat(self):
        """All SDK exceptions subclass requests.HTTPError."""
        sdk_exceptions = [
            DarktraceError,
            BadRequestError,
            AuthenticationError,
            ForbiddenError,
            NotFoundError,
            RateLimitError,
            ServerError,
            DarktraceConnectionError,
        ]
        for exc_class in sdk_exceptions:
            assert issubclass(exc_class, requests.HTTPError), (
                f"{exc_class.__name__} does not subclass requests.HTTPError"
            )

    def test_exception_message_contains_status(self, client):
        """Exception message includes status code, reason, and URL."""
        resp = _error_response(404, reason="Not Found", url="https://test.example.com/devices")
        with patch.object(client._session, "request", return_value=resp):
            with pytest.raises(NotFoundError, match="404 Not Found") as exc_info:
                client.devices.get()
            assert "https://test.example.com/devices" in str(exc_info.value)

    def test_darktrace_error_url_attribute(self, client):
        """DarktraceError stores url and method attributes."""
        resp = _error_response(401, reason="Unauthorized", url="https://test.example.com/pcaps")
        with patch.object(client._session, "request", return_value=resp):
            with pytest.raises(AuthenticationError) as exc_info:
                client.pcaps.get()
            assert exc_info.value.url == "https://test.example.com/pcaps"
            assert exc_info.value.method == "GET"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
