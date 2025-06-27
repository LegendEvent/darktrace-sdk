# Antigena Module

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

- **`get_actions()`** - Retrieve current and past RESPOND actions with comprehensive filtering
- **`activate_action()`** - Activate pending RESPOND actions
- **`extend_action()`** - Extend active RESPOND actions
- **`clear_action()`** - Clear active, pending or expired actions
- **`reactivate_action()`** - Reactivate cleared or expired actions
- **`create_manual_action()`** - Create manual RESPOND/Network actions
- **`get_summary()`** - Get summary of active and pending actions

## Methods

### Get Actions

Retrieve information about current and past Darktrace RESPOND actions. If no time window is specified, returns all current actions with a future expiry date and all historic actions with an expiry date in the last 14 days.

```python
# Get all current and recent actions
actions = antigena.get_actions()

# Get actions with full device details
actions = antigena.get_actions(fulldevicedetails=True)

# Get all actions including cleared ones
actions = antigena.get_actions(includecleared=True)

# Get actions requiring confirmation
pending_actions = antigena.get_actions(needconfirming=True)

# Get actions for specific device with history
device_actions = antigena.get_actions(
    did=123,
    includehistory=True,
    includeconnections=True
)

# Get actions within time range
time_filtered = antigena.get_actions(
    starttime=1640995200000,  # Unix timestamp in milliseconds
    endtime=1641081600000,
    includecleared=True
)

# Get actions using human-readable time format
readable_time = antigena.get_actions(
    from_time="2024-01-01 10:00:00",
    to_time="2024-01-01 18:00:00"
)
```

#### Parameters

- `fulldevicedetails` (bool): Returns full device detail objects for all referenced devices. Alters JSON structure to include separate `actions` and `devices` objects
- `includecleared` (bool): Include already cleared RESPOND actions (default: False)
- `includehistory` (bool): Include additional history information about action state (creation, extension times)
- `needconfirming` (bool): Filter by actions requiring human confirmation (True) or not requiring confirmation (False)
- `endtime` (int): End time in millisecond format (Unix timestamp)
- `from_time` (str): Start time in "YYYY-MM-DD HH:MM:SS" format (alternative to starttime)
- `starttime` (int): Start time in millisecond format (Unix timestamp)
- `to_time` (str): End time in "YYYY-MM-DD HH:MM:SS" format (alternative to endtime)
- `includeconnections` (bool): Add connections object showing connections blocked by actions
- `responsedata` (str): Restrict returned JSON to specific top-level field or object
- `pbid` (int): Return only actions created by model breach with specified ID
- `did` (int): Filter actions for specific device ID

#### Response Structure

```python
# With fulldevicedetails=False (default)
{
  "actions": [
    {
      "code": 12345,
      "active": true,
      "cleared": false,
      "manual": false,
      "aiaScore": 95,
      "did": 123,
      "device": {...},
      "triggerer": {
        "username": "user@example.com",
        "reason": "Suspicious activity detected"
      },
      "created": 1641038400000,
      "expires": 1641042000000
    }
  ]
}

# With fulldevicedetails=True
{
  "actions": [...],
  "devices": {...}
}
```
- `ip` (str, optional): Filter by IP address (supports wildcards)
- `codeid` (int, optional): Get a specific action by its code ID

#### Response

```json
{
  "actions": [
    {
      "codeid": 12345,
      "did": 123,
      "hostname": "server01",
      "ip": "192.168.1.100",
      "action": "breachblock",
      "status": "active",
      "created": "2023-06-15T10:11:12Z",
      "expires": "2023-06-15T11:11:12Z",
      "reason": "Suspicious outbound connection",
      "pbid": 67890,
      "model": {
        "name": "Device / Anomalous Connection / External Destination",
        "uuid": "12345678-1234-1234-1234-123456789012"
      }
    },
    // ... more actions
  ]
}
```

### Approve Action

Approve/activate a pending Antigena action.

```python
# Approve an action
success = antigena.approve_action(
    code_id=12345,           # Action code ID (required)
    reason="Manually approved", # Reason for approval (optional)
    duration=3600            # Duration in seconds (optional, default is indefinite)
)
```

#### Parameters

- `code_id` (int, required): The action code ID to approve
- `reason` (str, optional): Reason for approving the action
- `duration` (int, optional): Duration in seconds for the action (0 = indefinite)

#### Response

Returns `True` if the approval was successful, `False` otherwise.

### Activate Action

Activate a pending Darktrace RESPOND action. Changes the state from pending to active.

