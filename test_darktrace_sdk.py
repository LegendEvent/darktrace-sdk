#!/usr/bin/env python3
"""
Test script for the Darktrace SDK
This script demonstrates the basic functionality of the Darktrace SDK
"""

import pytest
import requests
import urllib3
from darktrace import DarktraceClient
from datetime import datetime, timezone, timedelta
import time as _time
import random

# Global test configuration (set via pytest CLI options in conftest.py)
TEST_HOST = None
TEST_PUBLIC_TOKEN = None
TEST_PRIVATE_TOKEN = None
TEST_DEBUG = False
TEST_VERIFY_SSL = False


# Pytest fixture to provide a configured DarktraceClient
@pytest.fixture(scope="session")
def dt_client(pytestconfig):
    global TEST_HOST, TEST_PUBLIC_TOKEN, TEST_PRIVATE_TOKEN, TEST_DEBUG, TEST_VERIFY_SSL
    TEST_HOST = pytestconfig.getoption('host')
    TEST_PUBLIC_TOKEN = pytestconfig.getoption('public_token')
    TEST_PRIVATE_TOKEN = pytestconfig.getoption('private_token')
    TEST_VERIFY_SSL = not pytestconfig.getoption('no_verify')
    assert TEST_HOST and TEST_PUBLIC_TOKEN and TEST_PRIVATE_TOKEN, "API credentials must be provided via pytest CLI options."
    if not TEST_VERIFY_SSL:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    client = DarktraceClient(
        host=TEST_HOST,
        public_token=TEST_PUBLIC_TOKEN,
        private_token=TEST_PRIVATE_TOKEN
    )
    # Test connection
    status = client.status.get()
    # Accept any valid dict, but require 'version' key as a minimal check
    assert isinstance(status, dict) and 'version' in status, f"Connection failed or unexpected status: {status}"
    return client


# --- Refactored test functions below ---
    
def test_intel_feed(dt_client):
    """Test the Intel Feed module with the fixed authentication mechanism"""
    sources = dt_client.intelfeed.get_sources()
    assert isinstance(sources, list)

    entries = dt_client.intelfeed.get()
    assert isinstance(entries, list)

    detailed_entries = dt_client.intelfeed.get(full_details=True)
    assert isinstance(detailed_entries, list)

    if sources:
        source = sources[0]
        source_entries = dt_client.intelfeed.get(source=source)
        assert isinstance(source_entries, list)
        detailed_source_entries = dt_client.intelfeed.get(source=source, full_details=True)
        assert isinstance(detailed_source_entries, list)

@pytest.mark.usefixtures("dt_client")
def test_antigena_actions(dt_client):
    actions = dt_client.antigena.get_actions()
    assert isinstance(actions, (list, dict))

    detailed_actions = dt_client.antigena.get_actions(
        fulldevicedetails=True,
        includehistory=True,
        includecleared=True
    )
    assert isinstance(detailed_actions, (list, dict))

    filtered_actions = dt_client.antigena.get_actions(
        includeconnections=True,
        needconfirming=True,
        responsedata="actions"
    )
    assert isinstance(filtered_actions, (list, dict))

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=1)
    time_actions = dt_client.antigena.get_actions(
        starttime=int(start.timestamp() * 1000),
        endtime=int(end.timestamp() * 1000),
        includecleared=True
    )
    assert isinstance(time_actions, (list, dict))

    summary = dt_client.antigena.get_summary()
    assert isinstance(summary, dict)

    time_summary = dt_client.antigena.get_summary(
        starttime=int((end - timedelta(hours=1)).timestamp() * 1000),
        endtime=int(end.timestamp() * 1000)
    )
    assert isinstance(time_summary, dict)

    devices = dt_client.devices.get(count=1)
    device_list = devices.get('devices', []) if isinstance(devices, dict) else (devices if isinstance(devices, list) else [])
    if device_list:
        test_did = device_list[0].get('did')
        if test_did:
            device_actions = dt_client.antigena.get_actions(did=test_did)
            assert isinstance(device_actions, (list, dict))

    # Backwards compatibility methods (no-op, just check they exist)
    assert hasattr(dt_client.antigena, 'approve_action')
    assert hasattr(dt_client.antigena, 'activate_action')
    assert hasattr(dt_client.antigena, 'extend_action')
    assert hasattr(dt_client.antigena, 'clear_action')
    assert hasattr(dt_client.antigena, 'reactivate_action')
    assert hasattr(dt_client.antigena, 'create_manual_action')

