# Details Module

The Details module provides access to detailed connection and event information for devices and entities in the Darktrace platform. This module allows you to retrieve granular data about network connections, events, model breaches, and device history with extensive filtering capabilities.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the details module
details = client.details
```

## Methods Overview

The Details module provides the following method:

- **`get()`** - Retrieve detailed connection and event information with comprehensive filtering

## Methods

### Get Details

Retrieve detailed connection and event information for devices or entities. This method provides access to granular network data including connections, events, model breaches, and device history.

```python
# Get connection details for a specific device
device_connections = details.get(
    did=123,
    eventtype="connection",
    count=100
)

# Get unusual connections for a device
unusual_connections = details.get(
    did=123,
    eventtype="unusualconnection",
    starttime=1640995200000,
    endtime=1641081600000
)

# Get details for a specific model breach
breach_details = details.get(
    pbid=12345,
    eventtype="modelbreach"
)

# Get blocked connections from RESPOND actions
blocked_details = details.get(
    did=123,
    blockedconnections="all",
    eventtype="connection"
)

# Get notice events with specific message
notice_details = details.get(
    msg="Authentication failure",
    eventtype="notice",
    count=50
)

# Get device history
device_history = details.get(
    did=123,
    eventtype="devicehistory",
    from_="2024-01-01 10:00:00",
    to="2024-01-01 18:00:00"
)

# Get connections with protocol filtering
protocol_connections = details.get(
    did=123,
    protocol="TCP",
    applicationprotocol="HTTP",
    destinationport=80,
    count=200
)

# Get detailed connections with full device information
detailed_connections = details.get(
    did=123,
    fulldevicedetails=True,
    deduplicate=True,
    responsedata="connections"
)
```

#### Parameters

**Required Parameters (at least one must be specified):**
- `did` (int, optional): Device ID to filter data for
- `pbid` (int, optional): Model breach ID to filter data for  
- `msg` (str, optional): Message field value for notice events
- `blockedconnections` (str, optional): Filter for RESPOND/Network attempted actions ('all', 'failed', 'true')

**Event Type:**
- `eventtype` (str, optional): Event type to return (default: 'connection')
  - `'connection'`: Standard network connections
  - `'unusualconnection'`: Unusual network connections flagged by AI
  - `'newconnection'`: New connections not seen before
  - `'notice'`: System notices and alerts
  - `'devicehistory'`: Device activity history
  - `'modelbreach'`: Model breach events

**Time Filtering:**
- `count` (int, optional): Maximum number of items to return (cannot be used with time parameters)
- `starttime` (int, optional): Start time in milliseconds since epoch (must be paired with endtime)
- `endtime` (int, optional): End time in milliseconds since epoch (must be paired with starttime)
- `from_` (str, optional): Start time in 'YYYY-MM-DD HH:MM:SS' format (must be paired with to)
- `to` (str, optional): End time in 'YYYY-MM-DD HH:MM:SS' format (must be paired with from_)

**Connection Filtering:**
- `applicationprotocol` (str, optional): Filter by application protocol (see /enums endpoint for values)
- `destinationport` (int, optional): Filter by destination port
- `sourceport` (int, optional): Filter by source port
- `port` (int, optional): Filter by source OR destination port
- `protocol` (str, optional): Filter by IP protocol (see /enums endpoint for values)
- `ddid` (int, optional): Destination device ID
- `odid` (int, optional): Other device ID in connection
- `externalhostname` (str, optional): Filter by external hostname
- `intext` (str, optional): Filter for internal/external connections ('internal' or 'external')
- `uid` (str, optional): Specific connection UID to return

**Response Options:**
- `deduplicate` (bool, optional): Return only one equivalent connection per hour (default: False)
- `fulldevicedetails` (bool, optional): Return full device detail objects (default: False)
- `responsedata` (str, optional): Restrict returned JSON to specific field/object

#### Parameter Validation Rules

- **At least one required parameter** must be specified: `did`, `pbid`, `msg`, or `blockedconnections`
- **Time parameters must be in pairs**: `starttime`/`endtime` or `from_`/`to`
- **Count vs. time filtering**: `count` cannot be used with time parameters
- **Boolean parameters**: `deduplicate` and `fulldevicedetails` accept boolean values

#### Response Structure

```python
# Standard response
{
  "connections": [
    {
      "uid": "connection-uuid",
      "timestamp": 1641038400000,
      "sourceDevice": {
        "did": 123,
        "hostname": "client01",
        "ip": "192.168.1.100"
      },
      "destinationDevice": {
        "did": 456,
        "hostname": "server01", 
        "ip": "192.168.1.200"
      },
      "sourcePort": 49152,
      "destinationPort": 443,
      "protocol": "TCP",
      "applicationProtocol": "HTTPS",
      "bytesSent": 1024,
      "bytesReceived": 4096,
      "external": false
    }
  ]
}

