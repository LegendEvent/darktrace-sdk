# Antigena Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Antigena module provides access to Darktrace's RESPOND/Network (formerly Antigena Network) functionality, which includes automated response actions and manual intervention capabilities. This module allows you to manage active and pending RESPOND actions, create manual actions, and get comprehensive summaries.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the Antigena module
antigena = client.antigena
```

## Methods Overview

The Antigena module provides the following methods:

- **`get_actions()`** - Retrieve current and past RESPOND actions with filtering
- **`approve_action()`** - Deprecated no-op, kept for backwards compatibility
- **`activate_action()`** - Activate pending RESPOND actions
- **`extend_action()`** - Extend active RESPOND actions
- **`clear_action()`** - Clear active, pending or expired actions
- **`reactivate_action()`** - Reactivate cleared or expired actions
- **`create_manual_action()`** - Create manual RESPOND/Network actions
- **`get_summary()`** - Get summary of active and pending actions

All methods return the parsed JSON response (a `dict` or `list`), not a boolean. Failed requests raise an exception.

## Methods

### Get Actions

Retrieve information about current and past Darktrace RESPOND/Network actions. If no time window is specified, the request returns all current actions with a future expiry date and all historic actions with an expiry date in the last 14 days. Actions which were not activated are still returned. Information from active integrations such as firewalls is not included.

```python
# Get all current and recent actions
actions = antigena.get_actions()

# Get actions requiring confirmation, with full device details
result = antigena.get_actions(fulldevicedetails=True, needconfirming=True)

# Get all actions including cleared ones
actions = antigena.get_actions(includecleared=True)

# Actions created by one model breach, with history
actions = antigena.get_actions(pbid=1234, includehistory=True)

# Time window in epoch milliseconds
actions = antigena.get_actions(
    starttime=1640995200000,
    endtime=1641081600000,
    includecleared=True,
    includeconnections=True
)

# Time window in "YYYY-MM-DD HH:MM:SS" format
actions = antigena.get_actions(
    from_time="2024-01-01 10:00:00",
    to_time="2024-01-01 18:00:00"
)
```

#### Parameters

- `fulldevicedetails` (bool): Returns the full device detail objects for all devices referenced in the response. Alters the response structure (see below)
- `includecleared` (bool): Include actions that have already been cleared (default: false)
- `includehistory` (bool): Add a `history` object to each action describing the states it has been in, when the state changed and the user that triggered the change. Valid states: `created`, `created (requires confirmation)`, `extended`, `cleared`, `reactivated (expired)`, `reactivated (cleared)`
- `needconfirming` (bool): Filter by actions that need (true) or do not need (false) human confirmation
- `starttime` (int): Start time in epoch milliseconds
- `endtime` (int): End time in epoch milliseconds
- `from_time` (str): Start time in `YYYY-MM-DD HH:MM:SS` format (sent to the API as `from`)
- `to_time` (str): End time in `YYYY-MM-DD HH:MM:SS` format (sent to the API as `to`)
- `includeconnections` (bool): Add a `connections` object with the connections blocked by active RESPOND actions
- `responsedata` (str): Name of a single top-level field or object; restricts the returned JSON to only that field or object
- `pbid` (int): Only return actions created as a result of the model breach with this ID
- `did` (int): Only return actions for this device ID

Time parameters must always be specified in pairs (`starttime` with `endtime`, `from_time` with `to_time`). Booleans are sent as lowercase `true`/`false`.

#### Response Structure

By default the response is a list of actions:

```json
[
  {
    "codeid": 4764,
    "did": 316,
    "ip": "10.0.18.224",
    "action": "quarantine",
    "manual": false,
    "triggerer": null,
    "label": "Quarantine device",
    "detail": "",
    "score": 0.3,
    "pbid": 442301,
    "model": "Antigena / Network / External Threat / Antigena Quarantine Example",
    "modeluuid": "d92d6f73-gc1b-cg96-d4g8-df8a79f2a3cd",
    "start": 1582038124000,
    "expires": 1582041724000,
    "blocked": true,
    "agemail": false,
    "aghost": false,
    "active": true,
    "cleared": false
  }
]
```

With `fulldevicedetails=True` the response is a dict instead: actions are in an `actions` array and devices in a `devices` array. With `includeconnections=True` a `connections` array is added (blocked connections with `action`, `label`, `did`, `direction`, `ip`, `port`, `timems`, `time`).

`triggerer` is `null` for actions created automatically by RESPOND. For manual actions it is an object with `username` and `reason`. Manual actions have an empty `model`/`modeluuid` and a `score` of `0`. The API also returns an `updated` field (when the action was last updated, for example by an extension).

### Approve Action

`approve_action(codeid)` is **deprecated**. It is a no-op that sends no request, emits a `DeprecationWarning` and returns a dummy dictionary. To confirm a pending action use `activate_action()`.

### Activate Action

Activate a pending Darktrace RESPOND action (one that requires human confirmation).

```python
# Activate with the model's default duration
result = antigena.activate_action(
    codeid=12345,
    reason="Confirmed threat - activating response"
)

