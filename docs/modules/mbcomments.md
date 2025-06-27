# MBComments Module

The MBComments (Model Breach Comments) module provides access to comments associated with model breaches in Darktrace. This module allows you to retrieve existing comments and add new comments to model breaches for investigation tracking, analysis notes, and collaborative incident response.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the mbcomments module
mbcomments = client.mbcomments
```

## Methods Overview

The MBComments module provides the following methods:

- **`get()`** - Retrieve model breach comments with filtering options
- **`post()`** - Add new comments to model breaches

## Methods

### Get Comments

Retrieve comments associated with model breaches from Darktrace. This method allows filtering by time range, specific breaches, or individual comments.

```python
# Get all recent comments
all_comments = mbcomments.get()

# Get comments for specific model breach
breach_comments = mbcomments.get(pbid=12345)

# Get specific comment by ID
specific_comment = mbcomments.get(comment_id="comment-uuid-123")

# Get comments within time range
time_filtered = mbcomments.get(
    starttime=1705320000000,
    endtime=1705323600000
)

# Get limited number of comments
recent_comments = mbcomments.get(count=50)

# Get comments with limited response data
comment_overview = mbcomments.get(
    pbid=12345,
    responsedata="comment,timestamp,author"
)
```

#### Parameters

- `comment_id` (str, optional): Specific comment ID to retrieve. If provided, returns details for that comment only
- `starttime` (int, optional): Start time in milliseconds since epoch (UTC) for comments to return
- `endtime` (int, optional): End time in milliseconds since epoch (UTC) for comments to return
- `responsedata` (str, optional): Restrict returned JSON to specific fields or objects (comma-separated)
- `count` (int, optional): Number of comments to return (default 100)
- `pbid` (int, optional): Only return comments for the model breach with this ID
- Additional query parameters via `**params`

#### Response Structure

```python
# All comments response
[
  {
    "comment_id": "uuid-comment-123",
    "pbid": 12345,
    "comment": "Initial investigation shows unusual file access patterns. Escalating to security team.",
    "author": "analyst@company.com",
    "timestamp": 1705320120000,
    "created": "2024-01-15T10:02:00Z",
    "breach_details": {
      "model_name": "Device / Data Exfiltration",
      "device": {
        "did": 456,
        "hostname": "workstation-05",
        "ip": "192.168.1.105"
      },
      "score": 0.95,
      "time": 1705320000000
    },
    "priority": "high",
    "tags": ["investigation", "data-exfiltration"]
  },
  {
    "comment_id": "uuid-comment-124",
    "pbid": 12346,
    "comment": "False positive - confirmed legitimate backup process. Marking as resolved.",
    "author": "security@company.com",
    "timestamp": 1705321200000,
    "created": "2024-01-15T10:20:00Z",
    "breach_details": {
      "model_name": "Device / Suspicious Activity",
      "device": {
        "did": 789,
        "hostname": "server-backup",
        "ip": "10.0.1.50"
      },
      "score": 0.78,
      "time": 1705320900000
    },
    "priority": "low",
    "tags": ["resolved", "false-positive"]
  }
  // ... more comments
]

# Single comment response (when comment_id specified)
{
  "comment_id": "uuid-comment-123",
  "pbid": 12345,
  "comment": "Initial investigation shows unusual file access patterns. Escalating to security team.",
  "author": "analyst@company.com",
  "timestamp": 1705320120000,
  "created": "2024-01-15T10:02:00Z",
  "breach_details": {
    "model_name": "Device / Data Exfiltration",
    "device": {
      "did": 456,
      "hostname": "workstation-05",
      "ip": "192.168.1.105"
    },
    "score": 0.95,
    "time": 1705320000000
  },
  "priority": "high",
  "tags": ["investigation", "data-exfiltration"],
  "edit_history": [
    {
      "timestamp": 1705320120000,
      "author": "analyst@company.com",
      "action": "created"
    }
  ]
}

