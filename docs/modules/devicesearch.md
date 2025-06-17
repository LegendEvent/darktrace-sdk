# Devicesearch Module

The Devicesearch module provides access to device search functionality.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the devicesearch module
devicesearch = client.devicesearch
```

## Methods

### Get Devicesearch

Retrieve device search functionality from the Darktrace platform.

```python
# Get all devicesearchs
all_devicesearchs = devicesearch.get()

# Get a specific number of devicesearchs
recent_devicesearchs = devicesearch.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "devicesearchs": [
    {
      // Devicesearch data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Devicesearchs

```python
devicesearchs_data = client.devicesearch.get()
for item in devicesearchs_data.get("devicesearchs", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    devicesearchs_data = client.devicesearch.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
