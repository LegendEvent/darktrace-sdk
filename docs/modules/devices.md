# Devices Module

The Devices module provides comprehensive access to device information and management functionality in the Darktrace platform. This module allows you to retrieve, filter, and update device information with extensive filtering capabilities.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the devices module
devices = client.devices
```

## Methods Overview

The Devices module provides the following methods:

- **`get()`** - Retrieve device information with comprehensive filtering options
- **`update()`** - Update device properties and metadata

## Methods

### Get Devices

Retrieve information about devices in the Darktrace platform with extensive filtering capabilities.

```python
# Get all devices
all_devices = devices.get()

# Get specific device by ID
device = devices.get(did=123)

# Get device by IP address
device_by_ip = devices.get(ip="192.168.1.100")

# Get device by MAC address
device_by_mac = devices.get(mac="00:11:22:33:44:55")

# Get device that had specific IP at specific time
historical_device = devices.get(
    ip="192.168.1.100",
    iptime="2024-01-01 10:00:00"
)

# Get devices seen in last 2 minutes
recent_devices = devices.get(seensince="2min")

# Get devices with tags included
tagged_devices = devices.get(
    count=50,
    includetags=True
)

# Get devices from specific subnet
subnet_devices = devices.get(sid=456)

# Get only cloud security devices
cloud_devices = devices.get(cloudsecurity=True)

# Get SaaS users from specific platforms
saas_devices = devices.get(
    saasfilter=["Microsoft Office 365", "Google Workspace"]
)

# Get limited response data for performance
minimal_devices = devices.get(
    count=100,
    responsedata="hostname,ip,did"
)
```

#### Parameters

- `did` (int, optional): Specific device ID to retrieve
- `ip` (str, optional): Device IP address to search for
- `iptime` (str, optional): Returns the device that had the IP at the given time (format: "YYYY-MM-DD HH:MM:SS")
- `mac` (str, optional): Returns the device with this MAC address
- `seensince` (str, optional): Relative offset for recent activity (e.g., '2min', '1hour', '3600')
- `sid` (int, optional): Subnet ID to filter devices
- `count` (int, optional): Maximum number of devices to return
- `includetags` (bool, optional): Include tags applied to devices in the response
- `responsedata` (str, optional): Restrict returned JSON to specified field(s) - comma-separated
- `cloudsecurity` (bool, optional): Limit to devices identified by Darktrace Cloud Security
- `saasfilter` (str or list, optional): Filter by SaaS/Cloud/Zero Trust module users (can be repeated)

#### Response Structure

```python
# All devices response
{
  "devices": [
    {
      "did": 123,
      "hostname": "server01",
      "ip": "192.168.1.100",
      "mac": "00:11:22:33:44:55",
      "vendor": "Dell Inc.",
      "subnet": {...},
      "tags": [...],  # Only if includetags=True
      "firstSeen": 1640995200000,
      "lastSeen": 1641081600000,
      "priority": 0,
      "type": 1
    },
    // ... more devices
  ]
}

# Single device response (when did specified)
{
  "did": 123,
  "hostname": "server01",
  "ip": "192.168.1.100",
  "mac": "00:11:22:33:44:55",
  "vendor": "Dell Inc.",
  "subnet": {...},
  "firstSeen": 1640995200000,
  "lastSeen": 1641081600000,
  "priority": 0,
  "type": 1
}
```

### Update Device

Update device properties and metadata in the Darktrace platform.

```python
# Update device label
success = devices.update(
    did=123,
    label="Critical Web Server"
)

# Update device priority (-5 to 5 scale)
success = devices.update(
    did=123,
    priority=3
)

# Update device type
success = devices.update(
    did=123,
    type=5  # Device type enum value
)

# Update multiple properties
success = devices.update(
    did=123,
    label="Updated Server Name",
    priority=2,
    type=3
)

if success:
    print("Device updated successfully")
