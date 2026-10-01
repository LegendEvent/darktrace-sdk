# Devices Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Devices module (`/devices`) returns the list of devices identified by Darktrace, or the details of a single device (the information shown in the UI pop-up when hovering over a device). It can also change a device's label, priority and type.

For targeted searches, use the `/devicesearch` endpoint (see the Device Search module) instead.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the devices module
devices = client.devices
```

## Methods Overview

- **`get()`** - Retrieve devices (GET `/devices`)
- **`update()`** - Change a device's label, priority or type (POST `/devices`)

## Methods

### Get Devices

```python
# Get all devices (default timeframe is 7 days)
all_devices = devices.get()

# Get specific device by ID
device = devices.get(did=123)

# Get device by IP address
device_by_ip = devices.get(ip="192.168.1.100")

# Get device by MAC address
device_by_mac = devices.get(mac="00:11:22:33:44:55")

# Get the device that had a specific IP at a specific time
historical_device = devices.get(
    ip="192.168.1.100",
    iptime="2024-01-01 10:00:00"
)

# Get devices seen in the last 2 minutes on subnet 25
recent_devices = devices.get(seensince="2min", sid=25)

# Get devices seen in the last hour (a plain number means seconds)
hour_devices = devices.get(seensince="1hour")
hour_devices = devices.get(seensince="3600")

# Get devices with tags included
tagged_devices = devices.get(count=50, includetags=True)

# Get only devices identified by Darktrace Cloud Security
cloud_devices = devices.get(cloudsecurity=True)

# Get Google Cloud Platform and Microsoft 365 devices
saas_devices = devices.get(saasfilter=["gcp*", "office365*"])

# Restrict the response to one top-level field
hostnames = devices.get(responsedata="hostname")
```

#### Parameters

- `did` (int, optional): Device ID
- `ip` (str, optional): IP of the device
- `iptime` (str, optional): Returns the device which had the IP at the given time (the guide does not specify a format; the examples use `"YYYY-MM-DD HH:MM:SS"`)
- `mac` (str, optional): Returns the device with this MAC address
- `seensince` (str, optional): Relative offset for activity; devices with activity in that period are returned. Either a number of seconds before now (e.g. `"3600"`) or a number with a modifier such as `second`, `minute`, `hour`, `day` or `week` (e.g. `"2min"`, `"1hour"`). Minimum is 1 second.
- `sid` (int, optional): Subnet ID
- `count` (int, optional): Number of devices to return. Only limits the number of devices within the current timeframe.
- `includetags` (bool, optional): Include tags applied to the device in the response
- `responsedata` (str, optional): Name of ONE top-level field or object; restricts the returned JSON to only that field or object
- `cloudsecurity` (bool, optional): When `True`, limits the devices to those identified by Darktrace Cloud Security
- `saasfilter` (str or list, optional): Limit devices to specific Darktrace/Apps, Cloud or Zero Trust module users. The wildcard string is matched against the `SaaS::[platform]` value (e.g. `SaaS::Office365`), and a wildcard `*` must be given at the end (e.g. `office365*`, `gcp*`). A list is sent as repeated keys to include multiple modules.
- `timeout` (float or tuple, optional): Per-request timeout override

Booleans are sent as lowercase `true`/`false`.

#### Returns

The parsed JSON response: a list of device objects. Fields shown in the guide's example (`/devices?seensince=2hour&sid=23`):

```python
[
  {
    "id": 316,
    "ip": "10.0.56.12",
    "ips": [
      {"ip": "10.0.56.12", "timems": 1581508800000, "time": "2020-02-12 12:00:00", "sid": 23}
    ],
    "did": 316,
    "sid": 23,
    "hostname": "Sarah Development",
    "quarantine": 1623669514000,
    "time": 1528807083000,
    "endtime": 1587135192000,
    "os": "Linux 3.11 and newer",
    "typename": "desktop",
    "typelabel": "Desktop",
    "customFields": {"DT-MANUAL": {"notes": "Test Note"}}
  }
]
```

A device may lack some attributes: if it has no MAC address, label, credentials or hostname, they are omitted. Devices with priority 0 have no `priority` attribute. With `includetags=True` tags are added to each device; see the API guide for their structure. With `responsedata` the result is restricted to that field.

### Update Device

Change a device's label, priority or type (POST `/devices`, sent as a JSON body).

```python
# Update device label
result = devices.update(did=123, label="Critical Web Server")

# Update device priority (-5 to 5)
result = devices.update(did=123, priority=3)

# Update device type (enum value, see /enums?responsedata=sourcedevicetypes)
result = devices.update(did=123, type=10)

