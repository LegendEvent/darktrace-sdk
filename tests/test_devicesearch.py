"""
Test suite for DeviceSearch module with mocked API responses.
Tests Issue #45: Multi-parameter search returns 0 results.

These tests use mocked responses to validate correct behavior without
requiring a live Darktrace instance. Fix must comply with Darktrace_API_Guide.pdf.
"""

import json
import pytest
from unittest.mock import Mock, patch
from darktrace import DarktraceClient


# Load fixture data
def load_fixture(filename):
    """Load JSON fixture from tests/fixtures/ directory."""
    with open(f"tests/fixtures/{filename}", "r") as f:
        return json.load(f)


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock()
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def client():
    """Create DarktraceClient for testing (no connection required)."""
    return DarktraceClient(
        host="https://test.darktrace.com",
        public_token="test_public_token",
        private_token="test_private_token",
        debug=False,
    )


class TestDeviceSearchMultiParameter:
    """Test multi-parameter search functionality (Issue #45)."""

    def test_multi_param_search_type_and_mac(self, client, mock_response):
        """
        Test that searching with type and mac parameters returns correct results.

        This test reproduces the bug from Issue #45 where:
        - Single parameter search works
        - Multi-parameter search returns 0 results
        - Expected: Should return devices matching both criteria

        According to Darktrace_API_Guide.pdf:
        - Criteria separated by spaces use implicit AND logic
        - Query format: field1:"value1" field2:"value2"
        """
        # Load fixture with expected response
        fixture = load_fixture("devicesearch_multi_param_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            # Call with type and mac parameters (reproducing issue #45)
            result = client.devicesearch.get(type="Laptop", mac="00:11:22:33:44:55")

            # Verify the request was made
            assert mock_get.called
            call_args = mock_get.call_args

            # Extract the query parameter from the call
            # The query should be: type:"Laptop" mac:"00:11:22:33:44:55"
            # NOT: type:"Laptop" AND mac:"00:11:22:33:44:55"
            params = call_args[1]["params"]
            assert "query" in params
            query = params["query"]

            # Verify query format matches PDF specification (space-separated, no explicit AND)
            assert query == 'type:"Laptop" mac:"00:11:22:33:44:55"', (
                f"Query should be space-separated, got: {query}"
            )

            # Verify we get the expected result
            assert result["totalCount"] == 1
            assert len(result["devices"]) == 1
            assert result["devices"][0]["did"] == 12345
            assert result["devices"][0]["typelabel"] == "Laptop"
            assert result["devices"][0]["macaddress"] == "00:11:22:33:44:55"

    def test_multi_param_search_three_filters(self, client, mock_response):
        """
        Test searching with three filter parameters.
        Verifies that all filters are properly combined.
        """
        fixture = load_fixture("devicesearch_multi_param_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(
                type="Laptop", vendor="Dell Inc.", hostname="test-laptop-01"
            )

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            # All three filters should be present, space-separated
            assert 'type:"Laptop"' in query
            assert 'vendor:"Dell Inc."' in query
            assert 'hostname:"test-laptop-01"' in query
            # Should NOT contain explicit AND between them
            assert " AND " not in query

    def test_multi_param_search_with_wildcard(self, client, mock_response):
        """
        Test multi-parameter search with wildcard values.
        Verifies wildcards are preserved in the query.
        """
        fixture = load_fixture("devicesearch_multi_param_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(type="Laptop", ip="192.168.*")

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            # Wildcard should be preserved
            assert 'type:"Laptop"' in query
            assert 'ip:"192.168.*"' in query


class TestDeviceSearchSingleParameter:
    """Test single-parameter search functionality."""

    def test_single_param_search_type(self, client, mock_response):
        """Test searching by type parameter only."""
        fixture = load_fixture("devicesearch_single_param_type_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(type="Laptop")

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            # Single parameter query should work
            assert query == 'type:"Laptop"'
            assert result["totalCount"] == 1
            assert len(result["devices"]) == 1

    def test_single_param_search_mac(self, client, mock_response):
        """Test searching by mac parameter only."""
        fixture = load_fixture("devicesearch_single_param_mac_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(mac="00:11:22:33:44:55")

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            # Single parameter query should work
            assert query == 'mac:"00:11:22:33:44:55"'
            assert result["totalCount"] == 1
            assert len(result["devices"]) == 1

    def test_single_param_search_hostname(self, client, mock_response):
        """Test searching by hostname parameter only."""
        fixture = load_fixture("devicesearch_single_param_type_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(hostname="test-laptop-01")

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            assert query == 'hostname:"test-laptop-01"'
            assert result["totalCount"] == 1


class TestDeviceSearchEmptyResults:
    """Test empty search results."""

    def test_empty_search(self, client, mock_response):
        """Test searching with no matching results."""
        fixture = load_fixture("devicesearch_empty_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(type="NonExistentType")

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            assert query == 'type:"NonExistentType"'
            assert result["totalCount"] == 0
            assert len(result["devices"]) == 0


class TestDeviceSearchQueryParameter:
    """Test raw query parameter usage."""

    def test_raw_query_parameter(self, client, mock_response):
        """Test providing a raw query string directly."""
        fixture = load_fixture("devicesearch_multi_param_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            # User provides raw query string
            result = client.devicesearch.get(
                query='type:"Laptop" mac:"00:11:22:33:44:55"'
            )

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            # Raw query should be passed through unchanged
            assert query == 'type:"Laptop" mac:"00:11:22:33:44:55"'
            assert result["totalCount"] == 1

    def test_query_with_explicit_and(self, client, mock_response):
        """
        Test raw query with explicit AND operator.
        Users can still use explicit AND if they prefer.
        """
        fixture = load_fixture("devicesearch_multi_param_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            # User provides raw query with explicit AND
            result = client.devicesearch.get(
                query='type:"Laptop" AND mac:"00:11:22:33:44:55"'
            )

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            # Raw query with explicit AND should be preserved
            assert query == 'type:"Laptop" AND mac:"00:11:22:33:44:55"'
            assert result["totalCount"] == 1


class TestDeviceSearchParameterConflict:
    """Test parameter validation (query vs filter params)."""

    def test_query_and_filter_params_raises_error(self, client):
        """
        Test that providing both query and filter parameters raises ValueError.

        This prevents ambiguous requests where it's unclear whether
        the user wants to use the raw query or have filters built.
        """
        with pytest.raises(ValueError) as exc_info:
            client.devicesearch.get(
                query='type:"Laptop"',
                type="Desktop",  # This should raise an error
            )

        assert (
            "Do not use 'query' together with tag, label, type, vendor, hostname, ip, or mac"
            in str(exc_info.value)
        )

    def test_no_query_and_no_filters(self, client, mock_response):
        """
        Test calling get() without any search parameters.
        Should return all devices (no query parameter sent).
        """
        fixture = load_fixture("devicesearch_multi_param_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(count=100)

            params = mock_get.call_args[1]["params"]

            # No query parameter should be present
            assert "query" not in params
            assert params["count"] == 100


class TestDeviceSearchAdditionalParameters:
    """Test additional parameters like count, orderBy, order, offset, etc."""

    def test_search_with_count_and_ordering(self, client, mock_response):
        """Test search with count and ordering parameters."""
        fixture = load_fixture("devicesearch_multi_param_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(
                type="Laptop", count=50, orderBy="priority", order="desc"
            )

            params = mock_get.call_args[1]["params"]

            # Verify additional parameters are passed through
            assert params["count"] == 50
            assert params["orderBy"] == "priority"
            assert params["order"] == "desc"
            assert "query" in params

    def test_search_with_pagination(self, client, mock_response):
        """Test search with pagination parameters."""
        fixture = load_fixture("devicesearch_multi_param_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(type="Laptop", count=100, offset=200)

            params = mock_get.call_args[1]["params"]

            assert params["count"] == 100
            assert params["offset"] == 200

    def test_search_with_seensince(self, client, mock_response):
        """Test search with seensince time parameter."""
        fixture = load_fixture("devicesearch_multi_param_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get(type="Laptop", seensince="1hour")

            params = mock_get.call_args[1]["params"]

            assert params["seensince"] == "1hour"


class TestDeviceSearchHelperMethods:
    """Test the convenience helper methods (get_tag, get_type, etc.)."""

    def test_get_type_helper(self, client, mock_response):
        """Test the get_type() helper method."""
        fixture = load_fixture("devicesearch_single_param_type_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get_type("Laptop")

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            # Helper should build query correctly
            assert query == 'type:"Laptop"'
            assert result["totalCount"] == 1

    def test_get_mac_helper(self, client, mock_response):
        """Test the get_mac() helper method."""
        fixture = load_fixture("devicesearch_single_param_mac_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get_mac("00:11:22:33:44:55")

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            assert query == 'mac:"00:11:22:33:44:55"'
            assert result["totalCount"] == 1

    def test_get_hostname_helper(self, client, mock_response):
        """Test the get_hostname() helper method."""
        fixture = load_fixture("devicesearch_single_param_type_response.json")
        mock_response.json.return_value = fixture

        with patch(
            "darktrace.dt_devicesearch.requests.get", return_value=mock_response
        ) as mock_get:
            result = client.devicesearch.get_hostname("test-laptop-01")

            params = mock_get.call_args[1]["params"]
            query = params["query"]

            assert query == 'hostname:"test-laptop-01"'
            assert result["totalCount"] == 1
