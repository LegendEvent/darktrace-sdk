#!/usr/bin/env python3
"""
Comprehensive HMAC signature tests for DarktraceAuth.

Tests cover: generate_signature() with known input vectors, get_headers()
with/without json_body, parameter sorting, date format, and edge cases.

Run: pytest tests/test_auth.py -v
"""

import hashlib
import hmac
import json
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from darktrace.auth import DarktraceAuth

# ==============================================================================
# FIXTURES
# ==============================================================================

PUBLIC_TOKEN = "test_public_token"
PRIVATE_TOKEN = "test_private_token"


@pytest.fixture
def auth():
    """Create a DarktraceAuth instance for testing."""
    return DarktraceAuth(public_token=PUBLIC_TOKEN, private_token=PRIVATE_TOKEN)


# ==============================================================================
# HELPER
# ==============================================================================


def compute_signature(private_token: str, message: str) -> str:
    """Compute HMAC-SHA1 signature matching auth.py algorithm."""
    return hmac.new(
        private_token.encode("ASCII"),
        message.encode("ASCII"),
        hashlib.sha1,
    ).hexdigest()


def mock_utc_now(date_str: str):
    """Return a patcher that makes datetime.now(timezone.utc) return a fixed datetime."""
    _ = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    return patch("darktrace.auth.datetime")


# ==============================================================================
# TEST VECTORS — generate_signature()
# ==============================================================================


class TestGenerateSignature:
    """Test generate_signature() with hardcoded HMAC-SHA1 test vectors."""

    # Vector 1: Simple path, no params, no body
    # message = "/devices\ntest_public_token\n2025-01-15 12:30:00"
    # HMAC-SHA1(private_token, message) computed offline
    VECTOR_1_PATH = "/devices"
    VECTOR_1_DATE = "2025-01-15 12:30:00"
    VECTOR_1_EXPECTED = "e3c82b28eb735735b9d288d6d2d63b14cba2e008"

    # Vector 2: Path with sorted query params
    # message = "/devices?aparam=aval&mparam=mval&zparam=zval\ntest_public_token\n2025-06-01 00:00:00"
    VECTOR_2_PATH = "/devices?aparam=aval&mparam=mval&zparam=zval"
    VECTOR_2_DATE = "2025-06-01 00:00:00"
    VECTOR_2_EXPECTED = "2f247e5248b933fccf527bebc479248613c320a4"

    # Vector 3: Path with JSON body appended
    # message = '/modelbreaches/101/comments?{"message":"Test Comment","priority":"high"}\n...'
    VECTOR_3_PATH = '/modelbreaches/101/comments?{"message":"Test Comment","priority":"high"}'
    VECTOR_3_DATE = "2023-12-25 23:59:59"
    VECTOR_3_EXPECTED = "b309669f63f10c0de47230144c623b6869ebfac3"

    def test_vector1_simple_path(self, auth):
        """Vector 1: Simple path with no query params or body."""
        result = auth.generate_signature(self.VECTOR_1_PATH, self.VECTOR_1_DATE)
        assert result == self.VECTOR_1_EXPECTED
        # Cross-check with local computation
        message = f"{self.VECTOR_1_PATH}\n{PUBLIC_TOKEN}\n{self.VECTOR_1_DATE}"
        assert result == compute_signature(PRIVATE_TOKEN, message)

    def test_vector2_path_with_params(self, auth):
        """Vector 2: Path with sorted query parameters."""
        result = auth.generate_signature(self.VECTOR_2_PATH, self.VECTOR_2_DATE)
        assert result == self.VECTOR_2_EXPECTED
        message = f"{self.VECTOR_2_PATH}\n{PUBLIC_TOKEN}\n{self.VECTOR_2_DATE}"
        assert result == compute_signature(PRIVATE_TOKEN, message)

    def test_vector3_path_with_json_body(self, auth):
        """Vector 3: Path with compact JSON body appended as query parameter."""
        result = auth.generate_signature(self.VECTOR_3_PATH, self.VECTOR_3_DATE)
        assert result == self.VECTOR_3_EXPECTED
        message = f"{self.VECTOR_3_PATH}\n{PUBLIC_TOKEN}\n{self.VECTOR_3_DATE}"
        assert result == compute_signature(PRIVATE_TOKEN, message)


