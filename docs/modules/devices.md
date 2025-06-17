# Devices Module

The Devices module provides access to device information and management functionality in the Darktrace platform.

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

## Methods

### Get Devices

Retrieve information about devices in the Darktrace platform.

```python
# Get all devices (default limit is usually 100)
all_devices = devices.get()

# Get a specific number of devices
ten_devices = devices.get(count=10)

# Get devices with specific parameters
filtered_devices = devices.get(
    count=50,           # Number of devices to return
    offset=0,           # Starting offset
    hostname="server*", # Filter by hostname (supports wildcards)
    ip="192.168.1.*",   # Filter by IP address (supports wildcards)
    mac="00:11:22:*",   # Filter by MAC address (supports wildcards)
    vendor="Microsoft", # Filter by vendor
    subnet="192.168.1.0/24", # Filter by subnet
    tag="critical"      # Filter by tag
)
```

#### Parameters

- `count` (int, optional): Number of devices to return
- `offset` (int, optional): Starting offset for pagination
- `hostname` (str, optional): Filter by hostname (supports wildcards)
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

## Error Handling

```python
try:
    devices_data = client.devices.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
``` 