# Model Breaches Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.

The Model Breaches module provides access to model breach alerts in the Darktrace platform (`/modelbreaches`): retrieve breaches with filtering, read and add comments, and acknowledge or unacknowledge breaches.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the model breaches module
breaches = client.breaches
```

## Methods Overview

- **`get()`** - Retrieve model breach alerts with filtering
- **`get_comments()`** - Get comments for one or more model breaches
- **`add_comment()`** - Add a comment to a model breach
- **`acknowledge()`** - Acknowledge one or more model breaches
- **`unacknowledge()`** - Unacknowledge one or more model breaches
- **`acknowledge_with_comment()`** - Acknowledge a breach, then add a comment
- **`unacknowledge_with_comment()`** - Unacknowledge a breach, then add a comment

All methods return the parsed JSON response of the API (not a boolean). Errors are raised as exceptions.

## Methods

### Get Model Breaches

Returns a time-sorted list of model breaches matching the given parameters. All parameters are optional and are passed as keyword arguments.

```python
# All model breaches (default time window, see Notes)
breaches_data = breaches.get()

# Breaches for a device, reduced data, without acknowledged breaches
device_breaches = breaches.get(did=123, minimal=True, includeacknowledged=False)

# Breaches above a score of 80% in a time range (epoch milliseconds)
high_score_breaches = breaches.get(
    minscore=0.8,
    starttime=1640995200000,
    endtime=1641081600000,
    includebreachurl=True
)

# Human-readable time range
readable_time_breaches = breaches.get(
    from_time="2024-01-01 10:00:00",
    to_time="2024-01-01 18:00:00",
    expandenums=True
)

# SaaS breaches for specific platforms (repeated saasfilter keys)
saas_breaches = breaches.get(saasonly=True, saasfilter=["office365*", "gcp*"])

# A specific breach (single pbid, or several comma-separated)
specific_breach = breaches.get(pbid=12345)
several = breaches.get(pbid="12345,12346")

# Only some top-level fields
trimmed = breaches.get(responsedata="model")
```

#### Parameters

- `deviceattop` (bool): Return the device object at the top level rather than within each matched component. Defaults to `true` for the programmatic API.
- `did` (int): Device ID to filter by
- `endtime` (int): End time in milliseconds since epoch
- `expandenums` (bool): Expand numeric enumerated types to their string representation (codes are listed at `/enums`)
- `from_time` (str): Start time in `YYYY-MM-DD HH:MM:SS` format (sent as `from`)
- `historicmodelonly` (bool): Return only the historic version of the model details (the model at the time of breach)
- `includeacknowledged` (bool): Include acknowledged breaches
- `includebreachurl` (bool): Return a URL for the breach (requires the FQDN configuration parameter on the appliance, and only returned when `minimal=False`)
- `minimal` (bool): Reduce the amount of data returned. Always defaults to `false` programmatically.
- `minscore` (float): Minimum breach score as a fraction, e.g. `0.8` is a breach score of 80%
- `pbid` (int or str): Only return the breach with this ID; a comma-separated string returns several
- `pid` (int): Only return breaches for this model (ID unique only within the instance)
- `starttime` (int): Start time in milliseconds since epoch
- `to_time` (str): End time in `YYYY-MM-DD HH:MM:SS` format (sent as `to`)
- `uuid` (str): Only return breaches for this model (UUID is consistent across Darktrace environments)
- `responsedata` (str): Name of ONE top-level field or object; restricts the returned JSON to it
- `saasonly` (bool): Only return breaches classified as SaaS breaches
- `group` (str): With `group="device"` the `score` field shows the device score (see Notes)
- `includesuppressed` (bool): Include suppressed breaches (default `false`)
- `saasfilter` (str or list): Wildcard matched against the `SaaS::[platform]` value (e.g. `office365*`); a trailing `*` is required. A list is sent as repeated `saasfilter=` keys to include several modules.
- `creationtime` (bool): If `true`, time parameters filter on breach creation time; if `false` (default) they filter on the timestamp of the first activity relevant to the model logic
- `fulldevicedetails` (bool): Return full device/component information (forwarded as given)

#### Notes

- Time window: use `from_time`/`to_time` or `starttime`/`endtime`. Time parameters must always be specified in pairs. If no time period is given, breaches are pulled from the beginning of memory with a limit of one year per response.
- Time filters apply to the first relevant activity, not to the creation of the breach record; use `creationtime=True` to filter on creation.
- `includebreachurl` only returns a URL when `minimal=False`.
- `group="device"`: `score` (and `devicescore`) is the device score associated with the breach; the model breach score is in `pbscore`. The guide does not give a grouped response example, so the shape of grouped results is not documented here.
- Alert priority is only returned when `minimal=False` and cannot be used as a filter.
- `saasfilter` matches `SaaS::[platform]` values such as `SaaS::Office365`.
- For large environments, query shorter time frames more frequently; shorter windows return faster.
- The response schema is large; see the API guide's `/modelbreaches` response schema. Fields seen in the guide's example include `pbid`, `time`, `creationTime`, `commentCount` and `model`.

### Get Comments

Returns the comments of a breach as a list. If `pbid` is a list or tuple, a dict is returned mapping each `str(pbid)` to that breach's comment list.

```python
comments = breaches.get_comments(pbid=12345)

# Several breaches at once
all_comments = breaches.get_comments(pbid=[12345, 12346])