# ==============================================================================
# TEST VECTORS — get_headers() return format
# ==============================================================================


class TestGetHeadersFormat:
    """Test get_headers() return structure and header keys."""

    @mock_utc_now("2025-01-15 12:30:00")
    def test_returns_dict_with_headers_and_params(self, mock_dt, auth):
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime
        result = auth.get_headers("/devices")
        assert "headers" in result
        assert "params" in result

    @mock_utc_now("2025-01-15 12:30:00")
    def test_headers_contain_required_keys(self, mock_dt, auth):
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime
        result = auth.get_headers("/devices")
        headers = result["headers"]
        assert "DTAPI-Token" in headers
        assert "DTAPI-Date" in headers
        assert "DTAPI-Signature" in headers
        assert "Content-Type" in headers

    @mock_utc_now("2025-01-15 12:30:00")
    def test_dtapi_token_is_public_token(self, mock_dt, auth):
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime
        result = auth.get_headers("/devices")
        assert result["headers"]["DTAPI-Token"] == PUBLIC_TOKEN

    @mock_utc_now("2025-01-15 12:30:00")
    def test_dtapi_date_format(self, mock_dt, auth):
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime
        result = auth.get_headers("/devices")
        assert result["headers"]["DTAPI-Date"] == "2025-01-15 12:30:00"

    @mock_utc_now("2025-01-15 12:30:00")
    def test_content_type_is_application_json(self, mock_dt, auth):
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime
        result = auth.get_headers("/devices")
        assert result["headers"]["Content-Type"] == "application/json"


# ==============================================================================
# TEST: get_headers() signature matches generate_signature()
# ==============================================================================


