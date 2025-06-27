# AI Analyst Module

The AI Analyst module provides comprehensive access to Darktrace's AI Analyst endpoints including incidents, investigations, groups, statistics, and comments. This module has been enhanced with full parameter support based on the official API documentation.

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

The AI Analyst module provides the following methods:

- **`get_incident_events()`** - Get AI Analyst incident events with comprehensive filtering
- **`get_groups()`** - Get AI Analyst incident groups 
- **`get_investigations()`** - Get AI Analyst investigations
- **`create_investigation()`** - Create new AI Analyst investigations
- **`get_stats()`** - Get AI Analyst statistics
- **`get_comments()`** - Get comments for specific incidents
- **`add_comment()`** - Add comments to incidents
- **`acknowledge()`** - Acknowledge incident events
- **`unacknowledge()`** - Unacknowledge incident events
- **`pin()`** - Pin incident events
- **`unpin()`** - Unpin incident events
- **`acknowledge()`** - Acknowledge incident events
- **`unacknowledge()`** - Unacknowledge incident events

## Enhanced Methods

### 1. get_incident_events(**params)

Get AI Analyst incident events with comprehensive parameter support.

```python
# Basic usage
events = client.analyst.get_incident_events()

# Get high-score critical events from last 24 hours
import time
yesterday = int((time.time() - 24*60*60) * 1000)
now = int(time.time() * 1000)

events = client.analyst.get_incident_events(
    starttime=yesterday,
    endtime=now,
    minscore=80,
    groupcritical=True,
    includeacknowledged=False
)
```

#### Parameters

- `includeacknowledged` (bool): Include acknowledged events in the data
- `includeallpinned` (bool): True by default. Controls whether pinned events are returned
- `includeonlypinned` (bool): False by default. Used to only return pinned incident events
- `includeincidenteventurl` (bool): Controls whether links to events are included in the response
- `locale` (str): Language for returned strings (de_DE, en_GB, en_US, es_ES, es_419, fr_FR, it_IT, ja_JP, ko_KR, pt_BR, zh_Hans, zh_Hant)
- `endtime` (int): End time in millisecond format, relative to midnight January 1st 1970 UTC
- `starttime` (int): Start time in millisecond format, relative to midnight January 1st 1970 UTC
- `groupcompliance` (bool): Return only events that are part of incidents with "compliance" behavior category
- `groupsuspicious` (bool): Return only events that are part of incidents with "suspicious" behavior category
- `groupcritical` (bool): Return only events that are part of incidents with "critical" behavior category
- `maxscore` (int): Maximum score an event can possess (0-100)
- `minscore` (int): Minimum score an event can possess (0-100)
- `maxgroupscore` (int): Maximum incident score for the incident (0-100)
- `mingroupscore` (int): Minimum incident score for the incident (0-100)
- `did` (int): Device ID to include incident events for
- `excludedid` (int): Device ID to exclude incident events for
- `sid` (int): Subnet ID to include incident events for
- `excludesid` (int): Subnet ID to exclude incident events for
- `master` (int): Master instance ID under Unified View
- `saasonly` (bool): Restricts returned events to only those with SaaS activity
- `groupid` (str): Unique identifier of an AI Analyst incident
- `uuid` (str): Unique identifier of an AI Analyst incident event

### 2. get_groups(**params)

Get AI Analyst incident groups with comprehensive filtering.

```python
# Basic usage
groups = client.analyst.get_groups()

# Get critical SaaS-related incidents with score above 90
groups = client.analyst.get_groups(
    groupcritical=True,
    saasonly=True,
    minscore=90,
    includeacknowledged=False
)
```

#### Parameters

- `includeacknowledged` (bool): Include acknowledged events in the data
- `includeonlypinned` (bool): False by default. Used to only return pinned incident events
- `locale` (str): Language for returned strings
- `endtime` (int): End time in millisecond format
- `starttime` (int): Start time in millisecond format
- `groupcompliance` (bool): Return only events with "compliance" behavior category
- `groupsuspicious` (bool): Return only events with "suspicious" behavior category
- `groupcritical` (bool): Return only events with "critical" behavior category
- `maxscore` (int): Maximum score an incident can possess (0-100)
- `minscore` (int): Minimum score an incident can possess (0-100)
- `did` (int): Device ID to include incident events for
- `excludedid` (int): Device ID to exclude incident events for
- `sid` (int): Subnet ID to include incident events for
- `excludesid` (int): Subnet ID to exclude incident events for
- `master` (int): Master instance ID under Unified View
- `saasonly` (bool): Restricts returned incidents to only those with SaaS activity
- `groupid` (str): Unique identifier of an AI Analyst incident

