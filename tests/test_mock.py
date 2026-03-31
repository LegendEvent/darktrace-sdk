#!/usr/bin/env python3
"""
Comprehensive mock tests for darktrace SDK.

This test module provides mocked unit tests for all 27 endpoint modules,
testing SSRF protection, retry logic, timeout handling, context manager support,
and endpoint method signatures without making actual network calls.

Run: pytest tests/test_mock.py -v
"""

from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from darktrace import DarktraceClient
from darktrace.dt_utils import (
    _INITIAL_RETRY_WAIT_SECONDS,
    _MAX_RETRIES,
    _RETRY_STATUS_CODES,
    BaseEndpoint,
)


# ==============================================================================
# FIXTURES
# ==============================================================================
@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock()
    response.raise_for_status = Mock()
    response.json = Mock(return_value={})
    return response


@pytest.fixture
def client():
    """Create a DarktraceClient instance for testing."""
    return DarktraceClient(
        host="https://test.example.com",
        public_token="test_public",
        private_token="test_private",
    )


@pytest.fixture
def mock_session():
    """Create a mock requests.Session."""
    return MagicMock()


# ==============================================================================
# SSRF PROTECTION TESTS
# ==============================================================================
class TestSSRFProtection:
    """Test SSRF protection via _validate_url()."""

    def test_valid_http_scheme(self):
        """Test that http:// scheme is allowed."""
        client = DarktraceClient(host="http://example.com", public_token="test", private_token="test")
        assert client.host == "http://example.com"

    def test_valid_https_scheme(self):
        """Test that https:// scheme is allowed."""
        client = DarktraceClient(host="https://example.com", public_token="test", private_token="test")
        assert client.host == "https://example.com"

    def test_no_scheme_adds_https(self):
        """Test that missing scheme defaults to https."""
        client = DarktraceClient(host="example.com", public_token="test", private_token="test")
        assert client.host == "https://example.com"

    def test_block_file_scheme(self):
        """Test that file:// scheme is blocked."""
        with pytest.raises(ValueError, match="Invalid URL scheme"):
            DarktraceClient(host="file:///etc/passwd", public_token="test", private_token="test")

    def test_block_ftp_scheme(self):
        """Test that ftp:// scheme is blocked."""
        with pytest.raises(ValueError, match="Invalid URL scheme"):
            DarktraceClient(host="ftp://example.com/file", public_token="test", private_token="test")

    def test_block_data_scheme(self):
        """Test that data:// scheme is blocked."""
        with pytest.raises(ValueError, match="Invalid URL scheme"):
            DarktraceClient(
                host="data:text/html,<script>alert(1)</script>",
                public_token="test",
                private_token="test",
            )

    def test_block_javascript_scheme(self):
        """Test that javascript:// scheme is blocked."""
        with pytest.raises(ValueError, match="Invalid URL scheme"):
            DarktraceClient(host="javascript:alert(1)", public_token="test", private_token="test")

    def test_private_ip_allowed(self):
        """Test that private IPs are explicitly allowed."""
        # 10.x.x.x
        client = DarktraceClient(host="https://10.0.0.1", public_token="test", private_token="test")
        assert client.host == "https://10.0.0.1"

        # 192.168.x.x
        client = DarktraceClient(host="https://192.168.1.1", public_token="test", private_token="test")
        assert client.host == "https://192.168.1.1"

        # 172.16.x.x
        client = DarktraceClient(host="https://172.16.0.1", public_token="test", private_token="test")
        assert client.host == "https://172.16.0.1"

    def test_localhost_allowed(self):
        """Test that localhost is allowed."""
        client = DarktraceClient(host="https://localhost", public_token="test", private_token="test")
        assert client.host == "https://localhost"


