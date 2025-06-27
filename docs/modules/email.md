# Email Module

The Email module provides comprehensive access to Darktrace/Email security features, including email threat detection, analysis, dashboard statistics, user anomaly monitoring, audit events, and email management capabilities. This module is specifically designed for Darktrace/Email deployments.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the email module
email = client.email
```

## Methods Overview

The Email module provides the following methods:

- **`decode_link()`** - Decode encoded links from emails
- **`get_action_summary()`** - Retrieve action summary statistics
- **`get_dash_stats()`** - Get dashboard statistics
- **`get_data_loss()`** - Retrieve data loss information
- **`get_user_anomaly()`** - Get user anomaly data
- **`email_action()`** - Perform actions on emails
- **`get_email()`** - Retrieve specific email details
- **`download_email()`** - Download raw email content
- **`search_emails()`** - Search emails with filters
- **`get_tags()`** - Retrieve available email tags
- **`get_actions()`** - Get available email actions
- **`get_filters()`** - Retrieve available search filters
- **`get_event_types()`** - Get audit event types
- **`get_audit_events()`** - Retrieve audit events

## Methods

### Decode Link

Decode an encoded link from an email using the Darktrace/Email API. This is useful for analyzing suspicious or potentially malicious links that have been URL-encoded or obfuscated.

```python
# Decode a suspicious link
decoded = email.decode_link(link="https://...encoded...")

# Decode multiple links
links = [
    "https://suspicious-site.example/encoded-path",
    "https://another-encoded-url.example/path"
]

for link in links:
    decoded = email.decode_link(link=link)
    print(f"Original: {link}")
    print(f"Decoded: {decoded}")
```

#### Parameters

- `link` (str): The encoded link to decode

#### Response Structure

```python
{
  "original_link": "https://suspicious-site.example/encoded-path",
  "decoded_link": "https://actual-malicious-site.example/attack-path",
  "risk_score": 0.85,
  "threat_categories": ["phishing", "malware"],
  "reputation": "malicious",
  "analysis": {
    "domain_reputation": "poor",
    "url_structure": "suspicious",
    "encoding_type": "base64_obfuscation"
  }
}
```

### Get Action Summary

Retrieve summary statistics about actions taken on emails over a specified time period.

```python
# Get action summary for the last 7 days
recent_actions = email.get_action_summary(days=7, limit=10)

# Get action summary for the last month
monthly_actions = email.get_action_summary(days=30)

# Get unlimited action summary
all_actions = email.get_action_summary()
```

#### Parameters

- `days` (int, optional): Number of days to include in the summary
- `limit` (int, optional): Limit the number of results

#### Response Structure

```python
{
  "total_actions": 1547,
  "period_days": 7,
  "actions_by_type": {
    "quarantine": 892,
    "delete": 234,
    "release": 156,
    "block_sender": 89,
    "mark_safe": 176
  },
  "actions_by_day": [
    {
      "date": "2024-01-15",
      "actions": 245,
      "breakdown": {
        "quarantine": 145,
        "delete": 45,
        "release": 35,
        "block_sender": 20
      }
    }
    // ... more daily data
  ],
  "top_triggered_rules": [
    {
      "rule_name": "Suspicious Attachment",
      "actions": 234,
      "percentage": 15.1
    },
    {
      "rule_name": "Phishing Link Detected",
      "actions": 187,
      "percentage": 12.1
    }
  ],
  "user_activity": {
    "most_active_users": [
      {
        "email": "admin@company.com",
        "actions": 45,
        "action_types": ["release", "mark_safe"]
      }
    ]
  }
}
```

### Get Dashboard Statistics

Retrieve comprehensive dashboard statistics for email security monitoring.

```python
# Get dashboard stats for the last 28 days
stats = email.get_dash_stats(days=28, limit=2)

# Get recent dashboard overview
recent_stats = email.get_dash_stats(days=7)
```

#### Parameters

- `days` (int, optional): Number of days to include in the statistics
- `limit` (int, optional): Limit the number of results

#### Response Structure

```python
{
  "period_days": 28,
  "email_statistics": {
    "total_emails": 145872,
    "clean_emails": 132456,
    "suspicious_emails": 8934,
    "malicious_emails": 4482,
    "quarantined": 6789,
    "blocked": 2234
  },
  "threat_breakdown": {
    "phishing": 2134,
    "malware": 1567,
    "spam": 3456,
    "data_loss": 234,
    "anomalous_behavior": 1091
  },
  "top_threats": [
    {
      "threat_type": "phishing",
      "count": 2134,
      "percentage": 47.6,
      "trend": "increasing"
    },
    {
      "threat_type": "malware", 
      "count": 1567,
      "percentage": 35.0,
      "trend": "stable"
    }
  ],
  "user_metrics": {
    "total_users": 1250,
    "users_with_threats": 456,
    "high_risk_users": 23,
    "training_required": 89
  },
  "response_metrics": {
    "average_response_time": 45.2,  # seconds
    "auto_actions": 8934,
    "manual_actions": 1234,
    "false_positives": 89
  }
}
```

### Get Data Loss Information

Retrieve information about potential data loss incidents detected in email communications.

```python
# Get data loss info for the last week
data_loss = email.get_data_loss(days=7, limit=5)