```python
# Activate with default duration
success = antigena.activate_action(
    codeid=12345,
    reason="Confirmed threat - activating response"
)

# Activate with custom duration (10 minutes)
success = antigena.activate_action(
    codeid=12345,
    duration=600,
    reason="Extended monitoring required"
)
```

#### Parameters

- `codeid` (int): Unique numeric identifier of the RESPOND action
- `reason` (str, optional): Free text field specifying action purpose (required if "Audit Antigena" is enabled)
- `duration` (int, optional): Duration in seconds (uses model default if not specified)

#### Response

Returns `True` if the activation was successful, `False` otherwise.

### Extend Action

Extend an active Darktrace RESPOND action. The duration defines the new total length the action should cover.

```python
# Extend action to run for total of 300 seconds
success = antigena.extend_action(
    codeid=12345,
    duration=300,
    reason="Extended monitoring needed"
)
```

#### Parameters

- `codeid` (int): Unique numeric identifier of the RESPOND action
- `duration` (int): New total duration in seconds (not additional time)
- `reason` (str, optional): Free text field for extension purpose

**Warning**: The duration parameter sets the total action length, not additional time. If an action has 100 seconds remaining and you specify duration=110, it extends by 10 seconds. If you specify duration=10, it reduces to 10 seconds remaining.

#### Response

Returns `True` if the extension was successful, `False` otherwise.

### Clear Action

Clear an active, pending, or expired Darktrace RESPOND action.

```python
# Clear an action
success = antigena.clear_action(
    codeid=12345,
    reason="False positive confirmed"
)
```

#### Parameters

- `codeid` (int): Unique numeric identifier of the RESPOND action
- `reason` (str, optional): Free text field for clearing purpose

#### Response

Returns `True` if the clearing was successful, `False` otherwise.

### Reactivate Action

Reactivate a cleared or expired Darktrace RESPOND action.

```python
# Reactivate a cleared action for 10 minutes
success = antigena.reactivate_action(
    codeid=12345,
    duration=600,
    reason="New evidence requires action"
)
```

#### Parameters

- `codeid` (int): Unique numeric identifier of the RESPOND action
- `duration` (int): Duration for reactivated action in seconds (required)
- `reason` (str, optional): Free text field for reactivation purpose

#### Response

Returns `True` if the reactivation was successful, `False` otherwise.

### Create Manual Action

Create manual Darktrace RESPOND/Network actions. Available from Darktrace Threat Visualizer 6+.

```python
# Create quarantine action
codeid = antigena.create_manual_action(
    did=123,
    action="quarantine",
    duration=600,
    reason="Suspicious device behavior"
)

# Create connection blocking action
codeid = antigena.create_manual_action(
    did=123,
    action="connection",
    duration=600,
    reason="Block malicious connections",
    connections=[
        {"src": "10.10.10.10", "dst": "8.8.8.8"},
        {"src": "10.10.10.10", "dst": "malicious.com", "port": 443}
    ]
)

# Enforce pattern of life
codeid = antigena.create_manual_action(
    did=123,
    action="pol",
    duration=1800,
    reason="Unusual behavior detected"
)
```

#### Parameters

- `did` (int): Device ID for the target device
- `action` (str): Action type:
  - `'connection'`: Block Matching Connections
  - `'pol'`: Enforce pattern of life
  - `'gpol'`: Enforce group pattern of life  
  - `'quarantine'`: Quarantine device
  - `'quarantineOutgoing'`: Block all outgoing traffic
  - `'quarantineIncoming'`: Block all incoming traffic
- `duration` (int): Action duration in seconds
- `reason` (str, optional): Free text field for action purpose
- `connections` (list, optional): Connection pairs to block (only for 'connection' action):
  - `'src'` (str): Source IP or hostname
  - `'dst'` (str): Destination IP or hostname
  - `'port'` (int, optional): Destination port

#### Returns

Returns the `codeid` (unique numeric ID) of the created action, or 0 if creation failed.

### Get Summary

Get a summary of active and pending Darktrace RESPOND actions.

```python
# Get current summary
summary = antigena.get_summary()
print(f"Active actions: {summary['activeCount']}")
print(f"Pending actions: {summary['pendingCount']}")

# Get summary for specific time window
summary = antigena.get_summary(
    starttime=1640995200000,
    endtime=1641081600000
)
```

#### Parameters

