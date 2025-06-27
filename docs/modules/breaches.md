# Model Breaches Module

The Model Breaches module provides comprehensive access to model breach alerts in the Darktrace platform. This module allows you to retrieve, acknowledge, comment on, and manage model breach alerts with extensive filtering capabilities.

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

The Model Breaches module provides the following methods:

- **`get()`** - Retrieve model breach alerts with comprehensive filtering
- **`get_comments()`** - Get comments for specific model breach alerts
- **`add_comment()`** - Add comments to model breach alerts
- **`acknowledge()`** - Acknowledge model breach alerts
- **`unacknowledge()`** - Unacknowledge model breach alerts

## Methods

### Get Model Breaches

Retrieve model breach alerts from the Darktrace platform with extensive filtering and customization options.

```python
# Get all model breaches (with defaults)
breaches_data = breaches.get()

# Get breaches with full device details at top level
breaches_data = breaches.get(deviceattop=True)

# Get breaches for specific device with minimal data
device_breaches = breaches.get(
    did=123,
    minimal=True,
    includeacknowledged=False
)

# Get high-score breaches within time range
high_score_breaches = breaches.get(
    minscore=80.0,
    starttime=1640995200000,  # Unix timestamp in milliseconds
    endtime=1641081600000,
    includebreachurl=True
)

# Get breaches using human-readable time format
readable_time_breaches = breaches.get(
    from_time="2024-01-01 10:00:00",
    to_time="2024-01-01 18:00:00",
    expandenums=True
)

# Get SaaS-only breaches with specific platform filter
saas_breaches = breaches.get(
    saasonly=True,
    saasfilter=["Microsoft Office 365", "Google Workspace"]
)

# Get specific breach by ID
specific_breach = breaches.get(pbid=12345)

# Get breaches grouped by device
grouped_breaches = breaches.get(
    group="device",
    includesuppressed=True,
    fulldevicedetails=True
)
```

#### Parameters

- `deviceattop` (bool): Return device JSON at top-level (default: True)
- `did` (int): Device ID to filter by
- `endtime` (int): End time in milliseconds since epoch
- `expandenums` (bool): Expand numeric enums to human-readable strings
- `from_time` (str): Start time in "YYYY-MM-DD HH:MM:SS" format (alternative to starttime)
- `historicmodelonly` (bool): Return only historic model details
- `includeacknowledged` (bool): Include acknowledged breaches in results
- `includebreachurl` (bool): Include breach URLs in response for direct access
- `minimal` (bool): Reduce data returned for performance (default: False)
- `minscore` (float): Minimum breach score filter (0.0-100.0)
- `pbid` (int): Specific breach ID to return (returns single breach)
- `pid` (int): Filter by specific model ID
- `starttime` (int): Start time in milliseconds since epoch
- `to_time` (str): End time in "YYYY-MM-DD HH:MM:SS" format (alternative to endtime)
- `uuid` (str): Filter by model UUID
- `responsedata` (str): Restrict response to specific top-level fields
- `saasonly` (bool): Return only SaaS-related breaches
- `group` (str): Group results (e.g., 'device')
- `includesuppressed` (bool): Include suppressed breaches
- `saasfilter` (str or list): Filter by SaaS platform(s) - can be single string or list
- `creationtime` (bool): Use creation time instead of detection time for filtering
- `fulldevicedetails` (bool): Return complete device/component information

#### Notes

- Time parameters (`starttime`/`endtime` or `from_time`/`to_time`) must be specified in pairs
- When `minimal=true`, response data is significantly reduced for performance
- Multiple `saasfilter` values can be provided as a list for OR filtering
- The API response structure varies based on parameters like `deviceattop` and `group`

### Get Comments

Retrieve comments for a specific model breach alert.

```python
# Get all comments for a breach
comments = breaches.get_comments(pbid=12345)

# Get comments with restricted response data
comments = breaches.get_comments(
    pbid=12345,
    responsedata="comments"
)
```

#### Parameters

- `pbid` (int): Policy breach ID of the model breach (required)
- `responsedata` (str, optional): Restrict response to specific fields

#### Response

Returns a list of comment objects with details like author, timestamp, and message content.

### Add Comment

Add a comment to a model breach alert.