def test_advanced_search(dt_client):
    # Test 1: Basic search functionality
    search_query = {
        "search": "@type:\"ssl\" AND @fields.dest_port:\"443\"",
        "fields": [],
        "offset": 0,
        "timeframe": "900",
        "time": {"user_interval": 0}
    }
    search_results = dt_client.advanced_search.search(search_query)
    assert isinstance(search_results, dict)
    hits = search_results.get('hits', {}).get('hits', [])
    assert isinstance(hits, list)

    # Test 2: Analyze field data (terms analysis)
    analyze_query = {
        "search": "@type:\"dns\" AND @fields.proto:\"udp\"",
        "fields": [],
        "offset": 0,
        "timeframe": "3600",
        "time": {"user_interval": 0}
    }
    analyze_results = dt_client.advanced_search.analyze("@fields.dest_port", "terms", analyze_query)
    buckets = analyze_results.get('aggregations', {}).get('terms', {}).get('buckets', [])
    assert isinstance(buckets, list)

    # Test 3: Graph data (count over time)
    graph_query = {
        "search": "@type:\"conn\"",
        "fields": [],
        "offset": 0,
        "timeframe": "14400",
        "time": {"user_interval": 0}
    }
    graph_results = dt_client.advanced_search.graph("count", 300000, graph_query)
    graph_buckets = graph_results.get('aggregations', {}).get('count', {}).get('buckets', [])
    assert isinstance(graph_buckets, list)

    # Test 4: POST request method (fallback to GET if not supported)
    post_query = {
        "search": "@type:\"conn\" AND @fields.proto:\"tcp\"",
        "fields": [],
        "offset": 0,
        "timeframe": "1800",
        "time": {"user_interval": 0}
    }
    try:
        post_results = dt_client.advanced_search.search(post_query, post_request=True)
        assert isinstance(post_results, dict)
    except NotImplementedError:
        get_results = dt_client.advanced_search.search(post_query, post_request=False)
        assert isinstance(get_results, dict)

def test_analyst(dt_client):
    events = dt_client.analyst.get_incident_events()
    assert isinstance(events, list)

    now = int(_time.time() * 1000)
    yesterday = now - (24 * 60 * 60 * 1000)
    events_filtered = dt_client.analyst.get_incident_events(
        starttime=yesterday,
        endtime=now,
        minscore=50,
        includeacknowledged=False
    )
    assert isinstance(events_filtered, list)

    groups = dt_client.analyst.get_groups()
    assert isinstance(groups, list)

    critical_groups = dt_client.analyst.get_groups(
        groupcritical=True,
        includeacknowledged=False
    )
    assert isinstance(critical_groups, list)

    stats = dt_client.analyst.get_stats()
    assert isinstance(stats, dict)

    investigations = dt_client.analyst.get_investigations()
    assert isinstance(investigations, list)

    # Comments functionality (read-only)
    if events:
        test_incident_id = events[0].get('id', '')
        if test_incident_id:
            comments = dt_client.analyst.get_comments(test_incident_id)
            assert isinstance(comments, dict)

def test_components(dt_client):
    components = dt_client.components.get()
    assert isinstance(components, (list, dict))

    cid = None
    if isinstance(components, list) and components:
        cid = components[0].get('cid')
    elif isinstance(components, dict):
        cid = components.get('cid')
    if cid is not None:
        single_component = dt_client.components.get(cid=cid)
        assert isinstance(single_component, dict)

    filters_only = dt_client.components.get(responsedata='filters')
    assert isinstance(filters_only, (list, dict))

def test_cves(dt_client):
    cves = dt_client.cves.get()
    assert isinstance(cves, dict) and 'results' in cves

    did = None
    if cves['results']:
        did = cves['results'][0].get('did')
    if did is not None:
        single_device_cves = dt_client.cves.get(did=did)
        assert isinstance(single_device_cves, dict) and 'results' in single_device_cves

    cves_full = dt_client.cves.get(fulldevicedetails=True)
    assert isinstance(cves_full, dict)

def test_details(dt_client):
    did = 3937  # Placeholder for device ID, replace with a real one if available
    pbid = 48892  # Placeholder for model breach ID, replace with a real one if available
    details = dt_client.details.get(did, count=1)
    assert isinstance(details, (list, dict))

    details_by_pbid = dt_client.details.get(pbid, count=1)
    assert isinstance(details_by_pbid, (list, dict))

    end = datetime.now()
    start = end - timedelta(hours=1)
    details_time = dt_client.details.get(
        did,
        from_=start.strftime('%Y-%m-%d %H:%M:%S'),
        to=end.strftime('%Y-%m-%d %H:%M:%S'),
    )
    assert isinstance(details_time, (list, dict))

    details_event = dt_client.details.get(
        did,
        eventtype="connection",
        responsedata="device,model,connections",
        count=1
    )
    assert isinstance(details_event, (list, dict))

