# AI Analyst Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.

The AI Analyst module wraps the `/aianalyst` endpoints: incident events, incident groups, investigations, statistics, comments, and acknowledge/pin management. Query parameters are passed through as keyword arguments (`**params`) unchanged; the module does not validate them. Refer to the Darktrace API guide for the authoritative parameter list.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the analyst module
analyst = client.analyst
```

## Methods Overview

| Method | Endpoint | Returns |
|---|---|---|
| `get_incident_events(**params)` | `GET /aianalyst/incidentevents` | parsed JSON (list of events) |
| `get_groups(**params)` | `GET /aianalyst/groups` | parsed JSON (list of incidents) |
| `get_investigations(**params)` | `GET /aianalyst/investigations` | parsed JSON (list of investigations) |
| `create_investigation(investigate_time, did)` | `POST /aianalyst/investigations` (JSON) | parsed JSON |
| `get_stats(**params)` | `GET /aianalyst/stats` | parsed JSON (dict) |
| `get_comments(incident_id, response_data="")` | `GET /aianalyst/incident/comments` | parsed JSON (dict with a `comments` list) |
| `add_comment(incident_id, message)` | `POST /aianalyst/incident/comments` (JSON) | parsed JSON |
| `acknowledge(uuids)` / `unacknowledge(uuids)` | `POST /aianalyst/acknowledge` / `/unacknowledge` (form) | parsed JSON |
| `pin(uuids)` / `unpin(uuids)` | `POST /aianalyst/pin` / `/unpin` (form) | parsed JSON |

All methods also accept `timeout=`. None of them return a `bool`; the value is whatever the server answers, already parsed from JSON.

## 1. get_incident_events(**params)

Get AI Analyst incident events (the individual events that make up incidents).

```python
import time

# Basic usage: events of the last seven days (plus pinned events)
events = client.analyst.get_incident_events()

# Events of critical incidents from the last 24 hours with a minimum event score
now = int(time.time() * 1000)
yesterday = now - 24 * 60 * 60 * 1000

events = client.analyst.get_incident_events(
    starttime=yesterday,
    endtime=now,
    minscore=80,
    groupcritical=True,
    includeacknowledged=False,
)

for event in events:
    print(event["title"], event["aiaScore"], event["currentGroup"])
```

### Parameters

- `includeacknowledged` (bool): Include acknowledged events
- `includeallpinned` (bool): True by default. Controls whether pinned events are returned alongside those from the timeframe
- `includeonlypinned` (bool): False by default. Only return pinned incident events
- `includeincidenteventurl` (bool): Include links to events in the response (requires the FQDN to be set and valid on the instance)
- `locale` (str): Language for returned strings: `de_DE`, `en_GB`, `en_US`, `es_ES`, `es_419`, `fr_FR`, `it_IT`, `ja_JP`, `ko_KR`, `pt_BR`, `zh_Hans`, `zh_Hant`. Defaults to `en_GB` if missing or unsupported; non-ASCII text is returned in unicode format and must be parsed
- `starttime` / `endtime` (int): Time window in milliseconds since the epoch
- `groupcompliance` / `groupsuspicious` / `groupcritical` (bool): Only events that are part of incidents with that behavior category. Several can be combined
- `minscore` / `maxscore` (int): Event score range, 0-100
- `mingroupscore` / `maxgroupscore` (int): Score range of the incident the event belongs to, 0-100
- `did` / `excludedid` (int): Device ID to include / exclude
- `sid` / `excludesid` (int): Subnet ID to include / exclude
- `master` (int): Master instance ID (Unified View only)
- `saasonly` (bool): Only events that contain SaaS activity
- `groupid` (str): Incident group ID; overrides all other filters except `uuid`
- `uuid` (str): Incident event UUID; overrides all other filters

### Notes

- Default window: if no time parameters are given, events of the last 7 days (and pinned events) are returned. With only `endtime`, `starttime` defaults to one week before it; with only `starttime`, `endtime` defaults to now.
- Pinned events and events in pinned incidents are always returned regardless of the window, unless `includeallpinned=False`.
- A `uuid` is the `id` field of an event. The incident ID (`groupid`) of an event is in its `currentGroup` field.
- Events from Darktrace/Email carry a `sender` value and an empty `breachDevices` array.

### Response (abridged, from the API guide)

```json
[
  {
    "summariser": "AdminConnSummary",
    "mitreTactics": ["lateral-movement"],
    "acknowledged": false,
    "pinned": true,
    "createdAt": 1628002089240,
    "attackPhases": [5],
    "title": "Extensive Unusual SSH Connections",
    "id": "04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
    "children": ["04a3f36e-4u8w-v9dh-x6lb-894778cf9633"],
    "category": "critical",
    "currentGroup": "g04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
    "groupCategory": "critical",
    "groupScore": "72.9174234",
    "groupPreviousGroups": null,
    "aiaScore": 98,
    "summary": "The device 10.1.2.3 was observed making unusual internal SSH connections...",
    "periods": [{"start": 1627985298683, "end": 1628000141220}],
    "breachDevices": [
      {"identifier": null, "hostname": null, "ip": "10.1.2.3", "mac": null, "subnet": "VPN", "did": 10, "sid": 12}
    ],
    "relatedBreaches": [
      {"modelName": "Unusual Activity / Unusual Activity from Re-Activated Device", "pbid": 1234, "threatScore": 37, "timestamp": 1627997157000}
    ],
    "details": [["..."]]
  }
]
```

See the API guide for the full schema, including the nested `details` array.

## 2. get_groups(**params)

Get AI Analyst incidents (groups of incident events).

```python
# Basic usage
groups = client.analyst.get_groups()

