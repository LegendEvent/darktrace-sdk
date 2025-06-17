# Advanced Search Module

The Advanced Search module provides access to advanced search functionality.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the advanced_search module
advanced_search = client.advanced_search
```

## Methods

### Get Advanced Search

Retrieve advanced search functionality from the Darktrace platform.

```python
# Get all advanced_searchs
all_advanced_searchs = advanced_search.get()

# Get a specific number of advanced_searchs
recent_advanced_searchs = advanced_search.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "advanced_searchs": [
    {
      // Advanced Search data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Advanced Searchs

```python
advanced_searchs_data = client.advanced_search.get()
for item in advanced_searchs_data.get("advanced_searchs", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    advanced_searchs_data = client.advanced_search.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