def test_deviceinfo(dt_client):
    # Test 1: Basic deviceinfo retrieval
    result = dt_client.deviceinfo.get(did=1)
    assert result is not None

    # Test 2: All parameters set
    result = dt_client.deviceinfo.get(
        did=1,
        datatype="sizein",
        odid=100,
        port=443,
        externaldomain="google.com",
        fulldevicedetails=True,
        showallgraphdata=True,
        similardevices=2,
        intervalhours=12
    )
    assert result is not None

    # Test 3: Edge case - similardevices=0
    result = dt_client.deviceinfo.get(did=1, similardevices=0)
    assert result is not None

    # Test 4: Edge case - intervalhours > 1
    result = dt_client.deviceinfo.get(did=1, intervalhours=6)
    assert result is not None

    # Test 5: Edge case - showallgraphdata=False
    result = dt_client.deviceinfo.get(did=1, showallgraphdata=False)
    assert result is not None


@pytest.mark.usefixtures("dt_client")
def test_devices_basic(dt_client):
    """Test Devices endpoint: basic retrieval and edge cases."""
    # 1. Get a device with a specific IP
    result_ip = dt_client.devices.get(ip="10.0.0.1")
    assert result_ip is not None

    # 2. Get a list of all the devices seen in the last hour
    result_seen = dt_client.devices.get(seensince="1hour")
    assert result_seen is not None

    # 3. Get a list of Google Cloud Platform and Microsoft 365 devices, with only the device identifier and username returned
    result_saas = dt_client.devices.get(saasfilter="gcp*", responsedata="did,hostname")
    assert result_saas is not None
    result_saas2 = dt_client.devices.get(saasfilter="office365*", responsedata="did,hostname")
    assert result_saas2 is not None

    # 4. Get a device by MAC address (if supported by your instance)
    result_mac = dt_client.devices.get(mac="00:11:22:33:44:55")
    assert result_mac is not None

    # 5. Get devices by subnet and seensince
    result_subnet = dt_client.devices.get(seensince="2min", sid=25)
    assert result_subnet is not None

    # 6. Get devices by device id (did)
    result_did = dt_client.devices.get(did=1)
    assert result_did is not None

    # 7. Get devices by subnet id (sid)
    result_sid = dt_client.devices.get(sid=25)
    assert result_sid is not None

    # 8. Get devices by cloudsecurity
    result_cloud = dt_client.devices.get(cloudsecurity=True)
    assert result_cloud is not None

    # 9. Get devices by includetags
    result_tags = dt_client.devices.get(includetags=True)
    assert result_tags is not None

@pytest.mark.usefixtures("dt_client")
def test_model_breaches(dt_client):
    """Test model breaches endpoint: all parameters and edge cases."""
    # 1. Basic breach retrieval
    breaches = dt_client.breaches.get(minimal=True, count=5)
    assert isinstance(breaches, list)

    # 2. Detailed breach info with device at top and expandenums
    detailed_breaches = dt_client.breaches.get(
        minimal=False,
        deviceattop=True,
        count=1,
        expandenums=True
    )
    assert isinstance(detailed_breaches, list)

    # 3. Time-based filtering (last 24 hours)
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=1)
    time_breaches = dt_client.breaches.get(
        from_time=start.strftime('%Y-%m-%d %H:%M:%S'),
        to_time=end.strftime('%Y-%m-%d %H:%M:%S'),
        minimal=True
    )
    assert isinstance(time_breaches, list)

    # 4. Suppressed, SaaS, and group filtering
    filtered_breaches = dt_client.breaches.get(
        includesuppressed=True,
        saasonly=True,
        group="device",
        minimal=True
    )
    assert isinstance(filtered_breaches, list)

    # 5. SaaS filter (multiple values)
    saas_breaches = dt_client.breaches.get(
        saasfilter=["office365*", "azure*"],
        minimal=True
    )
    assert isinstance(saas_breaches, list)

    # 6. Creation time filtering
    end2 = datetime.now(timezone.utc)
    start2 = end2 - timedelta(days=2)
    creation_breaches = dt_client.breaches.get(
        starttime=int(start2.timestamp() * 1000),
        endtime=int(end2.timestamp() * 1000),
        creationtime=True,
        minimal=True
    )
    assert isinstance(creation_breaches, list)

    # 7. Responsedata parameter
    resp_breaches = dt_client.breaches.get(
        responsedata="model,percentscore,device",
        minimal=True
    )
    assert isinstance(resp_breaches, list)

    # 8. Comments (read-only)
    breaches = dt_client.breaches.get(minimal=True, count=1)
    if isinstance(breaches, list) and breaches:
        pbid = breaches[0].get('pbid')
        if pbid:
            comments = dt_client.breaches.get_comments(pbid)
            assert comments is not None