# Get comprehensive data loss analysis
full_data_loss = email.get_data_loss(days=30)
```

#### Parameters

- `days` (int, optional): Number of days to include in data loss statistics
- `limit` (int, optional): Limit the number of results

#### Response Structure

```python
{
  "period_days": 7,
  "total_incidents": 23,
  "data_loss_by_type": {
    "credit_card": 8,
    "ssn": 3,
    "personal_data": 7,
    "confidential_files": 5
  },
  "incidents": [
    {
      "incident_id": "DL-2024-0115-001",
      "timestamp": 1705324800,
      "sender": "user@company.com",
      "recipient": "external@partner.com",
      "data_type": "credit_card",
      "confidence": 0.92,
      "content_preview": "Credit card ending in ****1234",
      "action_taken": "quarantine",
      "status": "under_review"
    },
    {
      "incident_id": "DL-2024-0115-002", 
      "timestamp": 1705321200,
      "sender": "finance@company.com",
      "recipient": "contractor@external.com",
      "data_type": "confidential_files",
      "confidence": 0.88,
      "content_preview": "Financial report Q4 2023.xlsx",
      "action_taken": "block",
      "status": "confirmed_violation"
    }
  ],
  "trends": {
    "incidents_last_7_days": 23,
    "incidents_previous_7_days": 18,
    "percentage_change": 27.8,
    "trend": "increasing"
  },
  "top_users": [
    {
      "email": "user@company.com",
      "incidents": 3,
      "data_types": ["credit_card", "personal_data"]
    }
  ]
}
```

### Get User Anomaly Data

Retrieve information about users exhibiting anomalous email behavior.

```python
# Get user anomaly data for the last month
anomalies = email.get_user_anomaly(days=28, limit=2)

# Get recent anomaly overview
recent_anomalies = email.get_user_anomaly(days=7)
```

#### Parameters

- `days` (int, optional): Number of days to include in anomaly statistics
- `limit` (int, optional): Limit the number of results

#### Response Structure

```python
{
  "period_days": 28,
  "total_anomalous_users": 45,
  "anomaly_categories": {
    "unusual_sending_patterns": 23,
    "suspicious_recipients": 12,
    "abnormal_timing": 18,
    "content_anomalies": 15,
    "volume_spikes": 8
  },
  "users": [
    {
      "email": "user@company.com",
      "risk_score": 0.78,
      "anomalies": [
        {
          "type": "unusual_sending_patterns",
          "description": "Sending 300% more emails than baseline",
          "confidence": 0.85,
          "first_detected": 1705324800,
          "last_detected": 1705411200
        },
        {
          "type": "suspicious_recipients",
          "description": "New external domains not seen before",
          "confidence": 0.72,
          "details": ["new-domain.example", "suspicious-site.net"]
        }
      ],
      "baseline_metrics": {
        "average_daily_emails": 25,
        "current_daily_emails": 75,
        "typical_recipients": 12,
        "new_recipients": 8
      },
      "recommendations": [
        "Monitor user activity closely",
        "Verify with user if behavior is legitimate",
        "Consider additional authentication"
      ]
    }
  ],
  "global_trends": {
    "anomaly_rate": 3.6,  # percentage of users
    "false_positive_rate": 12.3,
    "confirmed_threats": 8
  }
}
```

### Email Actions

Perform actions on specific emails identified by UUID.

```python
# Quarantine an email
action_data = {
    "action": "quarantine",
    "reason": "Suspicious attachment detected",
    "notify_user": True
}
result = email.email_action(uuid="email-uuid-here", data=action_data)

# Release an email from quarantine
release_data = {
    "action": "release",
    "reason": "False positive confirmed",
    "notify_user": True
}
result = email.email_action(uuid="email-uuid-here", data=release_data)

# Delete an email permanently
delete_data = {
    "action": "delete",
    "reason": "Confirmed malware",
    "notify_user": False
}
result = email.email_action(uuid="email-uuid-here", data=delete_data)
```

#### Parameters

- `uuid` (str): Email UUID identifier
- `data` (dict): Action data containing action type and parameters

#### Available Actions

```python
# Action types and their parameters
actions = {
    "quarantine": {
        "action": "quarantine",
        "reason": "string",
        "notify_user": bool,
        "duration": int  # optional, hours
    },
    "release": {
        "action": "release", 
        "reason": "string",
        "notify_user": bool
    },
    "delete": {
        "action": "delete",
        "reason": "string",
        "notify_user": bool,
        "permanent": bool  # optional
    },
    "block_sender": {
        "action": "block_sender",
        "reason": "string",
        "scope": "user|domain|global"
    },
    "mark_safe": {
        "action": "mark_safe",
        "reason": "string",
        "learn": bool  # add to whitelist
    }
}
```

### Get Email Details

Retrieve detailed information about a specific email using its UUID.

```python
# Get basic email details
email_info = email.get_email(uuid="email-uuid-here")

