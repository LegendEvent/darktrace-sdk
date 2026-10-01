# Summary Statistics Module

The Summary Statistics module wraps `/summarystatistics`: simple statistics on device counts, processed bandwidth and the number of active Darktrace RESPOND actions. It is intended for simple NOC monitoring of an instance.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

summary = client.summarystatistics
```

## Methods

### `get()`

`GET /summarystatistics`. Returns the parsed JSON (`dict`). The shape depends on which one of `eventtype`, `csensor` or `mitreTactics` is used.

| Parameter | Type | Description |
|-----------|------|-------------|
| `responsedata` | str | Name of ONE top-level field or object; restricts the JSON to it. A comma-separated list is not supported. |
| `eventtype` | str | Returns numeric event counts per category and/or type (see below). |
| `endtime` | int | End time in milliseconds since epoch (UTC). Requires `eventtype`. |
| `to` | str | End time as `YYYY-MM-DD HH:MM:SS`. Requires `eventtype`. |
| `hours` | int | Number of hour intervals back from the end time (or now). Requires `eventtype`. |
| `csensor` | bool | `true`: only bandwidth for Darktrace/Endpoint cSensor agents. `false`: Darktrace/Network bandwidth. |
| `mitreTactics` | bool | `true`: processed raw events and analysis outputs broken down by MITRE ATT&CK tactic. No device counts are returned. |
| `timeout` | float or tuple | Request timeout in seconds. |

Booleans are sent as lowercase `true`/`false`.

### Rules from the API guide

- Only ONE of `eventtype`, `csensor` or `mitreTactics` may be used. Neither the SDK nor (observed on 7.0.42) the server rejects a mix; the server silently picks one format.
- `endtime`, `to` and `hours` require `eventtype`.
- Default (no parameters): 28 days, one interval = 24 hours. With `eventtype`, one interval = 1 hour.
- Time windows of the default response: `devicecount`, `subnets`, `totalClient`, `totalServer` are unique values over the last 7 days; `licenseIPCount` is the peak unique IP count in any 24h period of the last 7 days; `usercredentialcount` covers 28 days; `patterns` covers 12 weeks.
- Device counts and values are affected by visibility restrictions.
- The guide lists no minimum permission for this endpoint.

### `eventtype`

There are four categories (`saas`, `csensor`, `network`, `loginput`) and three types (`notices`, `devicedetails`, `modelevents`). They can be requested alone or concatenated:

```python
summary.get(eventtype="saas")
summary.get(eventtype="devicedetails")
summary.get(eventtype="networkdevicedetails")   # category + type
```

The category `saas` cannot be combined with the type `devicedetails`.

The guide's example counts network device-tracking events in 24 hourly intervals with `to` and `hours`:

```python
summary.get(eventtype="networkdevicedetails", to="2021-02-12 12:00:00", hours=24)
```

Observed on Threat Visualizer 7.0.42: `eventtype` alone and `eventtype` with `endtime` work, but any request that includes `hours` (with or without `to`) is rejected with `{"summarystatistics": "INPUT ERROR"}` (HTTP 400), although the guide documents it.

## Response (no parameters)

Abbreviated, from the guide's example:

```json
{
  "usercredentialcount": 82,
  "subnets": 23,
  "patterns": 3278640,
  "bandwidth": [{"timems": 1621528800000, "time": "2021-05-20 16:40:00", "kb": 310565202}],
  "antigenaDevices": 4,
  "antigenaActions": 5,
  "devicecount": {
    "unknown": 7, "laptop": 6, "mobile": 1,
    "saas": {"Amazon": 3, "AzureActiveDirectory": 39, "total": 135},
    "licenseIPCount": 249,
    "totalClient": 285, "totalServer": 87, "totalOther": 12, "total": 519
  }
}
```

| Field | Description |
|-------|-------------|
| `usercredentialcount` | Active credentials, last 28 days |
| `subnets` | Active subnets, last 7 days |
| `patterns` | Unique connections/events/activity, last 12 weeks |
| `bandwidth[]` | Time series: `timems` (epoch ms), `time` (string), `kb` (volume ingested) |
| `antigenaDevices` | Devices controlled by active RESPOND actions, last 7 days |
| `antigenaActions` | RESPOND actions triggered and activated, last 7 days |
| `devicecount` | Device counts by type (`unknown`, `laptop`, `mobile`, `tablet`, `desktop`, `server`, `router`, `keyasset`, `dnsserver`, `proxyserver`, `logserver`, `tv`, `camera`, `fileserver`, `ipphone`, `iot`) |
| `devicecount.saas` | Per-SaaS-service device counts plus `total` |
| `devicecount.licenseIPCount` / `licenseCloudIPCount` | Peak distinct internal IPs in a 24h period (cloud VLAN IPs counted separately, no overlap) |
| `devicecount.totalClient` / `totalServer` / `totalOther` / `total` | Totals, last 7 days |

For `eventtype`, `csensor=true` and `mitreTactics=true` the response format changes. The guide only gives a full example for `eventtype=loginput` (`events` and `data[{timems, time, events}]`); for the other values see the API guide schema.

## Examples

```python
# Device counts and latest bandwidth sample
stats = summary.get()
print(stats["devicecount"]["total"], stats["antigenaActions"])
latest = stats["bandwidth"][-1]
print(latest["time"], latest["kb"])

# Only the device counts
counts = summary.get(responsedata="devicecount")

# MITRE ATT&CK breakdown
mitre = summary.get(mitreTactics=True)

# cSensor bandwidth only
csensor = summary.get(csensor=True)

# loginput event counts (ending now)
loginput = summary.get(eventtype="loginput")
```

### Bandwidth trend over the default window

`bandwidth` is a list of `{timems, time, kb}` samples (one per 24h interval by default).

```python
samples = summary.get(responsedata="bandwidth")["bandwidth"]
peak = max(samples, key=lambda s: s["kb"])
avg_kb = sum(s["kb"] for s in samples) / len(samples)
print(f"Peak {peak['time']}: {peak['kb']} kB, average {avg_kb:.0f} kB")
```

### Device counts by type

```python
counts = summary.get(responsedata="devicecount")["devicecount"]
print("Total:", counts["total"], "SaaS:", counts["saas"]["total"])
for dtype in ("laptop", "mobile", "server", "iot"):
    if dtype in counts:
        print(dtype, counts[dtype])
```

### Event counts for a fixed end time

`endtime` (milliseconds since epoch, UTC) and `to` (`YYYY-MM-DD HH:MM:SS`) are alternatives and both require `eventtype`.

```python
from datetime import datetime, timezone

end = datetime(2021, 2, 12, 12, 0, 0, tzinfo=timezone.utc)
by_endtime = summary.get(eventtype="networkdevicedetails", endtime=int(end.timestamp() * 1000))
by_to = summary.get(eventtype="saas", to="2021-02-12 12:00:00")
```

### Comparing cSensor and Network bandwidth

```python
endpoint_bw = summary.get(csensor=True)
network_bw = summary.get(csensor=False)
```

### Timeouts

```python
# Single value, or (connect, read)
stats = summary.get(timeout=(5, 30))
```

## Error handling

```python
import requests

try:
    stats = summary.get()
except requests.exceptions.HTTPError as e:
    print(f"API error: {e}")
```

Combining `eventtype`, `csensor` and `mitreTactics` is not supported by the guide. Observed on 7.0.42: the server does not return an error but silently answers in one format (`mitreTactics=true` takes precedence over the others), so send only one of them:

```python
try:
    stats = summary.get(mitreTactics=True)
except requests.exceptions.HTTPError as e:
    print(e.response.status_code, e.response.text)
```