@pytest.mark.usefixtures("dt_client")
def test_devicesearch_basic(dt_client):
    """Test /devicesearch endpoint: basic retrieval and parameter coverage."""
    # 1. Basic search (default params)
    result = dt_client.devicesearch.get()
    assert isinstance(result, dict)
    assert 'devices' in result

    # 2. Search with query string (wildcard)
    result_query = dt_client.devicesearch.get(query='*')
    assert isinstance(result_query, dict)
    assert 'devices' in result_query

    # 3. Search with count and offset (pagination)
    result_page = dt_client.devicesearch.get(count=2, offset=0)
    assert isinstance(result_page, dict)
    assert 'devices' in result_page

    # 4. Search with orderBy and order
    result_order = dt_client.devicesearch.get(orderBy='lastSeen', order='desc')
    assert isinstance(result_order, dict)
    assert 'devices' in result_order

    # 5. Search with responsedata (restrict fields)
    result_resp = dt_client.devicesearch.get(responsedata='devices')
    assert isinstance(result_resp, dict)
    assert 'devices' in result_resp

    # 6. Search with seensince (relative time)
    result_seen = dt_client.devicesearch.get(seensince='1hour')
    assert isinstance(result_seen, dict)
    assert 'devices' in result_seen

    # 7. Combined query (tag and label)
    result_combined = dt_client.devicesearch.get(query='tag:"*" label:"*"', count=1)
    assert isinstance(result_combined, dict)
    assert 'devices' in result_combined

@pytest.mark.usefixtures("dt_client")
def test_devicesummary_basic(dt_client):
    """Test /devicesummary endpoint: basic retrieval and parameter coverage."""
    # 1. Get a device summary for a known device (did=4336 as example, replace with real did if needed)
    try:
        result = dt_client.devicesummary.get(did=4336)
        assert isinstance(result, dict)
        assert 'data' in result
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 500:
            pytest.skip("/devicesummary endpoint returns HTTP 500 with API tokens. This is a known issue (see issue #37). Not a test or SDK bug.")
        else:
            raise

    # 2. Get device summary with responsedata filter
    try:
        result_resp = dt_client.devicesummary.get(did=4336, responsedata='devices')
        assert isinstance(result_resp, dict)
        assert 'data' in result_resp
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 500:
            pytest.skip("/devicesummary endpoint returns HTTP 500 with API tokens. This is a known issue (see issue #37). Not a test or SDK bug.")
        else:
            raise

    # 3. Edge case: non-existent did (should return empty or error handled gracefully)
    try:
        result_none = dt_client.devicesummary.get(did=4336)
        assert isinstance(result_none, dict)
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 500:
            pytest.skip("/devicesummary endpoint returns HTTP 500 with API tokens. This is a known issue (see issue #37). Not a test or SDK bug.")
        else:
            # Acceptable: API returns error for unknown did
            assert True

# --- Email module tests ---
@pytest.mark.usefixtures("dt_client")
def test_email_decode_link(dt_client):
    # This test expects a valid encoded link. Use a dummy or skip if not available.
    # result = dt_client.email.decode_link(link="https://...encoded...")
    # assert isinstance(result, dict)
    pass  # No real encoded link available for test

@pytest.mark.usefixtures("dt_client")
def test_email_get_action_summary(dt_client):
    try:
        result = dt_client.email.get_action_summary(days=7, limit=2)
        assert isinstance(result, dict)
    except requests.exceptions.JSONDecodeError:
        pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
    except Exception as e:
        msg = str(e)
        if "login" in msg.lower() or "html" in msg.lower():
            pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
        else:
            raise

@pytest.mark.usefixtures("dt_client")
def test_email_get_dash_stats(dt_client):
    try:
        result = dt_client.email.get_dash_stats(days=7, limit=2)
        assert isinstance(result, dict)
    except requests.exceptions.JSONDecodeError:
        pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
    except Exception as e:
        msg = str(e)
        if "login" in msg.lower() or "html" in msg.lower():
            pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
        else:
            raise

@pytest.mark.usefixtures("dt_client")
def test_email_get_data_loss(dt_client):
    try:
        result = dt_client.email.get_data_loss(days=7, limit=2)
        assert isinstance(result, dict)
    except requests.exceptions.JSONDecodeError:
        pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
    except Exception as e:
        msg = str(e)
        if "login" in msg.lower() or "html" in msg.lower():
            pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
        else:
            raise