# Critical SaaS incidents with a score of at least 90
groups = client.analyst.get_groups(
    critical=True,
    saasonly=True,
    minscore=90,
    includeacknowledged=False,
)

for group in groups:
    print(group["id"], group["category"], group["groupScore"])
    for event in group["incidentEvents"]:
        print("  ", event["uuid"], event["title"])
```

### Parameters

- `includeacknowledged` (bool): Include acknowledged incidents. False by default
- `includeallpinned` (bool): True by default. Controls whether pinned incidents are returned alongside those from the timeframe
- `includeonlypinned` (bool): False by default. Only return pinned incidents
- `starttime` / `endtime` (int): Time window in milliseconds since the epoch
- `locale` (str): Language for returned strings (same values as for `get_incident_events`)
- `includegroupurl` (bool): Include links to the incident in the Threat Visualizer (requires the FQDN to be set and valid). False by default
- `compliance` / `suspicious` / `critical` (bool): Only incidents with that behavior category. Several can be combined. **Note:** on this endpoint the names have no `group` prefix; `groupcompliance`/`groupsuspicious`/`groupcritical` belong to `get_incident_events`
- `minscore` / `maxscore` (int): Incident score range, 0-100
- `did` / `excludedid` (int): Device ID to include / exclude
- `sid` / `excludesid` (int): Subnet ID to include / exclude
- `master` (int): Master instance ID (Unified View only)
- `saasonly` (bool): Only incidents with at least one SaaS incident event
- `groupid` (str): Incident ID; takes priority over all other filters
- `uuid` (str): Incident event UUID; returns the incidents containing it. Takes priority over all filters except `groupid`

### Notes

- Default window: last 7 days plus pinned incidents; with only `endtime`, `starttime` is one week before; with only `starttime`, `endtime` is now.
- `did`/`sid`: at least one event in the incident must include the device or a device in the subnet. `excludedid`/`excludesid`: no event in the incident may include it.
- Incident scores can increase over time as events are added, so `minscore`/`maxscore` results can change.
- Merged incidents: the ID of an incident merged into another is listed in `previousIds` of the surviving incident.
- A `groupid` is the `id` of an incident (or `currentGroup` of an incident event); an event `uuid` is `incidentEvents[].uuid`.

### Response (abridged, from the API guide)

```json
[
  {
    "id": "g04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
    "active": true,
    "acknowledged": false,
    "pinned": false,
    "userTriggered": false,
    "externalTriggered": false,
    "previousIds": ["gc6e8baed-0729-437d-9268-e68d696491c1"],
    "incidentEvents": [
      {
        "uuid": "04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
        "start": 1702392635000,
        "title": "Unusual Internal Upload",
        "triggerDid": 1044,
        "sender": null,
        "visible": true,
        "acknowledged": false
      }
    ],
    "mitreTactics": ["collection", "exfiltration", "lateral-movement"],
    "devices": [1044, 1155],
    "initialDevices": [1044],
    "category": "critical",
    "groupScore": 99.93292997390672,
    "start": 1702392635000,
    "end": 1702392719930,
    "edges": ["..."]
  }
]
```

## 3. get_investigations(**params)

Get manual AI Analyst investigations (launched by users from the Threat Visualizer, the mobile app or the API).

```python
import time