# Restrict the response to one top-level field
comments = breaches.get_comments(pbid=12345, responsedata="message")
```

#### Parameters

- `pbid` (int or list): Policy breach ID(s) (required)
- `responsedata` (str, optional): Name of one top-level field or object to restrict the response to (GET only)

#### Response

```json
[
  {"message": "Test Comment", "username": "ecarr", "time": 1582120499000, "pid": 12},
  {"message": "Assigned to Aidan Johnston for investigation", "username": "cchester_admin", "time": 1582120616000, "pid": 12}
]
```

`message` is the comment text, `username` the user who posted it, `time` the posting time in epoch milliseconds and `pid` the ID of the breached model.

### Add Comment

Posts a comment to `/modelbreaches/<pbid>/comments`. The comment is sent as a JSON body; the API supports no other parameters for POST.

```python
result = breaches.add_comment(
    pbid=12345,
    message="Investigated - appears to be a false positive"
)
print(result)  # {'response': 'SUCCESS'}
```

#### Parameters

- `pbid` (int): Policy breach ID (required)
- `message` (str): The comment text (required)

#### Response

The parsed JSON response, e.g. `{"response": "SUCCESS"}`.

### Acknowledge

Acknowledges a breach (sends `{"acknowledge": true}` as JSON; JSON bodies require Darktrace 6.0+, older appliances expect form parameters).

```python
result = breaches.acknowledge(pbid=12345)

# Several breaches: returns {pbid: response, ...}
results = breaches.acknowledge(pbid=[12345, 12346])
```

#### Parameters

- `pbid` (int or list): Policy breach ID(s) (required)

#### Response

The parsed JSON response of the API (for a list of `pbid`, a dict keyed by the integer `pbid`).

### Unacknowledge

Unacknowledges a breach (sends `{"unacknowledge": true}` as JSON; same 6.0+ note as above).

```python
result = breaches.unacknowledge(pbid=12345)
```

#### Parameters

- `pbid` (int or list): Policy breach ID(s) (required)

#### Response

The parsed JSON response of the API (for a list of `pbid`, a dict keyed by the integer `pbid`).

### Acknowledge / Unacknowledge with Comment

Convenience methods that call `acknowledge()` (or `unacknowledge()`) and then `add_comment()` for one breach.

```python
result = breaches.acknowledge_with_comment(pbid=12345, message="Reviewed, benign")
# {"acknowledge": <response>, "add_comment": <response>}

result = breaches.unacknowledge_with_comment(pbid=12345, message="Reopened")
# {"unacknowledge": <response>, "add_comment": <response>}
```

## Examples

### Breach Triage Workflow

```python
import time
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Unacknowledged breaches above 80%
high_priority = client.breaches.get(
    minscore=0.8,
    includeacknowledged=False,
    expandenums=True
)

for breach in high_priority:
    pbid = breach["pbid"]
    model_name = breach.get("model", {}).get("name", "Unknown")
    print(f"Breach {pbid}: {model_name}")

    comments = client.breaches.get_comments(pbid)
    print(f"Existing comments: {len(comments)}")

    client.breaches.acknowledge_with_comment(
        pbid, f"Reviewed automatically at {time.ctime()}"
    )
```

### SaaS Breaches in a Time Range

```python
saas_breaches = client.breaches.get(
    saasonly=True,
    saasfilter=["office365*", "gcp*", "azure*"],
    minscore=0.5,
    includeacknowledged=False,
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-31 23:59:59"
)
print(f"{len(saas_breaches)} SaaS breaches")
```

### Breaches of One Device

```python
device_breaches = client.breaches.get(
    did=123,
    includeacknowledged=True,
    includesuppressed=True
)

for breach in device_breaches:
    pbid = breach["pbid"]
    model_name = breach.get("model", {}).get("name", "Unknown")
    print(f"  {pbid}: {model_name}")

    comments = client.breaches.get_comments(pbid)
    if comments:
        print(f"    Latest comment: {comments[-1]['message'][:50]}")
```

### Last 7 Days

```python
import datetime

end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=7)

weekly_breaches = client.breaches.get(
    from_time=start_time.strftime("%Y-%m-%d %H:%M:%S"),
    to_time=end_time.strftime("%Y-%m-%d %H:%M:%S"),
    expandenums=True
)

daily_counts = {}
for breach in weekly_breaches:
    day = datetime.datetime.fromtimestamp(breach["time"] / 1000).strftime("%Y-%m-%d")
    daily_counts[day] = daily_counts.get(day, 0) + 1

for day, count in sorted(daily_counts.items()):
    print(f"{day}: {count}")
```

## Error Handling

```python
import requests

try:
    for breach in client.breaches.get(minscore=0.5, includeacknowledged=False):
        client.breaches.add_comment(pbid=breach["pbid"], message="Automated processing")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
```

## Response Structure Examples

Truncated from the API guide's example for `/modelbreaches/123?historicmodelonly=true`; see the guide for the complete schema.

```json
{
  "creationTime": 1582213002000,
  "commentCount": 0,
  "pbid": 287232,
  "time": 1582212986000,
  "model": {
    "name": "Compromise::HTTP Beaconing to Rare Destination",
    "pid": 143,
    "phid": 123,
    "uuid": "1a814475-5fef-499b-a467-4e2e68352cbb"
  }
}
```

## Notes

- `time` and `creationTime` in responses are epoch milliseconds; `from_time`/`to_time` are `YYYY-MM-DD HH:MM:SS` strings.
- `minimal`, `deviceattop`, `creationtime` and `includesuppressed` defaults are described above (programmatic API: `minimal=false`, `deviceattop=true`).
- `responsedata` accepts the name of a single top-level field or object.
- Suppressed breaches (models that trigger too frequently) require `includesuppressed=True`; acknowledged breaches require `includeacknowledged=True`.
