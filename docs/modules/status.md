# Status Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Status module provides the detailed system health information shown on the Darktrace Status page (`GET /status`), such as version, license dates, log ingestion, device counts, resource usage and the state of connected probes. The endpoint is read-only and well suited to monitoring in a NOC environment.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the status module
status = client.status
```

## Methods Overview

The Status module provides the following method:

- **`get()`** - Retrieve detailed system health and status information

## Methods

### Get System Status

```python
# Complete status of the queried instance, including probes
full_status = status.get()

# Faster response without probe data
quick_status = status.get(includechildren=False, fast=True)

# Only the probes object
probes = status.get(responsedata="probes")

# Only a single top-level field
version = status.get(responsedata="version")
```

#### Parameters

- `includechildren` (bool, optional): Whether information about child instances such as probes (and, in Unified View, subordinate masters) is returned. True by default
- `fast` (bool, optional): When true, the response is returned faster but subnet connectivity information is not included (if not cached). `/status` data is cached for a short period, so a `fast=True` request may still return subnet connectivity information if a request was made recently
- `responsedata` (str, optional): The name of ONE top-level field or object. Restricts the returned JSON to only that field or object. Can be used to return only information about probes or subnets, or a single specific field. A comma-separated list is not supported
- `timeout` (float or tuple, optional): Request timeout in seconds. Either a single value or `(connect_timeout, read_timeout)`

Boolean parameters are sent as lowercase `true`/`false`.

#### Return Value

The parsed JSON response (a `dict`). The queried instance is described by fields at the top level; there is no wrapper object.

#### Response Structure

Abbreviated example for `includechildren=False, fast=True` (the response contains many more fields, see the Darktrace API guide for the complete `/status` schema):

```python
{
  "excessTraffic": False,
  "time": "2023-12-08 10:21",
  "installed": "2018-10-22",
  "version": "5.1.0 (dd351a)",
  "ipAddress": "10.0.18.224",
  "label": "holdingsinc-master",
  "hostname": "example-darktrace",
  "uuid": "07dcf0e5-217b-4e98-96b9-549b3dd87706",
  "license": "2024-12-30 00:00:00",
  "antigenaNetworkEnabled": True,
  "antigenaNetworkLicense": "2025-12-31 00:00:00",
  "logIngestionProcessed": 463930,
  "licenseCounts": {
    "saas": {"total": 0},
    "licenseIPCount": 880,
    "licenseCloudIPCount": 12
  },
  "type": "master",
  "diskUtilization": 1,
  "load": 10,
  "cpu": 11,
  "memoryUsed": 87,
  "networkInterfacesState_eth0": "up",
  ...
}
```

#### Probes, Masters and Unified View

With `includechildren=True` (the default), data from child instances is included:

- The queried instance is represented by the top-level fields.
- Probes (vSensor and hardware) are contained in a `probes` object, a dictionary with each probe identified by a numeric ID (as a string key). Each probe has fields such as `id`, `version`, `ipAddress`, `load`, `cpu`, `memoryUsed`, `osSensors`, `bandwidthCurrent` and `connectionsPerMinuteCurrent`.
- When a Unified View instance is queried, subordinate masters are contained in an `instances` object, identified by numeric ID. Each of these may have its own `probes` object for the probes associated directly with it.
- With `includechildren=False`, or where a master has no probes, no `probes` object is returned.

```python
{
  "time": "2024-01-05 14:44",
  "probes": {
    "12": {
      "id": 12,
      "configuredServer": "example-vsensor-2.example.com",
      "version": "6.1.23 (f35936c6)",
      "ipAddress": "10.10.12.12",
      "load": 25,
      "cpu": 6,
      "memoryUsed": 18,
      "bandwidthCurrent": 542011,
      "connectionsPerMinuteCurrent": 169
    }
  }
}
```

## Examples

### Get Basic Status Information

```python
status_info = client.status.get(includechildren=False, fast=True)

print(f"Connected to: {status_info.get('label', 'Unknown')} ({status_info.get('hostname', 'Unknown')})")
print(f"Version: {status_info.get('version', 'Unknown')}")
print(f"License valid until: {status_info.get('license', 'Unknown')}")
```

### List Connected Probes

```python
probes = client.status.get(responsedata="probes").get("probes", {})

for probe_id, probe in probes.items():
    print(
        f"Probe {probe_id}: {probe.get('ipAddress')} "
        f"v{probe.get('version')} - CPU {probe.get('cpu')}%, "
        f"memory {probe.get('memoryUsed')}%"
    )
```

### Basic Health Check

```python
status_info = client.status.get(fast=True)

print(f"Load: {status_info.get('load')}")
print(f"CPU: {status_info.get('cpu')}%")
print(f"Memory used: {status_info.get('memoryUsed')}%")
print(f"Disk utilization: {status_info.get('diskUtilization')}%")

counts = status_info.get("licenseCounts", {})
print(f"Licensed IPs: {counts.get('licenseIPCount')}")

# Network interface state fields are named networkInterfacesState_<interface>
for key, value in status_info.items():
    if key.startswith("networkInterfacesState_"):
        print(f"{key.split('_', 1)[1]}: {value}")
```

### Unified View

```python
status_info = client.status.get()

for instance_id, instance in status_info.get("instances", {}).items():
    probes = instance.get("probes", {})
    print(f"Instance {instance_id}: {len(probes)} probe(s)")
```

## Error Handling

```python
import requests

try:
    system_status = client.status.get(fast=True, includechildren=False)
    print(f"Version: {system_status.get('version')}")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")

except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")

except requests.exceptions.Timeout as e:
    print(f"Request timeout: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

- `GET /status` is read-only; it cannot be used to manage probes.
- The `format=json` parameter from the API guide is only needed when accessing the endpoint in a browser and is not used by this module.
- `fast` only affects subnet connectivity information; use `includechildren=False` to leave out probe/child instance data.
- The naming and numbering of network interface fields depends on your environment and the connected probe types.
- To read only one part of the response (for example `probes` or `subnetData`), use `responsedata` with that single top-level name.
