# MetricData Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The MetricData module provides access to time-series metric data from Darktrace. This module allows you to retrieve actual metric values over time for analysis, monitoring, and reporting purposes. It works closely with the Metrics module: use the `name` field returned by `/metrics` (the system name, e.g. `externaldatatransfervolume`), not the label.

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

## Methods Overview

The MetricData module provides the following method:

- **`get()`** - Retrieve time-series metric data with extensive filtering and aggregation options

## Methods

### Get Metric Data

Retrieve time-series data for one or more metrics (`GET /metricdata`). The data is the same as shown in the Threat Visualizer when "Open Graph" is clicked for a device.

```python
# One metric for one device, explicit window (epoch milliseconds), hourly buckets
data = metricdata.get(
    metric="externalconnections",
    did=1,
    starttime=1582900189000,
    endtime=1582921789000,
    interval=3600
)

# Same, using date strings
data = metricdata.get(
    metric="connections",
    did=1,
    from_="2020-03-20 00:00:00",
    to="2020-03-20 23:59:59",
    interval=3600
)

# Several metrics (sent as metric1=, metric2=, ...)
data = metricdata.get(
    metrics=["externalconnections", "internalconnections"],
    did=1,
    interval=300
)

# TCP connections from device 1 to device 18 (protocol numbers: see /enums)
data = metricdata.get(
    metric="internalconnections",
    did=1,
    ddid=18,
    protocol=6,
    starttime=1584694800000,
    endtime=1584698400000,
    interval=300
)

# Include model breach times
data = metricdata.get(
    metric="externalconnections",
    did=1,
    starttime=1582900189000,
    endtime=1582921789000,
    breachtimes=True
)
```

#### Parameters

- `metric` (str, optional): System name of a metric (the `name` field of `/metrics`)
- `metrics` (list of str, optional): Several metric names; sent as `metric1=`, `metric2=`, ... and one metric object is returned per name. Use this instead of `metric`
- `did` (int, optional): Device ID
- `ddid` (int, optional): Destination device ID
- `odid` (int, optional): Other device ID; typically used with `ddid` to specify device pairs
- `port` (int, optional): Filter by source or destination port
- `sourceport` (int, optional): Filter by source port
- `destinationport` (int, optional): Filter by destination port
- `protocol` (int or str, optional): Filter by IP protocol; see `/enums` for the list (e.g. `6` for TCP)
- `applicationprotocol` (str, optional): Filter by application protocol; see `/enums` for the list
- `starttime` (int, optional): Start time in epoch milliseconds (UTC)
- `endtime` (int, optional): End time in epoch milliseconds (UTC)
- `from_` (str, optional): Start time in `YYYY-MM-DD HH:MM:SS` format (sent as `from`)
- `to` (str, optional): End time in `YYYY-MM-DD HH:MM:SS` format
- `interval` (int, optional): Interval size in seconds to group data into (default 60 per the API guide; the maximum value for any interval is returned)
- `breachtimes` (bool, optional): Return additional information on model breach times for the device; alters the structure of the response
- `fulldevicedetails` (bool, optional): Return the full device detail objects for all devices referenced by the data; alters the JSON structure of the response for certain calls
- `timeout` (float or tuple, optional): Request timeout in seconds, or `(connect, read)`
- `**params`: Additional query parameters passed through unchanged

Rules:

- Time parameters must always be given in pairs: `starttime` + `endtime`, or `from_` + `to`. The SDK raises `ValueError` if only one of a pair is passed.
- Pass either `metric` or `metrics`; with `metrics` the list is sent as `metric1`, `metric2`, ...

#### Response Structure

The response is a list. Each requested metric yields an object:

```python
[
  {
    "metric": "externalconnections",
    "data": [
      {
        "time": "2020-02-28 14:29:00",
        "timems": 1582900140000,
        "size": 14,
        "in": 0,
        "out": 14
      }
      # ... more intervals
    ]
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `metric` | string | The metric the data is returned for |
| `data` | array | Time-series data for the metric, grouped by interval |
| `data[].time` | string | Readable timestamp (`YYYY-MM-DD HH:MM:SS`) |
| `data[].timems` | numeric | Timestamp in epoch milliseconds |
| `data[].size` | numeric | Total size of the data (in and out) |
| `data[].in` | numeric | Number of inbound events or total inbound data (metric-dependent) |
| `data[].out` | numeric | Number of outbound events or total outbound data (metric-dependent) |

With `breachtimes=True` the first element of the list is an additional object holding the model breaches in the time frame:

```python
[
  {
    "breachtimes": [
      {
        "pid": 341,
        "pbid": 292504,
        "score": 0.6043,
        "name": "Compromise::Sustained SSL or HTTP Increase",
        "time": 1582902068000
      }
    ]
  },
  {"metric": "externalconnections", "data": [ ... ]}
]
```

`fulldevicedetails=True` alters the structure of the response for certain calls; see the API guide for details.

## Examples

### Hourly Series for One Device

```python
import datetime

end = datetime.datetime.now(datetime.timezone.utc)
start = end - datetime.timedelta(hours=24)

result = client.metricdata.get(
    metric="externalconnections",
    did=1,
    starttime=int(start.timestamp() * 1000),
    endtime=int(end.timestamp() * 1000),
    interval=3600
)

for metric_obj in result:
    points = metric_obj.get("data", [])
    if not points:
        continue
    peak = max(points, key=lambda p: p["size"])
    print(f"{metric_obj['metric']}: {len(points)} intervals, "
          f"peak size {peak['size']} at {peak['time']}")
```

### Several Metrics

```python
result = client.metricdata.get(
    metrics=["externalconnections", "internalconnections"],
    did=1,
    starttime=1582900189000,
    endtime=1582921789000,
    interval=300
)

for metric_obj in result:
    total_out = sum(p["out"] for p in metric_obj["data"])
    print(f"{metric_obj['metric']}: total out = {total_out}")
```

### Breach Times

```python
result = client.metricdata.get(
    metric="externalconnections",
    did=1,
    starttime=1582900189000,
    endtime=1582921789000,
    breachtimes=True
)

for obj in result:
    if "breachtimes" in obj:
        for breach in obj["breachtimes"]:
            print(f"pbid {breach['pbid']}: {breach['name']} (score {breach['score']})")
    else:
        print(f"{obj['metric']}: {len(obj['data'])} intervals")
```

## Error Handling

```python
import requests

try:
    result = client.metricdata.get(metric="externalconnections", did=1, interval=3600)
    print(f"Retrieved {len(result)} metric object(s)")
except ValueError as e:
    print(f"Invalid arguments: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

- **Metric names**: use the `name` field of `/metrics` (system name), not the label.
- **Time parameters**: `starttime`/`endtime` are epoch milliseconds; `from_`/`to` are `YYYY-MM-DD HH:MM:SS` strings. They must be given in pairs.
- **Interval**: numeric, in seconds; the default is 60 (one minute).
- **Protocol filters**: values for `protocol` and `applicationprotocol` come from `/enums`.
- **Breach times**: `breachtimes=True` returns breaches within the timeframe on the device (or the subnet specified) and alters the response structure.