# Activate with a custom duration (10 minutes)
result = antigena.activate_action(
    codeid=12345,
    duration=600,
    reason="Extended monitoring required"
)
```

#### Parameters

- `codeid` (int): Unique numeric identifier of the RESPOND action
- `reason` (str, optional): Free text field specifying the purpose of the change. **Required by the API if the "Audit Antigena" setting is enabled** on the Darktrace System Config page, otherwise requests fail; this applies to all POST methods below. Omitted from the request if empty
- `duration` (int, optional): Duration in seconds. If omitted, the action is activated for the default duration defined by the "Darktrace RESPOND Action Duration" setting on the model

Changes made via the API show the username of the user the API token is associated with in the action history. Requires Darktrace Threat Visualizer 6.0.16 or later.

### Extend Action

Extend an active RESPOND action. The `duration` defines the length the action should cover, not the time to add.

```python
# Set the action to cover a total of 300 seconds
result = antigena.extend_action(
    codeid=12345,
    duration=300,
    reason="Extended monitoring needed"
)
```

#### Parameters

- `codeid` (int): Unique numeric identifier of the RESPOND action
- `duration` (int): Duration in seconds; should be the current duration plus the amount the action should be extended for
- `reason` (str, optional): Free text field for the extension purpose

**Warning**: If an action has 100 seconds remaining, `duration=110` extends it by 10 seconds, whereas `duration=10` reduces the remaining time to 10 seconds so the action expires 90 seconds early.

### Clear Action

Clear an active, pending or expired RESPOND action.

```python
result = antigena.clear_action(
    codeid=12345,
    reason="False positive confirmed"
)
```

#### Parameters

- `codeid` (int): Unique numeric identifier of the RESPOND action
- `reason` (str, optional): Free text field for the clearing purpose

Clearing an active action also suppresses the combination of RESPOND action and model breach conditions for the remainder of the time the action was active for. Clearing an expired action removes it from the returned results unless `includecleared` is used.

### Reactivate Action

Reactivate a cleared or expired RESPOND action.

```python
# Reactivate for 10 minutes
result = antigena.reactivate_action(
    codeid=12345,
    duration=600,
    reason="New evidence requires action"
)
```

#### Parameters

- `codeid` (int): Unique numeric identifier of the RESPOND action
- `duration` (int): Duration for the reactivated action in seconds (required)
- `reason` (str, optional): Free text field for the reactivation purpose

### Create Manual Action

Create manual Darktrace RESPOND/Network actions (Darktrace Threat Visualizer 6+). Sends a POST to `/antigena/manual`.

```python
# Quarantine a device for 10 minutes
result = antigena.create_manual_action(
    did=123,
    action="quarantine",
    duration=600,
    reason="Suspicious device behavior"
)
print(result["code"])

# Block specific connections
result = antigena.create_manual_action(
    did=123,
    action="connection",
    duration=600,
    reason="Block malicious connections",
    connections=[
        {"src": "10.10.10.10", "dst": "8.8.8.8"},
        {"src": "10.10.10.10", "dst": "example.com", "port": 443}
    ]
)
```

#### Parameters

- `did` (int): Identification number of a device modelled in the Darktrace system
- `action` (str): Action type (matches the RESPOND/Network inhibitor):
  - `'connection'`: Block Matching Connections
  - `'pol'`: Enforce pattern of life
  - `'gpol'`: Enforce group pattern of life
  - `'quarantine'`: Quarantine device
  - `'quarantineOutgoing'`: Block all outgoing traffic
  - `'quarantineIncoming'`: Block all incoming traffic
- `duration` (int): Action duration in seconds
- `reason` (str, optional): Free text field for the action purpose. Always sent (empty string by default)
- `connections` (list, optional): Connection pairs to block. Only valid, and only sent by the SDK, for the `'connection'` action:
  - `'src'` (str): Source IP or hostname; must be paired with `dst`
  - `'dst'` (str): Destination IP or hostname; must be paired with `src`
  - `'port'` (int, optional): Port for the `dst` value; must be specified with `dst`

The reason and the username associated with the API token appear in the action history and are returned by `/antigena` as `triggerer.reason` and `triggerer.username`.

#### Response

The API responds with the unique numeric ID of the created action under the key `code`:

```json
{"code": 10170}
```

### Get Summary

Get a simple summary of active and pending RESPOND actions. Without a time window it returns the state of actions now; with a time window it returns information about active actions during that window.

```python
# Current summary
summary = antigena.get_summary()
print(f"Active actions: {summary['activeCount']}")
print(f"Pending actions: {summary['pendingCount']}")