# Update multiple properties at once
result = devices.update(did=123, label="Finance File Server", priority=2, type=10)
```

#### Parameters

- `did` (int): Device ID to update (required)
- `label` (str, optional): Label to add to the device
- `priority` (int, optional): Priority on a scale of -5 to 5. Priority affects the model breach score for the device and can be used to filter alert outputs.
- `type` (int, optional): Device type in enum format (see `/enums?responsedata=sourcedevicetypes`). Only types that do not have `hidden=true` can be set; industrial device types are not available outside the Darktrace/OT environment.
- `timeout` (float or tuple, optional): Per-request timeout override

`label`, `priority` and `type` are passed as keyword arguments (`**kwargs`) and are not validated by the SDK. Fields not supported by the API are ignored.

#### Returns

The parsed JSON response of the POST request (not a boolean). The guide documents no response body for updates; see the API guide. Failures raise an exception (see Error Handling).

## Examples

### Print Device Hostnames

```python
for device in client.devices.get():
    print(f"Device ID: {device.get('did')}, Hostname: {device.get('hostname')}")
```

### Count Devices per Subnet

```python
from collections import Counter

by_subnet = Counter(d.get("sid") for d in client.devices.get(includetags=True))
for sid, n in by_subnet.most_common():
    print(f"Subnet {sid}: {n} devices")
```

### Historical IP Investigation

```python
suspicious_ip = "192.168.1.100"
for time_point in ["2024-01-01 10:00:00", "2024-01-01 14:00:00"]:
    device = client.devices.get(ip=suspicious_ip, iptime=time_point)
    # The guide describes a list response; a single match may still come back as an object
    if isinstance(device, list):
        device = device[0] if device else None
    if device:
        print(f"{time_point}: Device {device.get('did')} ({device.get('hostname', 'Unknown')})")
    else:
        print(f"{time_point}: No device found with IP {suspicious_ip}")
```

### Recently Active Devices

```python
for interval in ["2min", "10min", "1hour"]:
    recent = client.devices.get(seensince=interval)
    print(f"Devices active in last {interval}: {len(recent)}")
```

### SaaS and Cloud Devices

```python
for platform in ["office365*", "gcp*"]:
    platform_devices = client.devices.get(saasfilter=platform, responsedata="did")
    print(f"{platform}: {len(platform_devices)} devices")

cloud_devices = client.devices.get(cloudsecurity=True)
print(f"Cloud Security devices: {len(cloud_devices)}")
```

### Count Devices by Type

```python
from collections import Counter

by_type = Counter(d.get("typelabel", "Unknown") for d in client.devices.get(seensince="1day"))
for label, n in by_type.most_common():
    print(f"{label}: {n}")
```

### Look Up a Device by MAC and Label It

```python
result = client.devices.get(mac="00:11:22:33:44:55")
# The guide describes a list response; a single match may still come back as an object
device = (result[0] if result else None) if isinstance(result, list) else result
if device:
    client.devices.update(did=device["did"], label="Finance File Server")
```

### Recently Active Devices per Subnet

```python
subnet_id = 25
recent = client.devices.get(sid=subnet_id, seensince="1hour")
for device in recent:
    print(f"{device.get('ip')}  {device.get('hostname', '-')}  {device.get('os', '-')}")
```

### Update Critical Servers

```python
for device in client.devices.get(count=1000):
    hostname = device.get("hostname", "")
    if any(k in hostname.lower() for k in ["dc", "domain", "exchange", "sql"]):
        client.devices.update(did=device["did"], priority=5, label=f"CRITICAL: {hostname}")
```

Batch updates with per-device error handling:

```python
import requests

for did in [123, 456, 789]:
    try:
        client.devices.update(did=did, priority=5)
    except requests.exceptions.HTTPError as e:
        print(f"Device {did} failed: {e}")
```

## Error Handling

```python
import requests

try:
    devices = client.devices.get(did=123)
    client.devices.update(did=123, label="Updated Device Name")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

- The default timeframe is 7 days; `count` only limits devices within the current timeframe.
- `/devices` only supports searching by `did`, `sid`, `ip` and `saasfilter` (plus `mac`, `iptime`, `seensince` as listed above). For custom searches use `/devicesearch`.
- The browser-only `minscore` parameter is not applicable to token-authenticated API calls (it is set to 0).
- As of Darktrace 6.1, device types changed through the API can only be overridden by manual changes or further API requests; passive analysis, model actions and hostname expressions no longer override them.
- `seensince` accepts seconds or a number with a modifier (`second`, `minute`, `hour`, `day`, `week`); minimum 1 second.
- Use `responsedata` to restrict the response to a single top-level field or object.
