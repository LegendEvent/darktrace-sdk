# Enums Module

The Enums module provides access to enumeration values used in the Darktrace platform.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the enums module
enums = client.enums
```

## Methods

### Get Enums

Retrieve enumeration values used in the Darktrace platform from the Darktrace platform.

```python
# Get all enums
all_enums = enums.get()

# Get a specific number of enums
recent_enums = enums.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "enums": [
    {
      // Enums data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Enumss

```python
enums_data = client.enums.get()
for item in enums_data.get("enums", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    enums_data = client.enums.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
