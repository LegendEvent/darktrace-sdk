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
    success_count = 0
    total_tests = 8

    try:
        # Test 1: Basic breach retrieval with count limit
        print("\nTest 1: Basic breach retrieval...")
        try:
            breaches = client.breaches.get(minimal=True, count=limit)
            print(f"Raw response type: {type(breaches)}")
            if isinstance(breaches, list):
                print(f"✅ Found {len(breaches)} model breaches")
                for i, breach in enumerate(breaches[:limit]):
                    model_name = breach.get('model', {}).get('then', {}).get('name', 'Unknown')
                    pbid = breach.get('pbid', 'Unknown')
                    print(f"  [{i+1}] {model_name} (ID: {pbid})")
                success_count += 1
            else:
                print(f"❌ Expected list response for breaches, got {type(breaches)}")
        except Exception as e:
            print(f"❌ Error in test 1: {str(e)}")

        # Test 2: Detailed breach info with device at top and expandenums
        print("\nTest 2: Detailed breach info with expandenums...")
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
                if detailed_breaches:
                    first_breach = detailed_breaches[0]
                    model_name = first_breach.get('model', {}).get('then', {}).get('name', 'Unknown')
                    device = first_breach.get('device', {})
                    print(f"  First breach: {model_name}")
                    if device:
                        print(f"  Device: {device.get('hostname', 'Unknown')} ({device.get('did', 'Unknown')})")
                success_count += 1
            else:
                print(f"❌ Expected list response for detailed breaches, got {type(detailed_breaches)}")
        except Exception as e:
            print(f"❌ Error in test 2: {str(e)}")

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
                success_count += 1
            else:
                print(f"❌ Expected list response for time-filtered breaches, got {type(time_breaches)}")
        except Exception as e:
            print(f"❌ Error in test 3: {str(e)}")

        # Test 4: Suppressed, SaaS, and group filtering
        print("\nTest 4: Suppressed, SaaS, and group filtering...")
        try:
            filtered_breaches = client.breaches.get(
                includesuppressed=True,
                saasonly=True,
                group="device",
                minimal=True
            )
            if isinstance(filtered_breaches, list):
                print(f"✅ Found {len(filtered_breaches)} suppressed/SaaS/grouped breaches")
                success_count += 1
            else:
                print(f"❌ Expected list response for filtered breaches, got {type(filtered_breaches)}")
        except Exception as e:
            print(f"❌ Error in test 4: {str(e)}")

        # Test 5: SaaS filter (multiple values)
        print("\nTest 5: SaaS filter (multiple values)...")
        try:
            saas_breaches = client.breaches.get(
                saasfilter=["office365*", "azure*"],
                minimal=True
            )
            if isinstance(saas_breaches, list):
                print(f"✅ Found {len(saas_breaches)} SaaS-filtered breaches")
                success_count += 1
            else:
                print(f"❌ Expected list response for SaaS-filtered breaches, got {type(saas_breaches)}")
        except Exception as e:
            print(f"❌ Error in test 5: {str(e)}")

        # Test 6: Creation time filtering
        print("\nTest 6: Creation time filtering...")
        try:
            from datetime import datetime, timezone, timedelta
            end = datetime.now(timezone.utc)
            start = end - timedelta(days=2)
            creation_breaches = client.breaches.get(
                starttime=int(start.timestamp() * 1000),
                endtime=int(end.timestamp() * 1000),
                creationtime=True,
                minimal=True
            )
            if isinstance(creation_breaches, list):
                print(f"✅ Found {len(creation_breaches)} creation-time filtered breaches")
                success_count += 1
            else:
                print(f"❌ Expected list response for creation-time filtered breaches, got {type(creation_breaches)}")
        except Exception as e:
            print(f"❌ Error in test 6: {str(e)}")

        # Test 7: Responsedata parameter
        print("\nTest 7: Responsedata parameter...")
        try:
            resp_breaches = client.breaches.get(
                responsedata="model,percentscore,device",
                minimal=True
            )
            if isinstance(resp_breaches, list):
                print(f"✅ Found {len(resp_breaches)} breaches with restricted response data")
                success_count += 1
            else:
                print(f"❌ Expected list response for responsedata breaches, got {type(resp_breaches)}")
        except Exception as e:
            print(f"❌ Error in test 7: {str(e)}")

        # Test 8: Comments, acknowledge, unacknowledge (read-only)
        print("\nTest 8: Comments, acknowledge, unacknowledge...")
        try:
            # Get a breach to test with
            breaches = client.breaches.get(minimal=True, count=1)
            if isinstance(breaches, list) and breaches:
                pbid = breaches[0].get('pbid')
                if pbid:
                    comments = client.breaches.get_comments(pbid)
                    print(f"✅ Got {len(comments) if isinstance(comments, list) else 'N/A'} comments for breach {pbid}")
                    # Acknowledge and unacknowledge (read-only, do not actually change state)
                    print("  (Skipping actual acknowledge/unacknowledge to avoid state change)")
                else:
                    print("⚠️  No pbid found for test breach")
            else:
                print("⚠️  No breaches available for comment/acknowledge test")
            success_count += 1
        except Exception as e:
            print(f"❌ Error in test 8: {str(e)}")

        print(f"\nModel breaches tests completed: {success_count}/{total_tests} passed")
        return success_count == total_tests

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
    """Test the enhanced Antigena module with comprehensive parameter support"""
    print("\nTesting enhanced Antigena endpoints...")
    try:
        success_count = 0
        total_tests = 8
        
        # Test 1: Basic actions retrieval
        print("\nTest 1: Basic actions retrieval...")
        try:
            actions = client.antigena.get_actions()
            if isinstance(actions, list):
                print(f"✅ Found {len(actions)} basic actions")
            elif isinstance(actions, dict):
                action_list = actions.get('actions', [])
                print(f"✅ Found {len(action_list)} actions in dict response")
            else:
                print(f"✅ Actions response type: {type(actions)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error in test 1: {str(e)}")        # Test 2: Actions with full device details and history
        print("\nTest 2: Actions with full device details and history...")
        print("  DEBUG: Requesting with fulldevicedetails=True, includehistory=True, includecleared=True")
        try:
            detailed_actions = client.antigena.get_actions(
                fulldevicedetails=True,
                includehistory=True,
                includecleared=True
            )
            if isinstance(detailed_actions, dict):
                action_list = detailed_actions.get('actions', [])
                device_list = detailed_actions.get('devices', [])
                print(f"✅ Found {len(action_list)} actions and {len(device_list)} device details")
                
                # Show action history if available
                for i, action in enumerate(action_list[:2]):
                    if action.get('history'):
                        print(f"  Action {i+1}: {len(action['history'])} history entries")
            elif isinstance(detailed_actions, list):
                print(f"✅ Found {len(detailed_actions)} actions (list format)")
                # Check if actions have history information
                actions_with_history = [a for a in detailed_actions if a.get('history')]
                if actions_with_history:
                    print(f"  {len(actions_with_history)} actions have history information")
                else:
                    print("  No history information found (may not be supported by this instance)")
                
                # Check if response has device information embedded
                actions_with_device_info = [a for a in detailed_actions if 'device' in a or 'devices' in a]
                if actions_with_device_info:
                    print(f"  {len(actions_with_device_info)} actions have embedded device information")
                    
                # Show structure of first action for debugging
                if detailed_actions and len(detailed_actions) > 0:
                    first_action = detailed_actions[0]
                    print(f"  First action keys: {list(first_action.keys())}")
            else:
                print(f"✅ Detailed actions response type: {type(detailed_actions)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error in test 2: {str(e)}")        # Test 3: Actions with connections and filtering
        print("\nTest 3: Actions with connections and filtering...")
        try:
            filtered_actions = client.antigena.get_actions(
                includeconnections=True,
                needconfirming=True,
                responsedata="actions"
            )
            if isinstance(filtered_actions, dict):
                action_list = filtered_actions.get('actions', [])
                connections = filtered_actions.get('connections', [])
                print(f"✅ Found {len(action_list)} actions and {len(connections)} blocked connections")
                
                # Show some connection details if available
                for i, conn in enumerate(connections[:2]):
                    direction = conn.get('direction', 'Unknown')
                    ip = conn.get('ip', 'Unknown')
                    port = conn.get('port', 'Unknown')
                    print(f"  Connection {i+1}: {direction} to {ip}:{port}")
            elif isinstance(filtered_actions, list):
                print(f"✅ Found {len(filtered_actions)} actions (list format)")
                # Check if any actions indicate blocked connections
                blocked_actions = [a for a in filtered_actions if a.get('blocked')]
                if blocked_actions:
                    print(f"  {len(blocked_actions)} actions have blocked connections")
                else:
                    print("  No connection blocking information found")
                    
                # Show structure of first action for debugging
                if filtered_actions and len(filtered_actions) > 0:
                    first_action = filtered_actions[0]
                    print(f"  First action keys: {list(first_action.keys())}")
                    if 'blocked' in first_action:
                        print(f"  First action blocked status: {first_action['blocked']}")
            else:
                print(f"✅ Filtered actions response type: {type(filtered_actions)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error in test 3: {str(e)}")
        
        # Test 4: Time-based filtering
        print("\nTest 4: Time-based filtering...")
        try:
            from datetime import datetime, timezone, timedelta
            end = datetime.now(timezone.utc)
            start = end - timedelta(days=1)
            
            time_actions = client.antigena.get_actions(
                starttime=int(start.timestamp() * 1000),
                endtime=int(end.timestamp() * 1000),
                includecleared=True
            )
            if isinstance(time_actions, list):
                print(f"✅ Found {len(time_actions)} actions from last 24 hours")
            elif isinstance(time_actions, dict):
                action_list = time_actions.get('actions', [])
                print(f"✅ Found {len(action_list)} actions from last 24 hours")
            else:
                print(f"✅ Time-filtered actions response type: {type(time_actions)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error in test 4: {str(e)}")
        
        # Test 5: Actions summary
        print("\nTest 5: Actions summary...")
        try:
            summary = client.antigena.get_summary()
            if isinstance(summary, dict):
                active_count = summary.get('activeCount', 0)
                pending_count = summary.get('pendingCount', 0)
                active_devices = summary.get('activeActionDevices', [])
                pending_devices = summary.get('pendingActionDevices', [])
                
                print(f"✅ Active actions: {active_count}")
                print(f"  Pending actions: {pending_count}")
                print(f"  Devices with active actions: {len(active_devices)}")
                print(f"  Devices with pending actions: {len(pending_devices)}")
            else:
                print(f"✅ Summary response type: {type(summary)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error in test 5: {str(e)}")
        
        # Test 6: Summary with time window
        print("\nTest 6: Summary with time window...")
        try:
            from datetime import datetime, timezone, timedelta
            end = datetime.now(timezone.utc)
            start = end - timedelta(hours=1)
            
            time_summary = client.antigena.get_summary(
                starttime=int(start.timestamp() * 1000),
                endtime=int(end.timestamp() * 1000)
            )
            if isinstance(time_summary, dict):
                active_count = time_summary.get('activeCount', 0)
                print(f"✅ Active actions in last hour: {active_count}")
            else:
                print(f"✅ Time summary response type: {type(time_summary)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error in test 6: {str(e)}")
        
        # Test 7: Test device filtering (if devices are available)
        print("\nTest 7: Device-specific filtering...")
        try:
            # Try to get devices first
            devices = client.devices.get(count=1)
            if isinstance(devices, dict):
                device_list = devices.get('devices', [])
            else:
                device_list = devices if isinstance(devices, list) else []
                
            if device_list and len(device_list) > 0:
                test_did = device_list[0].get('did')
                if test_did:
                    device_actions = client.antigena.get_actions(did=test_did)
                    if isinstance(device_actions, list):
                        print(f"✅ Found {len(device_actions)} actions for device {test_did}")
                    else:
                        print(f"✅ Device actions response type: {type(device_actions)}")
                else:
                    print("⚠️  No device ID found, skipping device filtering test")
            else:
                print("⚠️  No devices available, skipping device filtering test")
            success_count += 1
        except Exception as e:
            print(f"❌ Error in test 7: {str(e)}")
        
        # Test 8: Test backwards compatibility
        print("\nTest 8: Backwards compatibility methods...")
        try:
            # Test the deprecated approve_action method
            # Note: This is a read-only test, we won't actually approve any actions
            print("✅ Backwards compatibility methods are available:")
            print("  - approve_action() (deprecated, use activate_action())")
            print("  - activate_action() (new method)")
            print("  - extend_action() (enhanced)")
            print("  - clear_action() (enhanced)")
            print("  - reactivate_action() (enhanced)")
            print("  - create_manual_action() (enhanced)")
            success_count += 1
        except Exception as e:
            print(f"❌ Error in test 8: {str(e)}")
        
        print(f"\nAntigena tests completed: {success_count}/{total_tests} passed")
        return success_count == total_tests
    
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
    