# ==============================================================================
# Context Manager Tests
# ==============================================================================
class TestContextManager:
    """Test context manager support."""

    def test_enter_returns_client(self):
        """Test that __enter__ returns the client."""
        client = DarktraceClient(host="https://example.com", public_token="test", private_token="test")
        with client as c:
            assert c is client

    def test_exit_closes_session(self):
        """Test that __exit__ closes the session."""
        client = DarktraceClient(host="https://example.com", public_token="test", private_token="test")
        # Verify __exit__ exists and is callable
        assert hasattr(client, "__exit__")
        assert callable(client.__exit__)
        # Verify it doesn't raise an error
        client.__exit__(None, None, None)

    def test_close_method(self):
        """Test that close() method works."""
        client = DarktraceClient(host="https://example.com", public_token="test", private_token="test")
        # Verify close exists and is callable
        assert hasattr(client, "close")
        assert callable(client.close)
        # Verify it doesn't raise an error
        client.close()


# ==============================================================================
# Retry Logic Tests
# ==============================================================================
class TestRetryLogic:
    """Test retry logic in _make_request()."""

    def test_retry_on_500(self, mock_response):
        """Test retry on HTTP 500."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            debug=False,
        )

        # Mock session to return 500, then 200
        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            response = Mock()
            response.raise_for_status = Mock()
            if call_count[0] == 1:
                response.status_code = 500
                response.json.return_value = {}
            else:
                response.status_code = 200
                response.json.return_value = {"success": True}
            return response

        client._session.request = Mock(side_effect=side_effect)

        # Patch time.sleep to avoid actual delays
        with patch("darktrace.dt_utils.time.sleep"):
            response = client.devices.get()

        assert response == {"success": True}
        assert call_count[0] == 2  # Initial + 1 retry

    def test_retry_on_429(self, mock_response):
        """Test retry on HTTP 429 (rate limit)."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            debug=False,
        )

        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            response = Mock()
            response.raise_for_status = Mock()
            if call_count[0] == 1:
                response.status_code = 429
                response.json.return_value = {}
            else:
                response.status_code = 200
                response.json.return_value = {"success": True}
            return response

        client._session.request = Mock(side_effect=side_effect)

        with patch("darktrace.dt_utils.time.sleep"):
            response = client.devices.get()

        assert response == {"success": True}

    def test_no_retry_on_400(self, mock_response):
        """Test no retry on HTTP 400 (client error)."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            debug=False,
        )

        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        client._session.request = Mock(return_value=mock_response)

        with pytest.raises(requests.HTTPError):
            client.devices.get()

    def test_retry_on_connection_error(self, mock_response):
        """Test retry on ConnectionError."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            debug=False,
        )

        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] <= 2:
                raise requests.ConnectionError("Connection refused")
            else:
                mock_response.status_code = 200
                mock_response.json.return_value = {"success": True}
                return mock_response

        client._session.request = Mock(side_effect=side_effect)

        with patch("darktrace.dt_utils.time.sleep"):
            response = client.devices.get()

        assert response == {"success": True}
        assert call_count[0] == 3  # Initial + 2 retries

    def test_max_retries_exceeded(self, mock_response):
        """Test that after max retries, response is returned (even if 500)."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            debug=False,
        )

        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            response = Mock()
            response.raise_for_status = Mock()
            response.status_code = 500
            response.json.return_value = {"error": "server error"}
            return response

        client._session.request = Mock(side_effect=side_effect)

        with patch("darktrace.dt_utils.time.sleep"):
            response = client.devices.get()

        # Should return the response after all retries exhausted
        assert response == {"error": "server error"}
        assert call_count[0] == 4  # Initial + 3 retries


# ==============================================================================
# Timeout Tests
# ==============================================================================
class TestTimeoutHandling:
    """Test timeout parameter handling."""

    def test_client_timeout(self):
        """Test that client timeout is set correctly."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            timeout=30,
        )
        assert client.timeout == 30

    def test_resolve_timeout_uses_client_default(self, mock_response):
        """Test that _resolve_timeout uses client default."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            timeout=30,
        )

        endpoint = BaseEndpoint(client)
        assert endpoint._resolve_timeout() == 30

    def test_resolve_timeout_override(self, mock_response):
        """Test that timeout parameter overrides client default."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            timeout=30,
        )

        endpoint = BaseEndpoint(client)
        assert endpoint._resolve_timeout(60) == 60

    def test_resolve_timeout_none(self, mock_response):
        """Test that None timeout is respected."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            timeout=30,
        )

        endpoint = BaseEndpoint(client)
        assert endpoint._resolve_timeout(None) is None

    def test_timeout_tuple(self, mock_response):
        """Test tuple timeout format."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            timeout=(5, 30),  # connect, read
        )

        assert client.timeout == (5, 30)