```python
# Add a comment to a breach
success = breaches.add_comment(
    pbid=12345,
    message="Investigated - appears to be false positive due to legitimate admin activity"
)

if success:
    print("Comment added successfully")
else:
    print("Failed to add comment")
```

#### Parameters

- `pbid` (int): Policy breach ID of the model breach (required)
- `message` (str): The comment text to add (required)

### Acknowledge Breach

Acknowledge a model breach alert to mark it as reviewed.

```python
# Acknowledge a breach
success = breaches.acknowledge(pbid=12345)

if success:
    print("Breach acknowledged successfully")
else:
    print("Failed to acknowledge breach")
```

#### Parameters

- `pbid` (int): Policy breach ID of the model breach (required)

### Unacknowledge Breach

Unacknowledge a previously acknowledged model breach alert.

```python
# Unacknowledge a breach
success = breaches.unacknowledge(pbid=12345)

if success:
    print("Breach unacknowledged successfully")
else:
    print("Failed to unacknowledge breach")
```

#### Parameters

- `pbid` (int): Policy breach ID of the model breach (required)
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

### Complete Breach Management Workflow

```python
from darktrace import DarktraceClient
import time

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get high-priority unacknowledged breaches
high_priority_breaches = client.breaches.get(
    minscore=80.0,
    includeacknowledged=False,
    includebreachurl=True,
    expandenums=True
)

for breach in high_priority_breaches:
    pbid = breach.get('pbid')
    score = breach.get('score', 0)
    model_name = breach.get('model', {}).get('name', 'Unknown')
    
    print(f"Analyzing breach {pbid}: {model_name} (score: {score})")
    
    # Get existing comments
    comments = client.breaches.get_comments(pbid)
    print(f"Existing comments: {len(comments)}")
    
    # Add analysis comment
    client.breaches.add_comment(
        pbid=pbid,
        message=f"Auto-analysis: High-priority breach detected at {time.ctime()}"
    )
    
    # Auto-acknowledge low-confidence high-score breaches
    if 80 <= score < 90:
        client.breaches.acknowledge(pbid)
        client.breaches.add_comment(
            pbid=pbid,
            message="Auto-acknowledged: Medium confidence breach"
        )
        print(f"Auto-acknowledged breach {pbid}")
```

### SaaS Security Monitoring

```python
# Monitor SaaS breaches across multiple platforms
saas_platforms = ["Microsoft Office 365", "Google Workspace", "Salesforce"]

saas_breaches = client.breaches.get(
    saasonly=True,
    saasfilter=saas_platforms,
    minscore=50.0,
    includeacknowledged=False,
    from_time="2024-01-01 00:00:00",
    to_time="2024-01-31 23:59:59"
)

# Group by platform for analysis
platform_stats = {}
for breach in saas_breaches:
    # Extract SaaS platform info from breach data
    platform = breach.get('device', {}).get('hostname', 'Unknown')
    
    if platform not in platform_stats:
        platform_stats[platform] = {'count': 0, 'total_score': 0}
    
    platform_stats[platform]['count'] += 1
    platform_stats[platform]['total_score'] += breach.get('score', 0)

# Report platform risk
for platform, stats in platform_stats.items():
    avg_score = stats['total_score'] / stats['count'] if stats['count'] > 0 else 0
    print(f"{platform}: {stats['count']} breaches, avg score: {avg_score:.1f}")
```

### Device-Specific Incident Investigation

```python
# Investigate specific device
device_id = 123
device_breaches = client.breaches.get(
    did=device_id,
    includeacknowledged=True,
    includesuppressed=True,
    fulldevicedetails=True,
    group="device"
)

print(f"Breaches for device {device_id}:")
for breach in device_breaches:
    pbid = breach.get('pbid')
    model_name = breach.get('model', {}).get('name', 'Unknown')
    acknowledged = breach.get('acknowledged', False)
    suppressed = breach.get('suppressed', False)
    
    status = []
    if acknowledged:
        status.append("ACK")
    if suppressed:
        status.append("SUPP")
    
    status_str = f" [{', '.join(status)}]" if status else ""
    print(f"  {pbid}: {model_name} (score: {breach.get('score', 0)}){status_str}")
    
    # Get comments for context
    comments = client.breaches.get_comments(pbid)
    if comments:
        print(f"    Latest comment: {comments[-1].get('message', '')[:50]}...")

# Add investigation summary
investigation_summary = f"""
Device investigation completed:
- Total breaches: {len(device_breaches)}
- Investigation date: {time.ctime()}
- Analyst: Automated System
"""

if device_breaches:
    # Add summary to the most recent breach
    latest_breach = max(device_breaches, key=lambda x: x.get('time', 0))
    client.breaches.add_comment(
        pbid=latest_breach.get('pbid'),
        message=investigation_summary
    )
```

