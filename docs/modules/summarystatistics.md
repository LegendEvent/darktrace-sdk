# Summarystatistics Module

The Summarystatistics module provides access to overall system statistics.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the summarystatistics module
summarystatistics = client.summarystatistics
```

## Methods

### Get Summarystatistics

Retrieve overall system statistics from the Darktrace platform.

```python
# Get all summarystatistics
all_summarystatistics = summarystatistics.get()

# Get a specific number of summarystatistics
recent_summarystatistics = summarystatistics.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "summarystatistics": [
    {
      // Summarystatistics data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Summarystatisticss

```python
summarystatistics_data = client.summarystatistics.get()
for item in summarystatistics_data.get("summarystatistics", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    summarystatistics_data = client.summarystatistics.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
