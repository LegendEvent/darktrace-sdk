# Model Breaches Module

The Model Breaches module provides access to model breach alerts in the Darktrace platform, allowing you to retrieve, acknowledge, and comment on alerts.

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

## Methods

### Get Model Breaches

Retrieve model breach alerts from the Darktrace platform.

```python
# Get all model breaches (default limit is usually 100)
all_breaches = breaches.get()

# Get a specific number of breaches
recent_breaches = breaches.get(count=10)

# Get breaches with specific parameters
filtered_breaches = breaches.get(
    count=50,           # Number of breaches to return
    offset=0,           # Starting offset
    hostname="server*", # Filter by hostname (supports wildcards)
    ip="192.168.1.*",   # Filter by IP address (supports wildcards)
    model="Device / Anomalous Connection*", # Filter by model name
    acknowledged=False, # Filter by acknowledgment status
    min_score=80,       # Filter by minimum score
    max_score=100,      # Filter by maximum score
    start_time="2023-06-01T00:00:00Z", # Filter by start time
    end_time="2023-06-15T23:59:59Z"    # Filter by end time
)
```

#### Parameters

- `count` (int, optional): Number of breaches to return
- `offset` (int, optional): Starting offset for pagination
- `hostname` (str, optional): Filter by hostname (supports wildcards)
- `ip` (str, optional): Filter by IP address (supports wildcards)
- `model` (str, optional): Filter by model name (supports wildcards)
- `acknowledged` (bool, optional): Filter by acknowledgment status
- `min_score` (int, optional): Filter by minimum score
- `max_score` (int, optional): Filter by maximum score
- `start_time` (str, optional): Filter by start time (ISO format)
- `end_time` (str, optional): Filter by end time (ISO format)
- `pbid` (int, optional): Get a specific breach by ID

#### Response

```json
{
  "modelbreaches": [
    {
      "pbid": 12345,
      "did": 123,
      "hostname": "server01",
      "ip": "192.168.1.100",
      "score": 85,
      "time": "2023-06-15T10:11:12Z",
      "acknowledged": false,
      "model": {
        "name": "Device / Anomalous Connection / External Destination",
        "uuid": "12345678-1234-1234-1234-123456789012"
      },
      "comment_count": 2
    },
    // ... more breaches
  ]
}
```

### Get Comments

Retrieve comments for a specific model breach alert.

```python
# Get comments for a breach
comments = breaches.get_comments(pbid=12345)
```

#### Parameters

- `pbid` (int, required): The breach ID to get comments for

#### Response

```json
{
  "comments": [
    {
      "id": 1,
      "pbid": 12345,
      "message": "Investigating this alert",
      "timestamp": "2023-06-15T10:30:00Z",
      "username": "analyst1"
    },
    {
      "id": 2,
      "pbid": 12345,
      "message": "False positive - known behavior",
      "timestamp": "2023-06-15T11:15:00Z",
      "username": "analyst2"
    }
  ]
}
```

### Add Comment

Add a comment to a model breach alert.

```python
# Add a comment to a breach
success = breaches.add_comment(
    pbid=12345,
    message="Investigating this suspicious connection"
)
```

#### Parameters

- `pbid` (int, required): The breach ID to add a comment to
- `message` (str, required): The comment message to add

#### Response

Returns `True` if the comment was added successfully, `False` otherwise.

### Acknowledge

Acknowledge a model breach alert.

```python
# Acknowledge a breach
success = breaches.acknowledge(pbid=12345)
```

#### Parameters

- `pbid` (int, required): The breach ID to acknowledge

#### Response

Returns `True` if the breach was acknowledged successfully, `False` otherwise.

### Unacknowledge

Unacknowledge a previously acknowledged model breach alert.

```python
# Unacknowledge a breach
success = breaches.unacknowledge(pbid=12345)
```

#### Parameters

- `pbid` (int, required): The breach ID to unacknowledge

#### Response

Returns `True` if the breach was unacknowledged successfully, `False` otherwise.

## Examples

### Get High-Scoring Breaches

```python
# Get all breaches with a score of 80 or higher
high_score_breaches = client.breaches.get(min_score=80)
print(f"Found {len(high_score_breaches.get('modelbreaches', []))} high-scoring breaches")

# Print details of each high-scoring breach
for breach in high_score_breaches.get("modelbreaches", []):
    print(f"Breach ID: {breach.get('pbid')}")
    print(f"Device: {breach.get('hostname')} ({breach.get('ip')})")
    print(f"Score: {breach.get('score')}")
    print(f"Model: {breach.get('model', {}).get('name')}")
    print(f"Time: {breach.get('time')}")
    print(f"Acknowledged: {breach.get('acknowledged')}")
    print("---")
```

### Acknowledge and Comment on a Breach

```python
breach_id = 12345

# Acknowledge the breach
ack_success = client.breaches.acknowledge(pbid=breach_id)
if ack_success:
    print(f"Successfully acknowledged breach {breach_id}")
else:
    print(f"Failed to acknowledge breach {breach_id}")

# Add a comment explaining the acknowledgment
comment_success = client.breaches.add_comment(
    pbid=breach_id,
    message="Acknowledged - investigating this alert as part of incident #5678"
)
if comment_success:
    print(f"Successfully added comment to breach {breach_id}")
else:
    print(f"Failed to add comment to breach {breach_id}")
```

### Review Comments on a Breach

```python
breach_id = 12345

# Get comments for the breach
comments_data = client.breaches.get_comments(pbid=breach_id)
comments = comments_data.get("comments", [])

print(f"Found {len(comments)} comments for breach {breach_id}:")
for comment in comments:
    print(f"[{comment.get('timestamp')}] {comment.get('username')}: {comment.get('message')}")
```

## Error Handling

```python
try:
    breaches_data = client.breaches.get(min_score=90)
    # Process the breaches
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
``` 