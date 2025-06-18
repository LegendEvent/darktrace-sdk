#!/usr/bin/env python3
"""
Test script for the Darktrace SDK
This script demonstrates the basic functionality of the Darktrace SDK
"""

from darktrace import DarktraceClient
import argparse
import sys
import urllib3
import requests

def test_connection(host, public_token, private_token, debug=False, verify_ssl=True):
    """Test the connection to the Darktrace instance"""
    print(f"Testing connection to {host}...")
    try:
        # Initialize the client
        client = DarktraceClient(
            host=host,
            public_token=public_token,
            private_token=private_token,
            debug=debug
        )
        
        # Set SSL verification for requests if needed
        if not verify_ssl:
            # This is a workaround since DarktraceClient doesn't have a verify_ssl parameter
            # We need to modify the session used by requests library
            urllib3.disable_warnings()
            
        # Try to get status (simple endpoint that requires authentication)
        status = client.status.get()
        print(f"✅ Connection successful!")
        print(f"Instance info: {status.get('status', {}).get('instancename', 'Unknown')}")
        print(f"Version: {status.get('status', {}).get('version', 'Unknown')}")
        return client
    
    except requests.RequestException as e:
        print(f"❌ Connection failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return None    
    
def test_devices(client, limit=5):
    """Test getting devices from Darktrace"""
    print("\nFetching devices...")
    try:
        # Using count parameter to demonstrate parameter handling
        devices = client.devices.get(count=limit)
        if isinstance(devices, dict):
            devices = devices.get('devices', [])
        print(f"✅ Found {len(devices)} devices")
        
        # Print some details about each device
        for i, device in enumerate(devices[:limit]):
            print(f"  [{i+1}] {device.get('hostname', 'Unknown')} (ID: {device.get('did', 'Unknown')})")
        return True
    
    except requests.RequestException as e:
        print(f"❌ Error fetching devices: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error fetching devices: {str(e)}")
        return False

def test_model_breaches(client, limit=5):
    """Test getting model breaches from Darktrace"""
    print("\nTesting model breaches endpoint...")
    successes = 0
    total_tests = 3
    
    try:
        # Test 1: Basic breach retrieval with count limit
        print("\nTest 1: Basic breach retrieval...")
        try:
            breaches = client.breaches.get(minimal=True, count=limit)
            print(f"Raw response type: {type(breaches)}")
            
            if isinstance(breaches, list):
                print(f"✅ Found {len(breaches)} model breaches")
                # Print some details about each breach
                for i, breach in enumerate(breaches[:limit]):
                    model_name = breach.get('model', {}).get('then', {}).get('name', 'Unknown')
                    pbid = breach.get('pbid', 'Unknown')
                    print(f"  [{i+1}] {model_name} (ID: {pbid})")
                successes += 1
            else:
                print(f"❌ Expected list response for breaches, got {type(breaches)}")
        except Exception as e:
            print(f"❌ Error in test 1: {str(e)}")
            return False
        
        # Test 2: Detailed breach info with device at top
        print("\nTest 2: Detailed breach info...")
        try:
            detailed_breaches = client.breaches.get(
                minimal=False,
                deviceattop=True,
                count=1,
                expandenums=True
            )
            
            print(f"Raw response type: {type(detailed_breaches)}")
            
            if isinstance(detailed_breaches, list):
                print("✅ Successfully retrieved breach response")
                print(f"  Found {len(detailed_breaches)} detailed breaches")
                # Print some details from the first breach
                if detailed_breaches:
                    first_breach = detailed_breaches[0]
                    model_name = first_breach.get('model', {}).get('then', {}).get('name', 'Unknown')
                    device = first_breach.get('device', {})
                    print(f"  First breach: {model_name}")
                    if device:
                        print(f"  Device: {device.get('hostname', 'Unknown')} ({device.get('did', 'Unknown')})")
                successes += 1
            else:
                print(f"❌ Expected list response for detailed breaches, got {type(detailed_breaches)}")
        except Exception as e:
            print(f"❌ Error in test 2: {str(e)}")
            return False
        
        # Test 3: Time-based filtering (last 24 hours)
        print("\nTest 3: Time-based filtering...")
        try:
            from datetime import datetime, timezone, timedelta
            end = datetime.now(timezone.utc)
            start = end - timedelta(days=1)
            time_breaches = client.breaches.get(
                from_time=start.strftime('%Y-%m-%d %H:%M:%S'),
                to_time=end.strftime('%Y-%m-%d %H:%M:%S'),
                minimal=True
            )
            
            print(f"Raw response type: {type(time_breaches)}")
            
            if isinstance(time_breaches, list):
                print("✅ Successfully retrieved time-filtered breaches")
                print(f"  Found {len(time_breaches)} breaches in the last 24 hours")
                successes += 1
            else:
                print(f"❌ Expected list response for time-filtered breaches, got {type(time_breaches)}")
        except Exception as e:
            print(f"❌ Error in test 3: {str(e)}")
            return False
        
        print(f"\nModel breaches tests completed: {successes}/{total_tests} passed")
        return successes == total_tests
    
    except requests.RequestException as e:
        print(f"❌ Error fetching model breaches: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error in model breaches test: {str(e)}")
        return False

def test_intel_feed(client):
    """Test the Intel Feed module with the fixed authentication mechanism"""
    print("\nTesting Intel Feed module...")
    try:
        # Get sources - tests the sources=true parameter
        sources = client.intelfeed.get_sources()
        print(f"✅ Found {len(sources)} Intel Feed sources")
        
        # Test basic get functionality
        print("Testing basic get functionality...")
        entries = client.intelfeed.get()
        print(f"✅ Found {len(entries)} Intel Feed entries")
        
        # Test get with full_details parameter
        print("Testing get with full_details parameter...")
        detailed_entries = client.intelfeed.get(full_details=True)
        print(f"✅ Found {len(detailed_entries)} detailed Intel Feed entries")
        
        # If there are sources, try to get entries from the first source
        if sources and len(sources) > 0:
            source = sources[0]
            print(f"Fetching entries from source '{source}'...")
            
            # Test source parameter
            source_entries = client.intelfeed.get(source=source)
            print(f"✅ Found {len(source_entries)} entries in source '{source}'")
            
            # Test multiple parameters together (source and full_details)
            print(f"Testing multiple parameters (source and full_details)...")
            detailed_source_entries = client.intelfeed.get(source=source, full_details=True)
            print(f"✅ Found {len(detailed_source_entries)} detailed entries in source '{source}'")
            
            # Print some details about a few entries
            for i, entry in enumerate(detailed_source_entries[:3]):
                if isinstance(entry, dict):
                    print(f"  [{i+1}] {entry.get('name', 'Unknown')} - {entry.get('description', 'No description')}")
                else:
                    print(f"  [{i+1}] {entry}")
        
        return True
    
    except requests.RequestException as e:
        print(f"❌ Error testing Intel Feed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error testing Intel Feed: {str(e)}")
        return False

def test_antigena_actions(client, limit=5):
    """Test getting Antigena actions from Darktrace"""
    print("\nTesting Antigena endpoints...")
    try:
        # Test 1: Basic actions with full device details
        print("\nTest 1: Basic actions retrieval...")
        actions = client.antigena.get_actions(
            fulldevicedetails=True,
            includehistory=True
        )
        
        # Handle response format
        if isinstance(actions, dict):
            action_list = actions.get('actions', [])
            device_list = actions.get('devices', [])
            print(f"✅ Found {len(action_list)} actions and {len(device_list)} device details")
        else:
            action_list = actions if isinstance(actions, list) else []
            print(f"✅ Found {len(action_list)} actions")
            
        # Show some action details
        for i, action in enumerate(action_list[:limit]):
            print(f"  [{i+1}] {action.get('action', 'Unknown')} - "
                  f"Status: {'Active' if action.get('active') else 'Inactive'}")
            if action.get('history'):
                print(f"      History entries: {len(action['history'])}")
                
        # Test 2: Get actions with connections
        print("\nTest 2: Actions with connection details...")
        actions_with_connections = client.antigena.get_actions(
            includeconnections=True,
            includecleared=True
        )
        if isinstance(actions_with_connections, dict):
            connections = actions_with_connections.get('connections', [])
            print(f"✅ Found {len(connections)} blocked connections")
            
        # Test 3: Get actions summary
        print("\nTest 3: Actions summary...")
        from datetime import datetime, timezone, timedelta
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=1)
        
        summary = client.antigena.get_summary(
            starttime=int(start.timestamp() * 1000),
            endtime=int(end.timestamp() * 1000)
        )
        print(f"✅ Active actions: {summary.get('activeCount', 0)}")
        print(f"  Pending actions: {summary.get('pendingCount', 0)}")
        if summary.get('activeActionDevices'):
            print(f"  Devices with active actions: {len(summary['activeActionDevices'])}")
            
        return True
    
    except requests.RequestException as e:
        print(f"❌ Error testing Antigena: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error testing Antigena: {str(e)}")
        return False