### 3. get_investigations(**params) - NEW METHOD

Get AI Analyst investigations (manual investigations launched by users).

```python
# Get all investigations from the last week
week_ago = int((time.time() - 7*24*60*60) * 1000)
now = int(time.time() * 1000)

investigations = client.analyst.get_investigations(
    starttime=week_ago,
    endtime=now
)

# Get specific investigation
investigation = client.analyst.get_investigations(
    investigationid="52c75821-7c17-4a69-b07f-1c74789a9452"
)
```

#### Parameters

- `includeacknowledged` (bool): Include acknowledged events in the data
- `endtime` (int): End time in millisecond format
- `starttime` (int): Start time in millisecond format
- `did` (int): Device ID to include investigation events for
- `excludedid` (int): Device ID to exclude investigation events for
- `sid` (int): Subnet ID to include investigation events for
- `excludesid` (int): Subnet ID to exclude investigation events for
- `pbid` (int): Playbook ID that the search is filtered to
- `minfirstreporttime` (int): Earliest first report time for investigation
- `maxfirstreporttime` (int): Latest first report time for investigation
- `maxlastreporttime` (int): Latest last report time for investigation
- `minlastreporttime` (int): Earliest last report time for investigation
- `includefirstreports` (bool): Include first reports along with the investigation data
- `investigationid` (str): Unique identifier of an AI Analyst investigation

### 4. create_investigation(investigate_time, did) - NEW METHOD

Create a new AI Analyst investigation.

```python
# Create investigation for device 1234 at specific time
import time
investigate_time = str(int(time.time()))
result = client.analyst.create_investigation(investigate_time, 1234)
print(f"Investigation created with ID: {result.get('investigationId')}")
```

#### Parameters

- `investigate_time` (str): The time that the investigation should focus around (epoch timestamp)
- `did` (int): The device that an investigation should be created for

### 5. get_stats(**params)

Get AI Analyst statistics with enhanced filtering.

```python
# Basic usage
stats = client.analyst.get_stats()

# Get statistics for critical incidents in last week
stats = client.analyst.get_stats(
    starttime=week_ago,
    endtime=now,
    groupcritical=True
)
```

#### Parameters

- `includeacknowledged` (bool): Include acknowledged events in the data
- `endtime` (int): End time in millisecond format
- `starttime` (int): Start time in millisecond format
- `groupcompliance` (bool): Return only events with "compliance" behavior category
- `groupsuspicious` (bool): Return only events with "suspicious" behavior category
- `groupcritical` (bool): Return only events with "critical" behavior category
- `did` (int): Device ID to include incident events for
- `excludedid` (int): Device ID to exclude incident events for
- `sid` (int): Subnet ID to include incident events for
- `excludesid` (int): Subnet ID to exclude incident events for
- `master` (int): Master instance ID under Unified View
- `saasonly` (bool): Restricts returned events to only those with SaaS activity

### 6. get_comments(incident_id, response_data="")

Get comments for an AI Analyst incident event.

```python
# Get all comments for an incident
comments = client.analyst.get_comments("04a3f36e-4u8w-v9dh-x6lb-894778cf9633")

# Get only specific field
comments = client.analyst.get_comments(
    "04a3f36e-4u8w-v9dh-x6lb-894778cf9633", 
    response_data="comments"
)
```

#### Parameters

- `incident_id` (str): Unique identifier for the AI Analyst event to return comments for
- `response_data` (str): When given the name of a top-level field or object, restricts the returned JSON to only that field or object

### 7. add_comment(incident_id, message)

Add a comment to an AI Analyst incident event.

```python
# Add a comment to an incident
success = client.analyst.add_comment(
    "04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
    "Investigating potential compromise"
)
```

#### Parameters

- `incident_id` (str): Unique identifier for the AI Analyst event
- `message` (str): Text that should be added as a comment to the AI Analyst incident event

### 8. Event Management Methods

#### acknowledge(uuids)

Acknowledge AI Analyst incident events.

```python
# Acknowledge single event
success = client.analyst.acknowledge("04a3f36e-4u8w-v9dh-x6lb-894778cf9633")

# Acknowledge multiple events
success = client.analyst.acknowledge([
    "04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
    "af763617-2626-4e4c-84fc-e03d5cd8e6c8"
])
```

#### unacknowledge(uuids)

