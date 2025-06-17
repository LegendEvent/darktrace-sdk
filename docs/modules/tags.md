# Tags Module

The Tags module provides access to tag management for devices and entities.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the tags module
tags = client.tags
```

## Methods

### Get Tags

Retrieve tag management for devices and entities from the Darktrace platform.

```python
# Get all tags
all_tags = tags.get()

# Get a specific number of tags
recent_tags = tags.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "tags": [
    {
      // Tags data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Tagss

```python
tags_data = client.tags.get()
for item in tags_data.get("tags", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    tags_data = client.tags.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
