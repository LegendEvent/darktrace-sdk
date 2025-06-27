# Network Module

The Network module provides access to network connectivity and traffic statistics from Darktrace. This module allows you to analyze network flows, connections, protocols, and traffic patterns across your infrastructure.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the network module
network = client.network
```

## Methods Overview

The Network module provides the following method:

- **`get()`** - Retrieve network connectivity and traffic statistics with extensive filtering options

## Methods

### Get Network Data

Retrieve network connectivity and traffic statistics information from Darktrace. This method provides comprehensive network analysis capabilities with filtering by devices, protocols, ports, time ranges, and traffic direction.

```python
# Get all network data
all_network_data = network.get()

# Get network data for specific device
device_network = network.get(did=123)

# Get network data for specific IP
ip_network = network.get(ip="192.168.1.100")

# Get network data for time range
time_filtered = network.get(
    from_="2024-01-15 09:00:00",
    to="2024-01-15 17:00:00"
)

# Get external traffic only
external_traffic = network.get(intext="external")

# Get specific protocol traffic
web_traffic = network.get(
    protocol="tcp",
    destinationport=80
)

# Get network data with full device details
detailed_network = network.get(
    did=123,
    fulldevicedetails=True
)

# Get specific metrics only
bandwidth_data = network.get(
    metric="bandwidth",
    responsedata="traffic,bytes"
)
```

#### Parameters

- `applicationprotocol` (str, optional): Filter by application protocol (use /enums endpoint for available values)
- `destinationport` (int, optional): Filter by destination port number
- `did` (int, optional): Device ID to focus analysis on
- `endtime` (int, optional): End time in milliseconds since epoch (UTC)
- `from_` (str, optional): Start time in 'YYYY-MM-DD HH:MM:SS' format
- `fulldevicedetails` (bool, optional): Return full device detail objects for all referenced devices
- `intext` (str, optional): Filter by traffic direction ('internal' or 'external')
- `ip` (str, optional): Return data for specific IP address
- `metric` (str, optional): Name of specific metric (use /metrics endpoint for available metrics)
- `port` (int, optional): Filter by source or destination port
- `protocol` (str, optional): Filter by IP protocol (use /enums endpoint for available values)
- `sourceport` (int, optional): Filter by source port number
- `starttime` (int, optional): Start time in milliseconds since epoch (UTC)
- `to` (str, optional): End time in 'YYYY-MM-DD HH:MM:SS' format
- `viewsubnet` (int, optional): Subnet ID to focus analysis on
- `responsedata` (str, optional): Restrict returned JSON to specific fields or objects (comma-separated)

#### Response Structure

```python
# Basic network data response
{
  "traffic": [
    {
      "sourcedevice": {
        "did": 123,
        "ip": "192.168.1.100",
        "hostname": "workstation-01",
        "devicelabel": "Employee Workstation"
      },
      "destinationdevice": {
        "did": 456,
        "ip": "10.0.1.50",
        "hostname": "server-01",
        "devicelabel": "Database Server"
      },
      "protocol": "tcp",
      "sourceport": 54321,
      "destinationport": 3306,
      "applicationprotocol": "mysql",
      "bytes": 1048576,
      "packets": 768,
      "duration": 300,
      "starttime": 1705320000000,
      "endtime": 1705320300000,
      "direction": "internal",
      "flags": ["established", "ack"]
    }
    // ... more traffic entries
  ],
  "summary": {
    "totalconnections": 1543,
    "totalbytes": 536870912,
    "totalpackets": 245760,
    "timerange": {
      "start": 1705320000000,
      "end": 1705323600000
    },
    "topprotocols": [
      {"protocol": "tcp", "percentage": 78.5},
      {"protocol": "udp", "percentage": 19.3},
      {"protocol": "icmp", "percentage": 2.2}
    ],
    "topports": [
      {"port": 443, "percentage": 45.2},
      {"port": 80, "percentage": 23.1},
      {"port": 53, "percentage": 12.7}
    ]
  }
}