- `endtime` (int): End time in millisecond format (Unix timestamp)
- `starttime` (int): Start time in millisecond format (Unix timestamp)
- `responsedata` (str): Restrict returned JSON to specific field or object

#### Response Structure

```python
{
  "pendingCount": 3,
  "activeCount": 7,
  "pendingActionDevices": [123, 456, 789],
  "activeActionDevices": [111, 222, 333, 444, 555, 666, 777]
}
```

## Examples

### Complete Action Management Workflow

```python
from darktrace import DarktraceClient
import time

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get summary of current state
summary = client.antigena.get_summary()
print(f"Current state: {summary['activeCount']} active, {summary['pendingCount']} pending")

# Get pending actions requiring confirmation
pending_actions = client.antigena.get_actions(
    needconfirming=True,
    includehistory=True
)

for action in pending_actions.get('actions', []):
    codeid = action.get('code')
    device_id = action.get('did')
    score = action.get('aiaScore', 0)
    
    print(f"Reviewing action {codeid} for device {device_id} (score: {score})")
    
    # Activate high-score actions automatically
    if score > 90:
        success = client.antigena.activate_action(
            codeid=codeid,
            reason="High confidence threat - auto-activated"
        )
        print(f"Auto-activated action {codeid}: {success}")
    
    # Create manual quarantine for suspicious devices
    elif score > 70:
        manual_codeid = client.antigena.create_manual_action(
            did=device_id,
            action="quarantine",
            duration=300,  # 5 minutes
            reason="Preventive quarantine pending investigation"
        )
        print(f"Created manual quarantine {manual_codeid}")

# Monitor active actions
active_actions = client.antigena.get_actions(
    needconfirming=False,
    includeconnections=True
)

for action in active_actions.get('actions', []):
    if action.get('active') and not action.get('cleared'):
        expires = action.get('expires', 0)
        remaining = (expires - int(time.time() * 1000)) / 1000
        
        print(f"Action {action.get('code')} expires in {remaining:.0f} seconds")
        
        # Extend actions that are about to expire
        if remaining < 60:  # Less than 1 minute
            client.antigena.extend_action(
                codeid=action.get('code'),
                duration=600,  # Extend to 10 minutes total
                reason="Automatic extension - investigation ongoing"
            )
```

### Device-Specific Action Management

```python
# Monitor specific device
device_id = 123
device_actions = client.antigena.get_actions(
    did=device_id,
    includecleared=True,
    includehistory=True
)

print(f"Actions for device {device_id}:")
for action in device_actions.get('actions', []):
    status = "Active" if action.get('active') else "Inactive"
    if action.get('cleared'):
        status = "Cleared"
    
    print(f"  Action {action.get('code')}: {status}")
    print(f"    Type: {'Manual' if action.get('manual') else 'Automatic'}")
    print(f"    Score: {action.get('aiaScore', 'N/A')}")

# Create comprehensive response for suspicious device
if len(device_actions.get('actions', [])) == 0:
    # No existing actions - create quarantine
    codeid = client.antigena.create_manual_action(
        did=device_id,
        action="quarantine",
        duration=1800,  # 30 minutes
        reason="Suspicious device - comprehensive isolation"
    )
    print(f"Created quarantine action {codeid}")
```

## Error Handling

```python
try:
    # Attempt to activate action
    success = client.antigena.activate_action(
        codeid=12345,
        reason="Threat confirmation"
    )
    
    if success:
        print("Action activated successfully")
    else:
        print("Failed to activate action - check permissions and action state")
        
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
        
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Time Parameters
- All timestamp parameters expect Unix timestamps in milliseconds
- Time parameters (`starttime`/`endtime` or `from_time`/`to_time`) must be specified in pairs
- Human-readable time format: "YYYY-MM-DD HH:MM:SS"

### Action States
- `active=true`: Action has been activated (by confirmation or automatically)
- `cleared=true`: Action manually cleared by user
- `cleared=false`: Action expired naturally
- `manual=true`: Manual RESPOND/Network action

### Special Behaviors
- Actions without time windows return current actions + 14 days of history
- Clearing active actions suppresses action/breach combinations for remaining duration
- Full device details alter JSON structure to separate `actions` and `devices` objects
- Manual actions appear with triggerer username and reason in action history

### Action Types
Available manual action types:
- **connection**: Block specific connections
- **pol**: Enforce individual device pattern of life
- **gpol**: Enforce group pattern of life
- **quarantine**: Complete device isolation
- **quarantineOutgoing**: Block outbound traffic only
- **quarantineIncoming**: Block inbound traffic only