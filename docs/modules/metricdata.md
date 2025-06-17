# Metricdata Module

The Metricdata module provides access to time-series metric data.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the metricdata module
metricdata = client.metricdata
```

## Methods

### Get Metricdata

Retrieve time-series metric data from the Darktrace platform.

```python
# Get all metricdatas
all_metricdatas = metricdata.get()

# Get a specific number of metricdatas
recent_metricdatas = metricdata.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "metricdatas": [
    {
      // Metricdata data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Metricdatas

```python
metricdatas_data = client.metricdata.get()
for item in metricdatas_data.get("metricdatas", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    metricdatas_data = client.metricdata.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