# Summary for a time window
summary = antigena.get_summary(
    starttime=1640995200000,
    endtime=1641081600000
)
```

#### Parameters

- `starttime` (int): Start time in epoch milliseconds
- `endtime` (int): End time in epoch milliseconds
- `responsedata` (str): Name of a single top-level field or object; restricts the returned JSON to only that field or object

Time parameters must always be specified in pairs.

#### Response Structure

```json
{
  "pendingCount": 8,
  "activeCount": 29,
  "pendingActionDevices": [11],
  "activeActionDevices": [123, 551, 202, 6, 1301]
}
```

- `pendingCount` is always 0 when time parameters are given, because historically pending actions are not available.
- `pendingActionDevices` / `activeActionDevices` contain device IDs (`did`); use `/devices` for more information.
- A device may have more than one active or pending action, so action counts may not match the number of impacted devices.
- Only devices with active actions during the window are returned, without when or for how long; query small time periods, or use `/antigena` with `includehistory` for complex queries.

## Examples

### Confirming Pending Actions

Poll the summary for devices with pending actions, then find and activate their pending actions via the history.

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

summary = client.antigena.get_summary()
print(f"{summary['activeCount']} active, {summary['pendingCount']} pending")

for did in summary["pendingActionDevices"]:
    actions = client.antigena.get_actions(did=did, includehistory=True)
    for action in actions:  # a list, as fulldevicedetails is not set
        if action["score"] > 0.9:
            result = client.antigena.activate_action(
                codeid=action["codeid"],
                reason="High confidence threat - auto-activated"
            )
            print(f"Activated {action['codeid']}: {result}")
```

### Extending Expiring Actions

```python
import time

actions = client.antigena.get_actions()

for action in actions:
    if action["active"] and not action["cleared"]:
        remaining = (action["expires"] - int(time.time() * 1000)) / 1000
        if 0 < remaining < 60:
            # duration is the new TOTAL length: remaining time + extension
            client.antigena.extend_action(
                codeid=action["codeid"],
                duration=int(remaining) + 600,
                reason="Automatic extension - investigation ongoing"
            )
```

### Device-Specific Actions

```python
device_actions = client.antigena.get_actions(
    did=123,
    includecleared=True
)

for action in device_actions:
    status = "Active" if action["active"] else "Inactive"
    if action["cleared"]:
        status = "Cleared"
    print(f"Action {action['codeid']}: {status}")
    print(f"  Type: {'Manual' if action['manual'] else 'Automatic'}")
    print(f"  Score: {action['score']}")

if not device_actions:
    result = client.antigena.create_manual_action(
        did=123,
        action="quarantine",
        duration=1800,
        reason="Suspicious device - isolation"
    )
    print(f"Created quarantine action {result['code']}")
```

## Error Handling

```python
import requests

try:
    result = client.antigena.activate_action(codeid=12345, reason="Threat confirmation")
    print(result)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
```

## Notes

### Time Parameters
- `starttime`/`endtime` are epoch milliseconds; `from_time`/`to_time` use `YYYY-MM-DD HH:MM:SS`
- Time parameters must be specified in pairs
- `duration` values are in seconds

### Action States
- `active=true`: the action has been activated, by human confirmation or automatically. An action that expires naturally keeps `active=true`
- `cleared=true`: the action was cleared manually by a user; this also sets `active` to `false`
- `cleared=false`: not cleared manually (includes expired actions)
- `manual=true`: manual RESPOND/Network action

### POST Rules
- Requests are sent as JSON; `activate` and `clear` cannot be combined (the SDK never combines them)
- `reason` is optional unless "Audit Antigena" is enabled, in which case requests fail without it
