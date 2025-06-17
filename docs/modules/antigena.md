# Antigena Module

The Antigena module provides access to Darktrace's Antigena functionality, which includes automated and manual response actions.

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

## Methods

### Get Actions

Retrieve information about current and past Antigena actions.

```python
# Get all Antigena actions (default limit is usually 100)
all_actions = antigena.get_actions()

# Get a specific number of actions
recent_actions = antigena.get_actions(count=10)

# Get actions with specific parameters
filtered_actions = antigena.get_actions(
    count=50,           # Number of actions to return
    offset=0,           # Starting offset
    status="active",    # Filter by status (active, pending, expired, cleared)
    did=123,            # Filter by device ID
    hostname="server*", # Filter by hostname (supports wildcards)
    ip="192.168.1.*",   # Filter by IP address (supports wildcards)
)
```

#### Parameters

- `count` (int, optional): Number of actions to return
- `offset` (int, optional): Starting offset for pagination
- `status` (str, optional): Filter by action status (active, pending, expired, cleared)
- `did` (int, optional): Filter by device ID
- `hostname` (str, optional): Filter by hostname (supports wildcards)
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

### Extend Action

Extend an active Antigena action.

```python
# Extend an action
success = antigena.extend_action(
    code_id=12345,           # Action code ID (required)
    duration=3600,           # New duration in seconds (required)
    reason="Extended due to ongoing investigation" # Reason for extension (optional)
)
```

#### Parameters

- `code_id` (int, required): The action code ID to extend
- `duration` (int, required): New duration in seconds for the action
- `reason` (str, optional): Reason for extending the action

#### Response

Returns `True` if the extension was successful, `False` otherwise.

### Clear Action

Clear an active, pending, or expired Antigena action.

```python
# Clear an action
success = antigena.clear_action(
    code_id=12345,           # Action code ID (required)
    reason="Threat mitigated" # Reason for clearing (optional)
)
```

#### Parameters

- `code_id` (int, required): The action code ID to clear
- `reason` (str, optional): Reason for clearing the action

#### Response

Returns `True` if the clearing was successful, `False` otherwise.

### Reactivate Action

Reactivate a cleared or expired Antigena action.

```python
# Reactivate an action
success = antigena.reactivate_action(
    code_id=12345,           # Action code ID (required)
    duration=3600,           # Duration in seconds (required)
    reason="Threat still present" # Reason for reactivation (optional)
)
```

#### Parameters

- `code_id` (int, required): The action code ID to reactivate
- `duration` (int, required): Duration in seconds for the reactivated action
- `reason` (str, optional): Reason for reactivating the action

#### Response

Returns `True` if the reactivation was successful, `False` otherwise.

### Create Manual Action

Create a manual Antigena action for a device.

```python
# Create a manual action to block all traffic
action_id = antigena.create_manual_action(
    did=123,                # Device ID (required)
    action="breachblock",   # Action type (required)
    duration=3600,          # Duration in seconds (required)
    reason="Suspicious activity detected" # Reason (optional)
)

# Create a manual action to block specific connections
action_id = antigena.create_manual_action(
    did=123,
    action="connection",
    duration=3600,
    reason="Blocking suspicious connections",
    connections=[
        {"ip": "10.0.0.1", "port": 443, "proto": "tcp"},
        {"ip": "10.0.0.2", "port": 80, "proto": "tcp"}
    ]
)
```

#### Parameters

- `did` (int, required): The device ID to apply the action to
- `action` (str, required): The type of action to apply (breachblock, slowdown, connection)
- `duration` (int, required): Duration in seconds for the action
- `reason` (str, optional): Reason for creating the action
- `connections` (list, optional): List of connections to block (required when action='connection')

#### Response

Returns the code ID of the created action if successful, 0 otherwise.

### Get Summary

Get a summary of active and pending Antigena actions.

```python
# Get summary of all Antigena actions
summary = antigena.get_summary()
```

#### Parameters

None

#### Response

```json
{
  "summary": {
    "active": 5,
    "pending": 2,
    "total": 7,
    "actions": {
      "breachblock": 3,
      "slowdown": 2,
      "connection": 2
    }
  }
}
```

## Examples

### Get Active Antigena Actions

```python
active_actions = client.antigena.get_actions(status="active")
for action in active_actions.get("actions", []):
    print(f"Action ID: {action.get('codeid')}, Type: {action.get('action')}, Device: {action.get('hostname')}")
```

### Approve a Pending Action

```python
action_id = 12345
success = client.antigena.approve_action(
    code_id=action_id,
    reason="Manually approved after review",
    duration=7200  # 2 hours
)
if success:
    print(f"Successfully approved action {action_id}")
else:
    print(f"Failed to approve action {action_id}")
```

### Create a Manual Block Action

```python
device_id = 123
action_id = client.antigena.create_manual_action(
    did=device_id,
    action="breachblock",
    duration=3600,  # 1 hour
    reason="Manual block due to suspicious activity"
)
if action_id > 0:
    print(f"Successfully created manual action with ID {action_id}")
else:
    print("Failed to create manual action")
```

## Error Handling

```python
try:
    actions = client.antigena.get_actions()
    # Process the actions
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
``` 