# With fulldevicedetails=True
{
  "connections": [...],  # Connection objects with device IDs only
  "devices": {
    "123": {
      "did": 123,
      "hostname": "client01",
      // ... complete device information
    }
  }
}

# Notice events (eventtype="notice")
{
  "notices": [
    {
      "timestamp": 1641038400000,
      "message": "Authentication failure",
      "device": {...},
      "severity": "medium",
      "category": "authentication"
    }
  ]
}
```

## Examples

### Connection Analysis for Device

```python
from darktrace import DarktraceClient
import time

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Analyze connections for a specific device
device_id = 123

# Get recent connections
recent_connections = client.details.get(
    did=device_id,
    eventtype="connection",
    count=1000,
    deduplicate=True
)

print(f"Recent connections for device {device_id}:")
print(f"Total connections: {len(recent_connections.get('connections', []))}")

# Analyze connection patterns
external_connections = []
internal_connections = []
high_volume_connections = []

for conn in recent_connections.get('connections', []):
    bytes_total = conn.get('bytesSent', 0) + conn.get('bytesReceived', 0)
    
    if conn.get('external', False):
        external_connections.append(conn)
    else:
        internal_connections.append(conn)
    
    if bytes_total > 1000000:  # > 1MB
        high_volume_connections.append(conn)

print(f"External connections: {len(external_connections)}")
print(f"Internal connections: {len(internal_connections)}")
print(f"High volume connections: {len(high_volume_connections)}")

# Show top external destinations
external_hosts = {}
for conn in external_connections:
    dest = conn.get('destinationDevice', {}).get('hostname', conn.get('destinationDevice', {}).get('ip', 'Unknown'))
    external_hosts[dest] = external_hosts.get(dest, 0) + 1