else:
    print("Failed to update device")
```

#### Parameters

- `did` (int): Device ID to update (required)
- `label` (str, optional): Device label/name
- `priority` (int, optional): Device priority (-5 to 5, where higher values indicate higher priority)
- `type` (int, optional): Device type enum value

#### Returns

Returns `True` if the update was successful, `False` otherwise.
- `ip` (str, optional): Filter by IP address (supports wildcards)
- `mac` (str, optional): Filter by MAC address (supports wildcards)
- `vendor` (str, optional): Filter by vendor name
- `subnet` (str, optional): Filter by subnet
- `tag` (str, optional): Filter by tag name
- `did` (int, optional): Get a specific device by ID

#### Response

```json
{
  "devices": [
    {
      "did": 123,
      "hostname": "server01",
      "ip": "192.168.1.100",
      "mac": "00:11:22:33:44:55",
      "vendor": "Dell Inc.",
      "firstseen": "2023-01-15T12:34:56Z",
      "lastseen": "2023-06-15T10:11:12Z",
      "tags": ["critical", "servers"],
      "comment": "Production web server",
      "subnet": "192.168.1.0/24"
    },
    // ... more devices
  ]
}
```

### Update Device

Update properties of a specific device.

```python
# Update a device's comment
success = devices.update(
    did=123,             # Device ID (required)
    comment="Updated comment for this device"
)

# Update a device's tags
success = devices.update(
    did=123,
    tags=["critical", "production", "web-server"]
)
```

#### Parameters

- `did` (int, required): The device ID to update
- `comment` (str, optional): New comment for the device
- `tags` (list, optional): New tags for the device (replaces existing tags)

#### Response

Returns `True` if the update was successful, `False` otherwise.

## Examples

### Get All Devices and Print Their Hostnames

```python
devices_data = client.devices.get()
for device in devices_data.get("devices", []):
    print(f"Device ID: {device.get('did')}, Hostname: {device.get('hostname')}")
```

### Update a Device's Comment

```python
device_id = 123
new_comment = "Critical production server - Do not reboot without approval"

success = client.devices.update(did=device_id, comment=new_comment)
if success:
    print(f"Successfully updated device {device_id}")
else:
    print(f"Failed to update device {device_id}")
```

### Find Devices by Tag

```python
tagged_devices = client.devices.get(tag="critical")
print(f"Found {len(tagged_devices.get('devices', []))} critical devices")
```

### Comprehensive Device Discovery

```python
from darktrace import DarktraceClient
import time

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get all devices with tags for complete information
all_devices = client.devices.get(includetags=True)

print(f"Total devices: {len(all_devices.get('devices', []))}")

# Analyze device distribution
device_stats = {
    'by_vendor': {},
    'by_subnet': {},
    'by_priority': {},
    'with_tags': 0,
    'cloud_devices': 0
}

for device in all_devices.get('devices', []):
    # Vendor analysis
    vendor = device.get('vendor', 'Unknown')
    device_stats['by_vendor'][vendor] = device_stats['by_vendor'].get(vendor, 0) + 1
    
    # Subnet analysis
    subnet_id = device.get('subnet', {}).get('sid', 'Unknown')
    device_stats['by_subnet'][subnet_id] = device_stats['by_subnet'].get(subnet_id, 0) + 1
    
    # Priority analysis
    priority = device.get('priority', 0)
    device_stats['by_priority'][priority] = device_stats['by_priority'].get(priority, 0) + 1
    
    # Tag analysis
    if device.get('tags'):
        device_stats['with_tags'] += 1

# Report statistics
print("\nDevice Statistics:")
print(f"Top vendors: {sorted(device_stats['by_vendor'].items(), key=lambda x: x[1], reverse=True)[:5]}")
print(f"Devices with tags: {device_stats['with_tags']}")
print(f"Priority distribution: {device_stats['by_priority']}")
```

### Device Management Workflow

```python
# Find and update critical servers
critical_servers = client.devices.get(count=1000)