# With responsedata filtering
[
  {
    "comment": "Initial investigation shows unusual file access patterns.",
    "timestamp": 1705320120000,
    "author": "analyst@company.com"
  },
  {
    "comment": "False positive - confirmed legitimate backup process.",
    "timestamp": 1705321200000,
    "author": "security@company.com"
  }
  // ... more comments with only specified fields
]
```

### Add Comment

Add a new comment to a model breach for tracking investigation progress, analysis results, or incident response actions.

```python
# Add investigation comment
response = mbcomments.post(
    breach_id="pbid-12345",
    comment="Initial triage complete. Suspicious network connections identified. Proceeding with detailed analysis."
)

# Add resolution comment
response = mbcomments.post(
    breach_id="pbid-12346",
    comment="Investigation concluded: False positive caused by legitimate software update process. Adding exclusion rule."
)

# Add comment with additional metadata
response = mbcomments.post(
    breach_id="pbid-12347",
    comment="High priority escalation: Potential APT indicators detected. Initiating incident response procedures.",
    priority="critical",
    tags=["apt", "escalation", "incident-response"]
)
```

#### Parameters

- `breach_id` (str, required): The breach ID (pbid) to add the comment to
- `comment` (str, required): The comment text content
- Additional metadata via `**params` (priority, tags, etc.)

#### Response Structure

```python
{
  "comment_id": "uuid-new-comment-456",
  "pbid": "pbid-12345",
  "comment": "Initial triage complete. Suspicious network connections identified.",
  "author": "api-user@company.com",
  "timestamp": 1705325600000,
  "created": "2024-01-15T11:33:20Z",
  "status": "created",
  "success": true
}
```

## Examples

### Investigation Workflow Tracking

```python
from darktrace import DarktraceClient
import datetime

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get recent high-priority breaches that need investigation
recent_breaches = client.breaches.get(
    minscore=0.8,
    starttime=int((datetime.datetime.now() - datetime.timedelta(hours=24)).timestamp() * 1000),
    endtime=int(datetime.datetime.now().timestamp() * 1000)
)

print("High-Priority Breach Investigation Workflow")
print("=" * 60)

for breach in recent_breaches.get('breaches', [])[:5]:  # Process first 5
    pbid = breach.get('pbid')
    model_name = breach.get('model', {}).get('name', 'Unknown Model')
    score = breach.get('score', 0)
    
    print(f"\nBreach ID {pbid}: {model_name} (Score: {score:.2f})")
    
    # Check for existing comments
    existing_comments = client.mbcomments.get(pbid=pbid)
    
    if existing_comments:
        print(f"  Existing comments: {len(existing_comments)}")
        
        # Show latest comment
        latest_comment = max(existing_comments, key=lambda x: x.get('timestamp', 0))
        author = latest_comment.get('author', 'Unknown')
        comment_text = latest_comment.get('comment', '')
        comment_time = datetime.datetime.fromtimestamp(latest_comment.get('timestamp', 0) / 1000)
        
        print(f"  Latest comment ({author} at {comment_time.strftime('%H:%M:%S')}):")
        print(f"    \"{comment_text[:100]}{'...' if len(comment_text) > 100 else ''}\"")
        
        # Check if investigation is complete
        investigation_keywords = ['resolved', 'false positive', 'closed', 'complete']
        is_resolved = any(keyword in comment_text.lower() for keyword in investigation_keywords)
        
        if not is_resolved:
            print(f"  ⚠️  Investigation appears ongoing")
        else:
            print(f"  ✅ Investigation appears resolved")
    else:
        print(f"  No comments yet - needs initial triage")
        
        # Add initial triage comment for demonstration
        try:
            initial_comment = f"Auto-triage initiated for {model_name} breach with score {score:.2f}. Requires analyst review."
            
            comment_response = client.mbcomments.post(
                breach_id=str(pbid),
                comment=initial_comment
            )
            
            if comment_response.get('success'):
                print(f"  ✅ Initial triage comment added")
            else:
                print(f"  ❌ Failed to add triage comment")
                
        except Exception as e:
            print(f"  ❌ Error adding comment: {e}")