# Get email details with headers
email_with_headers = email.get_email(
    uuid="email-uuid-here",
    include_headers=True
)
```

#### Parameters

- `uuid` (str): Email UUID identifier
- `include_headers` (bool, optional): Include email headers in response

#### Response Structure

```python
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "<unique-message-id@sender.com>",
  "timestamp": 1705324800,
  "sender": {
    "email": "sender@external.com",
    "name": "John Doe",
    "reputation": 65,
    "is_internal": False
  },
  "recipients": [
    {
      "email": "recipient@company.com",
      "name": "Jane Smith",
      "type": "to"
    },
    {
      "email": "cc@company.com",
      "name": "Bob Johnson", 
      "type": "cc"
    }
  ],
  "subject": "Important Business Proposal",
  "size": 1048576,  # bytes
  "attachments": [
    {
      "filename": "proposal.pdf",
      "size": 524288,
      "type": "application/pdf",
      "hash": "sha256:abc123...",
      "threat_score": 0.12
    }
  ],
  "threat_analysis": {
    "overall_score": 0.65,
    "categories": ["suspicious_links", "unusual_sender"],
    "details": {
      "link_analysis": {
        "total_links": 3,
        "suspicious_links": 1,
        "malicious_links": 0
      },
      "attachment_analysis": {
        "total_attachments": 1,
        "clean": 1,
        "suspicious": 0,
        "malicious": 0
      },
      "sender_reputation": {
        "score": 65,
        "factors": ["new_sender", "external_domain"]
      }
    }
  },
  "actions_taken": [
    {
      "action": "quarantine",
      "timestamp": 1705324900,
      "user": "admin@company.com",
      "reason": "Suspicious link detected"
    }
  ],
  "status": "quarantined",
  
  # With include_headers=True
  "headers": {
    "received": ["from mail.external.com by mx.company.com..."],
    "return_path": "sender@external.com",
    "x_originating_ip": "203.0.113.42",
    "authentication_results": {
      "spf": "pass",
      "dkim": "fail", 
      "dmarc": "fail"
    },
    "all_headers": {
      "Date": "Mon, 15 Jan 2024 10:00:00 +0000",
      "From": "John Doe <sender@external.com>",
      "To": "recipient@company.com",
      "Subject": "Important Business Proposal",
      "Message-ID": "<unique-message-id@sender.com>",
      "Content-Type": "multipart/mixed"
    }
  }
}
```

### Download Email

Download the raw email content in MIME format for detailed analysis.

```python
# Download email content
email_content = email.download_email(uuid="email-uuid-here")

# Save to file
with open("suspicious_email.eml", "wb") as f:
    f.write(email_content)

# Parse MIME content (example)
import email.message
msg = email.message_from_bytes(email_content)
```

#### Parameters

- `uuid` (str): Email UUID identifier

#### Response

Returns raw email content as bytes in MIME format.

### Search Emails

Search emails using various filters and criteria.

```python
# Basic search by sender
search_data = {
    "filters": {
        "sender": "suspicious@external.com"
    },
    "limit": 10
}
results = email.search_emails(data=search_data)

# Advanced search with multiple criteria
advanced_search = {
    "filters": {
        "sender_domain": "suspicious-domain.com",
        "threat_score_min": 0.7,
        "date_range": {
            "start": "2024-01-01T00:00:00Z",
            "end": "2024-01-31T23:59:59Z"
        },
        "status": ["quarantined", "blocked"],
        "has_attachments": True
    },
    "sort": {
        "field": "timestamp",
        "order": "desc"
    },
    "limit": 50,
    "offset": 0
}
results = email.search_emails(data=advanced_search)

# Search by content keywords
content_search = {
    "filters": {
        "content_keywords": ["urgent", "payment", "click here"],
        "subject_contains": "invoice"
    },
    "limit": 25
}
results = email.search_emails(data=content_search)
```

#### Parameters

- `data` (dict): Search criteria and filters

#### Search Filters

```python
search_filters = {
    "sender": "string",                    # Exact sender email
    "sender_domain": "string",             # Sender domain
    "recipient": "string",                 # Recipient email  
    "recipient_domain": "string",          # Recipient domain
    "subject": "string",                   # Exact subject
    "subject_contains": "string",          # Subject contains text
    "content_keywords": ["string"],        # Content keywords
    "threat_score_min": float,            # Minimum threat score
    "threat_score_max": float,            # Maximum threat score
    "date_range": {                       # Date range filter
        "start": "ISO8601",
        "end": "ISO8601"
    },
    "status": ["string"],                 # Email status
    "has_attachments": bool,              # Has attachments
    "attachment_types": ["string"],       # Attachment types
    "tags": ["string"],                   # Email tags
    "actions_taken": ["string"],          # Actions performed
    "size_min": int,                      # Minimum size in bytes
    "size_max": int                       # Maximum size in bytes
}
```

### Resource Methods

#### Get Tags

Retrieve available email tags for classification and filtering.

```python
# Get all available tags
tags = email.get_tags()
```

#### Response Structure

```python
{
  "tags": [
    {
      "id": "phishing",
      "name": "Phishing",
      "description": "Emails identified as phishing attempts",
      "color": "#ff4444",
      "usage_count": 1234
    },
    {
      "id": "malware",
      "name": "Malware",
      "description": "Emails containing malicious attachments",
      "color": "#cc0000", 
      "usage_count": 567
    },
    {
      "id": "spam",
      "name": "Spam",
      "description": "Unsolicited bulk emails",
      "color": "#ffaa00",
      "usage_count": 3456
    }
  ]
}
```

#### Get Actions

Retrieve available email actions that can be performed.

```python
# Get all available actions
actions = email.get_actions()
```

#### Response Structure

```python
{
  "actions": [
    {
      "id": "quarantine",
      "name": "Quarantine",
      "description": "Move email to quarantine",
      "requires_reason": True,
      "user_notification": True,
      "reversible": True
    },
    {
      "id": "delete",
      "name": "Delete",
      "description": "Permanently delete email",
      "requires_reason": True,
      "user_notification": False,
      "reversible": False
    },
    {
      "id": "release",
      "name": "Release",
      "description": "Release from quarantine",
      "requires_reason": True,
      "user_notification": True,
      "reversible": True
    }
  ]
}
```

#### Get Filters

Retrieve available search filters for email queries.

```python
# Get all available filters
filters = email.get_filters()
```

#### Response Structure

```python
{
  "filters": [
    {
      "field": "sender",
      "type": "string",
      "description": "Email sender address",
      "operators": ["equals", "contains", "not_equals"]
    },
    {
      "field": "threat_score",
      "type": "float",
      "description": "Threat assessment score",
      "operators": ["greater_than", "less_than", "between"],
      "range": {"min": 0.0, "max": 1.0}
    },
    {
      "field": "timestamp",
      "type": "datetime",
      "description": "Email timestamp",
      "operators": ["before", "after", "between"]
    }
  ]
}
```

### Audit and System Methods

#### Get Event Types

Retrieve available audit event types for system monitoring.

```python
# Get all audit event types
event_types = email.get_event_types()
```

#### Response Structure

```python
{
  "event_types": [
    {
      "id": "login",
      "name": "User Login",
      "description": "User authentication events",
      "category": "authentication"
    },
    {
      "id": "email_action",
      "name": "Email Action",
      "description": "Actions performed on emails",
      "category": "email_management"
    },
    {
      "id": "config_change",
      "name": "Configuration Change",
      "description": "System configuration modifications",
      "category": "system"
    }
  ]
}
```

#### Get Audit Events

Retrieve audit events for system monitoring and compliance.

```python
# Get recent login events
login_events = email.get_audit_events(
    event_type="login",
    limit=10,
    offset=0
)

