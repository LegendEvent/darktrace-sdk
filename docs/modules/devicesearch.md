# Device Search Module

The Device Search module provides highly filterable search functionality for devices seen by Darktrace. This module offers advanced querying capabilities with field-specific filters, sorting, and pagination for efficient device discovery and analysis.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the device search module
devicesearch = client.devicesearch
```

## Methods Overview

The Device Search module provides the following method:

- **`get()`** - Search for devices with advanced filtering and sorting capabilities

## Methods

### Search Devices

Search for devices using the highly filterable `/devicesearch` endpoint. This provides more advanced search capabilities than the standard devices endpoint.

```python
# Basic device search
devices = devicesearch.get()

# Search with count limit
devices = devicesearch.get(count=50)

# Search devices by hostname pattern
devices = devicesearch.get(
    query="hostname:server*",
    count=100
)

# Search by multiple criteria (space-separated = implicit AND)
devices = devicesearch.get(
    query="label:critical type:server",
    orderBy="priority",
    order="desc"
)

# Search by IP address range
devices = devicesearch.get(
    query="ip:192.168.1.*",
    orderBy="lastSeen",
    order="desc"
)

# Search by vendor
devices = devicesearch.get(
    query="vendor:Microsoft",
    count=200,
    orderBy="hostname"
)

# Search devices seen in last hour
recent_devices = devicesearch.get(
    seensince="1hour",
    orderBy="lastSeen",
    order="desc"
)

# Paginated search
page1 = devicesearch.get(count=100, offset=0)
page2 = devicesearch.get(count=100, offset=100)

# Get minimal response data
minimal = devicesearch.get(
    query="tag:critical",
    responsedata="devices",
    count=50
)
```

#### Parameters

- `count` (int, optional): Number of devices to return (default: 100, maximum: 300)
- `orderBy` (str, optional): Field to order results by:
  - `'priority'`: Device priority
  - `'hostname'`: Device hostname
  - `'ip'`: IP address
  - `'macaddress'`: MAC address
  - `'vendor'`: Device vendor
  - `'os'`: Operating system
  - `'firstSeen'`: First seen timestamp
  - `'lastSeen'`: Last seen timestamp
  - `'devicelabel'`: Device label
  - `'typelabel'`: Device type label
- `order` (str, optional): Sort order ('asc' or 'desc', default: 'asc')
- `query` (str, optional): Search query string with field filters (see Query Syntax below)
- `offset` (int, optional): Offset for pagination
- `responsedata` (str, optional): Restrict returned JSON to specific field/object
- `seensince` (str, optional): Relative time offset for activity ('1hour', '30minute', '60' seconds)

#### Query Syntax

The `query` parameter supports field-specific filtering:

- `label:value` - Search by device label
- `tag:value` - Search by device tag
- `type:value` - Search by device type
- `hostname:value` - Search by hostname (supports wildcards with *)
- `ip:value` - Search by IP address (supports wildcards with *)
- `mac:value` - Search by MAC address (supports wildcards with *)
- `vendor:value` - Search by device vendor
- `os:value` - Search by operating system

**Operators:**
- `AND` - Logical AND operator
- `OR` - Logical OR operator
- `*` - Wildcard character for partial matches
- `"value"` - Exact phrase matching

#### Response Structure

```python
{
  "devices": [
    {
      "did": 123,
      "hostname": "server01",
      "ip": "192.168.1.100",
      "mac": "00:11:22:33:44:55",
      "vendor": "Dell Inc.",
      "os": "Windows Server 2019",
      "priority": 3,
      "type": "Server",
      "labels": ["Critical", "Production"],
      "tags": ["web-server", "critical"],
      "firstSeen": 1640995200000,
      "lastSeen": 1641081600000,
      "subnet": {
        "sid": 456,
        "name": "Production Network"
      }
    },
    // ... more devices
  ],
  "totalCount": 1250,
  "offset": 0,
  "count": 100
}
```

## Examples

### Basic Device Discovery

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get all devices with basic search
all_devices = client.devicesearch.get(count=300)  # Maximum count

print(f"Total devices found: {len(all_devices.get('devices', []))}")

# Display basic device information
for device in all_devices.get('devices', [])[:10]:  # Show first 10
    print(f"Device: {device.get('hostname', 'Unknown')} ({device.get('ip', 'Unknown')})")
    print(f"  Vendor: {device.get('vendor', 'Unknown')}")
    print(f"  Type: {device.get('type', 'Unknown')}")
    print(f"  Priority: {device.get('priority', 0)}")
    print(f"  Last Seen: {device.get('lastSeen', 0)}")
```

