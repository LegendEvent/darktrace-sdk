# Details Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Details module wraps the `/details` endpoint, which returns a time-sorted list of connections and events for a device or entity (such as a SaaS credential). It is primarily used to populate log views such as device event logs, model breach event logs and metric logs.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the details module
details = client.details
```

## Methods Overview

- **`get()`** - Retrieve connections and events with comprehensive filtering

## Methods

### Get Details

`GET /details`. Returns the parsed JSON response (normally a list of event objects).

```python
# First 100 connections for a device (eventtype defaults to 'connection')
connections = details.get(did=123, count=100)

# Unusual connections in a millisecond time window
unusual = details.get(
    did=123,
    eventtype="unusualconnection",
    starttime=1640995200000,
    endtime=1641081600000
)

# Events for a specific model breach
breach_events = details.get(pbid=12345, eventtype="modelbreach")

# Connections Darktrace RESPOND/Network attempted to block
blocked = details.get(blockedconnections="all")

# Notice events with a specific message value
notices = details.get(msg="Authentication failure", eventtype="notice", count=50)

# Device history in a time window
history = details.get(
    did=123,
    eventtype="devicehistory",
    from_="2024-01-01 10:00:00",
    to="2024-01-01 18:00:00"
)

# Protocol and port filtering
http = details.get(
    did=123,
    protocol="TCP",
    applicationprotocol="HTTP",
    destinationport=80,
    count=200
)

# One equivalent connection per hour
dedup = details.get(did=123, deduplicate=True, count=500)
```

#### Parameters

**Selector (at least one of `did`, `pbid`, `msg`, `blockedconnections` is required; each is optional on its own):**
- `did` (int): Device ID
- `pbid` (int): Only return the model breach with this ID
- `msg` (str): Value of the message field in notice events to return details for; typically used to specify user credential strings
- `blockedconnections` (str): Restrict to connections Darktrace RESPOND/Network attempted to action. Valid values: `'all'` (all attempts, including failed ones), `'failed'` (failed attempts only), `'true'` (attempts that were performed)

**Event type:**
- `eventtype` (str): One of `'connection'`, `'unusualconnection'`, `'newconnection'`, `'notice'`, `'devicehistory'`, `'modelbreach'`. Default: `'connection'` (always sent by the SDK)

**Time and count:**
- `count` (int): Maximum number of items to return
- `starttime` / `endtime` (int): Start/end of the data in milliseconds since epoch (UTC)
- `from_` / `to` (str): Start/end of the data in `'YYYY-MM-DD HH:MM:SS'` format. The SDK sends `from_` as `from` and does not validate the format

**Connection filtering:**
- `applicationprotocol` (str): Application protocol (see `/enums` for the list)
- `protocol` (str): IP protocol (see `/enums` for the list)
- `destinationport` (int): Destination port
- `sourceport` (int): Source port
- `port` (int): Source or destination port
- `ddid` (int): Destination device ID
- `odid` (int): Other Device ID: the device to restrict data to regardless of whether it is source or destination; typically used with `did` and `ddid` to specify device pairs
- `externalhostname` (str): External hostname to return details for
- `intext` (str): `'internal'` or `'external'`
- `uid` (str): Connection UID to return

**Response options:**
- `deduplicate` (bool, default `False`): Display only one equivalent connection per hour
- `fulldevicedetails` (bool, default `False`): Return the full device detail objects for all devices referenced by the data. This can alter the JSON structure of the response; see the API guide
- `responsedata` (str): Name of ONE top-level field or object; the returned JSON is restricted to only that field or object

Any additional keyword arguments are passed through as query parameters. `deduplicate` and `fulldevicedetails` are only sent when `True`, as lowercase `true`.

#### Parameter Validation Rules

The SDK raises `ValueError` before sending the request if:
- none of `did`, `pbid`, `msg`, `blockedconnections` is given (any value other than `None` counts, so `did=0` is accepted)
- only one of `starttime`/`endtime` is given, or only one of `from_`/`to` (time parameters must always be specified in pairs)
- `count` is combined with `from_` or `starttime`

#### Response Structure

The response is a time-sorted list of event dictionaries. The fields differ by `eventtype`, protocol, model or platform (for example SaaS or ICS notices), and whether a proxy was detected; see the `/details` response schema in the API guide. Fields seen in the guide's examples:

```python
# eventtype="notice" (abbreviated)
{
  "time": "2020-04-06 16:50:50",
  "timems": 1586191850000,
  "eventType": "notice",
  "nid": 8180165,
  "uid": "ZJW3xVFQtEykPRPy",
  "direction": "in",
  "type": "SSH::Heuristic_Login_Success",
  "msg": "10.12.14.2 logged in to 192.168.72.4 successfully via SSH.",
  "destinationPort": 22,
  "sourceDevice": {"did": -6, "ip": "10.12.14.2", "typename": "networkrange", ...},
  "destinationDevice": {"did": 532, "ip": "192.168.72.4", "hostname": "workstation-local-82", ...},
  "source": "Internal Traffic",
  "destination": "workstation-local-82"
}