class TestGetHeadersSignature:
    """Test that get_headers() computes the correct signature internally."""

    @mock_utc_now("2025-01-15 12:30:00")
    def test_simple_path_signature(self, mock_dt, auth):
        """Simple path: signature matches manual HMAC computation."""
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        result = auth.get_headers("/devices")
        expected_sig = compute_signature(
            PRIVATE_TOKEN,
            "/devices\ntest_public_token\n2025-01-15 12:30:00",
        )
        assert result["headers"]["DTAPI-Signature"] == expected_sig

    @mock_utc_now("2025-06-01 00:00:00")
    def test_params_are_sorted_in_signature(self, mock_dt, auth):
        """Params sorted alphabetically; signature matches sorted path."""
        mock_dt.now.return_value = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        # Pass params in non-sorted order
        params = {"zparam": "zval", "aparam": "aval", "mparam": "mval"}
        result = auth.get_headers("/devices", params=params)

        # Expected path has sorted params
        expected_path = "/devices?aparam=aval&mparam=mval&zparam=zval"
        expected_sig = compute_signature(
            PRIVATE_TOKEN,
            f"{expected_path}\ntest_public_token\n2025-06-01 00:00:00",
        )
        assert result["headers"]["DTAPI-Signature"] == expected_sig

    @mock_utc_now("2023-12-25 23:59:59")
    def test_json_body_in_signature(self, mock_dt, auth):
        """JSON body is compact-serialized and appended with '?' separator."""
        mock_dt.now.return_value = datetime(2023, 12, 25, 23, 59, 59, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2023, 12, 25, 23, 59, 59, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        body = {"message": "Test Comment", "priority": "high"}
        result = auth.get_headers("/modelbreaches/101/comments", json_body=body)

        json_string = json.dumps(body, separators=(",", ":"))
        expected_path = f"/modelbreaches/101/comments?{json_string}"
        expected_sig = compute_signature(
            PRIVATE_TOKEN,
            f"{expected_path}\ntest_public_token\n2023-12-25 23:59:59",
        )
        assert result["headers"]["DTAPI-Signature"] == expected_sig

    @mock_utc_now("2024-07-04 10:20:30")
    def test_params_and_body_combined(self, mock_dt, auth):
        """When both params and body exist, body uses '&' separator."""
        mock_dt.now.return_value = datetime(2024, 7, 4, 10, 20, 30, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2024, 7, 4, 10, 20, 30, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        params = {"pagesize": 100, "from": 0}
        body = {"filter": "active"}
        result = auth.get_headers("/modelbreaches", params=params, json_body=body)

        # Sorted params: from=0&pagesize=100, then & compact JSON
        json_string = json.dumps(body, separators=(",", ":"))
        expected_path = f"/modelbreaches?from=0&pagesize=100&{json_string}"
        expected_sig = compute_signature(
            PRIVATE_TOKEN,
            f"{expected_path}\ntest_public_token\n2024-07-04 10:20:30",
        )
        assert result["headers"]["DTAPI-Signature"] == expected_sig


# ==============================================================================
# TEST: Parameter sorting
# ==============================================================================


class TestParameterSorting:
    """Test that get_headers() sorts parameters alphabetically."""

    @mock_utc_now("2025-01-15 12:30:00")
    def test_params_returned_sorted(self, mock_dt, auth):
        """Returned params dict has keys in sorted order."""
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        params = {"zebra": 3, "alpha": 1, "middle": 2}
        result = auth.get_headers("/test", params=params)
        sorted_keys = list(result["params"].keys())
        assert sorted_keys == ["alpha", "middle", "zebra"]

    @mock_utc_now("2025-01-15 12:30:00")
    def test_single_param_no_sorting_needed(self, mock_dt, auth):
        """Single param: returned as-is."""
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        result = auth.get_headers("/test", params={"key": "value"})
        assert result["params"] == {"key": "value"}

    @mock_utc_now("2025-01-15 12:30:00")
    def test_numeric_param_values_sorted_correctly(self, mock_dt, auth):
        """Numeric values in params are preserved after sorting."""
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        params = {"limit": 50, "offset": 0, "active": True}
        result = auth.get_headers("/devices", params=params)
        sorted_keys = list(result["params"].keys())
        assert sorted_keys == ["active", "limit", "offset"]


# ==============================================================================
# TEST: Edge cases
# ==============================================================================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @mock_utc_now("2025-01-15 12:30:00")
    def test_none_params(self, mock_dt, auth):
        """params=None: returned as None, no query string in signature."""
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        result = auth.get_headers("/devices", params=None)
        assert result["params"] is None
        # Signature should be for plain path only
        expected_sig = compute_signature(
            PRIVATE_TOKEN,
            "/devices\ntest_public_token\n2025-01-15 12:30:00",
        )
        assert result["headers"]["DTAPI-Signature"] == expected_sig

    @mock_utc_now("2025-01-15 12:30:00")
    def test_empty_params_dict(self, mock_dt, auth):
        """Empty dict params: treated as no params (len == 0 check)."""
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        result = auth.get_headers("/devices", params={})
        assert result["params"] == {}
        # Empty dict is falsy-ish but len==0, so no query string
        expected_sig = compute_signature(
            PRIVATE_TOKEN,
            "/devices\ntest_public_token\n2025-01-15 12:30:00",
        )
        assert result["headers"]["DTAPI-Signature"] == expected_sig

    @mock_utc_now("2025-03-15 08:45:00")
    def test_nested_json_body(self, mock_dt, auth):
        """Nested JSON body: compact serialization preserves structure."""
        mock_dt.now.return_value = datetime(2025, 3, 15, 8, 45, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 3, 15, 8, 45, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        body = {"action": {"type": "block", "duration": 3600}, "comment": "test"}
        result = auth.get_headers("/antigena/actions", json_body=body)

        json_string = json.dumps(body, separators=(",", ":"))
        expected_path = f"/antigena/actions?{json_string}"
        expected_sig = compute_signature(
            PRIVATE_TOKEN,
            f"{expected_path}\ntest_public_token\n2025-03-15 08:45:00",
        )
        assert result["headers"]["DTAPI-Signature"] == expected_sig

    @mock_utc_now("2025-01-15 12:30:00")
    def test_no_params_no_body(self, mock_dt, auth):
        """Default call with just a path: minimal signature."""
        mock_dt.now.return_value = datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.now.side_effect = lambda tz=None: datetime(2025, 1, 15, 12, 30, 0, tzinfo=timezone.utc)
        mock_dt.strptime = datetime.strptime

        result = auth.get_headers("/status")
        assert result["params"] is None
        expected_sig = compute_signature(
            PRIVATE_TOKEN,
            "/status\ntest_public_token\n2025-01-15 12:30:00",
        )
        assert result["headers"]["DTAPI-Signature"] == expected_sig

    def test_generate_signature_deterministic(self, auth):
        """Same inputs always produce same signature."""
        sig1 = auth.generate_signature("/devices", "2025-01-15 12:30:00")
        sig2 = auth.generate_signature("/devices", "2025-01-15 12:30:00")
        assert sig1 == sig2

    def test_different_paths_produce_different_signatures(self, auth):
        """Different paths produce different signatures."""
        date = "2025-01-15 12:30:00"
        sig1 = auth.generate_signature("/devices", date)
        sig2 = auth.generate_signature("/devicesearch", date)
        assert sig1 != sig2

    def test_different_dates_produce_different_signatures(self, auth):
        """Different dates produce different signatures."""
        sig1 = auth.generate_signature("/devices", "2025-01-15 12:30:00")
        sig2 = auth.generate_signature("/devices", "2025-01-15 12:30:01")
        assert sig1 != sig2


# ==============================================================================
# TEST: repr
# ==============================================================================


class TestRepr:
    """Test DarktraceAuth.__repr__()."""

    def test_repr_masks_public_token(self):
        auth = DarktraceAuth(public_token="abcdef123456", private_token="secret")
        r = repr(auth)
        assert "abcd..." in r
        assert "abcdef123456" not in r

    def test_repr_short_token(self):
        auth = DarktraceAuth(public_token="ab", private_token="secret")
        r = repr(auth)
        assert "***" in r

    def test_repr_format(self):
        auth = DarktraceAuth(public_token="test_pub", private_token="secret")
        r = repr(auth)
        assert r.startswith("<DarktraceAuth public_token=")


# ==============================================================================
# TEST: Hardcoded HMAC-SHA1 vectors (cross-validated)
# ==============================================================================


class TestHardcodedVectors:
    """
    Hardcoded HMAC-SHA1 test vectors computed independently from auth.py.
    These use known inputs and pre-computed hex digests.
    """

    # All vectors use: public="test_public_token", private="test_private_token"
    # Message format: "{path}\\n{public_token}\\n{date}"
    # Algorithm: HMAC-SHA1(private_token.encode('ASCII'), message.encode('ASCII'))

    VECTORS = [
        {
            "name": "simple_path",
            "path": "/devices",
            "date": "2025-01-15 12:30:00",
            "expected": "e3c82b28eb735735b9d288d6d2d63b14cba2e008",
        },
        {
            "name": "sorted_query_params",
            "path": "/devices?aparam=aval&mparam=mval&zparam=zval",
            "date": "2025-06-01 00:00:00",
            "expected": "2f247e5248b933fccf527bebc479248613c320a4",
        },
        {
            "name": "json_body_appended",
            "path": '/modelbreaches/101/comments?{"message":"Test Comment","priority":"high"}',
            "date": "2023-12-25 23:59:59",
            "expected": "b309669f63f10c0de47230144c623b6869ebfac3",
        },
    ]

    @pytest.mark.parametrize(
        "path,date,expected",
        [(v["path"], v["date"], v["expected"]) for v in VECTORS],
        ids=[v["name"] for v in VECTORS],
    )
    def test_hardcoded_vector(self, auth, path, date, expected):
        """Verify pre-computed HMAC-SHA1 signature matches."""
        assert auth.generate_signature(path, date) == expected
