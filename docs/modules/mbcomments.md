# Mbcomments Module

The Mbcomments module provides access to model breach comments.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the mbcomments module
mbcomments = client.mbcomments
```

## Methods

### Get Mbcomments

Retrieve model breach comments from the Darktrace platform.

```python
# Get all mbcomments
all_mbcomments = mbcomments.get()

# Get a specific number of mbcomments
recent_mbcomments = mbcomments.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "mbcomments": [
    {
      // Mbcomments data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Mbcommentss

```python
mbcomments_data = client.mbcomments.get()
for item in mbcomments_data.get("mbcomments", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    mbcomments_data = client.mbcomments.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