# eventtype="connection", blockedconnections="all" (abbreviated)
{
  "time": "2023-12-11 05:49:56",
  "timems": 1702273796155,
  "eventType": "connection",
  "uid": "CMtEGn3kBzavNfWgNd00",
  "antigenablocked": "true",
  "status": "failed",
  "sdid": 33,
  "ddid": 44,
  "port": 22,
  "sourcePort": 39260,
  "destinationPort": 22,
  "applicationprotocol": "SSH",
  "protocol": "TCP",
  "sourceDevice": {...},
  "destinationDevice": {...}
}
```

## Examples

### Connection Analysis for a Device

```python
from collections import Counter

events = client.details.get(did=123, eventtype="connection", count=1000, deduplicate=True)

print(f"Connections: {len(events)}")

# Top destinations by hostname (fall back to IP)
dests = Counter()
for ev in events:
    dev = ev.get("destinationDevice", {})
    dests[dev.get("hostname") or dev.get("ip", "Unknown")] += 1

for host, n in dests.most_common(10):
    print(f"  {host}: {n} connections")
```

### Model Breach Events

```python
events = client.details.get(pbid=12345, eventtype="modelbreach")

for ev in events:
    print(ev.get("time"), ev.get("msg"))
```

### Protocol and Port Statistics

```python
events = client.details.get(did=123, eventtype="unusualconnection", count=500)

combos = Counter(
    f"{ev.get('protocol', 'Unknown')}/{ev.get('applicationprotocol', 'Unknown')}"
    for ev in events
)
ports = Counter(ev["destinationPort"] for ev in events if "destinationPort" in ev)

print(combos.most_common(10))
print(ports.most_common(10))
```

### RESPOND Blocked Connections

```python
events = client.details.get(blockedconnections="all", count=500)

# "antigenablocked" is "true" for an attempted block; it is updated to "false"
# retrospectively if Darktrace sees that the connection continued
failed = [ev for ev in events if ev.get("antigenablocked") == "false"]
print(f"{len(events)} attempted blocks, {len(failed)} failed")
```

### Notice Events in a Time Window

```python
notices = client.details.get(
    msg="Authentication failure",
    eventtype="notice",
    from_="2024-01-01 00:00:00",
    to="2024-01-01 23:59:59"
)

for n in notices:
    print(n.get("time"), n.get("msg"))
```

### Restricting the Response

```python
# responsedata takes ONE top-level field or object name
only_msgs = client.details.get(did=123, eventtype="notice", count=100, responsedata="msg")
```

## Error Handling

```python
import requests

try:
    events = client.details.get(did=123, eventtype="connection", count=100)
    print(f"Retrieved {len(events)} events")
except ValueError as e:
    # Raised by the SDK before any request is sent
    print(f"Parameter validation error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
```

## Notes

- **Default eventtype** is `connection`.
- **Modules**: user devices covered by Darktrace modules do not return connection information. All Darktrace/Apps, Cloud and Zero Trust user activity is `eventtype=notice`.
- **Time pairs**: time parameters must always be specified in pairs (`starttime`/`endtime`, `from_`/`to`).
- **count vs. time**: if `from_` or `starttime` is used, `count` must not be used.
- **RESPOND blocks**: connections for which RESPOND created and sent a RST contain the `antigenablocked` key. `"true"` means an attempt only; it is changed to `"false"` retrospectively when Darktrace can tell the action failed. This is not always derivable (for example very short-lived connections), and a short delay is recommended before judging whether an action failed.
- **Response size**: use `responsedata`, `deduplicate` and `count` to limit large responses.