print("\nTop external destinations:")
for host, count in sorted(external_hosts.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {host}: {count} connections")
```

### Model Breach Investigation

```python
# Investigate a specific model breach in detail
breach_id = 12345

breach_details = client.details.get(
    pbid=breach_id,
    eventtype="modelbreach",
    fulldevicedetails=True
)

print(f"Model Breach {breach_id} Investigation:")

for breach in breach_details.get('modelbreaches', []):
    print(f"Breach Time: {time.ctime(breach.get('timestamp', 0) / 1000)}")
    print(f"Model: {breach.get('model', {}).get('name', 'Unknown')}")
    print(f"Score: {breach.get('score', 0)}")
    print(f"Device: {breach.get('device', {}).get('hostname', 'Unknown')}")
    
    # Get related connections for this breach
    device_id = breach.get('device', {}).get('did')
    if device_id:
        breach_time = breach.get('timestamp', 0)
        window_start = breach_time - 300000  # 5 minutes before
        window_end = breach_time + 300000    # 5 minutes after
        
        related_connections = client.details.get(
            did=device_id,
            eventtype="connection",
            starttime=window_start,
            endtime=window_end
        )
        
        print(f"Related connections (±5 min): {len(related_connections.get('connections', []))}")
```

### Unusual Connection Analysis

```python
# Analyze unusual connections for security monitoring
unusual_connections = client.details.get(
    did=123,
    eventtype="unusualconnection",
    from_="2024-01-01 00:00:00",
    to="2024-01-01 23:59:59",
    fulldevicedetails=True
)

print("Unusual Connection Analysis:")

protocol_stats = {}
port_stats = {}
external_unusual = 0

for conn in unusual_connections.get('connections', []):
    # Protocol analysis
    protocol = conn.get('protocol', 'Unknown')
    app_protocol = conn.get('applicationProtocol', 'Unknown')
    full_protocol = f"{protocol}/{app_protocol}"
    
    protocol_stats[full_protocol] = protocol_stats.get(full_protocol, 0) + 1
    
    # Port analysis
    dest_port = conn.get('destinationPort')
    if dest_port:
        port_stats[dest_port] = port_stats.get(dest_port, 0) + 1
    
    # External connection count
    if conn.get('external', False):
        external_unusual += 1

print(f"Total unusual connections: {len(unusual_connections.get('connections', []))}")
print(f"External unusual connections: {external_unusual}")

print("\nTop unusual protocols:")
for protocol, count in sorted(protocol_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {protocol}: {count}")

print("\nTop unusual destination ports:")
for port, count in sorted(port_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  Port {port}: {count}")
```

### RESPOND Action Analysis

```python
# Analyze blocked connections from RESPOND actions
blocked_analysis = client.details.get(
    did=123,
    blockedconnections="all",
    eventtype="connection",
    count=500
)

print("RESPOND Action Analysis:")

if 'connections' in blocked_analysis:
    blocked_connections = blocked_analysis['connections']
    
    # Analyze blocked connection patterns
    blocked_destinations = {}
    blocked_protocols = {}
    
    for conn in blocked_connections:
        # Destination analysis
        dest_ip = conn.get('destinationDevice', {}).get('ip', 'Unknown')
        blocked_destinations[dest_ip] = blocked_destinations.get(dest_ip, 0) + 1
        
        # Protocol analysis
        app_protocol = conn.get('applicationProtocol', 'Unknown')
        blocked_protocols[app_protocol] = blocked_protocols.get(app_protocol, 0) + 1
    
    print(f"Total blocked connections: {len(blocked_connections)}")
    
    print("\nTop blocked destinations:")
    for dest, count in sorted(blocked_destinations.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {dest}: {count} blocks")
    
    print("\nTop blocked protocols:")
    for protocol, count in sorted(blocked_protocols.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {protocol}: {count} blocks")
```

### Notice Event Monitoring

```python
# Monitor system notices and alerts
notices = client.details.get(
    msg="Authentication failure",
    eventtype="notice",
    from_="2024-01-01 00:00:00",
    to="2024-01-01 23:59:59"
)

print("Notice Event Analysis:")

notice_sources = {}
notice_timeline = {}

for notice in notices.get('notices', []):
    # Source device analysis
    device = notice.get('device', {})
    device_name = device.get('hostname', device.get('ip', 'Unknown'))
    notice_sources[device_name] = notice_sources.get(device_name, 0) + 1
    
    # Timeline analysis (by hour)
    timestamp = notice.get('timestamp', 0)
    hour = time.strftime('%H:00', time.localtime(timestamp / 1000))
    notice_timeline[hour] = notice_timeline.get(hour, 0) + 1

print(f"Total authentication failure notices: {len(notices.get('notices', []))}")

print("\nTop sources of auth failures:")
for source, count in sorted(notice_sources.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {source}: {count} failures")

print("\nAuth failure timeline:")
for hour, count in sorted(notice_timeline.items()):
    print(f"  {hour}: {count} failures")
```

### Device History Analysis

```python
# Analyze device activity history
device_history = client.details.get(
    did=123,
    eventtype="devicehistory",
    starttime=1640995200000,  # 24 hours ago
    endtime=1641081600000,    # now
    fulldevicedetails=True
)

print("Device History Analysis:")

activity_types = {}
hourly_activity = {}

for event in device_history.get('events', []):
    # Activity type analysis
    event_type = event.get('type', 'Unknown')
    activity_types[event_type] = activity_types.get(event_type, 0) + 1
    
    # Hourly activity pattern
    timestamp = event.get('timestamp', 0)
    hour = time.strftime('%H:00', time.localtime(timestamp / 1000))
    hourly_activity[hour] = hourly_activity.get(hour, 0) + 1

print(f"Total historical events: {len(device_history.get('events', []))}")

print("\nActivity types:")
for activity, count in sorted(activity_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {activity}: {count}")

print("\nHourly activity pattern:")
for hour, count in sorted(hourly_activity.items()):
    print(f"  {hour}: {count} events")
```

### Protocol and Port Analysis

```python
# Comprehensive protocol and port analysis
protocol_analysis = client.details.get(
    did=123,
    eventtype="connection",
    count=2000,
    deduplicate=True
)

print("Protocol and Port Analysis:")

# Protocol combinations
protocol_combinations = {}
# Port usage patterns
common_ports = {}
# Application protocols
app_protocols = {}

for conn in protocol_analysis.get('connections', []):
    # Protocol combination analysis
    ip_protocol = conn.get('protocol', 'Unknown')
    app_protocol = conn.get('applicationProtocol', 'Unknown')
    combo = f"{ip_protocol}/{app_protocol}"
    protocol_combinations[combo] = protocol_combinations.get(combo, 0) + 1
    
    # Destination port analysis
    dest_port = conn.get('destinationPort')
    if dest_port:
        common_ports[dest_port] = common_ports.get(dest_port, 0) + 1
    
    # Application protocol analysis
    if app_protocol != 'Unknown':
        app_protocols[app_protocol] = app_protocols.get(app_protocol, 0) + 1

print("\nTop protocol combinations:")
for combo, count in sorted(protocol_combinations.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {combo}: {count} connections")

print("\nMost used destination ports:")
for port, count in sorted(common_ports.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  Port {port}: {count} connections")

print("\nApplication protocol distribution:")
for app_proto, count in sorted(app_protocols.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {app_proto}: {count} connections")
```

### Performance-Optimized Queries

```python
# Efficient data retrieval for large-scale analysis
import datetime

# Get minimal connection data for trend analysis
minimal_connections = client.details.get(
    did=123,
    eventtype="connection",
    responsedata="connections",
    deduplicate=True,
    count=5000
)

# Process data efficiently
connection_volumes = []
for conn in minimal_connections.get('connections', []):
    volume = conn.get('bytesSent', 0) + conn.get('bytesReceived', 0)
    connection_volumes.append(volume)

# Calculate statistics
if connection_volumes:
    avg_volume = sum(connection_volumes) / len(connection_volumes)
    max_volume = max(connection_volumes)
    total_volume = sum(connection_volumes)
    
    print(f"Connection volume statistics:")
    print(f"  Total connections: {len(connection_volumes)}")
    print(f"  Average volume: {avg_volume:.0f} bytes")
    print(f"  Maximum volume: {max_volume:,} bytes")
    print(f"  Total volume: {total_volume:,} bytes")

# Time-windowed analysis for trending
end_time = int(time.time() * 1000)
start_time = end_time - (24 * 60 * 60 * 1000)  # 24 hours ago

time_windowed = client.details.get(
    did=123,
    eventtype="connection",
    starttime=start_time,
    endtime=end_time,
    responsedata="connections"
)

print(f"\n24-hour connection count: {len(time_windowed.get('connections', []))}")
```

## Error Handling

```python
try:
    # Attempt to get details with validation
    details_data = client.details.get(
        did=123,
        eventtype="connection",
        count=100
    )
    
    # Process the data
    connections = details_data.get('connections', [])
    print(f"Retrieved {len(connections)} connections")
    
    # Example of handling time parameter validation
    try:
        time_filtered = client.details.get(
            did=123,
            starttime=1640995200000,
            endtime=1641081600000,
            eventtype="connection"
        )
    except ValueError as e:
        print(f"Parameter validation error: {e}")
        
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check parameter combinations")
        elif e.response.status_code == 404:
            print("Entity not found - check did/pbid values")
        else:
            print(f"Response: {e.response.text}")
            
except ValueError as e:
    print(f"Parameter validation error: {e}")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Event Types
The Details module supports multiple event types:

- **connection**: Standard network connections between devices
- **unusualconnection**: Connections flagged as unusual by Darktrace AI
- **newconnection**: Connections to destinations not previously seen
- **notice**: System notices, alerts, and log events
- **devicehistory**: Historical device activity and state changes
- **modelbreach**: Model breach events and associated data

### Time Handling
- **Millisecond timestamps**: `starttime`/`endtime` expect Unix timestamps in milliseconds
- **Human-readable format**: `from_`/`to` accept "YYYY-MM-DD HH:MM:SS" format
- **Time pairs required**: Time parameters must always be specified in pairs
- **Mutual exclusivity**: Cannot use `count` with time parameters

### Required Parameters
At least one of these parameters must be specified:
- `did`: Device ID for device-specific data
- `pbid`: Model breach ID for breach-related data
- `msg`: Message content for notice events
- `blockedconnections`: For RESPOND action analysis

### Performance Considerations
- **Use `responsedata`** to limit response size for large queries
- **Enable `deduplicate`** to reduce redundant connection data
- **Limit `count`** appropriately for performance
- **Use specific time windows** rather than large date ranges
- **Consider `fulldevicedetails`** impact on response size

### Filtering Capabilities
- **Protocol filtering**: Support for both IP and application protocols
- **Port filtering**: Source, destination, or either port
- **Device relationships**: Source, destination, or "other" device in connections
- **Internal/external**: Filter by connection direction
- **RESPOND actions**: Analyze blocked connections

### Data Structure Variations
- **Standard response**: Events/connections with embedded device information
- **Full device details**: Separate events and devices objects for normalization
- **Response data filtering**: Restrict to specific JSON fields for performance

### Common Use Cases
- **Security investigation**: Analyze connections around security events
- **Performance monitoring**: Track connection volumes and patterns
- **Compliance reporting**: Generate detailed activity reports
- **Incident response**: Correlate events with network activity
- **Baseline establishment**: Understand normal connection patterns
