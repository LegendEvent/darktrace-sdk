# Network Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Network module provides access to network connectivity and traffic statistics from Darktrace. The endpoint returns data about connectivity between two or more devices; it can be focused on a device or a subnet and is used for investigative and monitoring purposes.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the network module
network = client.network
```

## Methods Overview

The Network module provides the following method:

- **`get()`** - Retrieve network connectivity and traffic statistics with extensive filtering options

## Methods

### Get Network Data

`get()` issues `GET /network` and returns the parsed JSON response (a `dict`). All parameters are optional. Booleans are sent lowercase (`true`/`false`).

```python
# Default query: data transfer volume, last hour, devices default to intext=internal
data = network.get()

# One device, specific metric, explicit time window (from_/to must be given as a pair)
device_volume = network.get(
    did=212,
    metric="datatransfervolume",
    from_="2024-01-15 09:00:00",
    to="2024-01-15 17:00:00"
)

# Same window as epoch milliseconds (starttime/endtime must be given as a pair)
by_epoch = network.get(did=212, starttime=1705309200000, endtime=1705338000000)

# Focus on a subnet (sid value)
subnet = network.get(viewsubnet=12)

# Include external devices the device interacted with
external = network.get(did=212, intext="external")

# Filter by protocol and port
dns = network.get(did=212, protocol="UDP", destinationport=53)

# Full device detail objects (alters the JSON structure)
detailed = network.get(did=212, fulldevicedetails=True)

# Only one top-level field
statistics_only = network.get(did=212, responsedata="statistics")
```

#### Parameters

- `applicationprotocol` (str, optional): Filter by application protocol (see the `/enums` endpoint for the list)
- `destinationport` (int, optional): Filter by destination port
- `did` (int, optional): Identification number of a device modelled in Darktrace
- `endtime` (int, optional): End time in milliseconds since epoch (UTC)
- `from_` (str, optional): Start time in `YYYY-MM-DD HH:MM:SS` format (sent as `from`)
- `fulldevicedetails` (bool, optional): Return the full device detail objects for all devices referenced by the response; this alters the JSON structure
- `intext` (str, optional): Restrict data to that which interacts with external sources and destinations, or to internal only. Valid values: `internal`, `external`
- `ip` (str, optional): Return data for this IP address
- `metric` (str, optional): Name of a metric (see the `/metrics` endpoint for the full list)
- `port` (int, optional): Filter by source or destination port
- `protocol` (str, optional): Filter by IP protocol (see the `/enums` endpoint for the list)
- `sourceport` (int, optional): Filter by source port
- `starttime` (int, optional): Start time in milliseconds since epoch (UTC)
- `to` (str, optional): End time in `YYYY-MM-DD HH:MM:SS` format
- `viewsubnet` (int, optional): Takes an `sid` value to focus on a specific subnet
- `responsedata` (str, optional): Name of ONE top-level field or object (for example `statistics`, `devices`, `connections`); the returned JSON is restricted to only that field or object
- `timeout` (float | tuple, optional): Per-request timeout override

#### Response Structure

The response is a dict with the top-level fields below. Example based on the API guide (`did=212&metric=datatransfervolume&fulldevicedetails=false`):

```python
{
  "statistics": [                      # list of single-key objects
    {"Views": [{"View": "Single device", "in": False, "out": False}, ...]},
    {"Connection Status": [{"Connections": "Normal", "in": 51430, "out": 25305}, ...]},
    {"Remote Ports": [{"rport": 53, "in": 51430, "out": 24990}, ...]},
    {"Local Ports": [{"lport": 58335, "in": 51430, "out": 24990}, ...]},
    {"devices": [{"device": "192.168.72.4", "ip": "192.168.72.4", "in": 43078, "out": 16660}, ...]},
    {"Subnets": []},
    {"intext": [{"intext": "Internal", "in": 51430, "out": 25305}]},
    {"protocols": [{"protocol": "UDP", "in": 51430, "out": 25305}, ...]},
    {"applicationprotocols": [{"applicationprotocol": "DNS", "in": 51430, "out": 25305}, ...]}
  ],
  "subnets": [],
  "devices": [
    {
      "did": 212,
      "size": 76735,
      "timems": 1587138366410,
      "ips": ["10.15.3.39"],
      "sid": 12,
      "ip": "10.15.3.39",
      "network": "10.15.3.0/24"
    }
  ],
  "metric": {
    "mlid": 17,
    "name": "datatransfervolume",
    "label": "Data Transfer",
    "units": "bytes",
    "filtertypes": ["Feature model", ...],
    "unitsinterval": 3600,
    "lengthscale": 599997600
  },
  "connections": [
    {
      "source": {"id": -6, "type": "subnet"},
      "target": {"id": 212, "ip": "10.15.3.39", "type": "device"},
      "timems": 1587138366593,
      "size": 36000000
    }
  ]
}
```

Field notes (from the API guide):

- `statistics` always describes data transfer, regardless of the `metric` requested. `in`/`out` are inbound/outbound data transfer in bytes; `Connections` is one of `Normal`, `Unusual`, `New`, `Breached`. It returns the information shown on the right-hand side of the Threat Visualizer when a subnet is focused.
- `devices` holds information about the specified device and any others it communicated with (internal source/destination devices; the connection direction is not given here). `size` is, depending on the metric, the data transferred or the number of matching connections; `timems` is the time the IP was last seen for the device.
- `connections` contains source/target pairs and their direction; `source.type`/`target.type` are e.g. `device` or `subnet`.
- `metric` describes the metric queried; `unitsinterval` is the default interval of the metric.
- With `intext="external"` an additional `externaldevices` object lists the external source/destination devices the device interacted with.
- With `fulldevicedetails=True` the device objects are replaced by full device details; see the API guide for that structure.

## Examples

### Data Transfer Statistics for a Device

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

data = client.network.get(
    did=212,
    metric="datatransfervolume",
    from_="2024-01-15 08:00:00",
    to="2024-01-15 18:00:00"
)

# statistics is a list of single-key dicts; merge them into one dict
stats = {k: v for item in data.get("statistics", []) for k, v in item.items()}

for row in stats.get("Connection Status", []):
    print(f"{row['Connections']}: in={row['in']} out={row['out']}")

print("Top remote ports:")
for row in sorted(stats.get("Remote Ports", []), key=lambda r: r["in"] + r["out"], reverse=True)[:5]:
    print(f"  {row['rport']}: in={row['in']} out={row['out']}")

print("Protocols:")
for row in stats.get("protocols", []):
    print(f"  {row['protocol']}: in={row['in']} out={row['out']}")

print("Application protocols:")
for row in stats.get("applicationprotocols", []):
    print(f"  {row['applicationprotocol']}: in={row['in']} out={row['out']}")
```