# All investigations of the last week
now = int(time.time() * 1000)
week_ago = now - 7 * 24 * 60 * 60 * 1000
investigations = client.analyst.get_investigations(starttime=week_ago, endtime=now)

# One investigation, only its status field
status = client.analyst.get_investigations(
    investigationId="52c75821-7c17-4a69-b07f-1c74789a9452",
    responsedata="status",
)
```

### Parameters

- `starttime` / `endtime` (int): Time window. The guide describes milliseconds since the epoch, but its own example request uses second-based values (`starttime=1701388800`)
- `investigationId` (str): Unique identifier of a specific investigation (note the camelCase)
- `responseData` (str): Limit the response to the given top-level field(s); the guide's example request spells it `responsedata`

`did` and `investigateTime` are valid only for the POST request (see `create_investigation`). The guide documents no other GET parameters for this endpoint.

### Notes

- An investigation has the status `pending`, `processing` or `finished`.
- Activity of concern was found if the investigation has an `incidentId` and a non-empty `incidents` array. Each entry has the event `uuid` and `related` model breach IDs (`pbid`). Look up the incident with `get_groups(uuid=...)`, the event with `get_incident_events(uuid=...)`.
- The top-level `pbid` refers only to the system model `AI Analyst::AI Analyst Investigation` and cannot be used to review the associated model breaches; use the numeric values in `related` for that.

### Response (from the API guide)

```json
[
  {
    "investigationId": "52c75821-7c17-4a69-b07f-1c74789a9452",
    "time": 1702310487,
    "investigationTime": 1701864000,
    "did": 12345,
    "version": 2,
    "status": "finished",
    "createdBy": "i_west",
    "noticeUid": "NvUIJpg9MfXywYtc",
    "pbid": 630,
    "incidentId": "af763617-2626-4e4c-84fc-e03d5cd8e6c8",
    "summarizer": "SaasHijackSummary",
    "incidents": [
      {
        "uuid": "af763617-2626-4e4c-84fc-e03d5cd8e6c8",
        "related": [630, 608],
        "summariser": "SaasHijackSummary"
      }
    ]
  }
]
```

## 4. create_investigation(investigate_time, did)

Create a manual AI Analyst investigation (`POST`, JSON body `{"investigateTime": ..., "did": ...}`).

```python
# Investigate device 12345 around 2023-12-01 09:00 UTC (epoch seconds, as a string)
result = client.analyst.create_investigation("1701421200", 12345)
print(result)  # see the API guide for the POST response
```

### Parameters

- `investigate_time` (str): The time the investigation should focus around (not the time of creation); AI Analyst analyses roughly one hour around it
- `did` (int): The device the investigation is created for

### Notes

- The result is not instantaneous: poll `get_investigations(investigationId=...)` until `status` is `finished`. The `investigationId` is provided in the response to a valid POST.
- The guide recommends keeping the number of triggered investigations within reasonable bounds, mainly for cases with a custom model or a third-party alert for a device outside Darktrace.

## 5. get_stats(**params)

Get metadata on the investigations AI Analyst has performed and the resulting incidents and events.

```python
# Last 7 days (default)
stats = client.analyst.get_stats()

# Explicit window
stats = client.analyst.get_stats(starttime=week_ago, endtime=now)
print(stats["positiveInvestigations"], stats["negativeInvestigations"])
print(stats["groupStats"]["total"])
```

### Parameters

- `starttime` / `endtime` (int): Time window in milliseconds since the epoch. Default window is 7 days

The guide documents no other parameters for this endpoint.

### Response

A dict with `equivalentHumanTime`, `positiveInvestigations`, `negativeInvestigations`, `graphData`, `attackPhases`, `groupStats` (with `total`, `compliance`, `suspicious`, `critical`, `mitreTactics`) and `metadata`. See the API guide for the full schema.

## 6. get_comments(incident_id, response_data="")

Get comments for an AI Analyst incident event.

```python
event_uuid = "04a3f36e-4u8w-v9dh-x6lb-894778cf9633"