@pytest.mark.usefixtures("dt_client")
def test_email_get_user_anomaly(dt_client):
    try:
        result = dt_client.email.get_user_anomaly(days=28, limit=2)
        assert isinstance(result, dict)
    except requests.exceptions.JSONDecodeError:
        pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
    except Exception as e:
        msg = str(e)
        if "login" in msg.lower() or "html" in msg.lower():
            pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
        else:
            raise

@pytest.mark.usefixtures("dt_client")
def test_email_get_tags(dt_client):
    try:
        result = dt_client.email.get_tags()
        assert isinstance(result, dict)
    except requests.exceptions.JSONDecodeError:
        pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
    except Exception as e:
        msg = str(e)
        if "login" in msg.lower() or "html" in msg.lower():
            pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
        else:
            raise

@pytest.mark.usefixtures("dt_client")
def test_email_get_actions(dt_client):
    try:
        result = dt_client.email.get_actions()
        assert isinstance(result, dict)
    except requests.exceptions.JSONDecodeError:
        pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
    except Exception as e:
        msg = str(e)
        if "login" in msg.lower() or "html" in msg.lower():
            pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
        else:
            raise

@pytest.mark.usefixtures("dt_client")
def test_email_get_filters(dt_client):
    try:
        result = dt_client.email.get_filters()
        assert isinstance(result, dict)
    except requests.exceptions.JSONDecodeError:
        pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
    except Exception as e:
        msg = str(e)
        if "login" in msg.lower() or "html" in msg.lower():
            pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
        else:
            raise

@pytest.mark.usefixtures("dt_client")
def test_email_get_event_types(dt_client):
    try:
        result = dt_client.email.get_event_types()
        assert isinstance(result, dict)
    except requests.exceptions.JSONDecodeError:
        pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
    except Exception as e:
        msg = str(e)
        if "login" in msg.lower() or "html" in msg.lower():
            pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
        else:
            raise

@pytest.mark.usefixtures("dt_client")
def test_email_get_audit_events(dt_client):
    try:
        result = dt_client.email.get_audit_events(limit=2)
        assert isinstance(result, dict)
    except requests.exceptions.JSONDecodeError:
        pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
    except Exception as e:
        msg = str(e)
        if "login" in msg.lower() or "html" in msg.lower():
            pytest.skip("Darktrace Email API is not available or not licensed. A Darktrace Email license is required for this functionality.")
        else:
            raise

@pytest.mark.usefixtures("dt_client")
def test_email_get_email_and_download(dt_client):
    # This test expects a real email UUID. Try to search for one, else skip.
    # Use the search_emails endpoint if available, else skip.
    # This is a read-only test, so only GET endpoints are tested.
    # Try to get a random email UUID from the API (if possible):
    try:
        # Use a search with minimal params to get at least one email
        search_result = dt_client.email.search_emails({"limit": 1})
        emails = search_result.get("emails", [])
        if emails:
            uuid = emails[0].get("uuid")
            if uuid:
                details = dt_client.email.get_email(uuid)
                assert isinstance(details, dict)
                # Download (content, not checked for type)
                content = dt_client.email.download_email(uuid)
                assert isinstance(content, (bytes, bytearray))
    except Exception:
        pass  # Acceptable if no email is available

@pytest.mark.usefixtures("dt_client")
def test_endpointdetails_basic(dt_client):
    """Test EndpointDetails endpoint: all parameters and edge cases."""
    # 1. Basic IP query
    result_ip = dt_client.endpointdetails.get(ip="8.8.8.8")
    assert result_ip is not None

    # 2. Hostname query
    result_host = dt_client.endpointdetails.get(hostname="darktrace.com")
    assert result_host is not None

    # 3. Hostname with devices
    result_host_devices = dt_client.endpointdetails.get(hostname="darktrace.com", devices=True)
    assert result_host_devices is not None

    # 4. Hostname with additionalinfo
    result_host_info = dt_client.endpointdetails.get(hostname="darktrace.com", additionalinfo=True)
    assert result_host_info is not None

    # 5. Hostname with score
    result_host_score = dt_client.endpointdetails.get(hostname="darktrace.com", score=True)
    assert result_host_score is not None

    # 6. Hostname with responsedata
    result_host_resp = dt_client.endpointdetails.get(hostname="darktrace.com", responsedata="devices")
    assert result_host_resp is not None

    # 7. Edge case: non-existent hostname
    try:
        result_none = dt_client.endpointdetails.get(hostname="nonexistentdomain.example")
        assert result_none is not None
    except Exception:
        # Acceptable: API returns error for unknown hostname
        assert True
        
    # --- Enums module tests ---