# With fulldevicedetails=True
{
  "traffic": [
    {
      "sourcedevice": {
        "did": 123,
        "ip": "192.168.1.100",
        "hostname": "workstation-01",
        "devicelabel": "Employee Workstation",
        "macaddress": "00:1B:44:11:3A:B7",
        "vendor": "Dell Inc.",
        "os": "Windows 10",
        "devicetype": "desktop",
        "firstseen": 1705233600000,
        "lastseen": 1705320300000,
        "tags": ["corporate", "finance-dept"]
      },
      "destinationdevice": {
        // ... full device details
      },
      // ... connection details
    }
  ]
}

# With specific metric filtering
{
  "metric": "bandwidth",
  "data": [
    {
      "timestamp": 1705320000000,
      "device": {"did": 123, "ip": "192.168.1.100"},
      "bytes_in": 10485760,
      "bytes_out": 5242880,
      "packets_in": 7680,
      "packets_out": 3840,
      "connections": 15
    }
    // ... more metric data points
  ]
}

# With responsedata filtering
{
  "traffic": [
    {
      "bytes": 1048576,
      "packets": 768
    }
    // ... more entries with only specified fields
  ]
}
```

## Examples

### Network Traffic Analysis

```python
from darktrace import DarktraceClient
import datetime

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Analyze network traffic for the last hour
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(hours=1)

network_data = client.network.get(
    from_=start_time.strftime("%Y-%m-%d %H:%M:%S"),
    to=end_time.strftime("%Y-%m-%d %H:%M:%S"),
    fulldevicedetails=True
)

print("Network Traffic Analysis")
print("=" * 50)

# Analyze traffic patterns
total_connections = 0
total_bytes = 0
protocol_stats = {}
port_stats = {}
external_connections = 0

for connection in network_data.get('traffic', []):
    total_connections += 1
    total_bytes += connection.get('bytes', 0)
    
    # Protocol analysis
    protocol = connection.get('protocol', 'unknown')
    protocol_stats[protocol] = protocol_stats.get(protocol, 0) + 1
    
    # Port analysis
    dest_port = connection.get('destinationport')
    if dest_port:
        port_stats[dest_port] = port_stats.get(dest_port, 0) + 1
    
    # External traffic analysis
    direction = connection.get('direction', '')
    if direction == 'external':
        external_connections += 1

print(f"Total connections: {total_connections}")
print(f"Total bytes transferred: {total_bytes:,}")
print(f"External connections: {external_connections} ({external_connections/total_connections*100:.1f}%)")

