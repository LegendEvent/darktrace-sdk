# IntelFeed Module

The IntelFeed module provides programmatic access to Darktrace's Watched Domains feature, allowing you to manage threat intelligence feeds including domains, IP addresses, and hostnames. This module integrates with Darktrace's threat detection capabilities and can be used for automated threat intelligence management, STIX/TAXII integration, and custom watchlist management.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the intelfeed module
intelfeed = client.intelfeed
```

## Methods Overview

The IntelFeed module provides the following methods:

- **`get()`** - Retrieve watched domains, IPs, and hostnames with filtering options
- **`get_sources()`** - Get available intelligence sources
- **`get_by_source()`** - Get entries from specific source
- **`get_with_details()`** - Get entries with full metadata
- **`update()`** - Add or remove intelligence entries

## Methods

### Get Intelligence Feed

Retrieve watched domains, IP addresses, and hostnames from Darktrace's threat intelligence feeds. This method provides flexible filtering and detail levels for intelligence data.

```python
# Get all watched entries (domains, IPs, hostnames)
all_entries = intelfeed.get()

# Get list of available sources
sources_list = intelfeed.get_sources()

# Get entries from specific source
source_entries = intelfeed.get_by_source("CustomThreatFeed")

# Get entries with full details
detailed_entries = intelfeed.get_with_details()

# Get entries with specific response data
filtered_entries = intelfeed.get(responsedata="name,description")

# Get entries from multiple sources with details
custom_query = intelfeed.get(
    source="ExternalFeed",
    fulldetails=True
)
```

#### Parameters

- `sources` (bool, optional): If True, returns available sources instead of entries
- `source` (str, optional): Restrict entries to specific source (max 64 characters)
- `fulldetails` (bool, optional): If True, returns full metadata for each entry
- `responsedata` (str, optional): Restrict returned JSON to specific fields (comma-separated)

#### Response Structure

```python
# Basic response (list of entries)
[
  "malicious-domain.com",
  "threat-site.net",
  "192.168.1.100",
  "suspicious-host.example.com"
]

# Sources response (when sources=True)
[
  "CustomThreatFeed",
  "ExternalIntelligence", 
  "ManualWatchlist",
  "STIX_TAXII_Feed",
  "IOC_Import"
]

# Full details response (when fulldetails=True)
[
  {
    "name": "malicious-domain.com",
    "description": "Known C2 domain from APT campaign",
    "source": "ThreatIntelligence",
    "strength": "95",
    "type": "domain",
    "added": "2024-01-15T10:30:00Z",
    "expiry": "2024-07-15T10:30:00Z",
    "iagn": true,
    "hostname": false
  },
  {
    "name": "192.168.1.100",
    "description": "Suspicious IP from network scan",
    "source": "NetworkMonitoring",
    "strength": "70",
    "type": "ip",
    "added": "2024-01-15T14:20:00Z",
    "expiry": "2024-02-15T14:20:00Z",
    "iagn": false,
    "hostname": false
  },
  {
    "name": "command-server.evil.com",
    "description": "Command and control hostname",
    "source": "IncidentResponse", 
    "strength": "100",
    "type": "hostname",
    "added": "2024-01-14T09:15:00Z",
    "expiry": null,
    "iagn": true,
    "hostname": true
  }
]

# Filtered response (with responsedata parameter)
[
  {
    "name": "malicious-domain.com",
    "description": "Known C2 domain from APT campaign"
  },
  {
    "name": "192.168.1.100", 
    "description": "Suspicious IP from network scan"
  }
]
```

### Update Intelligence Feed

Add or remove entries from the Darktrace intelligence feeds. This method supports single entries, bulk operations, and various metadata options.

```python
# Add single domain
response = intelfeed.update(
    add_entry="malicious-site.com",
    description="Known malware distribution site",
    source="ThreatIntelligence"
)

# Add multiple entries with expiration
response = intelfeed.update(
    add_list=["threat1.com", "threat2.com", "192.168.1.50"],
    description="IOC batch import from incident",
    source="IncidentResponse",
    expiry="2024-06-30T23:59:59Z"
)

