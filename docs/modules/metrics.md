# Metrics Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Metrics module provides access to the list of metrics available for filtering other API calls and for use in model making (`/metrics`).

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

## Methods Overview

The Metrics module provides the following method:

- **`get()`** - Retrieve the list of metrics, or one metric by its `mlid`

## Methods

### Get Metrics

`GET /metrics` returns all metrics as a list; `GET /metrics/<mlid>` returns one metric as a dict.

```python
# Get all available metrics (list of dicts)
all_metrics = metrics.get()

# Get one metric by its mlid (dict)
internal_transfer = metrics.get(metric_id=4)

# Restrict the response to one top-level field
names = metrics.get(responsedata="name")
```

#### Parameters

- `metric_id` (int, optional): The metric logic ID (`mlid`). If provided, only that metric is returned
- `responsedata` (str, optional): The name of a single top-level field or object; restricts the returned JSON to only that field or object
- `timeout` (float or tuple, optional): Per-request timeout override
- `**params`: Additional query parameters are passed through unchanged

#### Response Structure

```python
# metrics.get() -> list
[
  {
    "mlid": 4,
    "name": "internaldatatransfervolume",
    "label": "Internal Data Transfer",
    "set": "A",
    "units": "bytes",
    "filtertypes": [
      "Feature model",
      "DNS host lookup",
      "Process popularity",
      # ... more filter types
    ],
    "unitsinterval": 3600,
    "lengthscale": 9999960
  },
  # ... more metrics
]

# metrics.get(metric_id=13) -> dict
{
  "mlid": 13,
  "name": "multicasts",
  "label": "Multicasts",
  "units": "",
  "filtertypes": ["Feature model", "Process popularity", "Destination IP", ...],
  "unitsinterval": 3600,
  "lengthscale": 9999960
}
```

| Field | Type | Description |
|-------|------|-------------|
| `mlid` | numeric | The "metric logic" id - unique identifier |
| `name` | string | The metric in system format (use this with `metricdata`) |
| `label` | string | The metric in readable format |
| `set` | string | Metric set; `"C"` metrics are used for visual analysis and are not available for model making |
| `units` | string | The units the metric is measured in, if applicable |
| `filtertypes` | array | Filters which can be used with this metric |
| `unitsinterval` | numeric | The default time interval for the metric |
| `lengthscale` | numeric | A system field |

The API guide's `/metrics/13` example response does not show the `set` field, so it may be absent on single-metric responses.

## Examples

### List metrics

```python
all_metrics = client.metrics.get()

print(f"Available metrics: {len(all_metrics)}")
for metric in all_metrics:
    print(f"{metric['mlid']:>4}  {metric['name']:<40} {metric['label']} ({metric.get('units', '')})")
```

### Metrics usable for model making

```python
# Metrics with set "C" are for visual analysis only
model_metrics = [m for m in client.metrics.get() if m.get("set") != "C"]
print(f"{len(model_metrics)} metrics available for model making")
```

### Look up a metric and its filters

```python
metric = client.metrics.get(metric_id=4)

print(f"{metric['label']} ({metric['name']}), default interval: {metric['unitsinterval']}")
for filtertype in metric.get("filtertypes", []):
    print(f"  - {filtertype}")
```

### Find a metric by label

```python
matches = [m for m in client.metrics.get() if "transfer" in m["label"].lower()]
for m in matches:
    print(m["mlid"], m["name"])
```

### Use a metric name with MetricData

```python
# The system name (not the label) identifies the metric in other endpoints
metric = client.metrics.get(metric_id=4)
data = client.metricdata.get(metric=metric["name"], did=123)
```

## Error Handling

```python
import requests

try:
    all_metrics = client.metrics.get()
    print(f"Retrieved {len(all_metrics)} metrics")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

- `responsedata` takes the name of ONE top-level field or object, not a comma-separated list.
- `mlid` is the unique identifier of a metric; `name` is the system-format name that other endpoints such as `/metricdata` expect.
- Metrics with a `set` value of `"C"` are used for visual analysis and are not available for model making.
- Metric definitions change rarely, so caching the list client-side is reasonable.