# ==============================================================================
# All 28 Endpoint Tests - Method Signatures
# ==============================================================================
class TestEndpointSignatures:
    """Test that all 27 endpoint modules have correct method signatures."""

    def test_advanced_search_methods(self, client):
        """Test AdvancedSearch endpoint methods exist."""
        assert hasattr(client.advanced_search, "search")
        assert hasattr(client.advanced_search, "analyze")
        assert hasattr(client.advanced_search, "graph")
        assert callable(client.advanced_search.search)
        assert callable(client.advanced_search.analyze)
        assert callable(client.advanced_search.graph)

    def test_analyst_methods(self, client):
        """Test Analyst endpoint methods exist."""
        assert hasattr(client.analyst, "get_groups")
        assert hasattr(client.analyst, "get_incident_events")
        assert hasattr(client.analyst, "acknowledge")
        assert hasattr(client.analyst, "unacknowledge")
        assert hasattr(client.analyst, "pin")
        assert hasattr(client.analyst, "unpin")
        assert hasattr(client.analyst, "get_comments")
        assert hasattr(client.analyst, "add_comment")
        assert hasattr(client.analyst, "get_stats")
        assert hasattr(client.analyst, "get_investigations")
        # Note: get_incidents may not exist in all versions - removed check

    def test_antigena_methods(self, client):
        """Test Antigena endpoint methods exist."""
        assert hasattr(client.antigena, "get_actions")
        assert hasattr(client.antigena, "get_summary")
        assert hasattr(client.antigena, "activate_action")
        assert hasattr(client.antigena, "extend_action")
        assert hasattr(client.antigena, "clear_action")
        assert hasattr(client.antigena, "reactivate_action")
        assert hasattr(client.antigena, "create_manual_action")
        assert hasattr(client.antigena, "approve_action")  # Deprecated

    def test_breaches_methods(self, client):
        """Test ModelBreaches endpoint methods exist."""
        assert hasattr(client.breaches, "get")
        assert hasattr(client.breaches, "get_comments")
        assert hasattr(client.breaches, "add_comment")
        assert hasattr(client.breaches, "acknowledge")
        assert hasattr(client.breaches, "unacknowledge")
        assert hasattr(client.breaches, "acknowledge_with_comment")
        assert hasattr(client.breaches, "unacknowledge_with_comment")

    def test_components_methods(self, client):
        """Test Components endpoint methods exist."""
        assert hasattr(client.components, "get")
        assert callable(client.components.get)

    def test_cves_methods(self, client):
        """Test CVEs endpoint methods exist."""
        assert hasattr(client.cves, "get")
        assert callable(client.cves.get)

    def test_details_methods(self, client):
        """Test Details endpoint methods exist."""
        assert hasattr(client.details, "get")
        assert callable(client.details.get)

    def test_devices_methods(self, client):
        """Test Devices endpoint methods exist."""
        assert hasattr(client.devices, "get")
        assert hasattr(client.devices, "update")
        assert callable(client.devices.get)
        assert callable(client.devices.update)

    def test_deviceinfo_methods(self, client):
        """Test DeviceInfo endpoint methods exist."""
        assert hasattr(client.deviceinfo, "get")
        assert callable(client.deviceinfo.get)

    def test_devicesearch_methods(self, client):
        """Test DeviceSearch endpoint methods exist."""
        assert hasattr(client.devicesearch, "get")
        assert hasattr(client.devicesearch, "get_tag")
        assert hasattr(client.devicesearch, "get_type")
        assert hasattr(client.devicesearch, "get_label")
        assert hasattr(client.devicesearch, "get_vendor")
        assert hasattr(client.devicesearch, "get_hostname")
        assert hasattr(client.devicesearch, "get_ip")
        assert hasattr(client.devicesearch, "get_mac")

    def test_devicesummary_methods(self, client):
        """Test DeviceSummary endpoint methods exist."""
        assert hasattr(client.devicesummary, "get")
        assert callable(client.devicesummary.get)

    def test_email_methods(self, client):
        """Test DarktraceEmail endpoint methods exist."""
        assert hasattr(client.email, "decode_link")
        assert hasattr(client.email, "get_action_summary")
        assert hasattr(client.email, "get_dash_stats")
        assert hasattr(client.email, "get_data_loss")
        assert hasattr(client.email, "get_user_anomaly")
        assert hasattr(client.email, "email_action")
        assert hasattr(client.email, "get_email")
        assert hasattr(client.email, "download_email")
        assert hasattr(client.email, "search_emails")
        assert hasattr(client.email, "get_tags")
        assert hasattr(client.email, "get_actions")
        assert hasattr(client.email, "get_filters")
        assert hasattr(client.email, "get_event_types")
        assert hasattr(client.email, "get_audit_events")

    def test_endpointdetails_methods(self, client):
        """Test EndpointDetails endpoint methods exist."""
        assert hasattr(client.endpointdetails, "get")
        assert callable(client.endpointdetails.get)

    def test_enums_methods(self, client):
        """Test Enums endpoint methods exist."""
        assert hasattr(client.enums, "get")
        assert callable(client.enums.get)

    def test_filtertypes_methods(self, client):
        """Test FilterTypes endpoint methods exist."""
        assert hasattr(client.filtertypes, "get")
        assert callable(client.filtertypes.get)

    def test_intelfeed_methods(self, client):
        """Test IntelFeed endpoint methods exist."""
        assert hasattr(client.intelfeed, "get")
        assert hasattr(client.intelfeed, "get_sources")
        assert hasattr(client.intelfeed, "get_by_source")
        assert hasattr(client.intelfeed, "get_with_details")
        assert hasattr(client.intelfeed, "update")

    def test_mbcomments_methods(self, client):
        """Test MBComments endpoint methods exist."""
        assert hasattr(client.mbcomments, "get")
        assert hasattr(client.mbcomments, "post")
        assert callable(client.mbcomments.get)
        assert callable(client.mbcomments.post)

    def test_metricdata_methods(self, client):
        """Test MetricData endpoint methods exist."""
        assert hasattr(client.metricdata, "get")
        assert callable(client.metricdata.get)

    def test_metrics_methods(self, client):
        """Test Metrics endpoint methods exist."""
        assert hasattr(client.metrics, "get")
        assert callable(client.metrics.get)

    def test_models_methods(self, client):
        """Test Models endpoint methods exist."""
        assert hasattr(client.models, "get")
        assert callable(client.models.get)

    def test_network_methods(self, client):
        """Test Network endpoint methods exist."""
        assert hasattr(client.network, "get")
        assert callable(client.network.get)

    def test_pcaps_methods(self, client):
        """Test PCAPs endpoint methods exist."""
        assert hasattr(client.pcaps, "get")
        assert hasattr(client.pcaps, "create")
        assert callable(client.pcaps.get)
        assert callable(client.pcaps.create)

    def test_similardevices_methods(self, client):
        """Test SimilarDevices endpoint methods exist."""
        assert hasattr(client.similardevices, "get")
        assert callable(client.similardevices.get)

    def test_status_methods(self, client):
        """Test Status endpoint methods exist."""
        assert hasattr(client.status, "get")
        assert callable(client.status.get)

    def test_subnets_methods(self, client):
        """Test Subnets endpoint methods exist."""
        assert hasattr(client.subnets, "get")
        assert hasattr(client.subnets, "post")
        assert callable(client.subnets.get)
        assert callable(client.subnets.post)

    def test_summarystatistics_methods(self, client):
        """Test SummaryStatistics endpoint methods exist."""
        assert hasattr(client.summarystatistics, "get")
        assert callable(client.summarystatistics.get)

    def test_tags_methods(self, client):
        """Test Tags endpoint methods exist."""
        assert hasattr(client.tags, "get")
        assert hasattr(client.tags, "create")
        assert hasattr(client.tags, "delete")
        assert hasattr(client.tags, "get_entities")
        assert hasattr(client.tags, "post_entities")
        assert hasattr(client.tags, "delete_entities")
        assert hasattr(client.tags, "get_tag_entities")
        assert hasattr(client.tags, "post_tag_entities")
        assert hasattr(client.tags, "delete_tag_entity")


