# Subnets Module

The Subnets module provides access to subnet information and management.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the subnets module
subnets = client.subnets
```

## Methods

### Get Subnets

Retrieve subnet information and management from the Darktrace platform.

```python
# Get all subnets
all_subnets = subnets.get()

# Get a specific number of subnets
recent_subnets = subnets.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "subnets": [
    {
      // Subnets data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Subnetss

```python
subnets_data = client.subnets.get()
for item in subnets_data.get("subnets", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    subnets_data = client.subnets.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