Unacknowledge AI Analyst incident events.

```python
success = client.analyst.unacknowledge("04a3f36e-4u8w-v9dh-x6lb-894778cf9633")
```

#### pin(uuids)

Pin AI Analyst incident events.

```python
success = client.analyst.pin("04a3f36e-4u8w-v9dh-x6lb-894778cf9633")
```

#### unpin(uuids)

Unpin AI Analyst incident events.

```python
success = client.analyst.unpin("04a3f36e-4u8w-v9dh-x6lb-894778cf9633")
```

## Advanced Usage Examples

### Time-based Analysis

```python
import time

# Get critical incidents from last 7 days
week_ago = int((time.time() - 7*24*60*60) * 1000)
now = int(time.time() * 1000)

critical_incidents = client.analyst.get_incident_events(
    starttime=week_ago,
    endtime=now,
    groupcritical=True,
    minscore=75,
    includeacknowledged=False
)

print(f"Found {len(critical_incidents)} critical incidents in the last week")
```

### Device-specific Investigation

```python
# Get all incidents for a specific device
device_incidents = client.analyst.get_incident_events(
    did=1234,
    includeacknowledged=True
)

# Create investigation for suspicious device
investigation = client.analyst.create_investigation(
    investigate_time=str(int(time.time())),
    did=1234
)
```

### SaaS Security Analysis

```python
# Get SaaS-related suspicious incidents
saas_incidents = client.analyst.get_groups(
    saasonly=True,
    groupsuspicious=True,
    minscore=50
)

# Get statistics for SaaS incidents
saas_stats = client.analyst.get_stats(
    saasonly=True,
    starttime=week_ago,
    endtime=now
)
```

### Multi-language Support

```python
# Get incidents in German
german_incidents = client.analyst.get_incident_events(
    locale="de_DE",
    groupcritical=True
)

# Get incidents in Japanese
japanese_incidents = client.analyst.get_incident_events(
    locale="ja_JP",
    minscore=80
)
```

## Response Examples

### Incident Event Response

```json
{
  "summariser": "AdminConnSummary",
  "mitreTactics": ["lateral-movement"],
  "acknowledged": false,
  "pinned": true,
  "createdAt": 1628002089240,
  "attackPhases": [5],
  "title": "Extensive Unusual SSH Connections",
  "id": "04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
  "category": "critical",
  "currentGroup": "g04a3f36e-4u8w-v9dh-x6lb-894778cf9633",
  "groupScore": "72.9174234",
  "aiaScore": 98,
  "summary": "The device 10.1.2.3 was observed making unusual internal SSH connections...",
  "breachDevices": [
    {
      "ip": "10.1.2.3",
      "subnet": "VPN",
      "did": 10,
      "sid": 12
    }
  ]
}
```

### Investigation Response

```json
{
  "investigationId": "52c75821-7c17-4a69-b07f-1c74789a9452",
  "time": 1702310487,
  "investigationTime": 1701864000,
  "did": 12345,
  "status": "finished",
  "createdBy": "analyst_user",
  "incidentId": "af763617-2626-4e4c-84fc-e03d5cd8e6c8",
  "incidents": [
    {
      "uuid": "af763617-2626-4e4c-84fc-e03d5cd8e6c8",
      "related": [630, 608]
    }
  ]
}
```

## Error Handling

```python
try:
    incidents = client.analyst.get_incident_events(
        groupcritical=True,
        minscore=90
    )
    # Process the incidents
    for incident in incidents:
        print(f"Incident: {incident.get('title')} - Score: {incident.get('aiaScore')}")
        
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Key Features

### Enhanced Parameter Support
- **Complete API Coverage**: All parameters from the official Darktrace API documentation
- **Backward Compatibility**: Existing code continues to work unchanged
- **Advanced Filtering**: Score-based, time-based, device-based, and category-based filtering

### New Capabilities
- **Manual Investigations**: Create and manage AI Analyst investigations programmatically
- **Comprehensive Statistics**: Detailed analytics with advanced filtering options
- **Multi-language Support**: 11 supported languages for international deployments
- **Enhanced Comments**: Full comments management with read and write capabilities

### Authentication & Security
- **Consistent Authentication**: Uses the same secure authentication mechanism as other modules
- **Parameter Validation**: Proper parameter handling and validation
- **Error Handling**: Comprehensive error handling with detailed debugging information

This enhanced AI Analyst module provides complete coverage of Darktrace's AI Analyst API endpoints with all documented parameters and functionality.