### Connections and Peer Devices

```python
data = client.network.get(
    did=212,
    intext="external",
    from_="2024-01-15 00:00:00",
    to="2024-01-15 23:59:59"
)

for dev in data.get("devices", []):
    print(f"Device {dev['did']} ({dev.get('ip')}) in {dev.get('network')}")

for conn in data.get("connections", []):
    src, dst = conn["source"], conn["target"]
    print(f"{src['type']} {src['id']} -> {dst['type']} {dst['id']}: size={conn['size']}")

# Peers the device exchanged data with (statistics -> devices)
stats = {k: v for item in data.get("statistics", []) for k, v in item.items()}
for peer in sorted(stats.get("devices", []), key=lambda r: r["in"] + r["out"], reverse=True)[:10]:
    print(f"  {peer['device']}: in={peer['in']} out={peer['out']}")
```

### Subnet View

```python
data = client.network.get(
    viewsubnet=12,   # an sid value
    from_="2024-01-15 00:00:00",
    to="2024-01-15 23:59:59"
)

stats = {k: v for item in data.get("statistics", []) for k, v in item.items()}
for row in stats.get("Subnets", []):
    print(row)
```

### Restricting the Response

```python
# responsedata takes ONE top-level field or object name
conns = client.network.get(did=212, responsedata="connections")
print(len(conns.get("connections", [])))
```

## Error Handling

```python
from darktrace.exceptions import DarktraceError

try:
    data = client.network.get(
        did=212,
        from_="2024-01-15 09:00:00",
        to="2024-01-15 17:00:00"
    )
    print(f"Retrieved {len(data.get('connections', []))} connections")
except DarktraceError as e:
    # DarktraceError subclasses requests.HTTPError
    print(f"API error (status {e.status_code}): {e}")
```

## Notes

- **Default timeframe**: one hour when no time parameters are given.
- **Time parameters must always be specified in pairs**: either (`starttime`, `endtime`) in epoch milliseconds (UTC) or (`from_`, `to`) as `YYYY-MM-DD HH:MM:SS`.
- **Default metric**: Data Transfer Volume (`datatransfervolume`). Any metric from `/metrics` may be specified to monitor connectivity, behavior and protocol usage. SaaS metrics are not supported by this endpoint.
- **`intext` defaults**: for devices the default is `intext=internal` (connections filtered to internal only); `intext="external"` adds an `externaldevices` object. For subnets the default returns both internal and external.
- **`responsedata`**: takes the name of one top-level field or object.
- **`fulldevicedetails`**: returns full device objects for all referenced devices and alters the JSON structure.
- **Permissions**: with per-user API tokens the associated user needs the minimum permissions listed for `/network` in the API guide; the global token is not subject to these restrictions.
