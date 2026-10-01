# CVEs Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The CVEs module retrieves information on device CVEs created by the Darktrace/OT ICS Vulnerability Tracker integration (`/cves` endpoint). **This endpoint is only available for Darktrace/OT environments.**

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the CVEs module
cves = client.cves
```

## Methods Overview

- **`get()`** - Retrieve CVE information, optionally for a single device

## Methods

### Get CVEs

`GET /cves` - returns the CVEs associated with devices in the network, grouped per device.

```python
# All CVEs for all devices
all_cves = cves.get()

# CVEs for one device
device_cves = cves.get(did=12)

# CVEs for one device, plus full details of the referenced devices
detailed = cves.get(did=12, fulldevicedetails=True)
```

#### Parameters

- `did` (int, optional): Identification number of a device modelled in the Darktrace system
- `fulldevicedetails` (bool, optional): Return the full device detail objects for all devices referenced in the response. This adds a `devices` object alongside `results` (sent as `true`/`false`)
- `timeout` (float or tuple, optional): Per-request timeout override
- `**params`: Additional query parameters passed through to the API

#### Return Value

Returns the parsed JSON response (a `dict`) with a `results` key.

#### Response Structure

```python
{
  "results": [
    {
      "did": 12,
      "platform mappings (CPEs)": [
        {
          "vendor": "rockwellautomation",
          "product": "compactlogix_1769-l16er-bb1b",
          "version": "All ",
          "patch": "",
          "cves": [
            {
              "LAST_MODIFIED_DATE": "2018-05-20",
              "CVE_ID": "CVE-2016-2279",
              "BASE_SEVERITY": "Medium",
              "DESCRIPTION": "Cross-site scripting (XSS) vulnerability in ..."
            }
          ],
          "applies to": ["CVE-2016-2279"]
        }
      ],
      "cves": [
        {
          "LAST_MODIFIED_DATE": "2018-05-20",
          "CVE_ID": "CVE-2016-2279",
          "BASE_SEVERITY": "Medium",
          "DESCRIPTION": "Cross-site scripting (XSS) vulnerability in ..."
        }
      ]
    }
  ]
}
```

Fields of each entry in `results`:

- `did`: unique identifier of the device
- `platform mappings (CPEs)`: CVEs matched to the device, grouped by CPE (some CVEs may be matched by multiple CPEs)
  - `vendor`, `product`: the vendor and the product (CPE) that has been matched
  - `version`: the product version the CVEs apply to
  - `patch`: if a patch is available, which software version is required to mitigate
  - `cves`: the specific CVEs matched to the device by this CPE (`LAST_MODIFIED_DATE`, `CVE_ID`, `BASE_SEVERITY`, `DESCRIPTION`)
  - `applies to`: array of the CVE IDs matched by this CPE
- `cves`: all CVEs successfully matched to the device (same fields as above)

`BASE_SEVERITY` is the base severity of the CVE as denoted by NIST and `DESCRIPTION` is the description as provided by NIST. With `fulldevicedetails=True`, a `devices` object with the full details of the devices referenced in `results` is added; the guide does not show its contents (see the API guide).

## Examples

### List CVEs per device

```python
data = client.cves.get()

for entry in data.get("results", []):
    cve_ids = [c.get("CVE_ID") for c in entry.get("cves", [])]
    print(f"Device {entry.get('did')}: {len(cve_ids)} CVEs")
    for cve in entry.get("cves", []):
        print(f"  {cve.get('CVE_ID')} ({cve.get('BASE_SEVERITY')}), "
              f"modified {cve.get('LAST_MODIFIED_DATE')}")
```

### CVEs for one device, grouped by product

```python
data = client.cves.get(did=12)

for entry in data.get("results", []):
    for cpe in entry.get("platform mappings (CPEs)", []):
        print(f"{cpe.get('vendor')} / {cpe.get('product')} (version: {cpe.get('version')})")
        if cpe.get("patch"):
            print(f"  Patch: {cpe['patch']}")
        for cve in cpe.get("cves", []):
            print(f"  {cve.get('CVE_ID')}: {cve.get('BASE_SEVERITY')}")
```

### Severity summary

```python
from collections import Counter

data = client.cves.get()
counts = Counter(
    cve.get("BASE_SEVERITY", "Unknown")
    for entry in data.get("results", [])
    for cve in entry.get("cves", [])
)
for severity, count in counts.most_common():
    print(f"{severity}: {count}")
```

### Filter by severity (client-side)

```python
data = client.cves.get()

wanted = {"high", "critical"}
for entry in data.get("results", []):
    hits = [c for c in entry.get("cves", [])
            if str(c.get("BASE_SEVERITY", "")).lower() in wanted]
    if hits:
        print(f"Device {entry.get('did')}: {', '.join(c['CVE_ID'] for c in hits)}")
```

### Devices ranked by number of CVEs

```python
data = client.cves.get()

ranked = sorted(
    data.get("results", []),
    key=lambda e: len(e.get("cves", [])),
    reverse=True,
)
for entry in ranked[:10]:
    print(f"Device {entry.get('did')}: {len(entry.get('cves', []))} CVEs")
```

### Unique CVEs across the network

```python
data = client.cves.get()

devices_per_cve = {}
for entry in data.get("results", []):
    for cve in entry.get("cves", []):
        devices_per_cve.setdefault(cve.get("CVE_ID"), set()).add(entry.get("did"))

for cve_id, dids in sorted(devices_per_cve.items(), key=lambda kv: len(kv[1]), reverse=True):
    print(f"{cve_id}: {len(dids)} device(s)")
```

### Check several devices

```python
for did in [12, 34, 56]:
    data = client.cves.get(did=did)
    cve_ids = [c.get("CVE_ID")
               for entry in data.get("results", [])
               for c in entry.get("cves", [])]
    print(f"Device {did}: {len(cve_ids)} CVEs {cve_ids}")
```

### CPEs with an available patch

```python
data = client.cves.get()

for entry in data.get("results", []):
    for cpe in entry.get("platform mappings (CPEs)", []):
        if cpe.get("patch"):
            print(f"Device {entry.get('did')}: {cpe.get('vendor')} / {cpe.get('product')} "
                  f"-> patch {cpe['patch']} ({len(cpe.get('cves', []))} CVEs)")
```

### Full device details

```python
data = client.cves.get(did=12, fulldevicedetails=True)

print(data.get("results"))
print(data.get("devices"))  # added by fulldevicedetails=True
```

## Error Handling

```python
import requests

try:
    data = client.cves.get()
    print(f"{len(data.get('results', []))} devices with CVEs")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Notes

- Only available for Darktrace/OT environments
- Only `did` and `fulldevicedetails` are documented parameters; severity filtering must be done client-side
- Some CVEs may appear under several CPEs of the same device, so `cves` may contain entries that are also listed in `platform mappings (CPEs)`
- Use `did` to reduce response size when only one device is of interest