### Time-Based Trend Analysis

```python
import datetime

# Get breaches from the last 7 days
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=7)

weekly_breaches = client.breaches.get(
    from_time=start_time.strftime("%Y-%m-%d %H:%M:%S"),
    to_time=end_time.strftime("%Y-%m-%d %H:%M:%S"),
    minimal=False,
    expandenums=True
)

# Analyze trends
daily_counts = {}
score_distribution = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}

for breach in weekly_breaches:
    # Daily trend
    breach_date = datetime.datetime.fromtimestamp(
        breach.get('time', 0) / 1000
    ).strftime('%Y-%m-%d')
    
    daily_counts[breach_date] = daily_counts.get(breach_date, 0) + 1
    
    # Score distribution
    score = breach.get('score', 0)
    if score < 25:
        score_distribution['low'] += 1
    elif score < 50:
        score_distribution['medium'] += 1
    elif score < 75:
        score_distribution['high'] += 1
    else:
        score_distribution['critical'] += 1

print("Daily breach counts:")
for date, count in sorted(daily_counts.items()):
    print(f"  {date}: {count}")

print(f"\nScore distribution:")
for category, count in score_distribution.items():
    print(f"  {category}: {count}")
```

## Error Handling

```python
try:
    # Attempt to get breaches
    breaches_data = client.breaches.get(
        minscore=50.0,
        includeacknowledged=False
    )
    
    # Process each breach
    for breach in breaches_data:
        pbid = breach.get('pbid')
        
        # Attempt to add comment
        success = client.breaches.add_comment(
            pbid=pbid,
            message="Automated processing"
        )
        
        if not success:
            print(f"Failed to add comment to breach {pbid}")
            
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
        
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Response Structure Examples

### Basic Breach Object

```python
{
  "pbid": 12345,
  "score": 85.5,
  "time": 1641038400000,
  "acknowledged": false,
  "suppressed": false,
  "model": {
    "name": "Device / Anomalous Connection",
    "uuid": "model-uuid-here",
    "pid": 67
  },
  "device": {
    "did": 123,
    "hostname": "server01",
    "ip": "192.168.1.100"
  },
  "connectionDetails": {...},
  "url": "https://darktrace.instance/modelbreaches/12345"
}
```

### Comment Object

```python
{
  "id": 456,
  "message": "Investigated - legitimate activity",
  "author": "analyst@company.com",
  "timestamp": 1641042000000,
  "edited": false
}
```

## Notes

### Time Handling
- All timestamps are Unix timestamps in milliseconds
- Time parameters must be specified in pairs (`starttime`/`endtime` or `from_time`/`to_time`)
- Human-readable format: "YYYY-MM-DD HH:MM:SS"

### Performance Considerations
- Use `minimal=true` for large datasets to reduce response size
- Consider using `responsedata` parameter to limit returned fields
- Time-based filtering is more efficient than post-processing large datasets

### SaaS Filtering
- `saasfilter` accepts single platform or list of platforms
- `saasonly=true` restricts results to SaaS breaches only
- Common platforms: "Microsoft Office 365", "Google Workspace", "Salesforce", "AWS", "Azure"

### Data Structure Variations
- `deviceattop=true` (default) includes device data in each breach object
- `group="device"` groups breaches by device
- `fulldevicedetails=true` provides complete device information
- `expandenums=true` converts numeric codes to human-readable strings

### Acknowledgment States
- Acknowledged breaches are excluded by default unless `includeacknowledged=true`
- Suppressed breaches require `includesuppressed=true` to be included
- Use `acknowledge()` and `unacknowledge()` to manage breach states