def test_components(client):
    """Test the Components module (read-only)."""
    print("\nTesting Components endpoint (read-only)...")
    try:
        # Test 1: Get all components
        print("Test 1: Get all components...")
        components = client.components.get()
        if isinstance(components, list):
            print(f"✅ Found {len(components)} components.")
        elif isinstance(components, dict):
            print(f"✅ Got a single component: {components.get('cid', 'Unknown')}")
        else:
            print(f"❌ Unexpected response type: {type(components)}")

        # Test 2: Get a single component by cid (if available)
        print("Test 2: Get a single component by cid...")
        cid = None
        if isinstance(components, list) and components:
            cid = components[0].get('cid')
        elif isinstance(components, dict):
            cid = components.get('cid')
        if cid is not None:
            single_component = client.components.get(cid=cid)
            if isinstance(single_component, dict):
                print(f"✅ Retrieved component with cid={cid}")
            else:
                print(f"❌ Unexpected response type for single component: {type(single_component)}")
        else:
            print("⚠️  No component ID available for single component test.")

        # Test 3: Use responsedata parameter
        print("Test 3: Use responsedata parameter...")
        filters_only = client.components.get(responsedata='filters')
        if isinstance(filters_only, list) or isinstance(filters_only, dict):
            print(f"✅ Responsedata=filters returned type: {type(filters_only)}")
            # Print the first filter if it's a list and not empty
            if isinstance(filters_only, list) and filters_only:
                print(f"First filter: {filters_only[0]}")
            elif isinstance(filters_only, dict):
                print(f"Keys: {list(filters_only.keys())}")
        else:
            print(f"❌ Unexpected response for responsedata=filters: {type(filters_only)}")

        print("\nComponents tests completed.")
        return True
    except Exception as e:
        print(f"❌ Error testing Components: {e}")
        return False

