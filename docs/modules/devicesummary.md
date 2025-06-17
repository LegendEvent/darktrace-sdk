# Devicesummary Module

The Devicesummary module provides access to summarized device information.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the devicesummary module
devicesummary = client.devicesummary
```

## Methods

### Get Devicesummary

Retrieve summarized device information from the Darktrace platform.

```python
# Get all devicesummaries
all_devicesummaries = devicesummary.get()

# Get a specific number of devicesummaries
recent_devicesummaries = devicesummary.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "devicesummaries": [
    {
      // Devicesummary data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Devicesummarys

```python
devicesummaries_data = client.devicesummary.get()
for item in devicesummaries_data.get("devicesummaries", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    devicesummaries_data = client.devicesummary.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
