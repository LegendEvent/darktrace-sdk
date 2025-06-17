# Metrics Module

The Metrics module provides access to available metrics and their information.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the metrics module
metrics = client.metrics
```

## Methods

### Get Metrics

Retrieve available metrics and their information from the Darktrace platform.

```python
# Get all metrics
all_metrics = metrics.get()

# Get a specific number of metrics
recent_metrics = metrics.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "metrics": [
    {
      // Metrics data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Metricss

```python
metrics_data = client.metrics.get()
for item in metrics_data.get("metrics", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    metrics_data = client.metrics.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