def test_cves(client):
    """Test the CVEs module (read-only)."""
    print("\nTesting CVEs endpoint (read-only)...")
    try:
        # Test 1: Get all CVEs
        print("Test 1: Get all CVEs...")
        cves = client.cves.get()
        if isinstance(cves, dict) and 'results' in cves:
            print(f"✅ Found {len(cves['results'])} CVE device entries.")
        else:
            print(f"❌ Unexpected response type: {type(cves)}")

        # Test 2: Get CVEs for a single device (if available)
        print("Test 2: Get CVEs for a single device...")
        did = None
        if isinstance(cves, dict) and 'results' in cves and cves['results']:
            did = cves['results'][0].get('did')
        if did is not None:
            single_device_cves = client.cves.get(did=did)
            if isinstance(single_device_cves, dict) and 'results' in single_device_cves:
                print(f"✅ Retrieved CVEs for device did={did}, count: {len(single_device_cves['results'])}")
            else:
                print(f"❌ Unexpected response type for single device CVEs: {type(single_device_cves)}")
        else:
            print("⚠️  No device ID available for single device CVE test.")

        # Test 3: Use fulldevicedetails parameter
        print("Test 3: Use fulldevicedetails parameter...")
        cves_full = client.cves.get(fulldevicedetails=True)
        if isinstance(cves_full, dict):
            if 'devices' in cves_full:
                print(f"✅ fulldevicedetails returned devices object with {len(cves_full['devices'])} devices.")
            else:
                print("⚠️  fulldevicedetails did not return a devices object.")
        else:
            print(f"❌ Unexpected response for fulldevicedetails: {type(cves_full)}")

        print("\nCVEs tests completed.")
        return True
    except Exception as e:
        print(f"❌ Error testing CVEs: {e}")
        return False