# Get all recent events
all_events = email.get_audit_events(limit=50)

# Get events with pagination
page_events = email.get_audit_events(
    limit=25,
    offset=25
)
```

#### Parameters

- `event_type` (str, optional): Filter by specific event type
- `limit` (int, optional): Limit number of results
- `offset` (int, optional): Offset for pagination

#### Response Structure

```python
{
  "events": [
    {
      "id": "evt_001",
      "timestamp": 1705324800,
      "event_type": "login",
      "user": "admin@company.com",
      "source_ip": "192.168.1.100",
      "details": {
        "success": True,
        "method": "username_password",
        "user_agent": "Mozilla/5.0..."
      },
      "risk_score": 0.1
    },
    {
      "id": "evt_002",
      "timestamp": 1705324750,
      "event_type": "email_action",
      "user": "analyst@company.com",
      "details": {
        "action": "quarantine",
        "email_uuid": "550e8400-e29b-41d4-a716-446655440000",
        "reason": "Suspicious attachment"
      }
    }
  ],
  "pagination": {
    "total": 1247,
    "limit": 10,
    "offset": 0,
    "has_more": True
  }
}
```

## Examples

### Comprehensive Email Security Dashboard

```python
from darktrace import DarktraceClient
from datetime import datetime, timedelta

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def generate_security_dashboard(days=7):
    """Generate comprehensive email security dashboard"""
    
    print("Email Security Dashboard")
    print("=" * 60)
    print(f"Period: Last {days} days")
    
    try:
        # Get dashboard statistics
        stats = client.email.get_dash_stats(days=days)
        
        # Get action summary
        actions = client.email.get_action_summary(days=days)
        
        # Get user anomalies
        anomalies = client.email.get_user_anomaly(days=days)
        
        # Get data loss incidents
        data_loss = client.email.get_data_loss(days=days)
        
        # Display overview
        email_stats = stats.get('email_statistics', {})
        print(f"\nEMAIL OVERVIEW:")
        print(f"  Total emails processed: {email_stats.get('total_emails', 0):,}")
        print(f"  Clean emails: {email_stats.get('clean_emails', 0):,}")
        print(f"  Suspicious emails: {email_stats.get('suspicious_emails', 0):,}")
        print(f"  Malicious emails: {email_stats.get('malicious_emails', 0):,}")
        print(f"  Quarantined: {email_stats.get('quarantined', 0):,}")
        print(f"  Blocked: {email_stats.get('blocked', 0):,}")
        
        # Threat breakdown
        threat_breakdown = stats.get('threat_breakdown', {})
        print(f"\nTHREAT BREAKDOWN:")
        for threat_type, count in threat_breakdown.items():
            print(f"  {threat_type.replace('_', ' ').title()}: {count:,}")
        
        # Top threats
        top_threats = stats.get('top_threats', [])
        if top_threats:
            print(f"\nTOP THREATS:")
            for threat in top_threats[:5]:
                trend_icon = "📈" if threat.get('trend') == 'increasing' else "📊" if threat.get('trend') == 'stable' else "📉"
                print(f"  {threat_icon} {threat['threat_type'].title()}: {threat['count']:,} ({threat['percentage']:.1f}%)")
        
        # Action summary
        actions_by_type = actions.get('actions_by_type', {})
        print(f"\nACTIONS TAKEN:")
        total_actions = actions.get('total_actions', 0)
        print(f"  Total actions: {total_actions:,}")
        for action_type, count in actions_by_type.items():
            percentage = (count / total_actions * 100) if total_actions > 0 else 0
            print(f"    {action_type.replace('_', ' ').title()}: {count:,} ({percentage:.1f}%)")
        
        # User anomalies
        anomalous_users = anomalies.get('total_anomalous_users', 0)
        print(f"\nUSER ANOMALIES:")
        print(f"  Anomalous users detected: {anomalous_users}")
        
        anomaly_categories = anomalies.get('anomaly_categories', {})
        for category, count in anomaly_categories.items():
            print(f"    {category.replace('_', ' ').title()}: {count}")
        
        # Data loss incidents
        dl_incidents = data_loss.get('total_incidents', 0)
        print(f"\nDATA LOSS PREVENTION:")
        print(f"  Incidents detected: {dl_incidents}")
        
        if dl_incidents > 0:
            dl_by_type = data_loss.get('data_loss_by_type', {})
            for data_type, count in dl_by_type.items():
                print(f"    {data_type.replace('_', ' ').title()}: {count}")
        
        # Risk assessment
        print(f"\nRISK ASSESSMENT:")
        
        total_emails = email_stats.get('total_emails', 1)
        threat_rate = (email_stats.get('suspicious_emails', 0) + email_stats.get('malicious_emails', 0)) / total_emails * 100
        
        if threat_rate >= 10:
            risk_level = "🔴 HIGH RISK"
        elif threat_rate >= 5:
            risk_level = "🟡 MEDIUM RISK"
        elif threat_rate >= 1:
            risk_level = "🟠 LOW RISK"
        else:
            risk_level = "🟢 MINIMAL RISK"
        
        print(f"  Overall risk level: {risk_level}")
        print(f"  Threat rate: {threat_rate:.2f}%")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        
        recommendations = []
        
        if threat_rate >= 10:
            recommendations.append("• Immediate review of email security policies required")
            recommendations.append("• Consider implementing stricter filtering rules")
        
        if anomalous_users >= 10:
            recommendations.append("• Investigate users with anomalous behavior")
            recommendations.append("• Consider additional user training")
        
        if dl_incidents > 0:
            recommendations.append("• Review data loss prevention policies")
            recommendations.append("• Audit sensitive data sharing practices")
        
        response_time = stats.get('response_metrics', {}).get('average_response_time', 0)
        if response_time > 120:  # 2 minutes
            recommendations.append("• Optimize response time for threat handling")
        
        if not recommendations:
            recommendations.append("• Continue current monitoring practices")
            recommendations.append("• Regular review of security metrics")
        
        for rec in recommendations:
            print(f"  {rec}")
        
        return {
            'stats': stats,
            'actions': actions,
            'anomalies': anomalies,
            'data_loss': data_loss,
            'risk_level': risk_level,
            'recommendations': recommendations
        }
        
    except Exception as e:
        print(f"Error generating dashboard: {e}")
        return None

