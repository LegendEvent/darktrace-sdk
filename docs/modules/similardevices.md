# Similardevices Module

The Similardevices module provides access to similar device detection.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the similardevices module
similardevices = client.similardevices
```

## Methods

### Get Similardevices

Retrieve similar device detection from the Darktrace platform.

```python
# Get all similardevices
all_similardevices = similardevices.get()

# Get a specific number of similardevices
recent_similardevices = similardevices.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "similardevices": [
    {
      // Similardevices data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Similardevicess

```python
similardevices_data = client.similardevices.get()
for item in similardevices_data.get("similardevices", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    similardevices_data = client.similardevices.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