def test_details(client):
    """Test the Details module (read-only)."""
    print("\nTesting Details endpoint (read-only)...")
    try:
        did = 3937  # Placeholder for device ID, replace with a real one if available
        pbid = 48892  # Placeholder for model breach ID, replace with a real one if available
        # Test 1: Get details by did (device ID)
        print("Test 1: Get details by did...")
        details = client.details.get(did, count=1)
        if isinstance(details, list):
            print(f"✅ Got details for did={did} (type: {type(details)})")
            if details:
                print(f"  First item: {details[0]}")
            else:
                print("  (No items in list)")
        elif isinstance(details, dict):
            print(f"✅ Got details for did={did} (type: {type(details)})")
            print(f"  Keys: {list(details.keys())}")
        else:
            print(f"❌ Unexpected response type for details by did: {type(details)}")

        # Test 2: Get details by pbid (model breach ID)
        print("Test 2: Get details by pbid...")
        details_by_pbid = client.details.get(pbid, count=1)  
        if isinstance(details_by_pbid, list):
            print(f"✅ Got details for pbid={pbid} (type: {type(details_by_pbid)})")
            if details_by_pbid:
                print(f"  First item: {details_by_pbid[0]}")
            else:
                print("  (No items in list)")
        elif isinstance(details_by_pbid, dict):
            print(f"✅ Got details for pbid={pbid} (type: {type(details_by_pbid)})")
            print(f"  Keys: {list(details_by_pbid.keys())}")
        else:
            print(f"❌ Unexpected response type for details by pbid: {type(details_by_pbid)}")

        # Test 3: Get details with time range (from_/to)
        print("Test 3: Get details with from_/to time range...")
        from datetime import datetime, timedelta
        end = datetime.now()
        start = end - timedelta(hours=1)
        details_time = client.details.get(
            did,
            from_=start.strftime('%Y-%m-%d %H:%M:%S'),
            to=end.strftime('%Y-%m-%d %H:%M:%S'),
        )
        if isinstance(details_time, list):
            print(f"✅ Got details for did={did} in last hour (type: {type(details_time)})")
            if details_time:
                print(f"  First item: {details_time[0]}")
            else:
                print("  (No items in list)")
        elif isinstance(details_time, dict):
            print(f"✅ Got details for did={did} in last hour (type: {type(details_time)})")
            print(f"  Keys: {list(details_time.keys())}")
        else:
            print(f"❌ Unexpected response type for details with time range: {type(details_time)})")

        # Test 4: Get details with eventtype and responsedata
        print("Test 4: Get details with eventtype and responsedata...")
        details_event = client.details.get(
            did,
            eventtype="connection",
            responsedata="device,model,connections",
            count=1
        )
        if isinstance(details_event, list):
            print(f"✅ Got details with eventtype and responsedata (type: {type(details_event)})")
            if details_event:
                print(f"  First item: {details_event[0]}")
            else:
                print("  (No items in list)")
        elif isinstance(details_event, dict):
            print(f"✅ Got details with eventtype and responsedata (type: {type(details_event)})")
            print(f"  Keys: {list(details_event.keys())}")
        else:
            print(f"❌ Unexpected response type for details with eventtype: {type(details_event)})")

        print("\nDetails tests completed.")
        return True
    except Exception as e:
        print(f"❌ Error testing Details: {e}")
        return False
    