# Generate dashboard
dashboard = generate_security_dashboard(days=7)
```

### Threat Investigation Workflow

```python
def investigate_suspicious_email(email_uuid):
    """Comprehensive investigation of a suspicious email"""
    
    print(f"Email Threat Investigation")
    print("=" * 50)
    print(f"Email UUID: {email_uuid}")
    
    try:
        # Get detailed email information
        email_details = client.email.get_email(
            uuid=email_uuid,
            include_headers=True
        )
        
        print(f"\nBASIC INFORMATION:")
        print(f"  From: {email_details['sender']['email']}")
        print(f"  To: {', '.join([r['email'] for r in email_details['recipients']])}")
        print(f"  Subject: {email_details['subject']}")
        print(f"  Timestamp: {datetime.fromtimestamp(email_details['timestamp'])}")
        print(f"  Size: {email_details['size']:,} bytes")
        
        # Threat analysis
        threat_analysis = email_details.get('threat_analysis', {})
        overall_score = threat_analysis.get('overall_score', 0)
        
        print(f"\nTHREAT ANALYSIS:")
        print(f"  Overall threat score: {overall_score:.3f}")
        
        if overall_score >= 0.8:
            threat_level = "🔴 HIGH THREAT"
        elif overall_score >= 0.6:
            threat_level = "🟡 MEDIUM THREAT"
        elif overall_score >= 0.3:
            threat_level = "🟠 LOW THREAT"
        else:
            threat_level = "🟢 MINIMAL THREAT"
        
        print(f"  Threat level: {threat_level}")
        
        categories = threat_analysis.get('categories', [])
        if categories:
            print(f"  Threat categories: {', '.join(categories)}")
        
        # Detailed analysis
        details = threat_analysis.get('details', {})
        
        # Link analysis
        link_analysis = details.get('link_analysis', {})
        if link_analysis:
            print(f"\nLINK ANALYSIS:")
            print(f"  Total links: {link_analysis.get('total_links', 0)}")
            print(f"  Suspicious links: {link_analysis.get('suspicious_links', 0)}")
            print(f"  Malicious links: {link_analysis.get('malicious_links', 0)}")
        
        # Attachment analysis
        attachment_analysis = details.get('attachment_analysis', {})
        if attachment_analysis:
            print(f"\nATTACHMENT ANALYSIS:")
            print(f"  Total attachments: {attachment_analysis.get('total_attachments', 0)}")
            print(f"  Clean: {attachment_analysis.get('clean', 0)}")
            print(f"  Suspicious: {attachment_analysis.get('suspicious', 0)}")
            print(f"  Malicious: {attachment_analysis.get('malicious', 0)}")
        
        # List attachments
        attachments = email_details.get('attachments', [])
        if attachments:
            print(f"\nATTACHMENTS:")
            for att in attachments:
                print(f"  • {att['filename']} ({att['type']})")
                print(f"    Size: {att['size']:,} bytes")
                print(f"    Threat score: {att['threat_score']:.3f}")
        
        # Sender reputation
        sender = email_details['sender']
        print(f"\nSENDER ANALYSIS:")
        print(f"  Email: {sender['email']}")
        print(f"  Name: {sender.get('name', 'Unknown')}")
        print(f"  Reputation: {sender.get('reputation', 'Unknown')}/100")
        print(f"  Internal: {'Yes' if sender.get('is_internal', False) else 'No'}")
        
        # Authentication results
        headers = email_details.get('headers', {})
        auth_results = headers.get('authentication_results', {})
        if auth_results:
            print(f"\nAUTHENTICATION:")
            print(f"  SPF: {auth_results.get('spf', 'Unknown')}")
            print(f"  DKIM: {auth_results.get('dkim', 'Unknown')}")
            print(f"  DMARC: {auth_results.get('dmarc', 'Unknown')}")
        
        # Actions taken
        actions_taken = email_details.get('actions_taken', [])
        if actions_taken:
            print(f"\nACTIONS TAKEN:")
            for action in actions_taken:
                action_time = datetime.fromtimestamp(action['timestamp'])
                print(f"  • {action['action'].title()} at {action_time}")
                print(f"    By: {action['user']}")
                print(f"    Reason: {action['reason']}")
        
        # Current status
        status = email_details.get('status', 'unknown')
        print(f"\nCURRENT STATUS: {status.upper()}")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        
        recommendations = []
        
        if overall_score >= 0.8:
            recommendations.append("• Immediately quarantine or delete this email")
            recommendations.append("• Investigate other emails from this sender")
            recommendations.append("• Check if recipients clicked any links")
        elif overall_score >= 0.6:
            recommendations.append("• Quarantine email for further analysis")
            recommendations.append("• Notify recipients about potential threat")
        elif overall_score >= 0.3:
            recommendations.append("• Monitor email closely")
            recommendations.append("• Consider user education about this threat type")
        else:
            recommendations.append("• Email appears legitimate")
            recommendations.append("• Continue normal monitoring")
        
        # Additional recommendations based on specific threats
        if link_analysis.get('malicious_links', 0) > 0:
            recommendations.append("• Block malicious domains identified")
            recommendations.append("• Scan endpoints that may have accessed links")
        
        if attachment_analysis.get('malicious', 0) > 0:
            recommendations.append("• Scan systems for malware execution")
            recommendations.append("• Block file hashes across security tools")
        
        auth_failures = []
        if auth_results.get('spf') == 'fail':
            auth_failures.append('SPF')
        if auth_results.get('dkim') == 'fail':
            auth_failures.append('DKIM')
        if auth_results.get('dmarc') == 'fail':
            auth_failures.append('DMARC')
        
        if auth_failures:
            recommendations.append(f"• Email failed authentication: {', '.join(auth_failures)}")
            recommendations.append("• Consider strengthening email authentication policies")
        
        for rec in recommendations:
            print(f"  {rec}")
        
        return email_details
        
    except Exception as e:
        print(f"Error investigating email: {e}")
        return None

