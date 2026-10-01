# IntelFeed Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The IntelFeed module provides programmatic access to Darktrace's Watched Domains (Customer Portal), a list of domains, IPs and hostnames used by the Darktrace system, Darktrace Inoculation and STIX/TAXII integration to create model breaches. Multiple watched domains can be added and removed in one request.

Watched domains are categorized by **sources**: if no source is specified in a request, the source is set to `"default"`. A source is a textual label (under 64 characters) used to manage multiple lists of entities; it can be used as a filter in models, and a single entry can belong to any number of sources.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the intelfeed module
intelfeed = client.intelfeed
```

## Methods Overview

- **`get()`** - Retrieve watched domains, IPs, and hostnames with filtering options
- **`get_sources()`** - Get the current set of sources
- **`get_by_source()`** - Get entries from a specific source
- **`get_with_details()`** - Get entries with description, expiry, strength and iagn
- **`update()`** - Add or remove entries

All methods return the parsed JSON response (`list` or `dict`).

## Methods

### Get Intelligence Feed

```python
# Get all watched entries for the "default" source
all_entries = intelfeed.get()

# Get the current set of sources
sources_list = intelfeed.get_sources()

# Get entries for one source
source_entries = intelfeed.get_by_source("CustomSet1")

# Get entries with full details
detailed_entries = intelfeed.get_with_details()

# Combine parameters
custom_query = intelfeed.get(source="CustomSet1", fulldetails=True)
```

#### Parameters

- `sources` (bool, optional): Return the current set of sources rather than the list of watched entries
- `source` (str, optional): Restrict the retrieved list of entries to a particular source (under 64 characters). Without a source, the `default` source is returned
- `fulldetails` (bool, optional): Return full details about expiry time and description for each entry
- `responsedata` (str, optional): Restrict the returned JSON to a single top-level field or object (one name only)

#### Response Structure

Without `fulldetails`, the response is an array of entries:

```python
["example1.com", "example2.com", "0.0.0.0"]
```

With `fulldetails=True`, each element is an object:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The domain, IP or hostname on the watch list |
| `description` | string | Optional description of why the entry was added |
| `expiry` | string | Optional expiry time at which the entry is removed (e.g. `"2020-12-31T12:00:00"`) |
| `strength` | numeric | Confidence score out of 100, assigned manually or by a populating threat intelligence feed |
| `iagn` | boolean | Whether the entry triggers an automatic Darktrace RESPOND/Network (formerly Antigena Network) action if seen |

```python
[
  {
    "name": "example.net",
    "description": "Test",
    "expiry": "2020-04-03 15:23:20"
  }
]
```

The response of `sources=True` is not specified further in the API guide; inspect it with `get_sources()`.

### Update Intelligence Feed

Add or remove entries. The method sends a JSON body (POST with parameters or JSON is supported on Darktrace 6.0+) and returns the parsed JSON response. The API guide does not document the POST response body, so do not rely on specific keys such as `success`; failed requests raise an HTTP error.

```python
# Add a single entry
intelfeed.update(
    add_entry="example.com",
    description="Test",
    source="test"
)

# Add several entries
intelfeed.update(
    add_list=["example1.com", "example2.com", "192.0.2.50"],
    description="Test",
    source="ThreatIntel",
    expiry="2020-12-31T12:00:00"
)

# Add a hostname with RESPOND/Network actions
intelfeed.update(
    add_entry="c2-server.example.com",
    source="APT_Investigation",
    is_hostname=True,
    enable_antigena=True
)

# Remove one entry (source required if multiple sources are in place)
intelfeed.update(remove_entry="old-threat.com", source="ThreatIntel")