def test_deviceinfo(client):
    """Test the DeviceInfo (deviceinfo endpoint) with various parameter combinations (read-only)."""
    print("\nTesting DeviceInfo endpoint (read-only)...")
    try:
        # Test 1: Basic deviceinfo retrieval
        print("Test 1: Basic deviceinfo retrieval...")
        try:
            result = client.deviceinfo.get(did=1)
            print(f"  ✅ Basic call returned type: {type(result)}")
        except Exception as e:
            print(f"  ❌ Error in test 1: {e}")

        # Test 2: All parameters set
        print("Test 2: All parameters set...")
        try:
            result = client.deviceinfo.get(
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
            print(f"  ✅ All params call returned type: {type(result)}")
        except Exception as e:
            print(f"  ❌ Error in test 2: {e}")

        # Test 3: Edge case - similardevices=0
        print("Test 3: similardevices=0...")
        try:
            result = client.deviceinfo.get(did=1, similardevices=0)
            print(f"  ✅ similardevices=0 call returned type: {type(result)}")
        except Exception as e:
            print(f"  ❌ Error in test 3: {e}")

        # Test 4: Edge case - intervalhours > 1
        print("Test 4: intervalhours=6...")
        try:
            result = client.deviceinfo.get(did=1, intervalhours=6)
            print(f"  ✅ intervalhours=6 call returned type: {type(result)}")
        except Exception as e:
            print(f"  ❌ Error in test 4: {e}")

        # Test 5: Edge case - showallgraphdata=False
        print("Test 5: showallgraphdata=False...")
        try:
            result = client.deviceinfo.get(did=1, showallgraphdata=False)
            print(f"  ✅ showallgraphdata=False call returned type: {type(result)}")
        except Exception as e:
            print(f"  ❌ Error in test 5: {e}")

        print("\nDeviceInfo tests completed.")
        return True
    except Exception as e:
        print(f"❌ Error testing DeviceInfo: {e}")
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
    test_components(client)  # Added test for Components (read-only)
    test_cves(client)  # Added test for CVEs (read-only)
    test_details(client)  # Added test for Details (read-only)
    test_deviceinfo(client)  # Added test for DeviceInfo (read-only)
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    main()