# Example investigation
# suspicious_email_uuid = "550e8400-e29b-41d4-a716-446655440000"
# investigation_result = investigate_suspicious_email(suspicious_email_uuid)
```

### Automated Response System

```python
def automated_email_response(threat_threshold=0.7, days=1):
    """Automated response system for email threats"""
    
    print("Automated Email Response System")
    print("=" * 50)
    print(f"Threat threshold: {threat_threshold}")
    print(f"Processing emails from last {days} day(s)")
    
    # Search for high-threat emails
    search_criteria = {
        "filters": {
            "threat_score_min": threat_threshold,
            "date_range": {
                "start": (datetime.now() - timedelta(days=days)).isoformat(),
                "end": datetime.now().isoformat()
            },
            "status": ["pending", "delivered"]  # Not yet acted upon
        },
        "sort": {
            "field": "threat_score",
            "order": "desc"
        },
        "limit": 100
    }
    
    try:
        search_results = client.email.search_emails(data=search_criteria)
        emails = search_results.get('emails', [])
        
        print(f"\nFound {len(emails)} high-threat emails")
        
        actions_taken = {
            'quarantined': 0,
            'deleted': 0,
            'blocked_senders': 0,
            'errors': 0
        }
        
        for email_info in emails:
            email_uuid = email_info['uuid']
            threat_score = email_info.get('threat_score', 0)
            sender = email_info.get('sender', {})
            
            print(f"\nProcessing email: {email_uuid}")
            print(f"  Threat score: {threat_score:.3f}")
            print(f"  Sender: {sender.get('email', 'Unknown')}")
            
            try:
                # Determine action based on threat score
                if threat_score >= 0.9:
                    # Very high threat - delete immediately
                    action_data = {
                        "action": "delete",
                        "reason": f"Automated deletion: High threat score {threat_score:.3f}",
                        "notify_user": False
                    }
                    client.email.email_action(uuid=email_uuid, data=action_data)
                    actions_taken['deleted'] += 1
                    print(f"  🗑️  Deleted (threat score: {threat_score:.3f})")
                    
                    # Also block sender if external
                    if not sender.get('is_internal', True):
                        block_data = {
                            "action": "block_sender",
                            "reason": f"Automated block: High threat sender {threat_score:.3f}",
                            "scope": "domain"
                        }
                        client.email.email_action(uuid=email_uuid, data=block_data)
                        actions_taken['blocked_senders'] += 1
                        print(f"  🚫 Blocked sender domain")
                
                elif threat_score >= threat_threshold:
                    # High threat - quarantine
                    action_data = {
                        "action": "quarantine",
                        "reason": f"Automated quarantine: Threat score {threat_score:.3f}",
                        "notify_user": True,
                        "duration": 72  # 72 hours
                    }
                    client.email.email_action(uuid=email_uuid, data=action_data)
                    actions_taken['quarantined'] += 1
                    print(f"  📦 Quarantined (threat score: {threat_score:.3f})")
                
            except Exception as e:
                print(f"  ❌ Error processing email: {e}")
                actions_taken['errors'] += 1
        
        # Summary
        print(f"\n" + "="*50)
        print(f"AUTOMATED RESPONSE SUMMARY:")
        print(f"  Emails processed: {len(emails)}")
        print(f"  Deleted: {actions_taken['deleted']}")
        print(f"  Quarantined: {actions_taken['quarantined']}")
        print(f"  Senders blocked: {actions_taken['blocked_senders']}")
        print(f"  Errors: {actions_taken['errors']}")
        
        # Generate report for human review
        if actions_taken['deleted'] > 0 or actions_taken['errors'] > 0:
            print(f"\n🚨 HUMAN REVIEW REQUIRED:")
            if actions_taken['deleted'] > 0:
                print(f"  • {actions_taken['deleted']} emails were automatically deleted")
            if actions_taken['errors'] > 0:
                print(f"  • {actions_taken['errors']} errors occurred during processing")
        
        return actions_taken
        
    except Exception as e:
        print(f"Error in automated response system: {e}")
        return None