### Advanced Search Queries

```python
# Search for critical servers
critical_servers = client.devicesearch.get(
    query="label:critical AND type:server",
    orderBy="priority",
    order="desc",
    count=100
)

print(f"Critical servers found: {len(critical_servers.get('devices', []))}")

# Search for Windows devices
windows_devices = client.devicesearch.get(
    query="os:Windows*",
    orderBy="hostname",
    order="asc"
)

# Search for devices by IP subnet
subnet_devices = client.devicesearch.get(
    query="ip:192.168.1.*",
    orderBy="lastSeen",
    order="desc"
)

# Search for devices by vendor
dell_devices = client.devicesearch.get(
    query="vendor:Dell*",
    count=50
)

# Complex query with multiple conditions
complex_search = devicesearch.get(
    query='vendor:Microsoft vendor:Dell tag:production',
    orderBy="priority",
    order="desc"
)

print(f"Complex search results: {len(complex_search.get('devices', []))}")
```

### Device Inventory Management

```python
# Create comprehensive device inventory
def create_device_inventory():
    inventory = {
        'by_vendor': {},
        'by_type': {},
        'by_os': {},
        'by_priority': {},
        'critical_devices': [],
        'recent_activity': []
    }
    
    # Get all devices
    all_devices = client.devicesearch.get(count=300)
    devices = all_devices.get('devices', [])
    
    for device in devices:
        # Vendor analysis
        vendor = device.get('vendor', 'Unknown')
        inventory['by_vendor'][vendor] = inventory['by_vendor'].get(vendor, 0) + 1
        
        # Type analysis
        device_type = device.get('type', 'Unknown')
        inventory['by_type'][device_type] = inventory['by_type'].get(device_type, 0) + 1
        
        # OS analysis
        os = device.get('os', 'Unknown')
        inventory['by_os'][os] = inventory['by_os'].get(os, 0) + 1
        
        # Priority analysis
        priority = device.get('priority', 0)
        inventory['by_priority'][priority] = inventory['by_priority'].get(priority, 0) + 1
        
        # Critical devices (priority >= 3)
        if priority >= 3:
            inventory['critical_devices'].append({
                'did': device.get('did'),
                'hostname': device.get('hostname'),
                'ip': device.get('ip'),
                'priority': priority
            })
    
    # Get recently active devices
    recent = client.devicesearch.get(
        seensince="1hour",
        orderBy="lastSeen",
        order="desc",
        count=100
    )
    
    inventory['recent_activity'] = recent.get('devices', [])
    
    return inventory

# Generate inventory report
inventory = create_device_inventory()

print("Device Inventory Report")
print("=" * 50)

print(f"\nTotal Devices: {sum(inventory['by_vendor'].values())}")

print(f"\nTop 5 Vendors:")
for vendor, count in sorted(inventory['by_vendor'].items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {vendor}: {count}")

print(f"\nDevice Types:")
for device_type, count in sorted(inventory['by_type'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {device_type}: {count}")

print(f"\nCritical Devices: {len(inventory['critical_devices'])}")
for device in inventory['critical_devices'][:10]:  # Top 10
    print(f"  {device['hostname']} ({device['ip']}) - Priority: {device['priority']}")

print(f"\nRecently Active: {len(inventory['recent_activity'])}")
```

### Security-Focused Device Search