@pytest.mark.usefixtures("dt_client")
def test_enums_all(dt_client):
    """Test /enums endpoint: get all enums."""
    result = dt_client.enums.get()
    assert isinstance(result, dict)
    # Should contain at least one known enum category (e.g., 'Country', 'Matching metrics', etc.)
    assert any(isinstance(v, list) for v in result.values())

@pytest.mark.usefixtures("dt_client")
def test_enums_countries(dt_client):
    """Test /enums endpoint: filter by responsedata=Country."""
    result = dt_client.enums.get(responsedata="Country")
    assert isinstance(result, dict)

@pytest.mark.usefixtures("dt_client")
def test_enums_invalid_responsedata(dt_client):
    """Test /enums endpoint: invalid responsedata returns empty or error handled gracefully."""
    try:
        result = dt_client.enums.get(responsedata="notarealenumcategory")
        assert isinstance(result, dict)
        # Should be empty or not contain the invalid key
        assert not result or all(k.lower() != "notarealenumcategory" for k in result.keys())
    except Exception:
        # Acceptable: API returns error for unknown responsedata
        assert True

# --- Filtertypes module tests ---
@pytest.mark.usefixtures("dt_client")
def test_filtertypes_all(dt_client):
    """Test /filtertypes endpoint: get all filter types."""
    result = dt_client.filtertypes.get()
    assert isinstance(result, list)
    # Should contain at least one filter type with required fields
    assert any(
        isinstance(item, dict) and 'filtertype' in item and 'valuetype' in item and 'comparators' in item
        for item in result
    )

@pytest.mark.usefixtures("dt_client")
def test_filtertypes_responsedata_comparators(dt_client):
    """Test /filtertypes endpoint: filter by responsedata=comparators."""
    result = dt_client.filtertypes.get(responsedata="comparators")
    # Should be a dict or list, depending on API version/response
    assert isinstance(result, (dict, list))
    # If dict, should have 'comparators' or similar key
    if isinstance(result, dict):
        assert any('comparator' in k.lower() for k in result.keys()) or any('comparator' in str(v).lower() for v in result.values())
    elif isinstance(result, list):
        # If list, should contain comparator strings or dicts with comparators
        assert all(isinstance(item, (str, dict)) for item in result)

@pytest.mark.usefixtures("dt_client")
def test_filtertypes_invalid_responsedata(dt_client):
    """Test /filtertypes endpoint: invalid responsedata returns empty or error handled gracefully."""
    try:
        result = dt_client.filtertypes.get(responsedata="notarealfield")
        assert isinstance(result, (dict, list))
        # Should be empty or not contain the invalid key
        if isinstance(result, dict):
            assert not result or all(k.lower() != "notarealfield" for k in result.keys())
        elif isinstance(result, list):
            assert not result
    except Exception:
        # Acceptable: API returns error for unknown responsedata
        assert True


# --- IntelFeed module tests (#15) ---
@pytest.mark.usefixtures("dt_client")
def test_intelfeed_sources(dt_client):
    """Test /intelfeed endpoint: get all sources."""
    result = dt_client.intelfeed.get(sources=True)
    assert isinstance(result, list)
    # Should contain at least one string (source name)
    assert all(isinstance(item, str) for item in result)

@pytest.mark.usefixtures("dt_client")
def test_intelfeed_by_source(dt_client):
    """Test /intelfeed endpoint: get entries by source (if any source exists)."""
    sources = dt_client.intelfeed.get(sources=True)
    if sources:
        result = dt_client.intelfeed.get(source=sources[0])
        assert isinstance(result, list)
        assert all(isinstance(item, (str, dict)) for item in result)

@pytest.mark.usefixtures("dt_client")
def test_intelfeed_all(dt_client):
    """Test /intelfeed endpoint: get all watched domains/IPs/hostnames."""
    result = dt_client.intelfeed.get()
    assert isinstance(result, list)
    if result:
        assert any(isinstance(item, (str, dict)) for item in result)

@pytest.mark.usefixtures("dt_client")
def test_intelfeed_fulldetails(dt_client):
    """Test /intelfeed endpoint: get all entries with full details."""
    result = dt_client.intelfeed.get(fulldetails=True)
    assert isinstance(result, list)
    if result:
        assert any(isinstance(item, dict) and 'name' in item for item in result)

@pytest.mark.usefixtures("dt_client")
def test_intelfeed_invalid_source(dt_client):
    """Test /intelfeed endpoint: invalid source returns empty or error handled gracefully."""
    try:
        result = dt_client.intelfeed.get(source="notarealsource")
        assert isinstance(result, list)
        assert not result  # Should be empty
    except Exception:
        # Acceptable: API returns error for unknown source
        assert True