# All comments
result = client.analyst.get_comments(event_uuid)
for comment in result["comments"]:
    print(comment["username"], comment["time"], comment["message"])

# Restrict the response to one top-level field
result = client.analyst.get_comments(event_uuid, response_data="comments")
```

### Parameters

- `incident_id` (str): Event UUID (the `id` of an incident event, or `incidentEvents[].uuid` from `get_groups`). Only one value at a time
- `response_data` (str): Sent as `responsedata`. Restricts the returned JSON to the given top-level field or object

### Response (from the API guide)

```json
{
  "comments": [
    {
      "username": "smartinez_admin",
      "time": 1595501000000,
      "incident_id": "04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
      "message": "Assigned to Aidan Johnston for investigation."
    }
  ]
}
```

## 7. add_comment(incident_id, message)

Add a comment to an AI Analyst incident event (`POST`, JSON body `{"incident_id": ..., "message": ...}`; supported since Threat Visualizer 6.0.2).

```python
result = client.analyst.add_comment(
    "04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
    "Investigating potential compromise",
)
```

### Parameters

- `incident_id` (str): Event UUID
- `message` (str): Comment text

> **Observed behaviour (not in the API guide), Threat Visualizer 7.0.42:** the endpoint answers `SUCCESS` but the comment is **not stored** (it does the same for IDs that do not exist), and `get_comments()` never returns it. The 7.x UI comments on an incident group or a model breach instead. To leave a comment that is actually stored, use `client.breaches.add_comment(pbid, message)` and verify with `get_comments()` if you rely on this endpoint.

## 8. Event management

`acknowledge`, `unacknowledge`, `pin` and `unpin` take one UUID (str) or a list of UUIDs. Lists are sent comma-joined as a form-encoded `uuid` (the endpoints do not accept JSON). They return the parsed server response; the guide documents no response body for them.

```python
event_uuid = "04a3f36e-4u8w-v9dh-x6lb-894778cf9633"

# Single event
client.analyst.acknowledge(event_uuid)

# Several events
client.analyst.acknowledge([event_uuid, "af763617-2626-4e4c-84fc-e03d5cd8e6c8"])

client.analyst.unacknowledge(event_uuid)
client.analyst.pin(event_uuid)
client.analyst.unpin(event_uuid)
```

The `uuid` is the `id` of an event from `get_incident_events`, or `incidentEvents[].uuid` from `get_groups`. Pinned events are always returned by `/aianalyst/incidentevents` and `/aianalyst/groups` regardless of the time window, unless `includeallpinned=False` is passed.

## Advanced Usage Examples

### Time-based Analysis

```python
import time

now = int(time.time() * 1000)
week_ago = now - 7 * 24 * 60 * 60 * 1000

critical_events = client.analyst.get_incident_events(
    starttime=week_ago,
    endtime=now,
    groupcritical=True,
    minscore=75,
    includeacknowledged=False,
)
print(f"Found {len(critical_events)} critical events in the last week")
```

### Device-specific Investigation

```python
# All events for a specific device, including acknowledged ones
device_events = client.analyst.get_incident_events(did=1234, includeacknowledged=True)

# Create an investigation for that device
investigation = client.analyst.create_investigation(
    investigate_time=str(int(time.time())),
    did=1234,
)
```

### SaaS Security Analysis

```python
# Suspicious incidents with SaaS activity
saas_incidents = client.analyst.get_groups(
    saasonly=True,
    suspicious=True,
    minscore=50,
)
```

### Multi-language Support

```python
german_events = client.analyst.get_incident_events(locale="de_DE", groupcritical=True)
japanese_events = client.analyst.get_incident_events(locale="ja_JP", minscore=80)
```

## Error Handling

```python
import requests

try:
    events = client.analyst.get_incident_events(groupcritical=True, minscore=90)
    for event in events:
        print(f"Event: {event.get('title')} - Score: {event.get('aiaScore')}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
    if e.response is not None:
        print(f"Response status: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
except Exception as e:
    print(f"An error occurred: {e}")
```