```

### Comment Analysis and Reporting

```python
# Analyze investigation patterns through comments
def analyze_investigation_patterns():
    # Get all comments from last 7 days
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=7)
    
    all_comments = client.mbcomments.get(
        starttime=int(start_time.timestamp() * 1000),
        endtime=int(end_time.timestamp() * 1000)
    )
    
    print("Investigation Patterns Analysis (Last 7 Days)")
    print("=" * 60)
    
    # Analyze comment patterns
    comment_stats = {
        'total_comments': len(all_comments),
        'unique_breaches': set(),
        'authors': {},
        'resolution_patterns': {},
        'response_times': [],
        'priority_distribution': {}
    }
    
    # Keywords for analysis
    resolution_keywords = {
        'false_positive': ['false positive', 'legitimate', 'normal behavior'],
        'resolved': ['resolved', 'fixed', 'mitigated'],
        'escalated': ['escalated', 'escalating', 'high priority'],
        'investigating': ['investigating', 'analyzing', 'reviewing']
    }
    
    for comment in all_comments:
        pbid = comment.get('pbid')
        author = comment.get('author', 'Unknown')
        comment_text = comment.get('comment', '').lower()
        timestamp = comment.get('timestamp', 0)
        
        # Track unique breaches
        comment_stats['unique_breaches'].add(pbid)
        
        # Track authors
        comment_stats['authors'][author] = comment_stats['authors'].get(author, 0) + 1
        
        # Analyze resolution patterns
        for pattern, keywords in resolution_keywords.items():
            if any(keyword in comment_text for keyword in keywords):
                comment_stats['resolution_patterns'][pattern] = comment_stats['resolution_patterns'].get(pattern, 0) + 1
        
        # Priority analysis
        priority = comment.get('priority', 'normal')
        comment_stats['priority_distribution'][priority] = comment_stats['priority_distribution'].get(priority, 0) + 1
    
    # Display analysis results
    print(f"Total comments: {comment_stats['total_comments']}")
    print(f"Unique breaches with comments: {len(comment_stats['unique_breaches'])}")
    
    print(f"\nTop commenters:")
    top_authors = sorted(comment_stats['authors'].items(), key=lambda x: x[1], reverse=True)[:5]
    for author, count in top_authors:
        print(f"  {author}: {count} comments")
    
    print(f"\nResolution patterns:")
    for pattern, count in sorted(comment_stats['resolution_patterns'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / comment_stats['total_comments']) * 100
        print(f"  {pattern.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
    
    print(f"\nPriority distribution:")
    for priority, count in sorted(comment_stats['priority_distribution'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / comment_stats['total_comments']) * 100
        print(f"  {priority.title()}: {count} ({percentage:.1f}%)")
    
    return comment_stats

# Run analysis
analysis_results = analyze_investigation_patterns()
```

### Breach Investigation Timeline

```python
# Create investigation timeline for specific breach
breach_id = 12345  # Replace with actual breach ID

def create_investigation_timeline(pbid):
    # Get all comments for the breach
    breach_comments = client.mbcomments.get(pbid=pbid)
    
    if not breach_comments:
        print(f"No comments found for breach {pbid}")
        return
    
    # Get breach details
    breach_details = client.breaches.get(pbid=pbid)
    
    print(f"Investigation Timeline for Breach {pbid}")
    print("=" * 70)
    
    if breach_details:
        model_name = breach_details.get('model', {}).get('name', 'Unknown')
        device_info = breach_details.get('device', {})
        score = breach_details.get('score', 0)
        breach_time = datetime.datetime.fromtimestamp(breach_details.get('time', 0) / 1000)
        
        print(f"Breach: {model_name}")
        print(f"Device: {device_info.get('hostname', 'Unknown')} ({device_info.get('ip', 'Unknown')})")
        print(f"Score: {score:.2f}")
        print(f"Time: {breach_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    # Sort comments by timestamp
    sorted_comments = sorted(breach_comments, key=lambda x: x.get('timestamp', 0))
    
    print("Investigation Timeline:")
    for i, comment in enumerate(sorted_comments, 1):
        timestamp = comment.get('timestamp', 0)
        comment_time = datetime.datetime.fromtimestamp(timestamp / 1000)
        author = comment.get('author', 'Unknown')
        comment_text = comment.get('comment', '')
        priority = comment.get('priority', 'normal')
        
        print(f"\n{i}. {comment_time.strftime('%Y-%m-%d %H:%M:%S')} - {author}")
        if priority != 'normal':
            print(f"   Priority: {priority.upper()}")
        print(f"   \"{comment_text}\"")
        
        # Calculate time between comments
        if i > 1:
            prev_timestamp = sorted_comments[i-2].get('timestamp', 0)
            time_diff = (timestamp - prev_timestamp) / (1000 * 60)  # Convert to minutes
            
            if time_diff < 60:
                print(f"   (Response time: {time_diff:.0f} minutes)")
            elif time_diff < 1440:  # Less than 24 hours
                print(f"   (Response time: {time_diff/60:.1f} hours)")
            else:
                print(f"   (Response time: {time_diff/1440:.1f} days)")
    
    # Analysis summary
    if len(sorted_comments) > 1:
        total_time = (sorted_comments[-1].get('timestamp', 0) - sorted_comments[0].get('timestamp', 0)) / (1000 * 60 * 60)  # Hours
        print(f"\nInvestigation Summary:")
        print(f"Total investigation time: {total_time:.1f} hours")
        print(f"Number of updates: {len(sorted_comments)}")
        
        # Check resolution status
        last_comment = sorted_comments[-1].get('comment', '').lower()
        resolution_keywords = ['resolved', 'closed', 'false positive', 'mitigated']
        is_resolved = any(keyword in last_comment for keyword in resolution_keywords)
        
        print(f"Status: {'Resolved' if is_resolved else 'Ongoing'}")

# Create timeline
create_investigation_timeline(breach_id)
```

### Collaborative Investigation Management

```python
# Manage collaborative investigations across team
def manage_team_investigations():
    # Get recent high-priority breaches
    recent_breaches = client.breaches.get(
        minscore=0.7,
        starttime=int((datetime.datetime.now() - datetime.timedelta(hours=12)).timestamp() * 1000)
    )
    
    print("Team Investigation Management")
    print("=" * 50)
    
    # Track investigation assignments
    investigation_status = {}
    unassigned_breaches = []
    
    for breach in recent_breaches.get('breaches', []):
        pbid = breach.get('pbid')
        
        # Get comments for this breach
        comments = client.mbcomments.get(pbid=pbid)
        
        if comments:
            # Find latest assignment or status
            latest_comment = max(comments, key=lambda x: x.get('timestamp', 0))
            author = latest_comment.get('author', 'Unknown')
            comment_text = latest_comment.get('comment', '')
            
            # Determine status
            if any(keyword in comment_text.lower() for keyword in ['resolved', 'closed', 'false positive']):
                status = 'resolved'
            elif any(keyword in comment_text.lower() for keyword in ['investigating', 'assigned', 'analyzing']):
                status = 'investigating'
            elif any(keyword in comment_text.lower() for keyword in ['escalated', 'urgent', 'critical']):
                status = 'escalated'
            else:
                status = 'pending'
            
            investigation_status[pbid] = {
                'status': status,
                'assignee': author,
                'last_update': latest_comment.get('timestamp', 0),
                'breach': breach
            }
        else:
            unassigned_breaches.append(breach)
    
    # Display team workload
    print(f"Active Investigations: {len(investigation_status)}")
    print(f"Unassigned Breaches: {len(unassigned_breaches)}")
    
    # Group by status
    status_groups = {}
    for pbid, info in investigation_status.items():
        status = info['status']
        if status not in status_groups:
            status_groups[status] = []
        status_groups[status].append((pbid, info))
    
    for status, investigations in status_groups.items():
        print(f"\n{status.upper()} ({len(investigations)}):")
        for pbid, info in investigations[:5]:  # Show first 5
            assignee = info['assignee']
            breach = info['breach']
            model_name = breach.get('model', {}).get('name', 'Unknown')
            score = breach.get('score', 0)
            last_update = datetime.datetime.fromtimestamp(info['last_update'] / 1000)
            
            print(f"  Breach {pbid}: {model_name} (Score: {score:.2f})")
            print(f"    Assignee: {assignee}")
            print(f"    Last update: {last_update.strftime('%H:%M:%S')}")
    
    # Auto-assign unassigned breaches (example)
    team_members = ['analyst1@company.com', 'analyst2@company.com', 'analyst3@company.com']
    
    if unassigned_breaches:
        print(f"\nAuto-assigning {len(unassigned_breaches)} unassigned breaches:")
        
        for i, breach in enumerate(unassigned_breaches[:3]):  # Assign first 3
            pbid = breach.get('pbid')
            assignee = team_members[i % len(team_members)]
            model_name = breach.get('model', {}).get('name', 'Unknown')
            score = breach.get('score', 0)
            
            assignment_comment = f"Auto-assigned to {assignee} for initial triage. Model: {model_name}, Score: {score:.2f}"
            
            try:
                response = client.mbcomments.post(
                    breach_id=str(pbid),
                    comment=assignment_comment
                )
                
                if response.get('success'):
                    print(f"  ✅ Breach {pbid} assigned to {assignee}")
                else:
                    print(f"  ❌ Failed to assign breach {pbid}")
                    
            except Exception as e:
                print(f"  ❌ Error assigning breach {pbid}: {e}")

# Run team management
manage_team_investigations()
```

### Comment Search and Filtering

```python
# Advanced comment search and filtering
def search_comments(search_term, days_back=7):
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=days_back)
    
    all_comments = client.mbcomments.get(
        starttime=int(start_time.timestamp() * 1000),
        endtime=int(end_time.timestamp() * 1000)
    )
    
    print(f"Searching comments for: '{search_term}' (Last {days_back} days)")
    print("=" * 70)
    
    # Filter comments by search term
    matching_comments = []
    
    for comment in all_comments:
        comment_text = comment.get('comment', '').lower()
        author = comment.get('author', '').lower()
        
        if (search_term.lower() in comment_text or 
            search_term.lower() in author):
            matching_comments.append(comment)
    
    print(f"Found {len(matching_comments)} matching comments:")
    
    # Group by breach for better organization
    breach_groups = {}
    for comment in matching_comments:
        pbid = comment.get('pbid')
        if pbid not in breach_groups:
            breach_groups[pbid] = []
        breach_groups[pbid].append(comment)
    
    for pbid, comments in breach_groups.items():
        print(f"\nBreach {pbid} ({len(comments)} comments):")
        
        # Sort comments by timestamp
        sorted_comments = sorted(comments, key=lambda x: x.get('timestamp', 0))
        
        for comment in sorted_comments:
            timestamp = comment.get('timestamp', 0)
            comment_time = datetime.datetime.fromtimestamp(timestamp / 1000)
            author = comment.get('author', 'Unknown')
            comment_text = comment.get('comment', '')
            
            # Highlight search term in text
            highlighted_text = comment_text
            if search_term.lower() in comment_text.lower():
                highlighted_text = comment_text.replace(
                    search_term, 
                    f"**{search_term}**"
                )
            
            print(f"  {comment_time.strftime('%Y-%m-%d %H:%M')} - {author}:")
            print(f"    {highlighted_text}")
    
    return matching_comments

# Example searches
apt_comments = search_comments("APT", days_back=30)
malware_comments = search_comments("malware", days_back=14)
resolved_comments = search_comments("resolved", days_back=7)
```

## Error Handling

```python
try:
    # Attempt to get comments for a specific breach
    breach_comments = client.mbcomments.get(pbid=12345)
    
    print(f"Retrieved {len(breach_comments)} comments for breach")
    
    # Process each comment
    for comment in breach_comments:
        comment_id = comment.get('comment_id', 'Unknown')
        author = comment.get('author', 'Unknown')
        comment_text = comment.get('comment', '')
        
        print(f"Comment {comment_id} by {author}: {comment_text[:100]}...")
        
    # Attempt to add a new comment
    try:
        new_comment = client.mbcomments.post(
            breach_id="12345",
            comment="Investigation update: Analysis in progress"
        )
        
        if new_comment.get('success'):
            print(f"Successfully added comment: {new_comment.get('comment_id')}")
        else:
            print("Failed to add comment - check response for details")
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print("Bad request - check breach ID and comment content")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for adding comments")
        elif e.response.status_code == 404:
            print("Breach not found - verify breach ID exists")
        else:
            print(f"Error adding comment: {e}")
            
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 403:
            print("Access denied - check API permissions for mbcomments endpoint")
        elif e.response.status_code == 404:
            print("Comments not found - check breach ID or comment ID")
        else:
            print(f"Response: {e.response.text}")
            
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Comment Management
- **Unique identifiers**: Each comment has a unique comment_id (UUID)
- **Breach association**: Comments are linked to specific model breaches via pbid
- **Persistent storage**: Comments are permanently stored and retrievable
- **Edit limitations**: Comments may not be editable after creation (check API capabilities)

### Time Parameters
- **Timestamp format**: Unix epoch milliseconds (UTC)
- **Time ranges**: Use starttime/endtime for filtering comments by creation time
- **Default behavior**: Without time filters, returns recent comments (typically last 100)
- **Timezone**: All timestamps are in UTC

### Author Tracking
- **API user identification**: Comments added via API show the API user as author
- **User tracking**: Track investigation ownership through author field
- **Authentication context**: Author is determined by API credentials used

### Content Guidelines
- **Comment length**: Check API limits for maximum comment length
- **Content formatting**: Support for plain text (check if markdown/HTML supported)
- **Special characters**: Ensure proper encoding for special characters
- **Sensitive information**: Avoid including sensitive data in comments

### Breach Integration
- **Valid breach IDs**: Ensure breach exists before adding comments
- **Breach lifecycle**: Comments remain accessible even if breach status changes
- **Model correlation**: Comments inherit context from associated model breach
- **Device correlation**: Breach-device relationship provides context for comments

### Response Data Filtering
Use `responsedata` parameter to optimize queries:
- `"comment,timestamp,author"`: Basic comment information
- `"comment_id,pbid"`: Minimal identification data
- `"breach_details"`: Include associated breach information
- `"priority,tags"`: Metadata and classification information

### Search and Discovery
- **Text search**: Filter comments by content using application logic
- **Time-based search**: Use starttime/endtime for temporal analysis
- **Breach-based search**: Use pbid to find all comments for specific incidents
- **Author-based search**: Track investigations by specific team members

### Workflow Integration
- **SIEM integration**: Comments can be part of automated investigation workflows
- **Ticketing systems**: Link comments to external ticketing and case management
- **Reporting**: Use comments for investigation status reporting
- **Escalation tracking**: Track escalation decisions and outcomes

### Best Practices
- **Clear communication**: Write descriptive, actionable comments
- **Status updates**: Regularly update investigation progress
- **Resolution documentation**: Document investigation outcomes and decisions
- **Team coordination**: Use comments for handoffs and collaboration
- **Timestamp awareness**: Consider timezone differences in global teams

### Common Use Cases
- **Investigation tracking**: Document analysis steps and findings
- **Team collaboration**: Coordinate investigations across multiple analysts
- **Status reporting**: Provide investigation status to management
- **Knowledge sharing**: Document lessons learned and resolution strategies
- **Audit trails**: Maintain records of investigation decisions and actions

### Performance Considerations
- **Batch operations**: Consider API rate limits for bulk comment operations
- **Time range optimization**: Use appropriate time ranges to limit response size
- **Filtered queries**: Use pbid and other filters to reduce data volume
- **Caching strategy**: Cache comments for frequently accessed breaches