for device in critical_servers.get('devices', []):
    hostname = device.get('hostname', '')
    did = device.get('did')
    
    # Identify critical infrastructure
    if any(keyword in hostname.lower() for keyword in ['dc', 'domain', 'exchange', 'sql']):
        print(f"Updating critical device: {hostname} (ID: {did})")
        
        # Update device priority and label
        success = client.devices.update(
            did=did,
            priority=5,  # Maximum priority
            label=f"CRITICAL: {hostname}"
        )
        
        if success:
            print(f"  Successfully updated device {did}")
        else:
            print(f"  Failed to update device {did}")
```

### Historical IP Investigation

```python
# Investigate which device had a specific IP at different times
suspicious_ip = "192.168.1.100"
investigation_times = [
    "2024-01-01 10:00:00",
    "2024-01-01 14:00:00", 
    "2024-01-01 18:00:00"
]

print(f"Investigating IP {suspicious_ip}:")
for time_point in investigation_times:
    device = client.devices.get(
        ip=suspicious_ip,
        iptime=time_point
    )
    
    if device and 'did' in device:
        hostname = device.get('hostname', 'Unknown')
        did = device.get('did')
        mac = device.get('mac', 'Unknown')
        
        print(f"  {time_point}: Device {did} ({hostname}) - MAC: {mac}")
    else:
        print(f"  {time_point}: No device found with IP {suspicious_ip}")
```

### Activity-Based Device Monitoring

```python
# Monitor recently active devices
time_intervals = ['2min', '10min', '1hour']

for interval in time_intervals:
    recent_devices = client.devices.get(seensince=interval)
    device_count = len(recent_devices.get('devices', []))
    
    print(f"Devices active in last {interval}: {device_count}")
    
    # Show top 5 most recently active
    devices = recent_devices.get('devices', [])
    sorted_devices = sorted(devices, key=lambda x: x.get('lastSeen', 0), reverse=True)
    
    print(f"  Top 5 most recent:")
    for device in sorted_devices[:5]:
        hostname = device.get('hostname', 'Unknown')
        last_seen = device.get('lastSeen', 0)
        last_seen_readable = time.ctime(last_seen / 1000) if last_seen else 'Unknown'
        print(f"    {hostname}: {last_seen_readable}")
```

### SaaS and Cloud Device Analysis

```python
# Analyze SaaS users across different platforms
saas_platforms = [
    "Microsoft Office 365",
    "Google Workspace", 
    "Salesforce",
    "AWS",
    "Azure"
]

saas_analysis = {}

for platform in saas_platforms:
    platform_devices = client.devices.get(
        saasfilter=platform,
        includetags=True,
        responsedata="hostname,did,ip,tags"
    )
    
    device_count = len(platform_devices.get('devices', []))
    saas_analysis[platform] = {
        'count': device_count,
        'devices': platform_devices.get('devices', [])
    }
    
    print(f"{platform}: {device_count} devices")

# Get cloud security specific devices
cloud_devices = client.devices.get(
    cloudsecurity=True,
    includetags=True
)

print(f"\nCloud Security devices: {len(cloud_devices.get('devices', []))}")

# Cross-platform SaaS users
multi_platform_devices = client.devices.get(
    saasfilter=["Microsoft Office 365", "Google Workspace"],
    responsedata="hostname,did"
)

print(f"Multi-platform SaaS users: {len(multi_platform_devices.get('devices', []))}")
```

### Device Subnet Analysis

```python
# Analyze devices by subnet
subnet_analysis = {}

# Get all devices first
all_devices = client.devices.get(count=10000)  # Adjust as needed