# Add hostname with Antigena integration
response = intelfeed.update(
    add_entry="c2-server.malware.com",
    description="Command and control server",
    source="APT_Investigation",
    is_hostname=True,
    enable_antigena=True
)

# Remove specific entry
response = intelfeed.update(
    remove_entry="old-threat.com",
    source="ThreatIntelligence"
)

# Remove all entries (use with caution)
response = intelfeed.update(remove_all=True)
```

#### Parameters

- `add_entry` (str, optional): Single entry to add (domain, IP address, or hostname)
- `add_list` (List[str], optional): List of entries to add (domains, IP addresses, or hostnames)
- `description` (str, optional): Description for added entries (max 256 characters)
- `source` (str, optional): Source label for added entries (max 64 characters)
- `expiry` (str, optional): Expiration time for added entries (ISO 8601 format)
- `is_hostname` (bool, optional): If True, treat entries as hostnames rather than domains
- `remove_entry` (str, optional): Single entry to remove
- `remove_all` (bool, optional): If True, remove all entries from feed
- `enable_antigena` (bool, optional): If True, enable automatic Antigena Network actions

#### Response Structure

```python
{
  "success": true,
  "added": 3,
  "removed": 0,
  "errors": [],
  "message": "Successfully added 3 entries to intelligence feed",
  "entries": [
    {
      "name": "threat1.com",
      "status": "added",
      "source": "IncidentResponse"
    },
    {
      "name": "threat2.com", 
      "status": "added",
      "source": "IncidentResponse"
    },
    {
      "name": "192.168.1.50",
      "status": "added",
      "source": "IncidentResponse"
    }
  ]
}
```

### Convenience Methods

#### Get Sources

```python
sources = intelfeed.get_sources()
# Returns: ["CustomThreatFeed", "ExternalIntelligence", "ManualWatchlist"]
```

#### Get by Source

```python
source_entries = intelfeed.get_by_source("ThreatIntelligence")
# Returns entries only from specified source
```

#### Get with Details

```python
detailed_entries = intelfeed.get_with_details()
# Returns entries with full metadata (equivalent to fulldetails=True)
```

## Examples

### Threat Intelligence Management

```python
from darktrace import DarktraceClient
import datetime

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get current intelligence overview
print("Current Intelligence Feed Overview")
print("=" * 50)

# Get all sources
sources = client.intelfeed.get_sources()
print(f"Available sources: {len(sources)}")
for source in sources:
    print(f"  - {source}")

# Get entries with details for analysis
all_entries = client.intelfeed.get(fulldetails=True)
print(f"\nTotal intelligence entries: {len(all_entries)}")

# Analyze by type and source
entry_stats = {
    'domains': 0,
    'ips': 0,
    'hostnames': 0,
    'sources': {},
    'with_antigena': 0,
    'expiring_soon': 0
}

current_time = datetime.datetime.now()

for entry in all_entries:
    entry_type = entry.get('type', 'unknown')
    if entry_type in entry_stats:
        entry_stats[entry_type] += 1
    
    # Source analysis
    source = entry.get('source', 'unknown')
    entry_stats['sources'][source] = entry_stats['sources'].get(source, 0) + 1
    
    # Antigena integration
    if entry.get('iagn', False):
        entry_stats['with_antigena'] += 1
    
    # Expiry analysis
    expiry_str = entry.get('expiry')
    if expiry_str:
        try:
            expiry_date = datetime.datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            days_until_expiry = (expiry_date.replace(tzinfo=None) - current_time).days
            if days_until_expiry <= 7:  # Expiring within 7 days
                entry_stats['expiring_soon'] += 1
        except:
            pass

print(f"\nEntry Analysis:")
print(f"  Domains: {entry_stats['domains']}")
print(f"  IP Addresses: {entry_stats['ips']}")
print(f"  Hostnames: {entry_stats['hostnames']}")
print(f"  With Antigena: {entry_stats['with_antigena']}")
print(f"  Expiring soon (7 days): {entry_stats['expiring_soon']}")