```python
# Search for potentially vulnerable devices
def security_device_analysis():
    # Search for legacy Windows systems
    legacy_windows = client.devicesearch.get(
        query="os:Windows AND (os:*2008* OR os:*2012* OR os:*XP*)",
        orderBy="lastSeen",
        order="desc"
    )
    
    # Search for untagged devices (potential shadow IT)
    untagged_devices = client.devicesearch.get(
        query="NOT tag:*",
        count=100,
        orderBy="firstSeen",
        order="desc"
    )
    
    # Search for high-priority devices with recent activity
    high_priority_active = client.devicesearch.get(
        query="priority:5 OR priority:4",
        seensince="24hour",
        orderBy="priority",
        order="desc"
    )
    
    # Search for devices with suspicious patterns in hostname
    suspicious_hostnames = client.devicesearch.get(
        query="hostname:*temp* OR hostname:*test* OR hostname:*admin*",
        orderBy="firstSeen",
        order="desc"
    )
    
    return {
        'legacy_systems': legacy_windows.get('devices', []),
        'untagged': untagged_devices.get('devices', []),
        'high_priority_active': high_priority_active.get('devices', []),
        'suspicious_names': suspicious_hostnames.get('devices', [])
    }

security_analysis = security_device_analysis()

print("Security Device Analysis")
print("=" * 50)

print(f"Legacy Windows systems: {len(security_analysis['legacy_systems'])}")
for device in security_analysis['legacy_systems'][:5]:
    print(f"  {device.get('hostname')}: {device.get('os')}")

print(f"\nUntagged devices: {len(security_analysis['untagged'])}")
for device in security_analysis['untagged'][:5]:
    print(f"  {device.get('hostname')} ({device.get('ip')})")

print(f"\nHigh-priority active devices: {len(security_analysis['high_priority_active'])}")
print(f"Suspicious hostnames: {len(security_analysis['suspicious_names'])}")
```

### Paginated Device Processing

```python
# Process large device datasets with pagination
def process_all_devices():
    offset = 0
    page_size = 300  # Maximum allowed
    all_devices = []
    
    while True:
        # Get page of devices
        page = client.devicesearch.get(
            count=page_size,
            offset=offset,
            orderBy="did",
            order="asc"
        )
        
        devices = page.get('devices', [])
        if not devices:
            break
            
        all_devices.extend(devices)
        print(f"Processed {len(all_devices)} devices...")
        
        # Check if we got a full page (indicates more data)
        if len(devices) < page_size:
            break
            
        offset += page_size
    
    return all_devices

# Process all devices in batches
print("Processing all devices with pagination...")
all_devices = process_all_devices()
print(f"Total devices processed: {len(all_devices)}")

# Analyze the complete dataset
vendor_distribution = {}
for device in all_devices:
    vendor = device.get('vendor', 'Unknown')
    vendor_distribution[vendor] = vendor_distribution.get(vendor, 0) + 1

print("\nComplete vendor distribution:")
for vendor, count in sorted(vendor_distribution.items(), key=lambda x: x[1], reverse=True)[:10]:
    percentage = (count / len(all_devices)) * 100
    print(f"  {vendor}: {count} ({percentage:.1f}%)")
```

### Network Topology Discovery

```python
# Discover network topology using device search
def network_topology_analysis():
    # Search devices by subnet patterns
    subnets = {}
    
    # Common private network ranges
    network_ranges = [
        "192.168.*",
        "10.*", 
        "172.16.*",
        "172.17.*",
        "172.18.*",
        "172.19.*",
        "172.20.*"
    ]
    
    for network_range in network_ranges:
        devices = client.devicesearch.get(
            query=f"ip:{network_range}",
            count=300,
            orderBy="ip",
            order="asc"
        )
        
        if devices.get('devices'):
            subnets[network_range] = devices.get('devices', [])
    
    # Analyze subnet composition
    for subnet, devices in subnets.items():
        if devices:
            print(f"\nSubnet {subnet}: {len(devices)} devices")
            
            # Analyze device types in subnet
            type_distribution = {}
            for device in devices:
                device_type = device.get('type', 'Unknown')
                type_distribution[device_type] = type_distribution.get(device_type, 0) + 1
            
            print("  Device types:")
            for device_type, count in sorted(type_distribution.items(), key=lambda x: x[1], reverse=True):
                print(f"    {device_type}: {count}")

network_topology_analysis()
```

### Device Activity Monitoring