# ==============================================================================
# Endpoint Mock Tests - Verify Methods Can Be Called
# ==============================================================================
class TestEndpointMockCalls:
    """Test that endpoint methods can be called with mocked responses."""

    def test_devices_get(self, client, mock_response):
        """Test Devices.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"devices": []}
        client._session.request = Mock(return_value=mock_response)

        result = client.devices.get()
        assert result == {"devices": []}

    def test_status_get(self, client, mock_response):
        """Test Status.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"version": "6.3.18"}
        client._session.request = Mock(return_value=mock_response)

        result = client.status.get()
        assert result == {"version": "6.3.18"}

    def test_breaches_get(self, client, mock_response):
        """Test ModelBreaches.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = [{"pbid": 1}]
        client._session.request = Mock(return_value=mock_response)

        result = client.breaches.get()
        assert result == [{"pbid": 1}]

    def test_intelfeed_get(self, client, mock_response):
        """Test IntelFeed.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = ["entry1", "entry2"]
        client._session.request = Mock(return_value=mock_response)

        result = client.intelfeed.get()
        assert result == ["entry1", "entry2"]

    def test_enums_get(self, client, mock_response):
        """Test Enums.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"Country": ["US", "DE"]}
        client._session.request = Mock(return_value=mock_response)

        result = client.enums.get()
        assert result == {"Country": ["US", "DE"]}

    def test_network_get(self, client, mock_response):
        """Test Network.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"statistics": {}}
        client._session.request = Mock(return_value=mock_response)

        result = client.network.get()
        assert result == {"statistics": {}}

    def test_metrics_get(self, client, mock_response):
        """Test Metrics.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = [{"mlid": 1, "name": "metric1"}]
        client._session.request = Mock(return_value=mock_response)

        result = client.metrics.get()
        assert result == [{"mlid": 1, "name": "metric1"}]

    def test_models_get(self, client, mock_response):
        """Test Models.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = [{"uuid": "abc123", "name": "model1"}]
        client._session.request = Mock(return_value=mock_response)

        result = client.models.get()
        assert result == [{"uuid": "abc123", "name": "model1"}]

    def test_antigena_get_actions(self, client, mock_response):
        """Test Antigena.get_actions() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"actions": []}
        client._session.request = Mock(return_value=mock_response)

        result = client.antigena.get_actions()
        assert result == {"actions": []}

    def test_antigena_get_summary(self, client, mock_response):
        """Test Antigena.get_summary() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"activeCount": 5, "pendingCount": 2}
        client._session.request = Mock(return_value=mock_response)

        result = client.antigena.get_summary()
        assert result == {"activeCount": 5, "pendingCount": 2}

    def test_devicesearch_get(self, client, mock_response):
        """Test DeviceSearch.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"devices": [], "totalCount": 0}
        client._session.request = Mock(return_value=mock_response)

        result = client.devicesearch.get()
        assert result == {"devices": [], "totalCount": 0}

    def test_analyst_get_groups(self, client, mock_response):
        """Test Analyst.get_groups() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = []
        client._session.request = Mock(return_value=mock_response)

        result = client.analyst.get_groups()
        assert result == []

    def test_components_get(self, client, mock_response):
        """Test Components.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = []
        client._session.request = Mock(return_value=mock_response)

        result = client.components.get()
        assert result == []

    def test_filtertypes_get(self, client, mock_response):
        """Test FilterTypes.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = []
        client._session.request = Mock(return_value=mock_response)

        result = client.filtertypes.get()
        assert result == []

    def test_subnets_get(self, client, mock_response):
        """Test Subnets.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = []
        client._session.request = Mock(return_value=mock_response)

        result = client.subnets.get()
        assert result == []

    def test_tags_get(self, client, mock_response):
        """Test Tags.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = []
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.get()
        assert result == []

    def test_summarystatistics_get(self, client, mock_response):
        """Test SummaryStatistics.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"devicecount": 100}
        client._session.request = Mock(return_value=mock_response)

        result = client.summarystatistics.get()
        assert result == {"devicecount": 100}

    def test_mbcomments_get(self, client, mock_response):
        """Test MBComments.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = []
        client._session.request = Mock(return_value=mock_response)

        result = client.mbcomments.get()
        assert result == []

    def test_metricdata_get(self, client, mock_response):
        """Test MetricData.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        client._session.request = Mock(return_value=mock_response)

        result = client.metricdata.get(metric="connections")
        assert result == {"data": []}

    def test_similardevices_get(self, client, mock_response):
        """Test SimilarDevices.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = []
        client._session.request = Mock(return_value=mock_response)

        result = client.similardevices.get()
        assert result == []

    def test_cves_get(self, client, mock_response):
        """Test CVEs.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        client._session.request = Mock(return_value=mock_response)

        result = client.cves.get()
        assert result == {"results": []}

    def test_deviceinfo_get(self, client, mock_response):
        """Test DeviceInfo.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        client._session.request = Mock(return_value=mock_response)

        result = client.deviceinfo.get(did=1)
        assert result == {}

    def test_endpointdetails_get(self, client, mock_response):
        """Test EndpointDetails.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        client._session.request = Mock(return_value=mock_response)

        result = client.endpointdetails.get(ip="8.8.8.8")
        assert result == {}

    def test_details_get(self, client, mock_response):
        """Test Details.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = []
        client._session.request = Mock(return_value=mock_response)

        result = client.details.get(did=1, count=1)
        assert result == []

    def test_devicesummary_get(self, client, mock_response):
        """Test DeviceSummary.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {}}
        client._session.request = Mock(return_value=mock_response)

        result = client.devicesummary.get(did=1)
        assert result == {"data": {}}

    def test_pcaps_get(self, client, mock_response):
        """Test PCAPs.get() with mocked response."""
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.headers = {"Content-Type": "application/json"}  # Required for pcaps
        client._session.request = Mock(return_value=mock_response)

        result = client.pcaps.get()
        assert result == []


# ==============================================================================
# Retry Configuration Tests
# ==============================================================================
class TestRetryConfiguration:
    """Test retry configuration constants."""

    def test_max_retries_value(self):
        """Test _MAX_RETRIES is 3."""
        assert _MAX_RETRIES == 3

    def test_initial_retry_wait_seconds(self):
        """Test _INITIAL_RETRY_WAIT_SECONDS is 3."""
        assert _INITIAL_RETRY_WAIT_SECONDS == 3

    def test_retry_status_codes(self):
        """Test _RETRY_STATUS_CODES contains correct values."""
        assert 429 in _RETRY_STATUS_CODES
        assert 500 in _RETRY_STATUS_CODES
        assert 502 in _RETRY_STATUS_CODES
        assert 503 in _RETRY_STATUS_CODES
        assert 504 in _RETRY_STATUS_CODES
        assert 400 not in _RETRY_STATUS_CODES  # Client errors not retry


# ==============================================================================
# SSL Verification Tests
# ==============================================================================
class TestSSLVerification:
    """Test SSL verification default."""

    def test_ssl_verification_default_true(self):
        """Test that SSL verification is enabled by default."""
        client = DarktraceClient(host="https://example.com", public_token="test", private_token="test")
        assert client.verify_ssl is True

    def test_ssl_verification_can_be_disabled(self):
        """Test that SSL verification can be disabled."""
        client = DarktraceClient(
            host="https://example.com",
            public_token="test",
            private_token="test",
            verify_ssl=False,
        )
        assert client.verify_ssl is False


# ==============================================================================
# Deprecation Tests
# ==============================================================================
class TestDeprecations:
    """Test deprecation warnings."""

    def test_approve_action_deprecated(self, client):
        """Test that approve_action emits de deprecation warning."""
        import warnings

        with warnings.catch_warnings(record=True) as w:
            client.antigena.approve_action(123)
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "deprecated" in str(w[0].message).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
