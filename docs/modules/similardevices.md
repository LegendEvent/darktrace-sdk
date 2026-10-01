# SimilarDevices Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The SimilarDevices module wraps the `/similardevices` endpoint. Given the `did` of a device, it returns the devices Darktrace considers similar to it, ordered by a similarity score (most similar first). This is the data shown in the Threat Visualizer when "View Similar Devices" is clicked after searching for a device in Omnisearch.

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

## Methods Overview

The SimilarDevices module provides the following method:

- **`get()`** - Retrieve the devices similar to a given device

## Methods

### Get Similar Devices

`GET /similardevices?did=<device_id>`. The device is selected with the `did` query parameter (set by the `device_id` argument); the API guide documents no other way to select a device, so `device_id` should always be provided. The API guide lists no special permission for this endpoint.

```python
# The three most similar devices to device 123
top_similar = similardevices.get(device_id=123, count=3)

# Same, with full device detail objects (changes the response structure)
detailed_similar = similardevices.get(device_id=123, count=3, fulldevicedetails=True)

# Restrict the response to ONE top-level field
scores = similardevices.get(device_id=123, responsedata="score")

# Old and new similar-device lists for a "similar devices changed" system notice
changes = similardevices.get(device_id=123, token="TOKEN_FROM_SYSTEM_NOTICE")
```

#### Parameters

- `device_id` (int or str): Device ID (`did`) to find similar devices for. Sent as the `did` query parameter.
- `count` (int, optional): Maximum number of items to return
- `fulldevicedetails` (bool, optional): Return the full device detail objects for all devices referenced in the response. This alters the JSON structure of the response. Sent as lowercase `true`/`false`
- `token` (str, optional): A token value returned by a system notice about a change in similar devices for the given device. The response then contains the old and new list of devices. This is not a pagination token
- `responsedata` (str, optional): Name of a single top-level field or object; restricts the returned JSON to only that field or object
- `timeout` (float or tuple, optional): Request timeout in seconds, or `(connect_timeout, read_timeout)`
- `**kwargs`: Additional query parameters, passed through unchanged

#### Return value

Returns the parsed JSON (a `list` for the default response).

#### Response Structure

With `fulldevicedetails=False` the response is a list ordered by `score`, highest first (abbreviated example from the API guide):

```python
[
  {
    "did": 34,
    "score": 100,
    "ip": "10.91.44.12",
    "ips": [
      {
        "ip": "10.91.44.12",
        "timems": 1581933600000,
        "time": "2020-02-17 10:00:00",
        "sid": 7
      }
    ],
    "sid": 7,
    "firstSeen": 1550492002000,
    "lastSeen": 1581935040000,
    "os": "Linux 2.2.x-3.x",
    "typename": "desktop",
    "typelabel": "Desktop"
  },
  {
    "did": 72,
    "score": 99,
    # ...
  }
]
```

| Field | Description |
|---|---|
| `did` | Device ID of the similar device |
| `score` | How similar this device is to the queried device |
| `ip` | Current IP of the device |
| `ips` | Historic IPs of the device; each has `ip`, `timems` (epoch ms, last seen), `time` (readable) and `sid` (subnet ID of the IP) |
| `sid` | Subnet ID of the subnet the device is currently in |
| `hostname` | Current hostname |
| `firstSeen` / `lastSeen` | First / last time the device was seen on the network |
| `os` | Operating system, if Darktrace can derive it |
| `typename` / `typelabel` | Device type in system / readable format |

With `fulldevicedetails=True` the items carry the full device detail objects (for example including `tags`); see the `/similardevices` response schema in the API guide for the complete list of fields.

## Examples

### List the most similar devices

```python
similar = client.similardevices.get(device_id=123, count=10)

for dev in similar:  # already ordered by score, most similar first
    print(f"{dev['did']:>6}  score={dev['score']:>3}  {dev.get('hostname', dev['ip'])}  ({dev['typelabel']})")
```

### Filter by score

```python
similar = client.similardevices.get(device_id=123)
close_matches = [d for d in similar if d["score"] >= 90]
print(f"{len(close_matches)} devices with score >= 90")
```

## Error Handling

```python
import requests

try:
    similar = client.similardevices.get(device_id=123, count=5)
    print(f"{len(similar)} similar devices")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
```

## Notes

- The response is ordered by `score`, most similar device first.
- `did` is the only way the API guide documents for selecting a device; `get()` without `device_id` is not a documented call.
- `fulldevicedetails=True` changes the JSON structure of the response.
- `responsedata` accepts the name of one top-level field or object only, not a comma-separated list.
- `token` comes from a "similar devices changed" system notice (the notice's token field) and returns the old and new device lists.