print(f"\nTop protocols:")
for protocol, count in sorted(protocol_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
    percentage = count / total_connections * 100
    print(f"  {protocol}: {count} ({percentage:.1f}%)")

print(f"\nTop destination ports:")
for port, count in sorted(port_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
    percentage = count / total_connections * 100
    print(f"  {port}: {count} ({percentage:.1f}%)")
```

### Device Network Activity Analysis

```python
# Analyze network activity for specific device
device_id = 123

device_network = client.network.get(
    did=device_id,
    from_="2024-01-15 00:00:00",
    to="2024-01-15 23:59:59",
    fulldevicedetails=True
)

print(f"Device Network Activity Analysis (DID: {device_id})")
print("=" * 60)

# Get device information
device_info = None
traffic_data = device_network.get('traffic', [])

if traffic_data:
    # Extract device info from first connection
    first_connection = traffic_data[0]
    source_device = first_connection.get('sourcedevice', {})
    if source_device.get('did') == device_id:
        device_info = source_device
    else:
        device_info = first_connection.get('destinationdevice', {})
    
    if device_info:
        print(f"Device: {device_info.get('hostname', 'Unknown')} ({device_info.get('ip', 'Unknown IP')})")
        print(f"Label: {device_info.get('devicelabel', 'No label')}")
        print(f"OS: {device_info.get('os', 'Unknown')}")
        print(f"Type: {device_info.get('devicetype', 'Unknown')}")

# Analyze connections
outbound_connections = []
inbound_connections = []
external_destinations = set()
internal_destinations = set()

for connection in traffic_data:
    source_did = connection.get('sourcedevice', {}).get('did')
    dest_did = connection.get('destinationdevice', {}).get('did')
    direction = connection.get('direction', 'unknown')
    
    if source_did == device_id:
        outbound_connections.append(connection)
        dest_ip = connection.get('destinationdevice', {}).get('ip')
        if direction == 'external':
            external_destinations.add(dest_ip)
        else:
            internal_destinations.add(dest_ip)
    elif dest_did == device_id:
        inbound_connections.append(connection)

print(f"\nConnection Summary:")
print(f"  Outbound connections: {len(outbound_connections)}")
print(f"  Inbound connections: {len(inbound_connections)}")
print(f"  External destinations: {len(external_destinations)}")
print(f"  Internal destinations: {len(internal_destinations)}")

# Analyze outbound traffic by protocol and port
if outbound_connections:
    print(f"\nOutbound Traffic Analysis:")
    
    protocol_bytes = {}
    port_connections = {}
    
    for conn in outbound_connections:
        protocol = conn.get('protocol', 'unknown')
        bytes_sent = conn.get('bytes', 0)
        dest_port = conn.get('destinationport')
        
        protocol_bytes[protocol] = protocol_bytes.get(protocol, 0) + bytes_sent
        if dest_port:
            port_connections[dest_port] = port_connections.get(dest_port, 0) + 1
    
    print(f"  Data by protocol:")
    for protocol, bytes_val in sorted(protocol_bytes.items(), key=lambda x: x[1], reverse=True):
        print(f"    {protocol}: {bytes_val:,} bytes")
    
    print(f"  Top destination ports:")
    for port, count in sorted(port_connections.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {port}: {count} connections")

# List external destinations
if external_destinations:
    print(f"\nExternal Destinations:")
    for dest_ip in sorted(external_destinations):
        print(f"  {dest_ip}")
```

### Protocol and Port Analysis

```python
# Comprehensive protocol and port analysis
def analyze_network_protocols_ports():
    # Get recent network data
    network_data = client.network.get(
        from_="2024-01-15 08:00:00",
        to="2024-01-15 18:00:00"
    )
    
    protocol_analysis = {}
    port_analysis = {}
    app_protocol_analysis = {}
    
    for connection in network_data.get('traffic', []):
        protocol = connection.get('protocol', 'unknown')
        app_protocol = connection.get('applicationprotocol', 'unknown')
        source_port = connection.get('sourceport')
        dest_port = connection.get('destinationport')
        bytes_transferred = connection.get('bytes', 0)
        packets = connection.get('packets', 0)
        
        # Protocol analysis
        if protocol not in protocol_analysis:
            protocol_analysis[protocol] = {
                'connections': 0,
                'bytes': 0,
                'packets': 0
            }
        
        protocol_analysis[protocol]['connections'] += 1
        protocol_analysis[protocol]['bytes'] += bytes_transferred
        protocol_analysis[protocol]['packets'] += packets
        
        # Application protocol analysis
        if app_protocol != 'unknown':
            if app_protocol not in app_protocol_analysis:
                app_protocol_analysis[app_protocol] = {
                    'connections': 0,
                    'bytes': 0
                }
            
            app_protocol_analysis[app_protocol]['connections'] += 1
            app_protocol_analysis[app_protocol]['bytes'] += bytes_transferred
        
        # Port analysis
        for port_type, port_num in [('source', source_port), ('destination', dest_port)]:
            if port_num:
                port_key = f"{port_type}_{port_num}"
                if port_key not in port_analysis:
                    port_analysis[port_key] = {
                        'connections': 0,
                        'bytes': 0
                    }
                
                port_analysis[port_key]['connections'] += 1
                port_analysis[port_key]['bytes'] += bytes_transferred
    
    return protocol_analysis, app_protocol_analysis, port_analysis

# Run analysis
protocol_stats, app_protocol_stats, port_stats = analyze_network_protocols_ports()

print("Network Protocol and Port Analysis")
print("=" * 50)

print("Protocol Statistics:")
for protocol, stats in sorted(protocol_stats.items(), key=lambda x: x[1]['bytes'], reverse=True):
    print(f"  {protocol}:")
    print(f"    Connections: {stats['connections']:,}")
    print(f"    Bytes: {stats['bytes']:,}")
    print(f"    Packets: {stats['packets']:,}")

print(f"\nApplication Protocol Statistics:")
for app_protocol, stats in sorted(app_protocol_stats.items(), key=lambda x: x[1]['bytes'], reverse=True)[:10]:
    print(f"  {app_protocol}: {stats['connections']} connections, {stats['bytes']:,} bytes")

print(f"\nTop Ports by Traffic:")
top_ports = sorted(port_stats.items(), key=lambda x: x[1]['bytes'], reverse=True)[:15]
for port_info, stats in top_ports:
    port_type, port_num = port_info.split('_', 1)
    print(f"  {port_type} port {port_num}: {stats['connections']} connections, {stats['bytes']:,} bytes")
```

### External Traffic Analysis

```python
# Focus on external traffic patterns
external_traffic = client.network.get(
    intext="external",
    from_="2024-01-15 00:00:00",
    to="2024-01-15 23:59:59"
)

print("External Traffic Analysis")
print("=" * 50)

external_destinations = {}
external_sources = {}
suspicious_ports = [22, 23, 3389, 445, 135, 139, 1433, 3306]  # Common administrative/database ports

for connection in external_traffic.get('traffic', []):
    dest_device = connection.get('destinationdevice', {})
    source_device = connection.get('sourcedevice', {})
    dest_port = connection.get('destinationport')
    app_protocol = connection.get('applicationprotocol', 'unknown')
    bytes_transferred = connection.get('bytes', 0)
    
    # Track external destinations
    dest_ip = dest_device.get('ip')
    if dest_ip:
        if dest_ip not in external_destinations:
            external_destinations[dest_ip] = {
                'connections': 0,
                'bytes': 0,
                'ports': set(),
                'protocols': set()
            }
        
        external_destinations[dest_ip]['connections'] += 1
        external_destinations[dest_ip]['bytes'] += bytes_transferred
        if dest_port:
            external_destinations[dest_ip]['ports'].add(dest_port)
        if app_protocol != 'unknown':
            external_destinations[dest_ip]['protocols'].add(app_protocol)
    
    # Track internal sources making external connections
    source_ip = source_device.get('ip')
    if source_ip:
        if source_ip not in external_sources:
            external_sources[source_ip] = {
                'connections': 0,
                'bytes': 0,
                'destinations': set(),
                'suspicious_ports': set()
            }
        
        external_sources[source_ip]['connections'] += 1
        external_sources[source_ip]['bytes'] += bytes_transferred
        if dest_ip:
            external_sources[source_ip]['destinations'].add(dest_ip)
        if dest_port in suspicious_ports:
            external_sources[source_ip]['suspicious_ports'].add(dest_port)

print(f"Top External Destinations:")
top_destinations = sorted(external_destinations.items(), key=lambda x: x[1]['bytes'], reverse=True)[:10]
for dest_ip, stats in top_destinations:
    print(f"  {dest_ip}:")
    print(f"    Connections: {stats['connections']}")
    print(f"    Bytes: {stats['bytes']:,}")
    print(f"    Ports: {', '.join(map(str, sorted(stats['ports'])))}")
    print(f"    Protocols: {', '.join(stats['protocols'])}")

print(f"\nTop Internal Sources (External Activity):")
top_sources = sorted(external_sources.items(), key=lambda x: x[1]['connections'], reverse=True)[:10]
for source_ip, stats in top_sources:
    print(f"  {source_ip}:")
    print(f"    External connections: {stats['connections']}")
    print(f"    Bytes sent: {stats['bytes']:,}")
    print(f"    Unique destinations: {len(stats['destinations'])}")
    if stats['suspicious_ports']:
        print(f"    Suspicious ports: {', '.join(map(str, sorted(stats['suspicious_ports'])))}")
```

### Network Metrics and Bandwidth Analysis

```python
# Analyze specific network metrics
bandwidth_data = client.network.get(
    metric="bandwidth",
    from_="2024-01-15 08:00:00",
    to="2024-01-15 18:00:00"
)

print("Network Bandwidth Analysis")
print("=" * 50)

# Process bandwidth metrics
device_bandwidth = {}
hourly_bandwidth = {}

for metric_point in bandwidth_data.get('data', []):
    device = metric_point.get('device', {})
    device_ip = device.get('ip', 'unknown')
    timestamp = metric_point.get('timestamp', 0)
    bytes_in = metric_point.get('bytes_in', 0)
    bytes_out = metric_point.get('bytes_out', 0)
    
    # Device bandwidth totals
    if device_ip not in device_bandwidth:
        device_bandwidth[device_ip] = {
            'bytes_in': 0,
            'bytes_out': 0,
            'total': 0
        }
    
    device_bandwidth[device_ip]['bytes_in'] += bytes_in
    device_bandwidth[device_ip]['bytes_out'] += bytes_out
    device_bandwidth[device_ip]['total'] += bytes_in + bytes_out
    
    # Hourly bandwidth
    hour = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%H:00')
    if hour not in hourly_bandwidth:
        hourly_bandwidth[hour] = {'in': 0, 'out': 0}
    
    hourly_bandwidth[hour]['in'] += bytes_in
    hourly_bandwidth[hour]['out'] += bytes_out

print("Top Bandwidth Consumers:")
top_consumers = sorted(device_bandwidth.items(), key=lambda x: x[1]['total'], reverse=True)[:10]
for device_ip, bandwidth in top_consumers:
    total_mb = bandwidth['total'] / (1024 * 1024)
    in_mb = bandwidth['bytes_in'] / (1024 * 1024)
    out_mb = bandwidth['bytes_out'] / (1024 * 1024)
    print(f"  {device_ip}: {total_mb:.2f} MB total ({in_mb:.2f} MB in, {out_mb:.2f} MB out)")

print(f"\nHourly Bandwidth Distribution:")
for hour in sorted(hourly_bandwidth.keys()):
    bandwidth = hourly_bandwidth[hour]
    total_mb = (bandwidth['in'] + bandwidth['out']) / (1024 * 1024)
    print(f"  {hour}: {total_mb:.2f} MB total")
```

### Subnet Network Analysis

```python
# Analyze network traffic by subnet
subnet_id = 1  # Replace with actual subnet ID

subnet_network = client.network.get(
    viewsubnet=subnet_id,
    from_="2024-01-15 00:00:00",
    to="2024-01-15 23:59:59"
)

print(f"Subnet Network Analysis (Subnet ID: {subnet_id})")
print("=" * 60)

# Analyze intra-subnet vs inter-subnet traffic
intra_subnet_traffic = []
inter_subnet_traffic = []
subnet_devices = set()

for connection in subnet_network.get('traffic', []):
    source_device = connection.get('sourcedevice', {})
    dest_device = connection.get('destinationdevice', {})
    
    source_ip = source_device.get('ip')
    dest_ip = dest_device.get('ip')
    
    if source_ip:
        subnet_devices.add(source_ip)
    if dest_ip:
        subnet_devices.add(dest_ip)
    
    # Determine if traffic is intra-subnet or inter-subnet
    # This is simplified - in practice you'd check IP ranges
    if source_ip and dest_ip:
        if source_ip.startswith('192.168.') and dest_ip.startswith('192.168.'):
            intra_subnet_traffic.append(connection)
        else:
            inter_subnet_traffic.append(connection)

print(f"Subnet Devices: {len(subnet_devices)}")
print(f"Intra-subnet connections: {len(intra_subnet_traffic)}")
print(f"Inter-subnet connections: {len(inter_subnet_traffic)}")

# Analyze protocols within subnet
subnet_protocols = {}
for connection in intra_subnet_traffic:
    protocol = connection.get('applicationprotocol', 'unknown')
    if protocol not in subnet_protocols:
        subnet_protocols[protocol] = 0
    subnet_protocols[protocol] += 1

print(f"\nIntra-subnet protocols:")
for protocol, count in sorted(subnet_protocols.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {protocol}: {count} connections")

# List active devices in subnet
print(f"\nActive devices in subnet:")
for device_ip in sorted(subnet_devices)[:20]:  # Show first 20
    print(f"  {device_ip}")
if len(subnet_devices) > 20:
    print(f"  ... and {len(subnet_devices) - 20} more")
```

## Error Handling

```python
try:
    # Attempt to get network data
    network_data = client.network.get(
        from_="2024-01-15 09:00:00",
        to="2024-01-15 17:00:00",
        intext="external"
    )
    
    # Process network information
    traffic_entries = network_data.get('traffic', [])
    print(f"Retrieved {len(traffic_entries)} network connections")
    
    for connection in traffic_entries[:10]:  # Process first 10
        source_ip = connection.get('sourcedevice', {}).get('ip', 'Unknown')
        dest_ip = connection.get('destinationdevice', {}).get('ip', 'Unknown')
        protocol = connection.get('protocol', 'Unknown')
        bytes_transferred = connection.get('bytes', 0)
        
        print(f"  {source_ip} -> {dest_ip} ({protocol}): {bytes_transferred} bytes")
        
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check parameter values and formats")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for network endpoint")
        elif e.response.status_code == 422:
            print("Invalid parameters - check time ranges and filter values")
        else:
            print(f"Response: {e.response.text}")
            
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Time Parameters
- **Timestamp formats**: Use either epoch milliseconds or 'YYYY-MM-DD HH:MM:SS' format
- **Time pairs**: Use either (`starttime`, `endtime`) or (`from_`, `to`) - don't mix formats
- **UTC timezone**: All times are interpreted as UTC
- **Time range limits**: Large time ranges may result in timeouts or data limits

### Protocol Filtering
- **IP protocols**: tcp, udp, icmp, etc. (use /enums endpoint for complete list)
- **Application protocols**: http, https, smtp, ftp, ssh, etc.
- **Protocol hierarchy**: IP protocol is transport layer, application protocol is higher level

### Traffic Direction
- **Internal**: Traffic between devices within monitored network segments
- **External**: Traffic between internal devices and external destinations
- **Direction context**: Based on Darktrace's network visibility and configuration

### Device Details
- **Basic mode**: Returns device ID, IP, and hostname only
- **Full details mode**: Returns complete device information including MAC, vendor, OS, tags
- **Performance impact**: Full device details increase response size and processing time

### Port Analysis
- **Source ports**: Usually ephemeral/dynamic ports assigned by client
- **Destination ports**: Usually well-known service ports (80, 443, 22, etc.)
- **Port filtering**: Can filter by either source, destination, or both ports

### Response Data Optimization
Use `responsedata` parameter to optimize queries:
- `"traffic"`: Network flow data only
- `"summary"`: Aggregated statistics only
- `"sourcedevice,destinationdevice"`: Device information only
- `"bytes,packets"`: Traffic volume data only

### Common Use Cases
- **Traffic analysis**: Understanding communication patterns and volumes
- **Security monitoring**: Detecting unusual or suspicious network activity
- **Performance monitoring**: Identifying bandwidth usage and network bottlenecks
- **Compliance reporting**: Documenting network communications for audit purposes
- **Capacity planning**: Understanding network usage trends and growth patterns

### Best Practices
- **Use time ranges**: Always specify time ranges to avoid overwhelming responses
- **Filter appropriately**: Use device, protocol, or port filters to focus analysis
- **Consider data volume**: Network data can be very large - use responsedata filtering
- **Optimize queries**: Start with broad queries, then narrow down based on findings
- **Cache results**: Network patterns don't change frequently - consider caching

### Integration Considerations
- **Data correlation**: Network data correlates with devices, breaches, and other modules
- **Real-time vs historical**: Network endpoint provides historical data, not real-time
- **Sampling considerations**: High-volume networks may use sampling or aggregation
- **Subnet visibility**: Results depend on Darktrace's network monitoring coverage
