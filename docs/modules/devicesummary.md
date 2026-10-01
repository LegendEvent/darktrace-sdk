# DeviceSummary Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The DeviceSummary module wraps the `/devicesummary` endpoint, which returns the contextual information shown in the Threat Visualizer "Device Summary" window for one device. The data is aggregated from `/devices`, `/similardevices`, `/modelbreaches`, `/deviceinfo` and `/details`.

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

## Methods Overview

The DeviceSummary module provides the following method:

- **`get()`** - Retrieve the summary for a specific device (GET `/devicesummary`)

## Methods

### Get Device Summary

```python
# Complete device summary
summary = devicesummary.get(did=123)

# Only one top-level field (see "Parameters" - not documented for this endpoint)
only_data = devicesummary.get(did=123, responsedata="data")

# Custom timeout
summary = devicesummary.get(did=123, timeout=30)
```

#### Parameters

- `did` (int, **required**): Identification number of a device modelled in the Darktrace system.
- `timeout` (float | tuple, optional): Request timeout; defaults to the client timeout.
- `**kwargs`: Additional query parameters, passed through unchanged.

The API guide documents **only `did`** for this endpoint. The method also accepts the following optional keyword arguments and sends them as query parameters, but the guide does not list them for `/devicesummary`, so they may be ignored by the appliance: `device_name`, `ip_address`, `start_timestamp`, `end_timestamp`, `devicesummary_by`, `devicesummary_by_value`, `device_type`, `network_location`, `network_location_id`, `peer_id`, `source`, `status`, `responsedata`. The general `responsedata` rule in the guide is that it takes the name of a single top-level field or object and restricts the JSON to that field; for this endpoint the only top-level field is `data`.

#### Time windows

- Information from `/devices` is at the time of the query.
- The other sub-objects (`deviceinfo`, `modelbreaches`) cover a 28 day period. There are no time-range parameters in the guide.

#### Response Structure

`get()` returns the parsed JSON (a `dict`). The guide shows an abbreviated response:

```python
{
  "data": {
    "devices": {            # same as /devices for the did
      "id": 316,
      "ip": "10.0.56.12",
      "did": 316,
      "hostname": "Sarah Development",
      "os": "Linux 3.11 and newer",
      "typename": "desktop",
      "typelabel": "Desktop",
      # ...
    },
    "similardevices": [     # same as /similardevices for the did
      {"did": 34, "score": 100, "ip": "10.91.44.12"},
      # ...
    ],
    "deviceinfo": {         # same as /deviceinfo?showallgraphdata=true&fulldevicedetails=true
      "deviceInfo": [ {"did": 316, "similarityScore": 100, "graphData": [...], "info": {...}} ],
      "devices": [ ... ]
    },
    "details": [],          # same as /details; infrequently populated
    "modelbreaches": [      # same as /modelbreaches for the did
      {"creationTime": 1582213002000, "commentCount": 0, "pbid": 123,
       "time": 1582212986000, "model": {...}, "triggeredComponents": [...], "score": 0.325},
      # ...
    ]
  }
}
```

Because the endpoint aggregates the output of other endpoints, the field-level schema of each sub-object is the one of the corresponding endpoint (`/devices`, `/similardevices`, `/deviceinfo`, `/details`, `/modelbreaches`); see the API guide's Response Schema for those endpoints. The `modelbreaches` sub-object corresponds to a query with `deviceattop=false`, `includeacknowledged=true` and `historicmodelonly=false`.

Depending on the device type or on whether relevant model breaches occurred, some sub-objects may be empty.

## Examples

### Reading the sub-objects

```python
summary = client.devicesummary.get(did=316)
data = summary.get("data", {})

device = data.get("devices", {})
print(device.get("hostname"), device.get("ip"), device.get("typelabel"))

for similar in data.get("similardevices", []):
    print("similar:", similar.get("did"), similar.get("ip"), similar.get("score"))

for breach in data.get("modelbreaches", []):
    print("breach:", breach.get("pbid"), breach.get("score"))

if not data.get("details"):
    print("No /details data for this device")
```

### Summarising several devices

```python
for did in (123, 456, 789):
    data = client.devicesummary.get(did=did).get("data", {})
    host = data.get("devices", {}).get("hostname", "unknown")
    breaches = len(data.get("modelbreaches", []))
    similar = len(data.get("similardevices", []))
    print(f"{did} {host}: {breaches} breaches (28d), {similar} similar devices")
```

## Error Handling

```python
import requests

try:
    summary = client.devicesummary.get(did=123)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
```

## Notes

- GET only; `did` is the only parameter documented in the API guide.
- The guide lists minimum required permissions per endpoint (see its "Minimum Required Permissions for API Endpoints" table); without access to unrestricted devices, data may be returned anonymized.
- Not covered by the guide: an HTTP 500 on `/devicesummary` with API-token authentication was reported on Darktrace 6.3.18 (see [issue #37](https://github.com/LegendEvent/darktrace-sdk/issues/37)). If it occurs, query the underlying endpoints (`/devices`, `/similardevices`, `/modelbreaches`, `/deviceinfo`, `/details`) directly.