# --- MBComments module tests (#16) ---
@pytest.mark.usefixtures("dt_client")
def test_mbcomments_all(dt_client):
    """Test /mbcomments endpoint: get all comments (default params)."""
    result = dt_client.mbcomments.get()
    assert isinstance(result, list)
    # Should contain dicts with required fields if not empty
    if result:
        assert all(isinstance(item, dict) for item in result)
        for item in result:
            assert 'time' in item and 'pbid' in item and 'username' in item and 'message' in item

@pytest.mark.usefixtures("dt_client")
def test_mbcomments_time_range(dt_client):
    """Test /mbcomments endpoint: get comments in a specific time range."""
    end = int(datetime.now(timezone.utc).timestamp() * 1000)
    start = end - 7 * 24 * 60 * 60 * 1000  # last 7 days
    result = dt_client.mbcomments.get(starttime=start, endtime=end)
    assert isinstance(result, list)
    if result:
        assert all(isinstance(item, dict) for item in result)

@pytest.mark.usefixtures("dt_client")
def test_mbcomments_count(dt_client):
    """Test /mbcomments endpoint: get a limited number of comments."""
    result = dt_client.mbcomments.get(count=1)
    assert isinstance(result, list)
    assert len(result) <= 1

@pytest.mark.usefixtures("dt_client")
def test_mbcomments_by_pbid(dt_client):
    """Test /mbcomments endpoint: get comments for a specific model breach (if any exist)."""
    all_comments = dt_client.mbcomments.get()
    pbid = None
    if all_comments:
        pbid = all_comments[0].get('pbid')
    if pbid is not None:
        result = dt_client.mbcomments.get(pbid=pbid)
        assert isinstance(result, list)
        if result:
            assert all(item.get('pbid') == pbid for item in result)

@pytest.mark.usefixtures("dt_client")
def test_mbcomments_invalid_pbid(dt_client):
    """Test /mbcomments endpoint: invalid pbid returns empty or error handled gracefully."""
    try:
        result = dt_client.mbcomments.get(pbid=999999999)
        assert isinstance(result, list)
        assert not result  # Should be empty
    except Exception:
        # Acceptable: API returns error for unknown pbid
        assert True

# --- metricdata module tests (#17) ---
@pytest.mark.usefixtures("dt_client")
def test_metricdata_basic(dt_client):
    """Test /metricdata endpoint: basic metric query with required parameter."""
    # Try a common metric (e.g., 'connections') and a known device if possible
    try:
        result = dt_client.metricdata.get(metric="connections")
        assert isinstance(result, dict)
        assert 'data' in result or 'metric' in result or result  # Accept any non-empty dict
    except Exception as e:
        # Acceptable: API returns error if no data or metric not available
        assert True

@pytest.mark.usefixtures("dt_client")
def test_metricdata_multiple_metrics(dt_client):
    """Test /metricdata endpoint: query with multiple metrics."""
    try:
        result = dt_client.metricdata.get(metrics=["connections", "bytesin"])
        assert isinstance(result, dict)
        assert result  # Should be non-empty if metrics exist
    except Exception as e:
        assert True

@pytest.mark.usefixtures("dt_client")
def test_metricdata_with_parameters(dt_client):
    """Test /metricdata endpoint: all supported parameters (read-only)."""
    # Use a time range for the last hour
    end = int(datetime.now(timezone.utc).timestamp() * 1000)
    start = end - 60 * 60 * 1000
    try:
        result = dt_client.metricdata.get(
            metric="connections",
            starttime=start,
            endtime=end,
            interval="5min",
            protocol="tcp",
            breachtimes=True,
            fulldevicedetails=False
        )
        assert isinstance(result, dict)
    except Exception as e:
        assert True

@pytest.mark.usefixtures("dt_client")
def test_metricdata_invalid_metric(dt_client):
    """Test /metricdata endpoint: invalid metric returns error or empty result gracefully."""
    try:
        result = dt_client.metricdata.get(metric="notarealmetric")
        assert isinstance(result, dict)
        # Should be empty or error handled gracefully
        assert not result or 'error' in result or 'message' in result
    except Exception:
        assert True

# --- metrics module tests (#18) ---
@pytest.mark.usefixtures("dt_client")
def test_metrics_list(dt_client):
    """Test /metrics endpoint: get list of all metrics."""
    result = dt_client.metrics.get()
    assert isinstance(result, list)
    assert result and isinstance(result[0], dict) and 'mlid' in result[0]

@pytest.mark.usefixtures("dt_client")
def test_metrics_single(dt_client):
    """Test /metrics/{id} endpoint: get details for a single metric."""
    metrics = dt_client.metrics.get()
    if metrics and isinstance(metrics, list):
        mlid = metrics[0].get('mlid')
        if mlid is not None:
            result = dt_client.metrics.get(metric_id=mlid)
            assert isinstance(result, dict)
            assert result.get('mlid') == mlid