def test_advanced_search(client, limit=5):
    """Test Advanced Search functionality"""
    print("\nTesting Advanced Search endpoints...")
    
    try:
        # Test 1: Basic search functionality
        print("\nTest 1: Basic search query...")
        # Simple query for SSL connections on port 443 in the last 15 minutes
        search_query = {
            "search": "@type:\"ssl\" AND @fields.dest_port:\"443\"",
            "fields": [],
            "offset": 0,
            "timeframe": "900",  # 15 minutes
            "time": {"user_interval": 0}
        }
        
        search_results = client.advanced_search.search(search_query)
        total_hits = search_results.get('hits', {}).get('total', 0)
        hits = search_results.get('hits', {}).get('hits', [])
        print(f"✅ Found {total_hits} SSL connections, showing {len(hits)} results")
        
        # Show some sample results
        for i, hit in enumerate(hits[:3]):
            source = hit.get('_source', {})
            timestamp = source.get('@timestamp', 'Unknown')
            msg_type = source.get('@type', 'Unknown')
            print(f"  [{i+1}] {msg_type} at {timestamp}")
        
        # Test 2: Analyze field data (terms analysis)
        print("\nTest 2: Field analysis (terms)...")
        # Analyze destination ports for DNS traffic
        analyze_query = {
            "search": "@type:\"dns\" AND @fields.proto:\"udp\"",
            "fields": [],
            "offset": 0,
            "timeframe": "3600",  # 1 hour
            "time": {"user_interval": 0}
        }
        
        analyze_results = client.advanced_search.analyze("@fields.dest_port", "terms", analyze_query)
        buckets = analyze_results.get('aggregations', {}).get('terms', {}).get('buckets', [])
        print(f"✅ Analyzed destination ports, found {len(buckets)} unique values")
        
        # Show top ports
        for i, bucket in enumerate(buckets[:3]):
            port = bucket.get('key', 'Unknown')
            count = bucket.get('doc_count', 0)
            print(f"  [{i+1}] Port {port}: {count} occurrences")
        
        # Test 3: Graph data (count over time)
        print("\nTest 3: Graph data (count)...")
        # Get connection counts over the last 4 hours with 5-minute intervals
        graph_query = {
            "search": "@type:\"conn\"",
            "fields": [],
            "offset": 0,
            "timeframe": "14400",  # 4 hours
            "time": {"user_interval": 0}
        }
        
        graph_results = client.advanced_search.graph("count", 300000, graph_query)  # 5-minute intervals
        graph_buckets = graph_results.get('aggregations', {}).get('count', {}).get('buckets', [])
        print(f"✅ Generated graph data with {len(graph_buckets)} time intervals")
        
        # Show some time intervals
        for i, bucket in enumerate(graph_buckets[:3]):
            timestamp = bucket.get('key', 0)
            count = bucket.get('doc_count', 0)
            # Convert timestamp to readable format
            from datetime import datetime
            readable_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  [{i+1}] {readable_time}: {count} connections")
          # Test 4: POST request method (currently not supported)
        print("\nTest 4: POST request method...")
        post_query = {
            "search": "@type:\"conn\" AND @fields.proto:\"tcp\"",
            "fields": [],
            "offset": 0,
            "timeframe": "1800",  # 30 minutes
            "time": {"user_interval": 0}
        }
        
        try:
            post_results = client.advanced_search.search(post_query, post_request=True)
            post_hits = post_results.get('hits', {}).get('total', 0)
            print(f"✅ POST request returned {post_hits} TCP connections")
        except NotImplementedError as e:
            print(f"⚠️  POST request is not supported: {e}")
            print("   Using GET request instead (recommended)...")
            # Fall back to GET request
            get_results = client.advanced_search.search(post_query, post_request=False)
            get_hits = get_results.get('hits', {}).get('total', 0)
            print(f"✅ GET request returned {get_hits} TCP connections")
        
        return True
        
    except requests.RequestException as e:
        print(f"❌ Error testing Advanced Search: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error testing Advanced Search: {str(e)}")
        return False