```python
# Monitor device activity patterns
def device_activity_monitoring():
    # Different time windows for activity analysis
    time_windows = ["30minute", "1hour", "4hour", "24hour"]
    
    activity_analysis = {}
    
    for window in time_windows:
        devices = client.devicesearch.get(
            seensince=window,
            orderBy="lastSeen", 
            order="desc",
            count=300
        )
        
        activity_analysis[window] = {
            'count': len(devices.get('devices', [])),
            'devices': devices.get('devices', [])
        }
    
    # Report activity levels
    print("Device Activity Analysis")
    print("=" * 40)
    
    for window, data in activity_analysis.items():
        print(f"\nActive in last {window}: {data['count']} devices")
        
        # Show top 5 most recently active
        for device in data['devices'][:5]:
            hostname = device.get('hostname', 'Unknown')
            last_seen = device.get('lastSeen', 0)
            import time
            last_seen_str = time.ctime(last_seen / 1000) if last_seen else 'Unknown'
            print(f"    {hostname}: {last_seen_str}")
    
    # Identify constantly active vs intermittent devices
    always_active = set()
    intermittent = set()
    
    all_devices_24h = set(d.get('did') for d in activity_analysis['24hour']['devices'])
    all_devices_1h = set(d.get('did') for d in activity_analysis['1hour']['devices'])
    
    for did in all_devices_24h:
        if did in all_devices_1h:
            always_active.add(did)
        else:
            intermittent.add(did)
    
    print(f"\nConstantly active devices: {len(always_active)}")
    print(f"Intermittently active devices: {len(intermittent)}")

device_activity_monitoring()
```

## Error Handling

```python
try:
    # Search for devices with validation
    devices = client.devicesearch.get(
        query="hostname:server*",
        count=100,
        orderBy="hostname",
        order="asc"
    )
    
    # Process results
    device_list = devices.get('devices', [])
    print(f"Found {len(device_list)} devices")
    
    # Handle pagination if needed
    total_count = devices.get('totalCount', len(device_list))
    if total_count > len(device_list):
        print(f"Results truncated: {len(device_list)} of {total_count} total")
        
        # Get additional pages if needed
        remaining = total_count - len(device_list)
        additional_pages = (remaining + 299) // 300  # Round up
        
        for page in range(1, min(additional_pages + 1, 5)):  # Limit to 5 additional pages
            try:
                next_page = client.devicesearch.get(
                    query="hostname:server*",
                    count=300,
                    offset=page * 300,
                    orderBy="hostname",
                    order="asc"
                )
                device_list.extend(next_page.get('devices', []))
                print(f"Retrieved page {page + 1}, total devices: {len(device_list)}")
                
            except requests.exceptions.HTTPError as e:
                print(f"Error retrieving page {page + 1}: {e}")
                break
                
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check query syntax and parameters")
        elif e.response.status_code == 413:
            print("Request too large - reduce count parameter")
        else:
            print(f"Response: {e.response.text}")
            
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Query Syntax Best Practices
- **Use wildcards (*) wisely**: `hostname:server*` matches "server01", "server-prod", etc.
- **Combine filters**: `label:critical AND type:server` for precise targeting
- **Use quotes for exact matches**: `hostname:"web-server-01"` for exact hostname
- **Leverage boolean operators**: `(vendor:Dell OR vendor:HP) AND tag:production`

### Performance Considerations
- **Maximum count**: Limited to 300 devices per request
- **Use pagination**: For large datasets, implement proper pagination
- **Optimize queries**: Specific queries perform better than broad searches
- **Response data filtering**: Use `responsedata` to limit response size

### Sorting Options
Available `orderBy` fields:
- **priority**: Device priority level
- **hostname**: Alphabetical by hostname
- **ip**: Numerical IP address order
- **macaddress**: MAC address order
- **vendor**: Alphabetical by vendor
- **os**: Operating system name
- **firstSeen/lastSeen**: Chronological order
- **devicelabel/typelabel**: Label-based sorting

### Search Field Reference
- **label**: User-assigned device labels
- **tag**: System or user-assigned tags
- **type**: Device type classification
- **hostname**: Device hostname/name
- **ip**: IP address (supports wildcards)
- **mac**: MAC address (supports wildcards)
- **vendor**: Device vendor/manufacturer
- **os**: Operating system information

### Common Use Cases
- **Asset discovery**: Find all devices of specific types or vendors
- **Security auditing**: Identify untagged or legacy devices
- **Network mapping**: Discover devices by IP ranges or subnets
- **Compliance reporting**: Generate device inventories by criteria
- **Activity monitoring**: Track device presence and activity patterns

### Response Data Management
- **Standard fields**: All responses include core device information
- **Additional metadata**: Priority, labels, tags, timestamps
- **Subnet information**: Network context for devices
- **Pagination metadata**: Total counts and offset information for large datasets
