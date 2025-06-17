# Filtertypes Module

The Filtertypes module provides access to available filter types for searches.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the filtertypes module
filtertypes = client.filtertypes
```

## Methods

### Get Filtertypes

Retrieve available filter types for searches from the Darktrace platform.

```python
# Get all filtertypes
all_filtertypes = filtertypes.get()

# Get a specific number of filtertypes
recent_filtertypes = filtertypes.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "filtertypes": [
    {
      // Filtertypes data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Filtertypess

```python
filtertypes_data = client.filtertypes.get()
for item in filtertypes_data.get("filtertypes", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    filtertypes_data = client.filtertypes.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