# Remove all entries (all sources!)
intelfeed.update(remove_all=True)
```

#### Parameters

- `add_entry` (str, optional): Add an external domain, hostname or IP address (`addentry`)
- `add_list` (list[str] or str, optional): Entries to add (`addlist`). A list is joined with commas; a string is sent unchanged (the API accepts a new line or comma separated list)
- `description` (str, optional): Description for added entries, under 256 characters. Do not wrap it in quotes - that results in a double-quoted string
- `source` (str, optional): Source for added entries (under 64 characters). With `remove_entry`, identifies the source to remove from
- `expiry` (str, optional): Expiration time for added items. The guide does not specify the format; its examples use `2020-12-31T12:00:00`
- `is_hostname` (bool, optional): Treat added items as hostnames rather than domains (`hostname=true`). Hostnames are treated as exact values and shown with `*` on the Watched Domains list
- `remove_entry` (str, optional): Remove an external domain, hostname or IP address (`removeentry`). A source must also be given if multiple sources are in place
- `remove_all` (bool, optional): Remove all entries, regardless of source (`removeall`). Can be used together with `add_list`
- `enable_antigena` (bool, optional): Enable automatic Darktrace RESPOND/Network actions against the endpoint (`iagn`). Not applicable to IP ranges

Only parameters that are set (truthy) are sent; `False` values are omitted.

## Examples

### List entries per source

```python
for source in client.intelfeed.get_sources():
    entries = client.intelfeed.get_by_source(source)
    print(f"{source}: {len(entries)} entries")
```

### Inspect expiry and strength

```python
entries = client.intelfeed.get(source="CustomSet1", fulldetails=True)
for entry in entries:
    print(entry["name"], entry.get("expiry"), entry.get("strength"), entry.get("iagn"))

no_expiry = [e["name"] for e in entries if not e.get("expiry")]
```

### Batch import

```python
iocs = ["malicious-domain.com", "evil-site.net", "192.0.2.100"]

client.intelfeed.update(
    add_list=iocs,
    description="IOCs from incident 2024-001",
    source="Incident_2024_001",
    expiry="2030-12-31T12:00:00"
)

print(client.intelfeed.get_by_source("Incident_2024_001"))
```

### Replace a source's list

`removeall` and `addlist` can be combined, but `removeall` clears every source. To refresh a single source, remove entries individually:

```python
source = "ThreatIntel"
for name in client.intelfeed.get_by_source(source):
    client.intelfeed.update(remove_entry=name, source=source)

client.intelfeed.update(add_list=["new1.com", "new2.com"], source=source)
```

### Import IOCs by type

Hostnames are matched exactly and need `is_hostname=True`, so import them in a separate request from domains and IP addresses:

```python
domains_and_ips = ["malicious-domain.com", "evil-site.net", "192.0.2.100"]
hostnames = ["c2-server.example.com", "www.phishing-site.example.org"]

client.intelfeed.update(
    add_list=domains_and_ips,
    description="IOC batch import",
    source="IOC_Import",
    expiry="2030-12-31T12:00:00"
)
client.intelfeed.update(
    add_list=hostnames,
    description="IOC batch import (hostnames)",
    source="IOC_Import",
    is_hostname=True,
    expiry="2030-12-31T12:00:00"
)
```

### Find entries that trigger RESPOND/Network actions

```python
entries = client.intelfeed.get_with_details()
auto_action = [e["name"] for e in entries if e.get("iagn")]
print(f"{len(auto_action)} entries trigger automatic actions: {auto_action}")
```

### Find entries expiring soon

The guide shows `expiry` values both as `2020-12-31T12:00:00` and `2020-04-03 15:23:20`; normalise the separator before parsing:

```python
from datetime import datetime, timedelta

entries = client.intelfeed.get(source="CustomSet1", fulldetails=True)
cutoff = datetime.now() + timedelta(days=7)

expiring = [
    e["name"]
    for e in entries
    if e.get("expiry")
    and datetime.fromisoformat(e["expiry"].replace(" ", "T")) <= cutoff
]
```

## Error Handling

```python
import requests

try:
    client.intelfeed.update(add_entry="test-domain.example.com", description="API test", source="API_Test")
    client.intelfeed.update(remove_entry="test-domain.example.com", source="API_Test")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

- Entries may be domains, hostnames or IP addresses; hostnames require `is_hostname=True` and are matched exactly.
- Without a source, entries are stored under and read from the `default` source.
- `remove_all=True` removes every watched domain entry, regardless of source.
- `remove_entry` needs a `source` when multiple sources are in place.
- `enable_antigena` is not applicable to IP ranges.