for device in all_devices.get('devices', []):
    subnet_info = device.get('subnet', {})
    subnet_id = subnet_info.get('sid')
    subnet_name = subnet_info.get('name', f'Subnet_{subnet_id}')
    
    if subnet_id not in subnet_analysis:
        subnet_analysis[subnet_id] = {
            'name': subnet_name,
            'devices': [],
            'device_count': 0
        }
    
    subnet_analysis[subnet_id]['devices'].append(device)
    subnet_analysis[subnet_id]['device_count'] += 1

# Report subnet statistics
print("Subnet Analysis:")
for sid, info in sorted(subnet_analysis.items(), key=lambda x: x[1]['device_count'], reverse=True):
    print(f"  {info['name']} (ID: {sid}): {info['device_count']} devices")
    
    # Get specific subnet devices using API
    subnet_devices = client.devices.get(
        sid=sid,
        count=5,  # Top 5 devices
        responsedata="hostname,ip,priority"
    )
    
    print(f"    Top devices:")
    for device in subnet_devices.get('devices', []):
        hostname = device.get('hostname', 'Unknown')
        ip = device.get('ip', 'Unknown')
        priority = device.get('priority', 0)
        print(f"      {hostname} ({ip}) - Priority: {priority}")
```

### Performance-Optimized Queries

```python
# Get minimal device data for large-scale analysis
minimal_devices = client.devices.get(
    count=5000,
    responsedata="did,hostname,ip,lastSeen"
)

# Process large dataset efficiently
active_devices = []
for device in minimal_devices.get('devices', []):
    last_seen = device.get('lastSeen', 0)
    if last_seen and (time.time() * 1000 - last_seen) < 3600000:  # Active in last hour
        active_devices.append(device)

print(f"Active devices in last hour: {len(active_devices)}")

# Batch update critical devices
critical_device_ids = [123, 456, 789]  # Example IDs

for did in critical_device_ids:
    success = client.devices.update(
        did=did,
        priority=5,
        label="CRITICAL_INFRASTRUCTURE"
    )
    
    if success:
        print(f"Updated device {did}")
    else:
        print(f"Failed to update device {did}")
    
    # Small delay to avoid rate limiting
    time.sleep(0.1)
```

## Error Handling

```python
try:
    # Attempt to get device information
    device = client.devices.get(did=123)
    
    if device:
        print(f"Device found: {device.get('hostname')}")
        
        # Attempt to update device
        update_success = client.devices.update(
            did=123,
            label="Updated Device Name"
        )
        
        if update_success:
            print("Device updated successfully")
        else:
            print("Device update failed")
    else:
        print("Device not found")
        
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 404:
            print("Device not found")
        elif e.response.status_code == 403:
            print("Access denied - check permissions")
        else:
            print(f"Response: {e.response.text}")
            
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Time Formats
- `iptime` parameter expects format: "YYYY-MM-DD HH:MM:SS"
- `seensince` supports relative formats: '2min', '1hour', '3600' (seconds)
- Timestamps in responses are Unix timestamps in milliseconds

### Performance Optimization
- Use `responsedata` parameter to limit response size for large queries
- Specify `count` parameter to limit result sets
- Use specific filters (did, ip, mac) for targeted queries
- Consider using minimal data queries for large-scale analysis

### SaaS Filtering
- `saasfilter` can be single string or list of strings for multiple platforms
- Common platforms: "Microsoft Office 365", "Google Workspace", "Salesforce", "AWS", "Azure"
- Use `cloudsecurity=true` specifically for cloud security identified devices

### Device Properties
- **Priority**: Integer from -5 to 5 (higher = more important)
- **Type**: Enum value representing device category
- **Tags**: Applied manually or automatically based on device behavior
- **Labels**: Human-readable names for devices

### Update Limitations
- Only certain properties can be updated via API
- Priority range is strictly enforced (-5 to 5)
- Device type values must match Darktrace enum values
- Updates are applied immediately but may take time to reflect in UI

### Historical Data
- `iptime` parameter allows historical IP address lookups
- Useful for investigating IP address changes over time
- Historical data availability depends on system retention settings