print(f"\nEntries by source:")
for source, count in sorted(entry_stats['sources'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {source}: {count}")
```

### Automated IOC Import

```python
# Automated import of Indicators of Compromise
def import_ioc_batch(ioc_list, source_name, description_prefix=""):
    """Import a batch of IOCs with proper categorization"""
    
    # Categorize IOCs by type
    domains = []
    ips = []
    hostnames = []
    
    for ioc in ioc_list:
        ioc = ioc.strip()
        
        # Simple categorization logic
        if '.' in ioc and not ioc.replace('.', '').replace(':', '').isdigit():
            if ioc.count('.') >= 2:  # Likely a domain/hostname
                if ioc.startswith('www.') or 'mail.' in ioc or 'ftp.' in ioc:
                    hostnames.append(ioc)
                else:
                    domains.append(ioc)
            else:
                domains.append(ioc)
        elif ':' in ioc or ioc.replace('.', '').isdigit():  # IP address
            ips.append(ioc)
        else:
            domains.append(ioc)  # Default to domain
    
    print(f"IOC Import for source: {source_name}")
    print(f"Domains: {len(domains)}, IPs: {len(ips)}, Hostnames: {len(hostnames)}")
    
    # Import domains
    if domains:
        try:
            response = client.intelfeed.update(
                add_list=domains,
                description=f"{description_prefix}Domain indicators",
                source=source_name,
                expiry=(datetime.datetime.now() + datetime.timedelta(days=90)).isoformat() + "Z"
            )
            print(f"✅ Added {len(domains)} domains")
            
        except Exception as e:
            print(f"❌ Error adding domains: {e}")
    
    # Import IPs
    if ips:
        try:
            response = client.intelfeed.update(
                add_list=ips,
                description=f"{description_prefix}IP address indicators",
                source=source_name,
                expiry=(datetime.datetime.now() + datetime.timedelta(days=90)).isoformat() + "Z"
            )
            print(f"✅ Added {len(ips)} IP addresses")
            
        except Exception as e:
            print(f"❌ Error adding IPs: {e}")
    
    # Import hostnames
    if hostnames:
        try:
            response = client.intelfeed.update(
                add_list=hostnames,
                description=f"{description_prefix}Hostname indicators",
                source=source_name,
                is_hostname=True,
                expiry=(datetime.datetime.now() + datetime.timedelta(days=90)).isoformat() + "Z"
            )
            print(f"✅ Added {len(hostnames)} hostnames")
            
        except Exception as e:
            print(f"❌ Error adding hostnames: {e}")

# Example IOC list
sample_iocs = [
    "malicious-domain.com",
    "evil-site.net", 
    "192.168.1.100",
    "10.0.0.50",
    "c2-server.attacker.com",
    "www.phishing-site.org",
    "mail.compromised-domain.com"
]

# Import the IOCs
import_ioc_batch(
    sample_iocs, 
    "Incident_2024_001", 
    "IOCs from security incident #2024-001: "
)
```

### Intelligence Feed Maintenance

```python
# Regular maintenance of intelligence feeds
def maintain_intelligence_feeds():
    print("Intelligence Feed Maintenance")
    print("=" * 50)
    
    # Get all entries with details
    all_entries = client.intelfeed.get(fulldetails=True)
    
    current_time = datetime.datetime.now()
    expired_entries = []
    expiring_soon = []
    invalid_entries = []
    
    for entry in all_entries:
        name = entry.get('name', '')
        expiry_str = entry.get('expiry')
        
        # Check expiry
        if expiry_str:
            try:
                expiry_date = datetime.datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
                
                if expiry_date.replace(tzinfo=None) < current_time:
                    expired_entries.append(entry)
                elif (expiry_date.replace(tzinfo=None) - current_time).days <= 7:
                    expiring_soon.append(entry)
                    
            except Exception as e:
                print(f"Invalid expiry format for {name}: {expiry_str}")
                invalid_entries.append(entry)
    
    print(f"Maintenance Summary:")
    print(f"  Total entries: {len(all_entries)}")
    print(f"  Expired entries: {len(expired_entries)}")
    print(f"  Expiring soon (7 days): {len(expiring_soon)}")
    print(f"  Invalid entries: {len(invalid_entries)}")
    
    # Remove expired entries
    if expired_entries:
        print(f"\nRemoving {len(expired_entries)} expired entries:")
        
        for entry in expired_entries[:10]:  # Remove first 10 for demonstration
            try:
                response = client.intelfeed.update(remove_entry=entry.get('name'))
                if response.get('success'):
                    print(f"  ✅ Removed: {entry.get('name')}")
                else:
                    print(f"  ❌ Failed to remove: {entry.get('name')}")
                    
            except Exception as e:
                print(f"  ❌ Error removing {entry.get('name')}: {e}")
    
    # Report expiring entries
    if expiring_soon:
        print(f"\nEntries expiring soon:")
        for entry in expiring_soon[:5]:  # Show first 5
            name = entry.get('name')
            expiry = entry.get('expiry')
            source = entry.get('source')
            print(f"  {name} (Source: {source}, Expires: {expiry})")
    
    return {
        'total': len(all_entries),
        'expired': len(expired_entries),
        'expiring_soon': len(expiring_soon),
        'invalid': len(invalid_entries)
    }

# Run maintenance
maintenance_results = maintain_intelligence_feeds()
```

### Source-Based Intelligence Management

```python
# Manage intelligence by source
def manage_by_source():
    sources = client.intelfeed.get_sources()
    
    print("Source-Based Intelligence Management")
    print("=" * 60)
    
    for source in sources:
        print(f"\nSource: {source}")
        
        # Get entries from this source
        source_entries = client.intelfeed.get_by_source(source)
        print(f"  Total entries: {len(source_entries)}")
        
        # Get detailed entries for analysis
        detailed_entries = client.intelfeed.get(source=source, fulldetails=True)
        
        # Analyze source statistics
        stats = {
            'domains': 0,
            'ips': 0,
            'hostnames': 0,
            'with_antigena': 0,
            'permanent': 0
        }
        
        for entry in detailed_entries:
            entry_type = entry.get('type', 'unknown')
            if entry_type in stats:
                stats[entry_type] += 1
            
            if entry.get('iagn', False):
                stats['with_antigena'] += 1
            
            if not entry.get('expiry'):
                stats['permanent'] += 1
        
        print(f"    Domains: {stats['domains']}")
        print(f"    IPs: {stats['ips']}")
        print(f"    Hostnames: {stats['hostnames']}")
        print(f"    With Antigena: {stats['with_antigena']}")
        print(f"    Permanent entries: {stats['permanent']}")
        
        # Show sample entries
        if detailed_entries:
            print(f"  Sample entries:")
            for entry in detailed_entries[:3]:
                name = entry.get('name')
                description = entry.get('description', 'No description')
                print(f"    {name}: {description}")

# Run source management
manage_by_source()
```

### STIX/TAXII Integration Simulation

```python
# Simulate STIX/TAXII feed integration
def simulate_stix_taxii_integration():
    print("STIX/TAXII Integration Simulation")
    print("=" * 50)
    
    # Simulated STIX indicators (would come from actual STIX/TAXII feed)
    stix_indicators = [
        {
            "value": "malware-c2.badguys.com",
            "type": "domain-name",
            "description": "Malware C2 domain from STIX feed",
            "confidence": 85,
            "valid_until": "2024-06-30T23:59:59Z"
        },
        {
            "value": "198.51.100.42",
            "type": "ipv4-addr", 
            "description": "Known malicious IP from threat intel",
            "confidence": 95,
            "valid_until": "2024-05-31T23:59:59Z"
        },
        {
            "value": "evil-server.attacker.org",
            "type": "hostname",
            "description": "Command server hostname",
            "confidence": 90,
            "valid_until": "2024-07-31T23:59:59Z"
        }
    ]
    
    # Process STIX indicators
    for indicator in stix_indicators:
        value = indicator["value"]
        ioc_type = indicator["type"]
        description = f"STIX/TAXII: {indicator['description']} (Confidence: {indicator['confidence']}%)"
        expiry = indicator["valid_until"]
        
        # Determine if hostname
        is_hostname = ioc_type == "hostname"
        
        # Add to intelligence feed
        try:
            response = client.intelfeed.update(
                add_entry=value,
                description=description,
                source="STIX_TAXII_Feed",
                expiry=expiry,
                is_hostname=is_hostname,
                enable_antigena=indicator["confidence"] >= 90  # High confidence gets Antigena
            )
            
            if response.get('success'):
                print(f"✅ Added {ioc_type}: {value}")
            else:
                print(f"❌ Failed to add {ioc_type}: {value}")
                
        except Exception as e:
            print(f"❌ Error adding {value}: {e}")
    
    # Verify additions
    stix_entries = client.intelfeed.get_by_source("STIX_TAXII_Feed")
    print(f"\nTotal STIX/TAXII entries now: {len(stix_entries)}")

# Run STIX/TAXII simulation
simulate_stix_taxii_integration()
```

### Intelligence Feed Reporting

```python
# Generate comprehensive intelligence feed report
def generate_intelligence_report():
    print("Intelligence Feed Report")
    print("=" * 50)
    
    # Get all entries with details
    all_entries = client.intelfeed.get(fulldetails=True)
    
    # Initialize report data
    report = {
        'total_entries': len(all_entries),
        'by_type': {'domains': 0, 'ips': 0, 'hostnames': 0},
        'by_source': {},
        'antigena_enabled': 0,
        'expiry_analysis': {'permanent': 0, 'expiring_30d': 0, 'expiring_7d': 0, 'expired': 0},
        'top_sources': [],
        'recent_additions': []
    }
    
    current_time = datetime.datetime.now()
    
    # Analyze each entry
    for entry in all_entries:
        # Type analysis
        entry_type = entry.get('type', 'unknown')
        if entry_type in report['by_type']:
            report['by_type'][entry_type] += 1
        
        # Source analysis
        source = entry.get('source', 'unknown')
        report['by_source'][source] = report['by_source'].get(source, 0) + 1
        
        # Antigena analysis
        if entry.get('iagn', False):
            report['antigena_enabled'] += 1
        
        # Expiry analysis
        expiry_str = entry.get('expiry')
        if not expiry_str:
            report['expiry_analysis']['permanent'] += 1
        else:
            try:
                expiry_date = datetime.datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
                days_until_expiry = (expiry_date.replace(tzinfo=None) - current_time).days
                
                if days_until_expiry < 0:
                    report['expiry_analysis']['expired'] += 1
                elif days_until_expiry <= 7:
                    report['expiry_analysis']['expiring_7d'] += 1
                elif days_until_expiry <= 30:
                    report['expiry_analysis']['expiring_30d'] += 1
            except:
                pass
        
        # Recent additions (check if added field exists and is recent)
        added_str = entry.get('added')
        if added_str:
            try:
                added_date = datetime.datetime.fromisoformat(added_str.replace('Z', '+00:00'))
                if (current_time - added_date.replace(tzinfo=None)).days <= 7:
                    report['recent_additions'].append(entry)
            except:
                pass
    
    # Generate top sources
    report['top_sources'] = sorted(report['by_source'].items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Display report
    print(f"Total Intelligence Entries: {report['total_entries']}")
    print(f"\nBy Type:")
    for entry_type, count in report['by_type'].items():
        percentage = (count / report['total_entries']) * 100 if report['total_entries'] > 0 else 0
        print(f"  {entry_type.title()}: {count} ({percentage:.1f}%)")
    
    print(f"\nAntigena Integration: {report['antigena_enabled']} entries ({(report['antigena_enabled']/report['total_entries']*100):.1f}%)")
    
    print(f"\nExpiry Analysis:")
    for category, count in report['expiry_analysis'].items():
        percentage = (count / report['total_entries']) * 100 if report['total_entries'] > 0 else 0
        print(f"  {category.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
    
    print(f"\nTop Sources:")
    for source, count in report['top_sources']:
        percentage = (count / report['total_entries']) * 100 if report['total_entries'] > 0 else 0
        print(f"  {source}: {count} ({percentage:.1f}%)")
    
    print(f"\nRecent Additions (Last 7 days): {len(report['recent_additions'])}")
    for entry in report['recent_additions'][:5]:  # Show first 5
        name = entry.get('name')
        source = entry.get('source')
        added = entry.get('added', 'Unknown')
        print(f"  {name} (Source: {source}, Added: {added})")
    
    return report

# Generate report
intelligence_report = generate_intelligence_report()
```

## Error Handling

```python
try:
    # Attempt to get intelligence feed entries
    entries = client.intelfeed.get(fulldetails=True)
    
    print(f"Retrieved {len(entries)} intelligence entries")
    
    # Process entries
    for entry in entries[:5]:  # Process first 5
        name = entry.get('name', 'Unknown')
        source = entry.get('source', 'Unknown')
        description = entry.get('description', 'No description')
        
        print(f"Entry: {name}")
        print(f"  Source: {source}")
        print(f"  Description: {description}")
    
    # Attempt to add new entry
    try:
        response = client.intelfeed.update(
            add_entry="test-domain.example.com",
            description="Test entry for API validation",
            source="API_Test"
        )
        
        if response.get('success'):
            print(f"Successfully added test entry")
            
            # Remove test entry
            cleanup_response = client.intelfeed.update(
                remove_entry="test-domain.example.com"
            )
            
            if cleanup_response.get('success'):
                print(f"Successfully removed test entry")
                
        else:
            print("Failed to add test entry")
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print("Bad request - check entry format and parameters")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for intelfeed updates")
        elif e.response.status_code == 422:
            print("Invalid data - check entry format and source name")
        else:
            print(f"Error updating intelligence feed: {e}")
            
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 403:
            print("Access denied - check API permissions for intelfeed endpoint")
        elif e.response.status_code == 404:
            print("Intelligence feed endpoint not found")
        else:
            print(f"Response: {e.response.text}")
            
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Intelligence Entry Types
- **Domains**: Domain names like "example.com" (automatically detected)
- **IP Addresses**: IPv4/IPv6 addresses like "192.168.1.1" 
- **Hostnames**: Specific host names like "mail.example.com" (requires is_hostname=True)
- **Automatic detection**: System attempts to categorize entries automatically

### Source Management
- **Source labels**: Maximum 64 characters, used for organization and filtering
- **Multiple sources**: Different teams/feeds can use separate sources
- **Source persistence**: Sources are created automatically when first used
- **Source cleanup**: Empty sources may be automatically removed

### Expiry and Lifecycle
- **Expiry format**: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- **Permanent entries**: Entries without expiry remain until manually removed
- **Automatic cleanup**: Expired entries may be automatically removed by system
- **Grace period**: Check if system provides grace period for expired entries

### Antigena Integration
- **Automatic actions**: Entries with iagn=True trigger automatic Antigena responses
- **Action types**: May include blocking, alerting, or monitoring actions
- **Performance impact**: Consider system load when enabling Antigena for many entries
- **Testing**: Test Antigena integration with low-risk entries first

### Content Validation
- **Domain validation**: System validates domain name format
- **IP validation**: System validates IPv4/IPv6 address format
- **Hostname validation**: System validates hostname format when is_hostname=True
- **Duplicate handling**: System may reject or update duplicate entries

### Performance Considerations
- **Batch operations**: Use add_list for adding multiple entries efficiently
- **Rate limiting**: Consider API rate limits for large imports
- **Response time**: Large intelligence feeds may impact query performance
- **Caching**: Intelligence data may be cached, updates may take time to propagate

### Integration Patterns
- **STIX/TAXII**: Common pattern for automated threat intelligence imports
- **IOC feeds**: Regular imports from threat intelligence providers
- **Incident response**: Manual additions during security incidents
- **Automated workflows**: Integration with SIEM and security orchestration tools

### Best Practices
- **Source organization**: Use descriptive source names for different intelligence types
- **Expiry management**: Set appropriate expiry dates to avoid stale intelligence
- **Description quality**: Provide meaningful descriptions for investigation context
- **Regular maintenance**: Implement regular cleanup of expired entries
- **Testing workflow**: Test additions/removals in non-production environment first

### Common Use Cases
- **Threat intelligence import**: Automated import from external threat feeds
- **Incident response**: Manual addition of IOCs during investigations
- **Watchlist management**: Maintenance of custom domain/IP watchlists
- **Compliance**: Meeting regulatory requirements for threat monitoring
- **Integration**: Connecting with external security tools and feeds

### Data Retention
- **Persistence**: Intelligence entries persist until manually removed or expired
- **Backup**: Consider backup strategy for critical intelligence data
- **History**: System may maintain history of additions/removals
- **Export**: Use get() methods to export intelligence data for backup/analysis