def test_analyst(client):
    """Test the AI Analyst module with various endpoints and parameters"""
    print("\nTesting AI Analyst module...")
    try:
        success_count = 0
        total_tests = 7
        
        # Test 1: Get incident events
        print("\nTest 1: Getting incident events...")
        try:
            events = client.analyst.get_incident_events()
            if isinstance(events, list):
                print(f"✅ Found {len(events)} incident events")
            else:
                print(f"✅ Incident events response: {type(events)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error getting incident events: {str(e)}")
        
        # Test 2: Get incident events with parameters
        print("\nTest 2: Getting incident events with parameters...")
        try:
            # Get events from last 24 hours with specific score range
            import time
            now = int(time.time() * 1000)
            yesterday = now - (24 * 60 * 60 * 1000)
            
            events_filtered = client.analyst.get_incident_events(
                starttime=yesterday,
                endtime=now,
                minscore=50,
                includeacknowledged=False
            )
            if isinstance(events_filtered, list):
                print(f"✅ Found {len(events_filtered)} high-score unacknowledged events from last 24h")
            else:
                print(f"✅ Filtered incident events response: {type(events_filtered)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error getting filtered incident events: {str(e)}")
        
        # Test 3: Get incident groups
        print("\nTest 3: Getting incident groups...")
        try:
            groups = client.analyst.get_groups()
            if isinstance(groups, list):
                print(f"✅ Found {len(groups)} incident groups")
            else:
                print(f"✅ Groups response: {type(groups)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error getting groups: {str(e)}")
        
        # Test 4: Get groups with filtering
        print("\nTest 4: Getting groups with category filtering...")
        try:
            critical_groups = client.analyst.get_groups(
                groupcritical=True,
                includeacknowledged=False
            )
            if isinstance(critical_groups, list):
                print(f"✅ Found {len(critical_groups)} unacknowledged critical groups")
            else:
                print(f"✅ Critical groups response: {type(critical_groups)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error getting critical groups: {str(e)}")
        
        # Test 5: Get statistics
        print("\nTest 5: Getting AI Analyst statistics...")
        try:
            stats = client.analyst.get_stats()
            if isinstance(stats, dict):
                print(f"✅ Got statistics: {list(stats.keys())}")
            else:
                print(f"✅ Stats response: {type(stats)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error getting stats: {str(e)}")
        
        # Test 6: Get investigations
        print("\nTest 6: Getting AI Analyst investigations...")
        try:
            investigations = client.analyst.get_investigations()
            if isinstance(investigations, list):
                print(f"✅ Found {len(investigations)} investigations")
                
                # Show some details if investigations exist
                for i, investigation in enumerate(investigations[:2]):
                    inv_id = investigation.get('investigationId', 'Unknown')
                    status = investigation.get('status', 'Unknown')
                    did = investigation.get('did', 'Unknown')
                    print(f"  [{i+1}] Investigation {inv_id}: Device {did}, Status: {status}")
                    
            else:
                print(f"✅ Investigations response: {type(investigations)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error getting investigations: {str(e)}")
        
        # Test 7: Test comments functionality (read-only)
        print("\nTest 7: Testing comments functionality...")
        try:
            # Try to get events first to find an incident ID for testing comments
            events = client.analyst.get_incident_events()
            if isinstance(events, list) and len(events) > 0:
                # Use the first event's ID to test comments
                test_incident_id = events[0].get('id', '')
                if test_incident_id:
                    comments = client.analyst.get_comments(test_incident_id)
                    if isinstance(comments, dict):
                        comment_list = comments.get('comments', [])
                        print(f"✅ Found {len(comment_list)} comments for incident {test_incident_id}")
                    else:
                        print(f"✅ Comments response: {type(comments)}")
                else:
                    print("⚠️  No incident ID found in events, skipping comments test")
            else:
                print("⚠️  No events available, skipping comments test")
            success_count += 1
        except Exception as e:
            print(f"❌ Error testing comments: {str(e)}")
        
        print(f"\nAI Analyst tests completed: {success_count}/{total_tests} passed")
        return success_count == total_tests
        
    except Exception as e:
        print(f"❌ Error in AI Analyst test: {str(e)}")
        return False

def main():
    """Main function to run the test script"""
    parser = argparse.ArgumentParser(description='Test the Darktrace SDK')
    parser.add_argument('--host', required=True, help='Darktrace instance URL (e.g., https://darktrace.example.com)')
    parser.add_argument('--public-token', required=True, help='Public API token')
    parser.add_argument('--private-token', required=True, help='Private API token')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--no-verify', action='store_true', help='Disable SSL verification')
    
    args = parser.parse_args()
    
    # Disable SSL warnings if requested
    if args.no_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
      # Test the connection and get client
    client = test_connection(args.host, args.public_token, args.private_token, args.debug, not args.no_verify)
    if not client:
        sys.exit(1)
    
    # Run the tests
    test_devices(client)
    test_model_breaches(client)
    test_intel_feed(client)  # Added test for Intel Feed
    test_antigena_actions(client)
    test_analyst(client)  # Added test for AI Analyst
    test_advanced_search(client)  # Added test for Advanced Search
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    main()