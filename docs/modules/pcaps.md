# Pcaps Module

The Pcaps module provides access to packet capture functionality.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the pcaps module
pcaps = client.pcaps
```

## Methods

### Get Pcaps

Retrieve packet capture functionality from the Darktrace platform.

```python
# Get all pcaps
all_pcaps = pcaps.get()

# Get a specific number of pcaps
recent_pcaps = pcaps.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "pcaps": [
    {
      // Pcaps data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Pcapss

```python
pcaps_data = client.pcaps.get()
for item in pcaps_data.get("pcaps", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    pcaps_data = client.pcaps.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
