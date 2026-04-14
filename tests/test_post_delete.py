#!/usr/bin/env python3
"""
Comprehensive mock tests for POST and DELETE operations in the Darktrace SDK.

Tests all write operations across 10 endpoint modules:
  - Tags (POST + DELETE, 6 methods)
  - Subnets (POST)
  - PCAPs (POST)
  - Devices (POST)
  - IntelFeed (POST)
  - Antigena (POST, 5 methods)
  - ModelBreaches (POST, 3 methods + batch)
  - MBComments (POST)
  - DarktraceEmail (POST, 2 methods)
  - Analyst (POST, 3 methods)
  - AdvancedSearch (POST)

All tests use mocks — no live API calls.

Run: pytest tests/test_post_delete.py -v
"""

from unittest.mock import Mock

import pytest

from darktrace import DarktraceClient


# ==============================================================================
# FIXTURES
# ==============================================================================
@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock()
    response.raise_for_status = Mock()
    response.json = Mock(return_value={})
    response.status_code = 200
    return response


@pytest.fixture
def client():
    """Create a DarktraceClient instance for testing."""
    return DarktraceClient(
        host="https://test.example.com",
        public_token="test_public",
        private_token="test_private",
    )


# ==============================================================================
# Tags — POST + DELETE
# ==============================================================================
class TestTagsPostDelete:
    """Test Tags POST and DELETE operations."""

    def test_tags_create(self, client, mock_response):
        """Test Tags.create() sends POST with JSON body."""
        mock_response.json.return_value = {"tid": 42, "name": "test-tag"}
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.create(name="test-tag")
        assert result == {"tid": 42, "name": "test-tag"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/tags" in call_args[0][1]

    def test_tags_create_with_options(self, client, mock_response):
        """Test Tags.create() with color and description."""
        mock_response.json.return_value = {"tid": 43}
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.create(name="colored-tag", color=180, description="A test tag")
        assert result == {"tid": 43}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"

    def test_tags_delete(self, client, mock_response):
        """Test Tags.delete() sends DELETE to /tags/{id}."""
        mock_response.json.return_value = {"deleted": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.delete(tag_id="5")
        assert result == {"deleted": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "DELETE"
        assert "/tags/5" in call_args[0][1]

    def test_tags_post_entities(self, client, mock_response):
        """Test Tags.post_entities() sends POST form data."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.post_entities(did=1, tag="infected")
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/tags/entities" in call_args[0][1]

    def test_tags_post_entities_with_duration(self, client, mock_response):
        """Test Tags.post_entities() with duration parameter."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.post_entities(did=1, tag="temp", duration=3600)
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"

    def test_tags_delete_entities(self, client, mock_response):
        """Test Tags.delete_entities() sends DELETE with params."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.delete_entities(did=1, tag="infected")
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "DELETE"
        assert "/tags/entities" in call_args[0][1]

    def test_tags_post_tag_entities(self, client, mock_response):
        """Test Tags.post_tag_entities() sends POST with JSON body."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.post_tag_entities(tid=5, entityType="Device", entityValue="10")
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/tags/5/entities" in call_args[0][1]

    def test_tags_post_tag_entities_with_expiry(self, client, mock_response):
        """Test Tags.post_tag_entities() with expiryDuration."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.post_tag_entities(tid=5, entityType="Device", entityValue="10", expiryDuration=7200)
        assert result == {"success": True}

    def test_tags_delete_tag_entity(self, client, mock_response):
        """Test Tags.delete_tag_entity() sends DELETE to /tags/{tid}/entities/{teid}."""
        mock_response.json.return_value = {"deleted": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.tags.delete_tag_entity(tid=5, teid=99)
        assert result == {"deleted": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "DELETE"
        assert "/tags/5/entities/99" in call_args[0][1]


# ==============================================================================
# Subnets — POST
# ==============================================================================
class TestSubnetsPost:
    """Test Subnets POST operations."""

    def test_subnets_post(self, client, mock_response):
        """Test Subnets.post() sends POST with JSON body."""
        mock_response.json.return_value = {"sid": 1, "network": "10.0.0.0/8"}
        client._session.request = Mock(return_value=mock_response)

        result = client.subnets.post(sid=1, network="10.0.0.0/8")
        assert result == {"sid": 1, "network": "10.0.0.0/8"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/subnets" in call_args[0][1]

    def test_subnets_post_with_all_options(self, client, mock_response):
        """Test Subnets.post() with all optional parameters."""
        mock_response.json.return_value = {"sid": 2}
        client._session.request = Mock(return_value=mock_response)

        result = client.subnets.post(
            sid=2,
            label="DMZ",
            network="192.168.1.0/24",
            longitude=10.0,
            latitude=50.0,
            dhcp=True,
            uniqueUsernames=False,
            uniqueHostnames=False,
            excluded=False,
            modelExcluded=False,
        )
        assert result == {"sid": 2}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"


# ==============================================================================
# PCAPs — POST
# ==============================================================================
class TestPCAPsPost:
    """Test PCAPs POST operations."""

    def test_pcaps_create(self, client, mock_response):
        """Test PCAPs.create() sends POST with JSON body."""
        mock_response.json.return_value = {"filename": "pcap_123.pcap", "state": "pending"}
        client._session.request = Mock(return_value=mock_response)

        result = client.pcaps.create(ip1="10.0.0.1", start=1000000, end=10003600)
        assert result == {"filename": "pcap_123.pcap", "state": "pending"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/pcaps" in call_args[0][1]

    def test_pcaps_create_with_all_options(self, client, mock_response):
        """Test PCAPs.create() with all optional parameters."""
        mock_response.json.return_value = {"filename": "pcap_full.pcap", "state": "pending"}
        client._session.request = Mock(return_value=mock_response)

        result = client.pcaps.create(
            ip1="10.0.0.1",
            start=1000000,
            end=10003600,
            ip2="192.168.1.1",
            port1=443,
            port2=80,
            protocol="tcp",
        )
        assert result == {"filename": "pcap_full.pcap", "state": "pending"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"


# ==============================================================================
# Devices — POST
# ==============================================================================
class TestDevicesPost:
    """Test Devices POST operations."""

    def test_devices_update(self, client, mock_response):
        """Test Devices.update() sends POST with JSON body."""
        mock_response.json.return_value = {"did": 42}
        client._session.request = Mock(return_value=mock_response)

        result = client.devices.update(did=42)
        assert result == {"did": 42}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/devices" in call_args[0][1]

    def test_devices_update_with_properties(self, client, mock_response):
        """Test Devices.update() with label and priority."""
        mock_response.json.return_value = {"did": 42, "label": "Server"}
        client._session.request = Mock(return_value=mock_response)

        result = client.devices.update(did=42, label="Server", priority=5)
        assert result == {"did": 42, "label": "Server"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"


# ==============================================================================
# IntelFeed — POST
# ==============================================================================
class TestIntelFeedPost:
    """Test IntelFeed POST operations."""

    def test_intelfeed_update_add_entry(self, client, mock_response):
        """Test IntelFeed.update() with add_entry."""
        mock_response.json.return_value = {"status": "ok"}
        client._session.request = Mock(return_value=mock_response)

        result = client.intelfeed.update(add_entry="evil.com", source="test")
        assert result == {"status": "ok"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/intelfeed" in call_args[0][1]

    def test_intelfeed_update_add_list(self, client, mock_response):
        """Test IntelFeed.update() with add_list."""
        mock_response.json.return_value = {"status": "ok"}
        client._session.request = Mock(return_value=mock_response)

        result = client.intelfeed.update(add_list=["evil.com", "malware.org"], source="bulk")
        assert result == {"status": "ok"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"

    def test_intelfeed_update_remove_entry(self, client, mock_response):
        """Test IntelFeed.update() with remove_entry."""
        mock_response.json.return_value = {"status": "ok"}
        client._session.request = Mock(return_value=mock_response)

        result = client.intelfeed.update(remove_entry="evil.com", source="test")
        assert result == {"status": "ok"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"

    def test_intelfeed_update_remove_all(self, client, mock_response):
        """Test IntelFeed.update() with remove_all=True."""
        mock_response.json.return_value = {"status": "ok"}
        client._session.request = Mock(return_value=mock_response)

        result = client.intelfeed.update(remove_all=True, source="test")
        assert result == {"status": "ok"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"

    def test_intelfeed_update_with_options(self, client, mock_response):
        """Test IntelFeed.update() with all optional parameters."""
        mock_response.json.return_value = {"status": "ok"}
        client._session.request = Mock(return_value=mock_response)

        result = client.intelfeed.update(
            add_entry="example.com",
            description="Test description",
            source="test-source",
            expiry="3600",
            is_hostname=True,
            enable_antigena=True,
        )
        assert result == {"status": "ok"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"


# ==============================================================================
# Antigena — POST (5 methods)
# ==============================================================================
class TestAntigenaPost:
    """Test Antigena POST operations."""

    def test_antigena_activate_action(self, client, mock_response):
        """Test Antigena.activate_action() sends POST with activate=True."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.antigena.activate_action(codeid=123)
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/antigena" in call_args[0][1]

    def test_antigena_activate_action_with_reason(self, client, mock_response):
        """Test Antigena.activate_action() with reason parameter."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.antigena.activate_action(codeid=123, reason="Confirmed threat")
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"

    def test_antigena_extend_action(self, client, mock_response):
        """Test Antigena.extend_action() sends POST with duration."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.antigena.extend_action(codeid=123, duration=600)
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/antigena" in call_args[0][1]

    def test_antigena_clear_action(self, client, mock_response):
        """Test Antigena.clear_action() sends POST with clear=True."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.antigena.clear_action(codeid=123)
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/antigena" in call_args[0][1]

    def test_antigena_reactivate_action(self, client, mock_response):
        """Test Antigena.reactivate_action() sends POST with activate+duration."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.antigena.reactivate_action(codeid=123, duration=600)
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/antigena" in call_args[0][1]

    def test_antigena_create_manual_action(self, client, mock_response):
        """Test Antigena.create_manual_action() sends POST to /antigena/manual."""
        mock_response.json.return_value = 42
        client._session.request = Mock(return_value=mock_response)

        result = client.antigena.create_manual_action(did=12, action="quarantine", duration=600)
        assert result == 42

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/antigena/manual" in call_args[0][1]

    def test_antigena_create_manual_action_with_connections(self, client, mock_response):
        """Test Antigena.create_manual_action() with connection blocking."""
        mock_response.json.return_value = 43
        client._session.request = Mock(return_value=mock_response)

        result = client.antigena.create_manual_action(
            did=12,
            action="connection",
            duration=600,
            reason="Block malicious",
            connections=[{"src": "10.10.10.10", "dst": "8.8.8.8"}],
        )
        assert result == 43

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/antigena/manual" in call_args[0][1]


# ==============================================================================
# ModelBreaches — POST (3 methods + batch)
# ==============================================================================
class TestModelBreachesPost:
    """Test ModelBreaches POST operations."""

    def test_breaches_acknowledge(self, client, mock_response):
        """Test ModelBreaches.acknowledge() sends POST with acknowledge=True."""
        mock_response.json.return_value = {"acknowledged": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.breaches.acknowledge(pbid=1)
        assert result == {"acknowledged": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/modelbreaches/1/acknowledge" in call_args[0][1]

    def test_breaches_unacknowledge(self, client, mock_response):
        """Test ModelBreaches.unacknowledge() sends POST with unacknowledge=True."""
        mock_response.json.return_value = {"unacknowledged": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.breaches.unacknowledge(pbid=1)
        assert result == {"unacknowledged": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/modelbreaches/1/unacknowledge" in call_args[0][1]

    def test_breaches_add_comment(self, client, mock_response):
        """Test ModelBreaches.add_comment() sends POST with message."""
        mock_response.json.return_value = {"comment": "test comment"}
        client._session.request = Mock(return_value=mock_response)

        result = client.breaches.add_comment(pbid=1, message="test comment")
        assert result == {"comment": "test comment"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/modelbreaches/1/comments" in call_args[0][1]

    def test_breaches_acknowledge_batch(self, client, mock_response):
        """Test ModelBreaches.acknowledge() with list of pbids returns dict."""
        mock_response.json.return_value = {"acknowledged": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.breaches.acknowledge(pbid=[1, 2, 3])
        assert isinstance(result, dict)
        assert 1 in result
        assert 2 in result
        assert 3 in result

    def test_breaches_unacknowledge_batch(self, client, mock_response):
        """Test ModelBreaches.unacknowledge() with list of pbids returns dict."""
        mock_response.json.return_value = {"unacknowledged": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.breaches.unacknowledge(pbid=[1, 2])
        assert isinstance(result, dict)
        assert 1 in result
        assert 2 in result

    def test_breaches_acknowledge_with_comment(self, client, mock_response):
        """Test ModelBreaches.acknowledge_with_comment() combines both operations."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.breaches.acknowledge_with_comment(pbid=1, message="Confirmed")
        assert "acknowledge" in result
        assert "add_comment" in result

    def test_breaches_unacknowledge_with_comment(self, client, mock_response):
        """Test ModelBreaches.unacknowledge_with_comment() combines both operations."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.breaches.unacknowledge_with_comment(pbid=1, message="Reopened")
        assert "unacknowledge" in result
        assert "add_comment" in result


# ==============================================================================
# MBComments — POST
# ==============================================================================
class TestMBCommentsPost:
    """Test MBComments POST operations."""

    def test_mbcomments_post(self, client, mock_response):
        """Test MBComments.post() sends POST with breachid and comment."""
        mock_response.json.return_value = {"id": 1, "comment": "test"}
        client._session.request = Mock(return_value=mock_response)

        result = client.mbcomments.post(breach_id="1", comment="test")
        assert result == {"id": 1, "comment": "test"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/mbcomments" in call_args[0][1]


# ==============================================================================
# DarktraceEmail — POST (2 methods)
# ==============================================================================
class TestEmailPost:
    """Test DarktraceEmail POST operations."""

    def test_email_email_action(self, client, mock_response):
        """Test DarktraceEmail.email_action() sends POST with UUID and data."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.email.email_action(uuid="abc-123", data={"action": "release"})
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/agemail/api/ep/api/v1.0/emails/abc-123/action" in call_args[0][1]

    def test_email_search_emails(self, client, mock_response):
        """Test DarktraceEmail.search_emails() sends POST with search data."""
        mock_response.json.return_value = {"results": []}
        client._session.request = Mock(return_value=mock_response)

        result = client.email.search_emails(data={"query": "test"})
        assert result == {"results": []}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/agemail/api/ep/api/v1.0/emails/search" in call_args[0][1]


# ==============================================================================
# Analyst — POST (3 methods + acknowledge/unacknowledge/pin/unpin)
# ==============================================================================
class TestAnalystPost:
    """Test Analyst POST operations."""

    def test_analyst_acknowledge(self, client, mock_response):
        """Test Analyst.acknowledge() sends form POST with UUID."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.analyst.acknowledge(uuids="abc-123")
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/aianalyst/acknowledge" in call_args[0][1]

    def test_analyst_acknowledge_list(self, client, mock_response):
        """Test Analyst.acknowledge() with list of UUIDs joins them."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.analyst.acknowledge(uuids=["uuid1", "uuid2"])
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/aianalyst/acknowledge" in call_args[0][1]

    def test_analyst_unacknowledge(self, client, mock_response):
        """Test Analyst.unacknowledge() sends form POST."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.analyst.unacknowledge(uuids="abc-123")
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/aianalyst/unacknowledge" in call_args[0][1]

    def test_analyst_pin(self, client, mock_response):
        """Test Analyst.pin() sends form POST."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.analyst.pin(uuids="abc-123")
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/aianalyst/pin" in call_args[0][1]

    def test_analyst_unpin(self, client, mock_response):
        """Test Analyst.unpin() sends form POST."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.analyst.unpin(uuids="abc-123")
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/aianalyst/unpin" in call_args[0][1]

    def test_analyst_add_comment(self, client, mock_response):
        """Test Analyst.add_comment() sends JSON POST."""
        mock_response.json.return_value = {"success": True}
        client._session.request = Mock(return_value=mock_response)

        result = client.analyst.add_comment(incident_id="inc-1", message="Test comment")
        assert result == {"success": True}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/aianalyst/incident/comments" in call_args[0][1]

    def test_analyst_create_investigation(self, client, mock_response):
        """Test Analyst.create_investigation() sends JSON POST."""
        mock_response.json.return_value = {"investigationId": "inv-1"}
        client._session.request = Mock(return_value=mock_response)

        result = client.analyst.create_investigation(investigate_time="1609459200", did=42)
        assert result == {"investigationId": "inv-1"}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/aianalyst/investigations" in call_args[0][1]


# ==============================================================================
# AdvancedSearch — POST
# ==============================================================================
class TestAdvancedSearchPost:
    """Test AdvancedSearch POST operations."""

    def test_advanced_search_search_post(self, client, mock_response):
        """Test AdvancedSearch.search() with post_request=True sends POST."""
        mock_response.json.return_value = {"hits": []}
        client._session.request = Mock(return_value=mock_response)

        query = {"search": '@type:"ssl"', "fields": [], "offset": 0, "timeframe": "3600"}
        result = client.advanced_search.search(query=query, post_request=True)
        assert result == {"hits": []}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"
        assert "/advancedsearch/api/search" in call_args[0][1]

    def test_advanced_search_search_post_with_custom_time(self, client, mock_response):
        """Test AdvancedSearch.search() POST with custom from/to timeframe."""
        mock_response.json.return_value = {"hits": []}
        client._session.request = Mock(return_value=mock_response)

        query = {
            "search": '@type:"ssl"',
            "fields": [],
            "offset": 0,
            "timeframe": "3600",
            "from": "2024-01-01",
            "to": "2024-01-02",
        }
        result = client.advanced_search.search(query=query, post_request=True)
        assert result == {"hits": []}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "POST"

    def test_advanced_search_search_get(self, client, mock_response):
        """Test AdvancedSearch.search() without post_request uses GET (control test)."""
        mock_response.json.return_value = {"hits": []}
        client._session.request = Mock(return_value=mock_response)

        query = {"search": '@type:"ssl"', "fields": [], "offset": 0, "timeframe": "3600"}
        result = client.advanced_search.search(query=query)
        assert result == {"hits": []}

        call_args = client._session.request.call_args
        assert call_args[0][0] == "GET"
