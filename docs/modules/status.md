# Status Module

The Status module provides access to system status information from the Darktrace platform.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the status module
status = client.status
```

## Methods

### Get Status

Retrieve system status information from the Darktrace platform.

```python
# Get basic status information
basic_status = status.get()

# Get detailed status information
detailed_status = status.get(response_data="full")

# Get specific status information
custom_status = status.get(response_data="instancename,version,uptime")
```

#### Parameters

- `response_data` (str, optional): Comma-separated list of specific data to return. Options include:
  - `instancename`: Name of the Darktrace instance
  - `version`: Version of the Darktrace software
  - `uptime`: System uptime
  - `lastupdate`: Time of the last update
  - `models`: Information about models
  - `connections`: Connection statistics
  - `full`: All available information
- Additional parameters may be supported based on your Darktrace version

#### Response

```json
{
  "status": {
    "instancename": "Darktrace Enterprise",
    "version": "5.2.0",
    "uptime": "10 days, 5 hours, 32 minutes",
    "lastupdate": "2023-06-15T10:11:12Z",
    "models": {
      "total": 120,
      "active": 118
    },
    "connections": {
      "total": 15000,
      "active": 8750
    }
  }
}
```

## Examples

### Get Basic Status Information

```python
# Get basic status information
status_info = client.status.get()

# Extract and print instance name and version
instance_name = status_info.get("status", {}).get("instancename", "Unknown")
version = status_info.get("status", {}).get("version", "Unknown")
print(f"Connected to: {instance_name}")
print(f"Version: {version}")
```

### Check System Uptime

```python
# Get status with uptime information
status_info = client.status.get(response_data="uptime")

# Extract and print uptime
uptime = status_info.get("status", {}).get("uptime", "Unknown")
print(f"System uptime: {uptime}")
```

### Get Detailed Status Information

```python
# Get full status information
detailed_status = client.status.get(response_data="full")

# Process and display the information
status_data = detailed_status.get("status", {})
print(f"Instance: {status_data.get('instancename', 'Unknown')}")
print(f"Version: {status_data.get('version', 'Unknown')}")
print(f"Uptime: {status_data.get('uptime', 'Unknown')}")
print(f"Last Update: {status_data.get('lastupdate', 'Unknown')}")

# Display model information
models = status_data.get("models", {})
print(f"Models: {models.get('active', 0)} active out of {models.get('total', 0)} total")

# Display connection information
connections = status_data.get("connections", {})
print(f"Connections: {connections.get('active', 0)} active out of {connections.get('total', 0)} total")
```

## Error Handling

```python
try:
    status_info = client.status.get()
    # Process the status information
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Use Cases

1. **Health Monitoring**: Regularly check the status to ensure the Darktrace system is functioning properly
2. **Version Verification**: Verify the version of the Darktrace software
3. **Uptime Monitoring**: Track system uptime for reliability metrics
4. **Connection Statistics**: Monitor the number of active connections 