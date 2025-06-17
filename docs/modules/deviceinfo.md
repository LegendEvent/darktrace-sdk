# Deviceinfo Module

The Deviceinfo module provides access to detailed device information.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the deviceinfo module
deviceinfo = client.deviceinfo
```

## Methods

### Get Deviceinfo

Retrieve detailed device information from the Darktrace platform.

```python
# Get all deviceinfos
all_deviceinfos = deviceinfo.get()

# Get a specific number of deviceinfos
recent_deviceinfos = deviceinfo.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "deviceinfos": [
    {
      // Deviceinfo data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Deviceinfos

```python
deviceinfos_data = client.deviceinfo.get()
for item in deviceinfos_data.get("deviceinfos", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    deviceinfos_data = client.deviceinfo.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
