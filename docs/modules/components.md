# Components Module

The Components module provides access to Darktrace component information.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the components module
components = client.components
```

## Methods

### Get Components

Retrieve darktrace component information from the Darktrace platform.

```python
# Get all components
all_components = components.get()

# Get a specific number of components
recent_components = components.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "components": [
    {
      // Components data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Componentss

```python
components_data = client.components.get()
for item in components_data.get("components", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    components_data = client.components.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
