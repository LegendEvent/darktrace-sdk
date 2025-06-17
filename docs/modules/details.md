# Details Module

The Details module provides access to detailed information about specific entities.

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

## Methods

### Get Details

Retrieve detailed information about specific entities from the Darktrace platform.

```python
# Get all details
all_details = details.get()

# Get a specific number of details
recent_details = details.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "details": [
    {
      // Details data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Detailss

```python
details_data = client.details.get()
for item in details_data.get("details", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    details_data = client.details.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