# Run automated response
# response_summary = automated_email_response(threat_threshold=0.8, days=1)
```

### User Behavior Analysis

```python
def analyze_user_email_behavior(user_email, days=30):
    """Analyze email behavior patterns for a specific user"""
    
    print(f"User Email Behavior Analysis")
    print("=" * 50)
    print(f"User: {user_email}")
    print(f"Analysis period: {days} days")
    
    try:
        # Search for user's emails
        search_criteria = {
            "filters": {
                "sender": user_email,
                "date_range": {
                    "start": (datetime.now() - timedelta(days=days)).isoformat(),
                    "end": datetime.now().isoformat()
                }
            },
            "sort": {
                "field": "timestamp",
                "order": "desc"
            },
            "limit": 1000  # Analyze up to 1000 emails
        }
        
        search_results = client.email.search_emails(data=search_criteria)
        emails = search_results.get('emails', [])
        
        if not emails:
            print(f"No emails found for user {user_email}")
            return None
        
        # Analyze patterns
        analysis = {
            'total_emails': len(emails),
            'date_range': days,
            'threat_scores': [],
            'recipients': {},
            'domains': {},
            'time_patterns': {},
            'subjects': [],
            'attachments': 0,
            'external_emails': 0,
            'high_threat_emails': 0
        }
        
        for email_info in emails:
            # Threat scores
            threat_score = email_info.get('threat_score', 0)
            analysis['threat_scores'].append(threat_score)
            
            if threat_score >= 0.7:
                analysis['high_threat_emails'] += 1
            
            # Recipients analysis
            recipients = email_info.get('recipients', [])
            for recipient in recipients:
                email_addr = recipient.get('email', '')
                analysis['recipients'][email_addr] = analysis['recipients'].get(email_addr, 0) + 1
                
                # Domain analysis
                if '@' in email_addr:
                    domain = email_addr.split('@')[1]
                    analysis['domains'][domain] = analysis['domains'].get(domain, 0) + 1
                    
                    # External email detection
                    if not email_addr.endswith('@company.com'):  # Adjust for your domain
                        analysis['external_emails'] += 1
            
            # Time patterns
            timestamp = email_info.get('timestamp', 0)
            dt = datetime.fromtimestamp(timestamp)
            hour = dt.hour
            analysis['time_patterns'][hour] = analysis['time_patterns'].get(hour, 0) + 1
            
            # Subject analysis
            subject = email_info.get('subject', '')
            analysis['subjects'].append(subject)
            
            # Attachments
            if email_info.get('attachments'):
                analysis['attachments'] += 1
        
        # Calculate statistics
        threat_scores = analysis['threat_scores']
        avg_threat_score = sum(threat_scores) / len(threat_scores) if threat_scores else 0
        max_threat_score = max(threat_scores) if threat_scores else 0
        
        print(f"\nBEHAVIOR ANALYSIS RESULTS:")
        print(f"  Total emails sent: {analysis['total_emails']:,}")
        print(f"  Average daily emails: {analysis['total_emails'] / days:.1f}")
        print(f"  External emails: {analysis['external_emails']:,} ({analysis['external_emails']/analysis['total_emails']*100:.1f}%)")
        print(f"  Emails with attachments: {analysis['attachments']:,} ({analysis['attachments']/analysis['total_emails']*100:.1f}%)")
        
        print(f"\nTHREAT ANALYSIS:")
        print(f"  Average threat score: {avg_threat_score:.3f}")
        print(f"  Maximum threat score: {max_threat_score:.3f}")
        print(f"  High-threat emails: {analysis['high_threat_emails']:,} ({analysis['high_threat_emails']/analysis['total_emails']*100:.1f}%)")
        
        # Top recipients
        top_recipients = sorted(analysis['recipients'].items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"\nTOP RECIPIENTS:")
        for recipient, count in top_recipients:
            print(f"  {recipient}: {count:,} emails")
        
        # Top domains
        top_domains = sorted(analysis['domains'].items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"\nTOP DOMAINS:")
        for domain, count in top_domains:
            print(f"  {domain}: {count:,} emails")
        
        # Time patterns
        print(f"\nTIME PATTERNS (Emails by hour):")
        time_sorted = sorted(analysis['time_patterns'].items())
        for hour, count in time_sorted:
            bar = "█" * min(count // 5, 20)  # Simple bar chart
            print(f"  {hour:02d}:00 | {bar} {count}")
        
        # Anomaly detection
        print(f"\nANOMALY INDICATORS:")
        anomalies = []
        
        # High threat score anomaly
        if avg_threat_score > 0.5:
            anomalies.append(f"• High average threat score: {avg_threat_score:.3f}")
        
        # High external email ratio
        external_ratio = analysis['external_emails'] / analysis['total_emails']
        if external_ratio > 0.8:
            anomalies.append(f"• High external email ratio: {external_ratio:.1%}")
        
        # Unusual time patterns
        night_emails = sum(analysis['time_patterns'].get(h, 0) for h in range(0, 6))
        night_ratio = night_emails / analysis['total_emails']
        if night_ratio > 0.2:
            anomalies.append(f"• High night-time activity: {night_ratio:.1%}")
        
        # Volume anomaly
        daily_average = analysis['total_emails'] / days
        if daily_average > 100:
            anomalies.append(f"• High email volume: {daily_average:.1f} emails/day")
        
        if anomalies:
            for anomaly in anomalies:
                print(f"  {anomaly}")
        else:
            print(f"  No significant anomalies detected")
        
        # Risk assessment
        risk_score = 0
        if avg_threat_score > 0.5:
            risk_score += 0.3
        if external_ratio > 0.8:
            risk_score += 0.2
        if night_ratio > 0.2:
            risk_score += 0.2
        if daily_average > 100:
            risk_score += 0.3
        
        print(f"\nRISK ASSESSMENT:")
        if risk_score >= 0.7:
            risk_level = "🔴 HIGH RISK"
        elif risk_score >= 0.4:
            risk_level = "🟡 MEDIUM RISK"
        elif risk_score >= 0.2:
            risk_level = "🟠 LOW RISK"
        else:
            risk_level = "🟢 MINIMAL RISK"
        
        print(f"  Risk Level: {risk_level}")
        print(f"  Risk Score: {risk_score:.3f}")
        
        return analysis
        
    except Exception as e:
        print(f"Error analyzing user behavior: {e}")
        return None

# Example user behavior analysis
# user_analysis = analyze_user_email_behavior("user@company.com", days=30)
```

## Error Handling

```python
try:
    # Attempt various email operations
    
    # Get dashboard stats
    stats = client.email.get_dash_stats(days=7)
    print(f"Dashboard stats retrieved successfully")
    
    # Search for emails
    search_data = {
        "filters": {
            "threat_score_min": 0.5
        },
        "limit": 10
    }
    search_results = client.email.search_emails(data=search_data)
    print(f"Found {len(search_results.get('emails', []))} emails")
    
    # Get email details (example UUID)
    email_uuid = "550e8400-e29b-41d4-a716-446655440000"
    email_details = client.email.get_email(
        uuid=email_uuid,
        include_headers=True
    )
    print(f"Email details retrieved for {email_uuid}")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check parameters and data format")
        elif e.response.status_code == 401:
            print("Authentication failed - check tokens")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for Darktrace/Email")
        elif e.response.status_code == 404:
            print("Resource not found - check email UUID or endpoint availability")
        elif e.response.status_code == 429:
            print("Rate limit exceeded - reduce request frequency")
        else:
            print(f"Response: {e.response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
    print("Check network connectivity and host URL")

except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
    print("The response might not be valid JSON")

except ValueError as e:
    print(f"Value error: {e}")
    print("Check that all parameter values are valid")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Darktrace/Email Integration
- **Specialized module**: Specifically designed for Darktrace/Email deployments
- **API endpoints**: Uses `/agemail/` API paths specific to Email security
- **Authentication**: Requires appropriate permissions for Email module access
- **Version compatibility**: Ensure Darktrace/Email version supports these API endpoints

### Dashboard and Statistics
- **Real-time data**: Dashboard statistics reflect current email security status
- **Time-based analysis**: Most statistics support time range filtering
- **Trend analysis**: Historical data helps identify security trends
- **Performance metrics**: Response times and efficiency measurements

### Email Management
- **UUID-based operations**: All email-specific operations use UUID identifiers
- **Action logging**: All actions are logged for audit and compliance
- **Status tracking**: Email status changes are tracked throughout lifecycle
- **Reversible actions**: Some actions (like quarantine) can be reversed

### Search Capabilities
- **Advanced filtering**: Comprehensive search filters for email discovery
- **Performance optimization**: Use appropriate limits and pagination
- **Real-time search**: Search reflects current email status
- **Flexible criteria**: Multiple filter combinations supported

### Threat Analysis
- **Scoring system**: 0.0-1.0 threat scoring with higher scores indicating greater threat
- **Multi-factor analysis**: Links, attachments, sender reputation, authentication
- **Machine learning**: AI-powered threat detection and analysis
- **Continuous updates**: Threat intelligence continuously updated

### User Anomaly Detection
- **Behavioral baselines**: Establishes normal patterns for each user
- **Real-time monitoring**: Continuous monitoring for deviations
- **Risk scoring**: Quantified risk assessment for user activities
- **Investigation support**: Detailed anomaly information for investigations

### Data Loss Prevention
- **Content scanning**: Automated detection of sensitive data patterns
- **Policy enforcement**: Configurable policies for data handling
- **Incident tracking**: Complete audit trail for data loss events
- **Compliance support**: Features designed for regulatory compliance

### Audit and Compliance
- **Complete logging**: All system activities logged for audit
- **Event categorization**: Different event types for analysis
- **User tracking**: Attribution of all actions to specific users
- **Retention policies**: Configurable log retention for compliance

### Performance Considerations
- **API rate limiting**: Respect rate limits for bulk operations
- **Pagination**: Use appropriate pagination for large result sets
- **Selective queries**: Use responsedata parameter to limit data transfer
- **Caching**: Consider caching for frequently accessed reference data

### Security Best Practices
- **Principle of least privilege**: Grant minimum necessary API permissions
- **Action validation**: Verify actions before execution, especially destructive ones
- **Monitoring integration**: Integrate with broader security monitoring systems
- **Regular reviews**: Periodic review of automated actions and policies

### Common Use Cases
- **Security operations**: Real-time threat monitoring and response
- **Incident response**: Investigation and analysis of email-based threats
- **Compliance reporting**: Automated generation of compliance reports
- **User training**: Identification of users requiring additional security training
- **Policy optimization**: Analysis of threat patterns to optimize security policies