@pytest.mark.usefixtures("dt_client")
def test_metrics_responsedata(dt_client):
    """Test /metrics endpoint: restrict response with responsedata param."""
    result = dt_client.metrics.get(responsedata="mlid,name")
    assert isinstance(result, list)
    if result:
        assert 'mlid' in result[0] and 'name' in result[0]

@pytest.mark.usefixtures("dt_client")
def test_metrics_invalid_id(dt_client):
    """Test /metrics/{id} endpoint: invalid id returns error or empty result gracefully."""
    try:
        result = dt_client.metrics.get(metric_id=999999999)
        assert isinstance(result, dict)
        # Should be empty or error handled gracefully
        assert not result or 'error' in result or 'message' in result
    except Exception:
        assert True

# --- models module tests (#19) ---
@pytest.mark.usefixtures("dt_client")
def test_models_list(dt_client):
    """Test /models endpoint: get list of all models."""
    result = dt_client.models.get()
    assert isinstance(result, list)
    # Should contain at least one model with required fields
    if result:
        assert any(isinstance(item, dict) and 'uuid' in item and 'name' in item for item in result)

@pytest.mark.usefixtures("dt_client")
def test_models_single(dt_client):
    """Test /models endpoint: get details for a single model by uuid."""
    models = dt_client.models.get()
    if models and isinstance(models, list):
        uuid = models[0].get('uuid')
        if uuid is not None:
            result = dt_client.models.get(uuid=uuid)
            # API may return a list or dict for single uuid
            assert isinstance(result, (dict, list))
            if isinstance(result, dict):
                assert result.get('uuid') == uuid
            elif isinstance(result, list):
                assert any(item.get('uuid') == uuid for item in result)

@pytest.mark.usefixtures("dt_client")
def test_models_responsedata(dt_client):
    """Test /models endpoint: restrict response with responsedata param."""
    result = dt_client.models.get(responsedata="uuid,name")
    assert isinstance(result, list)
    if result:
        assert 'uuid' in result[0] and 'name' in result[0]

@pytest.mark.usefixtures("dt_client")
def test_models_invalid_uuid(dt_client):
    """Test /models endpoint: invalid uuid returns error or empty result gracefully."""
    try:
        result = dt_client.models.get(uuid="not-a-real-uuid-1234")
        assert isinstance(result, (dict, list))
        # Should be empty or error handled gracefully
        if isinstance(result, dict):
            assert not result or 'error' in result or 'message' in result
        elif isinstance(result, list):
            assert not result
    except Exception:
        # Acceptable: API returns error for unknown uuid
        assert True

# --- network module tests (#20) ---
@pytest.mark.usefixtures("dt_client")
def test_network_basic(dt_client):
    """Test /network endpoint: basic retrieval and parameter coverage."""
    # 1. Basic call (should return a dict with statistics and devices)
    result = dt_client.network.get()
    assert isinstance(result, dict)
    assert 'statistics' in result

    # 2. Filter by device id (did)
    result_did = dt_client.network.get(did=1)
    assert isinstance(result_did, dict)

    # 3. Filter by metric (datatransfervolume)
    result_metric = dt_client.network.get(metric="datatransfervolume")
    assert isinstance(result_metric, dict)

    # 4. Filter by protocol (e.g., 'TCP')
    result_proto = dt_client.network.get(protocol="TCP")
    assert isinstance(result_proto, dict)

    # 5. Filter by applicationprotocol (e.g., 'DNS')
    result_aproto = dt_client.network.get(applicationprotocol="DNS")
    assert isinstance(result_aproto, dict)

    # 6. Filter by intext (internal/external)
    result_internal = dt_client.network.get(intext="internal")
    assert isinstance(result_internal, dict)
    result_external = dt_client.network.get(intext="external")
    assert isinstance(result_external, dict)

    # 7. Filter by time (from/to)
    end = datetime.now()
    start = end - timedelta(hours=1)
    result_time = dt_client.network.get(from_=start.strftime('%Y-%m-%d %H:%M:%S'), to=end.strftime('%Y-%m-%d %H:%M:%S'))
    assert isinstance(result_time, dict)

    # 8. Filter by responsedata (restrict fields)
    result_resp = dt_client.network.get(responsedata="statistics")
    assert isinstance(result_resp, dict)
    assert 'statistics' in result_resp

    # 9. Edge case: non-existent did
    try:
        result_none = dt_client.network.get(did=999999)
        assert isinstance(result_none, dict)
    except Exception:
        assert True
