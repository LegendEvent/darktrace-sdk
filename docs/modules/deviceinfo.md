# DeviceInfo Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The DeviceInfo module wraps the `/deviceinfo` endpoint. It returns the data used in the "Connections Data" view of the Threat Visualizer for a specific device: time-series connection counts or data volumes, the ports and devices involved, and optionally data for similar devices. The data returned covers a fixed 4 week period.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the deviceinfo module
deviceinfo = client.deviceinfo
```

## Methods Overview

The DeviceInfo module provides the following method:

- **`get()`** - Retrieve connection information for a specific device

## Methods

### Get Device Information

`get()` sends `GET /deviceinfo` and returns the parsed JSON response.

```python
# Connection counts for a device (datatype defaults to "co")
device_connections = deviceinfo.get(did=12345)

# Data volume sent by the device, grouped into 4 hour intervals
data_out = deviceinfo.get(did=12345, datatype="sizeout", intervalhours=4)

# Data volume received by the device
data_in = deviceinfo.get(did=12345, datatype="sizein")

# Connections from the device to a specific destination device
device_to_device = deviceinfo.get(did=12345, odid=67890, datatype="co")

# Connections on a specific port, including full device details
port_connections = deviceinfo.get(did=12345, port=443, fulldevicedetails=True)

# External connectivity (odid=0) restricted to one domain
external_comms = deviceinfo.get(
    did=12345,
    odid=0,
    externaldomain="google.com",
    datatype="co"
)

# The device plus 3 similar devices
similar_analysis = deviceinfo.get(did=12345, similardevices=3, intervalhours=12)
```

#### Parameters

- `did` (int, required): Identification number of a device
- `datatype` (str, optional): Return data for connections (`"co"`), data size out (`"sizeout"`) or data size in (`"sizein"`). SDK default: `"co"`. The value is not validated client-side
- `odid` (int, optional): Identification number of a destination device modelled in Darktrace to restrict data to. Use `odid=0` to get external connectivity; this adds information about the external locations accessed to the response
- `port` (int, optional): Restricts returned connection data to the port specified
- `externaldomain` (str, optional): Restrict external data to a particular domain name
- `fulldevicedetails` (bool, optional): Returns the full device detail objects for all devices referenced by the response. This alters the JSON structure: a `devices` object with details of the specified device and the devices connected to is added. SDK default: `False` (always sent)
- `showallgraphdata` (bool, optional): Return an entry for every time interval in the graph data, including zero counts. `False` removes empty intervals, which can reduce noise. SDK default: `True` (always sent)
- `similardevices` (int, optional): Return data for the primary device and this number of similar devices. Only sent when set, so `0` is sent as `similardevices=0`
- `intervalhours` (int, optional): The size in hours that the returned time series data is grouped by. The minimum is 1 hour; a larger value creates a larger interval. SDK default: `1` (always sent)
- `timeout` (float or tuple, optional): Per-call request timeout override
- `**params`: Additional query parameters passed through to the API

Booleans are sent as lowercase `true`/`false`. The SDK defaults for `showallgraphdata`, `fulldevicedetails` and `intervalhours` are sent explicitly; they are SDK defaults, not documented API defaults.

#### Notes on the request

- Only the top results across the four week interval are returned; results below a certain threshold are grouped into an `others` category.
- Restricting the data to a domain or adding similar devices changes the structure of the returned JSON.
- Specifying a number of similar devices results in multiple objects in the `deviceInfo` array.

#### Response Structure

The response is a dict with a `deviceInfo` array (one entry for the device and one per similar device). Structure for `fulldevicedetails=False`, abbreviated:

```python
{
  "deviceInfo": [
    {
      "did": 316,
      "similarityScore": 100,      # original device is always 100
      "domain": "google.com",      # present when externaldomain was used
      "graphData": [
        {"time": 1582243200000, "count": 0},   # epoch ms; connections or data volume
        # ...
      ],
      "info": {
        "totalUsed": 302,          # connections/data where the device was the client
        "totalServed": 0,          # connections/data where the device was the server
        "totalDevicesAndPorts": 302,
        "devicesAndPorts": [],     # items: {"deviceAndPort": {"direction", "device", "port"}, "size"}
        "externalDomains": [{"domain": "google.com", "size": 100}],
        "portsUsed": [{"port": 443, "size": 100, "firstTime": 1584529392000}],
        "portsServed": [],         # items: {"port", "size", "firstTime"}
        "devicesUsed": [{"did": 0, "size": 100, "firstTime": 1584529392000}],
        "devicesServed": []        # items: {"did", "size", "firstTime"}
      }
    }
  ]
}
```

`size` values are percentages of the total connections or data transfer. `time` and `firstTime` are epoch timestamps in milliseconds. With `fulldevicedetails=True` a `devices` object is added; see the API guide for the full response schema.

## Examples

### Connection Analysis for a Device

```python
from datetime import datetime

result = client.deviceinfo.get(did=12345, datatype="co", intervalhours=12)

for entry in result.get("deviceInfo", []):
    graph = entry.get("graphData", [])
    total = sum(point["count"] for point in graph)
    peak = max(graph, key=lambda p: p["count"], default=None)
    print(f"Device {entry['did']} (similarity {entry['similarityScore']}): {total} in the window")
    if peak:
        peak_time = datetime.fromtimestamp(peak["time"] / 1000)
        print(f"  Peak: {peak['count']} at {peak_time:%Y-%m-%d %H:%M}")

    info = entry.get("info", {})
    print(f"  Client side: {info.get('totalUsed')}, server side: {info.get('totalServed')}")
    for p in info.get("portsUsed", []):
        print(f"  Port used {p['port']}: {p['size']}%")
    for p in info.get("portsServed", []):
        print(f"  Port served {p['port']}: {p['size']}%")
    for d in info.get("devicesUsed", []):
        print(f"  Connected to device {d['did']}: {d['size']}%")
```

### Data Transfer Comparison

```python
out_data = client.deviceinfo.get(did=12345, datatype="sizeout", intervalhours=4)
in_data = client.deviceinfo.get(did=12345, datatype="sizein", intervalhours=4)

total_out = sum(p["count"] for p in out_data["deviceInfo"][0]["graphData"])
total_in = sum(p["count"] for p in in_data["deviceInfo"][0]["graphData"])
print(f"Out: {total_out}  In: {total_in}")
```

### Similar Devices

```python
data = client.deviceinfo.get(did=12345, similardevices=3, intervalhours=12)

for entry in data["deviceInfo"]:
    total = sum(p["count"] for p in entry["graphData"])
    print(f"did={entry['did']} similarityScore={entry['similarityScore']} total={total}")
```

### External Connectivity

```python
# odid=0 requests external connectivity
data = client.deviceinfo.get(did=12345, odid=0, externaldomain="google.com")

entry = data["deviceInfo"][0]
for item in entry["info"].get("externalDomains", []):
    print(f"{item['domain']}: {item['size']}%")
```

### Full Device Details

```python
data = client.deviceinfo.get(did=12345, fulldevicedetails=True)

# The response structure changes: a "devices" object is added
print(data.get("devices"))
```

## Error Handling

```python
import requests

try:
    device_info = client.deviceinfo.get(did=12345, datatype="co", intervalhours=2)
    for entry in device_info.get("deviceInfo", []):
        print(entry["did"], len(entry.get("graphData", [])))
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```
