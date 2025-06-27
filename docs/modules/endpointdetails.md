# EndpointDetails Module

The EndpointDetails module provides comprehensive information about external endpoints that devices in your network have communicated with. This includes details about remote IP addresses and hostnames, their characteristics, reputation data, device interaction history, and rarity scoring.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the endpointdetails module
endpointdetails = client.endpointdetails
```

## Methods Overview

The EndpointDetails module provides the following method:

- **`get()`** - Retrieve detailed information about external endpoints

## Methods

### Get Endpoint Details

Retrieve comprehensive information about external endpoints, including IP addresses and hostnames that devices in your network have communicated with.

```python
# Get details for a specific IP address
ip_details = endpointdetails.get(ip="8.8.8.8")

# Get details for a specific hostname
hostname_details = endpointdetails.get(hostname="google.com")

# Get comprehensive details with additional information
full_details = endpointdetails.get(
    ip="1.1.1.1",
    additionalinfo=True,
    devices=True,
    score=True
)

# Get specific data fields only
basic_info = endpointdetails.get(
    hostname="github.com",
    responsedata="hostname,ip,country"
)
```

#### Parameters

- `ip` (str, optional): Return data for this specific IP address
- `hostname` (str, optional): Return data for this specific hostname  
- `additionalinfo` (bool, optional): Include additional endpoint information (geolocation, ASN, etc.)
- `devices` (bool, optional): Include list of devices that recently connected to this endpoint
- `score` (bool, optional): Include rarity/risk scoring data for this endpoint
- `responsedata` (str, optional): Restrict returned JSON to specific fields (comma-separated)

#### Response Structure

```python
{
  "ip": "8.8.8.8",
  "hostname": "dns.google",
  "country": "United States",
  "countrycode": "US",
  "port": 53,
  "protocol": "UDP",
  "firstseen": 1635724800,
  "lastseen": 1704067200,
  "connections": 15420,
  "totaltraffic": 52428800,  # bytes
  
  # With additionalinfo=True
  "additionalinfo": {
    "asn": "AS15169",
    "asnname": "Google LLC",
    "city": "Mountain View",
    "region": "California",
    "timezone": "America/Los_Angeles",
    "isp": "Google",
    "organization": "Google",
    "latitude": 37.4056,
    "longitude": -122.0775,
    "accuracy": 100,
    "threatcategories": [],
    "reputationscore": 95,
    "tags": ["search_engine", "dns_server", "legitimate"]
  },
  
  # With devices=True
  "devices": [
    {
      "deviceid": 12345,
      "hostname": "workstation-01",
      "ip": "192.168.1.100",
      "connections": 45,
      "firstconnection": 1703980800,
      "lastconnection": 1704067200,
      "totaltraffic": 1048576,
      "ports": [53, 443],
      "protocols": ["UDP", "TCP"]
    },
    {
      "deviceid": 12346,
      "hostname": "server-01", 
      "ip": "192.168.1.200",
      "connections": 12,
      "firstconnection": 1704000000,
      "lastconnection": 1704060000,
      "totaltraffic": 524288,
      "ports": [443],
      "protocols": ["TCP"]
    }
  ],
  
  # With score=True
  "score": {
    "rarity": 0.15,  # Lower = more rare
    "risk": 0.05,    # Higher = more risk
    "category": "common",
    "factors": {
      "geographic_rarity": 0.1,
      "temporal_rarity": 0.2,
      "protocol_rarity": 0.05,
      "connection_pattern": 0.15
    },
    "explanation": "Common legitimate service with established reputation",
    "confidence": 0.92
  }
}

# Hostname-based response
{
  "hostname": "malicious-site.example",
  "ip": "203.0.113.42",
  "country": "Unknown",
  "countrycode": "XX",
  "port": 80,
  "protocol": "TCP",
  "firstseen": 1704000000,
  "lastseen": 1704003600,
  "connections": 3,
  "totaltraffic": 15360,
  
  "additionalinfo": {
    "asn": "AS64512",
    "asnname": "Reserved AS",
    "city": "Unknown",
    "region": "Unknown",
    "threatcategories": ["malware", "command_control"],
    "reputationscore": 15,
    "tags": ["suspicious", "newly_registered", "low_reputation"]
  },
  
  "score": {
    "rarity": 0.95,  # Very rare
    "risk": 0.85,    # High risk
    "category": "suspicious",
    "factors": {
      "geographic_rarity": 0.9,
      "temporal_rarity": 0.95,
      "reputation_score": 0.85,
      "threat_intelligence": 0.9
    },
    "explanation": "Rare endpoint with poor reputation and threat indicators",
    "confidence": 0.88
  }
}

# With responsedata="hostname,ip,country"
{
  "hostname": "github.com",
  "ip": "140.82.112.3", 
  "country": "United States"
}
```

## Examples

### Comprehensive Endpoint Analysis

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def analyze_endpoint(identifier, is_hostname=False):
    """Perform comprehensive analysis of an endpoint"""
    
    print(f"Analyzing endpoint: {identifier}")
    print("=" * 60)
    
    try:
        # Get comprehensive endpoint details
        if is_hostname:
            details = client.endpointdetails.get(
                hostname=identifier,
                additionalinfo=True,
                devices=True,
                score=True
            )
        else:
            details = client.endpointdetails.get(
                ip=identifier,
                additionalinfo=True,
                devices=True,
                score=True
            )
        
        # Basic information
        print("BASIC INFORMATION:")
        print(f"  IP: {details.get('ip', 'Unknown')}")
        print(f"  Hostname: {details.get('hostname', 'Unknown')}")
        print(f"  Country: {details.get('country', 'Unknown')} ({details.get('countrycode', 'XX')})")
        print(f"  Primary Port: {details.get('port', 'Unknown')}")
        print(f"  Primary Protocol: {details.get('protocol', 'Unknown')}")
        
        # Traffic statistics
        print(f"\nTRAFFIC STATISTICS:")
        print(f"  First Seen: {details.get('firstseen', 'Unknown')}")
        print(f"  Last Seen: {details.get('lastseen', 'Unknown')}")
        print(f"  Total Connections: {details.get('connections', 0):,}")
        
        total_traffic = details.get('totaltraffic', 0)
        if total_traffic > 0:
            if total_traffic >= 1073741824:  # GB
                traffic_str = f"{total_traffic / 1073741824:.2f} GB"
            elif total_traffic >= 1048576:  # MB
                traffic_str = f"{total_traffic / 1048576:.2f} MB"
            elif total_traffic >= 1024:  # KB
                traffic_str = f"{total_traffic / 1024:.2f} KB"
            else:
                traffic_str = f"{total_traffic} bytes"
            print(f"  Total Traffic: {traffic_str}")
        
        # Additional information
        if 'additionalinfo' in details:
            additional = details['additionalinfo']
            print(f"\nADDITIONAL INFORMATION:")
            print(f"  ASN: {additional.get('asn', 'Unknown')}")
            print(f"  ISP: {additional.get('isp', 'Unknown')}")
            print(f"  Organization: {additional.get('organization', 'Unknown')}")
            print(f"  Location: {additional.get('city', 'Unknown')}, {additional.get('region', 'Unknown')}")
            
            # Reputation and threat information
            reputation = additional.get('reputationscore', 0)
            print(f"  Reputation Score: {reputation}/100")
            
            threat_categories = additional.get('threatcategories', [])
            if threat_categories:
                print(f"  Threat Categories: {', '.join(threat_categories)}")
            
            tags = additional.get('tags', [])
            if tags:
                print(f"  Tags: {', '.join(tags)}")
        
        # Risk scoring
        if 'score' in details:
            score_info = details['score']
            print(f"\nRISK ANALYSIS:")
            print(f"  Rarity Score: {score_info.get('rarity', 0):.3f} (lower = more rare)")
            print(f"  Risk Score: {score_info.get('risk', 0):.3f} (higher = more risk)")
            print(f"  Category: {score_info.get('category', 'Unknown')}")
            print(f"  Confidence: {score_info.get('confidence', 0):.2%}")
            
            explanation = score_info.get('explanation', '')
            if explanation:
                print(f"  Analysis: {explanation}")
            
            # Risk factors
            factors = score_info.get('factors', {})
            if factors:
                print(f"  Risk Factors:")
                for factor, value in factors.items():
                    print(f"    {factor.replace('_', ' ').title()}: {value:.3f}")
        
        # Connected devices
        if 'devices' in details:
            devices = details['devices']
            print(f"\nCONNECTED DEVICES ({len(devices)} devices):")
            
            for i, device in enumerate(devices[:10]):  # Show first 10 devices
                print(f"  Device {i+1}:")
                print(f"    Hostname: {device.get('hostname', 'Unknown')}")
                print(f"    IP: {device.get('ip', 'Unknown')}")
                print(f"    Connections: {device.get('connections', 0)}")
                print(f"    Ports: {', '.join(map(str, device.get('ports', [])))}")
                print(f"    Protocols: {', '.join(device.get('protocols', []))}")
                
                device_traffic = device.get('totaltraffic', 0)
                if device_traffic > 0:
                    if device_traffic >= 1048576:  # MB
                        traffic_str = f"{device_traffic / 1048576:.2f} MB"
                    elif device_traffic >= 1024:  # KB
                        traffic_str = f"{device_traffic / 1024:.2f} KB"
                    else:
                        traffic_str = f"{device_traffic} bytes"
                    print(f"    Traffic: {traffic_str}")
            
            if len(devices) > 10:
                print(f"    ... and {len(devices) - 10} more devices")
        
        # Risk assessment
        risk_level = "Unknown"
        if 'score' in details:
            risk_score = details['score'].get('risk', 0)
            if risk_score >= 0.8:
                risk_level = "HIGH RISK ⚠️"
            elif risk_score >= 0.6:
                risk_level = "MEDIUM RISK ⚡"
            elif risk_score >= 0.3:
                risk_level = "LOW RISK 📊"
            else:
                risk_level = "MINIMAL RISK ✅"
        
        print(f"\nOVERALL ASSESSMENT: {risk_level}")
        
        return details
        
    except Exception as e:
        print(f"Error analyzing endpoint {identifier}: {e}")
        return None

# Example analyses
endpoints_to_analyze = [
    ("8.8.8.8", False),           # Google DNS
    ("google.com", True),         # Google hostname
    ("1.1.1.1", False),          # Cloudflare DNS
    ("github.com", True),         # GitHub
]

for endpoint, is_hostname in endpoints_to_analyze:
    endpoint_data = analyze_endpoint(endpoint, is_hostname)
    if endpoint_data:
        print(f"\n{'='*80}\n")
```

### Threat Intelligence Integration

```python
# Integrate endpoint details with threat intelligence
def threat_intelligence_lookup(endpoint_ip):
    """Combine endpoint details with threat intelligence analysis"""
    
    print(f"Threat Intelligence Analysis: {endpoint_ip}")
    print("=" * 50)
    
    try:
        # Get endpoint details with all available information
        details = client.endpointdetails.get(
            ip=endpoint_ip,
            additionalinfo=True,
            score=True
        )
        
        # Extract threat-related information
        threat_indicators = []
        risk_score = 0
        
        if 'additionalinfo' in details:
            additional = details['additionalinfo']
            
            # Check reputation score
            reputation = additional.get('reputationscore', 50)
            if reputation < 30:
                threat_indicators.append(f"Low reputation score: {reputation}/100")
                risk_score += 0.3
            
            # Check threat categories
            threat_categories = additional.get('threatcategories', [])
            if threat_categories:
                threat_indicators.append(f"Threat categories: {', '.join(threat_categories)}")
                risk_score += 0.4 * len(threat_categories)
            
            # Check suspicious tags
            suspicious_tags = ['suspicious', 'malware', 'botnet', 'phishing', 'newly_registered']
            tags = additional.get('tags', [])
            found_suspicious = [tag for tag in tags if tag in suspicious_tags]
            if found_suspicious:
                threat_indicators.append(f"Suspicious tags: {', '.join(found_suspicious)}")
                risk_score += 0.2 * len(found_suspicious)
        
        # Check rarity score
        if 'score' in details:
            score_info = details['score']
            rarity = score_info.get('rarity', 0)
            endpoint_risk = score_info.get('risk', 0)
            
            if rarity > 0.8:  # Very rare
                threat_indicators.append(f"Very rare endpoint (rarity: {rarity:.3f})")
                risk_score += 0.2
            
            risk_score = max(risk_score, endpoint_risk)
        
        # Generate threat assessment
        print("THREAT ASSESSMENT:")
        if risk_score >= 0.8:
            threat_level = "🔴 HIGH THREAT"
        elif risk_score >= 0.6:
            threat_level = "🟡 MEDIUM THREAT"
        elif risk_score >= 0.3:
            threat_level = "🟠 LOW THREAT"
        else:
            threat_level = "🟢 MINIMAL THREAT"
        
        print(f"  Threat Level: {threat_level}")
        print(f"  Risk Score: {risk_score:.3f}")
        
        if threat_indicators:
            print(f"  Threat Indicators:")
            for indicator in threat_indicators:
                print(f"    • {indicator}")
        else:
            print(f"  No significant threat indicators found")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        if risk_score >= 0.8:
            print("  • Block this endpoint immediately")
            print("  • Investigate devices that connected to this endpoint")
            print("  • Check for signs of compromise on connected devices")
        elif risk_score >= 0.6:
            print("  • Monitor connections to this endpoint closely")
            print("  • Consider blocking if no legitimate business need")
            print("  • Review connection patterns for anomalies")
        elif risk_score >= 0.3:
            print("  • Monitor periodically")
            print("  • Document legitimate use cases if any")
        else:
            print("  • Continue normal monitoring")
            print("  • Endpoint appears legitimate")
        
        return {
            'endpoint': endpoint_ip,
            'threat_level': threat_level,
            'risk_score': risk_score,
            'indicators': threat_indicators,
            'details': details
        }
        
    except Exception as e:
        print(f"Error in threat intelligence lookup: {e}")
        return None

# Example threat intelligence analysis
suspicious_ips = [
    "203.0.113.42",  # Example suspicious IP
    "198.51.100.99", # Another example
    "8.8.8.8"        # Known legitimate IP for comparison
]

for ip in suspicious_ips:
    threat_analysis = threat_intelligence_lookup(ip)
    if threat_analysis:
        print(f"\n{'-'*60}\n")
```

### Endpoint Monitoring and Alerting

```python
# Monitor endpoints for changes and suspicious activity
def monitor_endpoint_changes(endpoints, threshold_hours=24):
    """Monitor endpoints for recent changes or suspicious activity"""
    
    import time
    from datetime import datetime, timedelta
    
    print("Endpoint Monitoring Report")
    print("=" * 50)
    print(f"Monitoring {len(endpoints)} endpoints")
    print(f"Alert threshold: {threshold_hours} hours")
    
    alerts = []
    current_time = int(time.time())
    threshold_timestamp = current_time - (threshold_hours * 3600)
    
    for endpoint in endpoints:
        try:
            # Determine if it's IP or hostname
            is_hostname = not all(c.isdigit() or c == '.' for c in endpoint)
            
            if is_hostname:
                details = client.endpointdetails.get(
                    hostname=endpoint,
                    additionalinfo=True,
                    devices=True,
                    score=True
                )
            else:
                details = client.endpointdetails.get(
                    ip=endpoint,
                    additionalinfo=True,
                    devices=True,
                    score=True
                )
            
            endpoint_alerts = []
            
            # Check for recent activity
            last_seen = details.get('lastseen', 0)
            if last_seen > threshold_timestamp:
                endpoint_alerts.append(f"Recent activity detected (last seen: {datetime.fromtimestamp(last_seen)})")
            
            # Check risk score
            if 'score' in details:
                risk_score = details['score'].get('risk', 0)
                if risk_score >= 0.7:
                    endpoint_alerts.append(f"High risk score: {risk_score:.3f}")
            
            # Check reputation
            if 'additionalinfo' in details:
                reputation = details['additionalinfo'].get('reputationscore', 100)
                if reputation < 40:
                    endpoint_alerts.append(f"Low reputation score: {reputation}/100")
                
                threat_categories = details['additionalinfo'].get('threatcategories', [])
                if threat_categories:
                    endpoint_alerts.append(f"Threat categories: {', '.join(threat_categories)}")
            
            # Check device connections
            if 'devices' in details:
                recent_devices = 0
                for device in details['devices']:
                    last_connection = device.get('lastconnection', 0)
                    if last_connection > threshold_timestamp:
                        recent_devices += 1
                
                if recent_devices > 0:
                    endpoint_alerts.append(f"{recent_devices} devices connected recently")
            
            # Report findings
            print(f"\nEndpoint: {endpoint}")
            if endpoint_alerts:
                print("  🚨 ALERTS:")
                for alert in endpoint_alerts:
                    print(f"    • {alert}")
                alerts.extend([(endpoint, alert) for alert in endpoint_alerts])
            else:
                print("  ✅ No alerts")
                
        except Exception as e:
            print(f"\nEndpoint: {endpoint}")
            print(f"  ❌ ERROR: {e}")
    
    # Summary
    print(f"\n" + "="*50)
    print(f"MONITORING SUMMARY:")
    print(f"  Total endpoints monitored: {len(endpoints)}")
    print(f"  Total alerts generated: {len(alerts)}")
    
    if alerts:
        print(f"\nALERT SUMMARY:")
        alert_counts = {}
        for endpoint, alert in alerts:
            alert_type = alert.split(':')[0]
            alert_counts[alert_type] = alert_counts.get(alert_type, 0) + 1
        
        for alert_type, count in sorted(alert_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {alert_type}: {count} alerts")
    
    return alerts

# Example monitoring
endpoints_to_monitor = [
    "8.8.8.8",
    "1.1.1.1", 
    "google.com",
    "github.com",
    "suspicious-domain.example"
]

monitoring_alerts = monitor_endpoint_changes(endpoints_to_monitor, threshold_hours=48)
```

### Bulk Endpoint Analysis

```python
# Analyze multiple endpoints efficiently
def bulk_endpoint_analysis(endpoint_list, include_devices=False):
    """Perform bulk analysis of multiple endpoints"""
    
    print(f"Bulk Endpoint Analysis")
    print("=" * 50)
    print(f"Analyzing {len(endpoint_list)} endpoints")
    
    results = {
        'successful': [],
        'failed': [],
        'high_risk': [],
        'statistics': {
            'total_endpoints': len(endpoint_list),
            'successful_lookups': 0,
            'failed_lookups': 0,
            'high_risk_count': 0,
            'average_risk_score': 0.0
        }
    }
    
    risk_scores = []
    
    for i, endpoint in enumerate(endpoint_list, 1):
        try:
            print(f"\nProcessing {i}/{len(endpoint_list)}: {endpoint}")
            
            # Determine endpoint type
            is_hostname = not all(c.isdigit() or c == '.' for c in endpoint)
            
            # Get endpoint details
            if is_hostname:
                details = client.endpointdetails.get(
                    hostname=endpoint,
                    additionalinfo=True,
                    devices=include_devices,
                    score=True
                )
            else:
                details = client.endpointdetails.get(
                    ip=endpoint,
                    additionalinfo=True,
                    devices=include_devices,
                    score=True
                )
            
            # Extract key information
            analysis = {
                'endpoint': endpoint,
                'ip': details.get('ip', 'Unknown'),
                'hostname': details.get('hostname', 'Unknown'),
                'country': details.get('country', 'Unknown'),
                'connections': details.get('connections', 0),
                'risk_score': 0.0,
                'reputation': 100,
                'threat_categories': [],
                'device_count': 0
            }
            
            # Risk scoring
            if 'score' in details:
                analysis['risk_score'] = details['score'].get('risk', 0.0)
                risk_scores.append(analysis['risk_score'])
            
            # Additional information
            if 'additionalinfo' in details:
                additional = details['additionalinfo']
                analysis['reputation'] = additional.get('reputationscore', 100)
                analysis['threat_categories'] = additional.get('threatcategories', [])
            
            # Device information
            if include_devices and 'devices' in details:
                analysis['device_count'] = len(details['devices'])
            
            # Categorize risk
            if analysis['risk_score'] >= 0.7:
                results['high_risk'].append(analysis)
                results['statistics']['high_risk_count'] += 1
            
            results['successful'].append(analysis)
            results['statistics']['successful_lookups'] += 1
            
            print(f"  ✅ Success - Risk: {analysis['risk_score']:.3f}, Reputation: {analysis['reputation']}")
            
        except Exception as e:
            error_info = {
                'endpoint': endpoint,
                'error': str(e)
            }
            results['failed'].append(error_info)
            results['statistics']['failed_lookups'] += 1
            print(f"  ❌ Failed: {e}")
    
    # Calculate statistics
    if risk_scores:
        results['statistics']['average_risk_score'] = sum(risk_scores) / len(risk_scores)
    
    # Generate summary report
    print(f"\n" + "="*60)
    print(f"BULK ANALYSIS SUMMARY:")
    print(f"  Total endpoints: {results['statistics']['total_endpoints']}")
    print(f"  Successful lookups: {results['statistics']['successful_lookups']}")
    print(f"  Failed lookups: {results['statistics']['failed_lookups']}")
    print(f"  High-risk endpoints: {results['statistics']['high_risk_count']}")
    print(f"  Average risk score: {results['statistics']['average_risk_score']:.3f}")
    
    # High-risk endpoint details
    if results['high_risk']:
        print(f"\nHIGH-RISK ENDPOINTS:")
        for endpoint in sorted(results['high_risk'], key=lambda x: x['risk_score'], reverse=True):
            print(f"  {endpoint['endpoint']}")
            print(f"    Risk Score: {endpoint['risk_score']:.3f}")
            print(f"    Reputation: {endpoint['reputation']}/100")
            if endpoint['threat_categories']:
                print(f"    Threats: {', '.join(endpoint['threat_categories'])}")
            print(f"    Connections: {endpoint['connections']:,}")
    
    # Failed lookups
    if results['failed']:
        print(f"\nFAILED LOOKUPS:")
        for failure in results['failed']:
            print(f"  {failure['endpoint']}: {failure['error']}")
    
    return results

# Example bulk analysis
endpoint_list = [
    "8.8.8.8",
    "1.1.1.1",
    "google.com", 
    "github.com",
    "stackoverflow.com",
    "microsoft.com",
    "invalid-endpoint-test.example"
]

bulk_results = bulk_endpoint_analysis(endpoint_list, include_devices=True)
```

### Custom Filtering and Reporting

```python
# Create custom reports based on endpoint details
def generate_endpoint_report(filters=None, output_format="text"):
    """Generate custom endpoint reports with filtering"""
    
    if filters is None:
        filters = {}
    
    print("Custom Endpoint Report")
    print("=" * 50)
    
    # Sample endpoints for demonstration
    sample_endpoints = [
        "8.8.8.8", "1.1.1.1", "google.com", "github.com", 
        "stackoverflow.com", "microsoft.com"
    ]
    
    filtered_results = []
    
    for endpoint in sample_endpoints:
        try:
            # Determine endpoint type and get details
            is_hostname = not all(c.isdigit() or c == '.' for c in endpoint)
            
            if is_hostname:
                details = client.endpointdetails.get(
                    hostname=endpoint,
                    additionalinfo=True,
                    score=True
                )
            else:
                details = client.endpointdetails.get(
                    ip=endpoint,
                    additionalinfo=True,
                    score=True
                )
            
            # Apply filters
            include_endpoint = True
            
            # Risk score filter
            if 'min_risk_score' in filters:
                risk_score = details.get('score', {}).get('risk', 0)
                if risk_score < filters['min_risk_score']:
                    include_endpoint = False
            
            # Reputation filter
            if 'min_reputation' in filters:
                reputation = details.get('additionalinfo', {}).get('reputationscore', 100)
                if reputation < filters['min_reputation']:
                    include_endpoint = False
            
            # Country filter
            if 'countries' in filters:
                country = details.get('country', 'Unknown')
                if country not in filters['countries']:
                    include_endpoint = False
            
            # Connection count filter
            if 'min_connections' in filters:
                connections = details.get('connections', 0)
                if connections < filters['min_connections']:
                    include_endpoint = False
            
            if include_endpoint:
                filtered_results.append({
                    'endpoint': endpoint,
                    'details': details
                })
                
        except Exception as e:
            print(f"Error processing {endpoint}: {e}")
    
    # Generate report
    if output_format == "text":
        print(f"\nFiltered Results: {len(filtered_results)} endpoints")
        
        for result in filtered_results:
            endpoint = result['endpoint']
            details = result['details']
            
            print(f"\n{endpoint}:")
            print(f"  IP: {details.get('ip', 'Unknown')}")
            print(f"  Country: {details.get('country', 'Unknown')}")
            print(f"  Connections: {details.get('connections', 0):,}")
            
            if 'score' in details:
                risk_score = details['score'].get('risk', 0)
                print(f"  Risk Score: {risk_score:.3f}")
            
            if 'additionalinfo' in details:
                reputation = details['additionalinfo'].get('reputationscore', 100)
                print(f"  Reputation: {reputation}/100")
    
    elif output_format == "csv":
        # Generate CSV output
        print(f"\nCSV Output:")
        print("Endpoint,IP,Country,Connections,Risk_Score,Reputation")
        
        for result in filtered_results:
            endpoint = result['endpoint']
            details = result['details']
            
            ip = details.get('ip', 'Unknown')
            country = details.get('country', 'Unknown')
            connections = details.get('connections', 0)
            risk_score = details.get('score', {}).get('risk', 0)
            reputation = details.get('additionalinfo', {}).get('reputationscore', 100)
            
            print(f"{endpoint},{ip},{country},{connections},{risk_score:.3f},{reputation}")
    
    return filtered_results

# Example custom reports
print("Report 1: High-risk endpoints")
high_risk_report = generate_endpoint_report({
    'min_risk_score': 0.3
}, output_format="text")

print("\n" + "="*60)
print("Report 2: Non-US endpoints with low reputation")  
foreign_low_rep = generate_endpoint_report({
    'min_reputation': 50,
    'countries': ['China', 'Russia', 'Unknown']
}, output_format="csv")
```

## Error Handling

```python
try:
    # Attempt to get endpoint details
    details = client.endpointdetails.get(
        ip="8.8.8.8",
        additionalinfo=True,
        devices=True,
        score=True
    )
    
    # Process endpoint information
    print(f"Endpoint: {details.get('ip', 'Unknown')}")
    print(f"Hostname: {details.get('hostname', 'Unknown')}")
    print(f"Country: {details.get('country', 'Unknown')}")
    
    # Handle additional information
    if 'additionalinfo' in details:
        additional = details['additionalinfo']
        print(f"ISP: {additional.get('isp', 'Unknown')}")
        print(f"Reputation: {additional.get('reputationscore', 'Unknown')}")
    
    # Handle scoring information
    if 'score' in details:
        score_info = details['score']
        print(f"Risk Score: {score_info.get('risk', 'Unknown')}")
        print(f"Category: {score_info.get('category', 'Unknown')}")
    
    # Handle device information
    if 'devices' in details:
        devices = details['devices']
        print(f"Connected Devices: {len(devices)}")
        
        for device in devices[:3]:  # Show first 3 devices
            print(f"  Device: {device.get('hostname', 'Unknown')} ({device.get('ip', 'Unknown')})")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check IP address or hostname format")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for endpointdetails endpoint")
        elif e.response.status_code == 404:
            print("Endpoint not found or no data available")
        elif e.response.status_code == 429:
            print("Rate limit exceeded - reduce request frequency")
        else:
            print(f"Response: {e.response.text}")
            
except ValueError as e:
    print(f"Value error: {e}")
    print("Check that IP address or hostname is properly formatted")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Endpoint Identification
- **IP addresses**: IPv4 addresses for external endpoints
- **Hostnames**: Domain names and hostnames for external services
- **Mutual exclusivity**: Use either `ip` or `hostname`, not both
- **External only**: This endpoint focuses on external/remote endpoints

### Information Categories
- **Basic details**: IP, hostname, country, port, protocol
- **Traffic statistics**: Connection counts, traffic volumes, timing
- **Additional info**: Geolocation, ASN, ISP, reputation, threat data
- **Risk scoring**: Rarity, risk factors, confidence levels
- **Device connections**: Internal devices that communicated with endpoint

### Risk Assessment Factors
- **Rarity scoring**: How uncommon the endpoint is in your environment
- **Reputation data**: Known reputation from threat intelligence sources
- **Geographic factors**: Location-based risk assessment
- **Temporal patterns**: Time-based connection analysis
- **Threat intelligence**: Known malicious activity associations

### Additional Information Fields
- **ASN data**: Autonomous System Number and organization
- **Geolocation**: City, region, coordinates, timezone
- **ISP/Organization**: Internet service provider and organization details
- **Reputation score**: 0-100 scale (higher = better reputation)
- **Threat categories**: Known threat associations
- **Tags**: Descriptive labels (legitimate, suspicious, etc.)

### Device Connection Data
- **Device identification**: Internal device hostname and IP
- **Connection metrics**: Count, timing, traffic volume
- **Port/protocol usage**: Communication patterns
- **Relationship mapping**: Which internal devices accessed which endpoints

### Response Data Filtering
Use `responsedata` parameter to optimize queries:
- `"ip,hostname,country"`: Basic identification only
- `"score"`: Risk assessment data only
- `"additionalinfo"`: Extended information only
- `"devices"`: Connected device information only
- Custom combinations for specific needs

### Performance Considerations
- **Selective data retrieval**: Use flags and responsedata to limit data
- **Caching strategy**: Cache endpoint details for frequently queried endpoints
- **Rate limiting**: Respect API rate limits for bulk operations
- **Pagination**: Handle large device lists appropriately

### Security Applications
- **Threat hunting**: Identify suspicious external endpoints
- **Risk assessment**: Evaluate external communication risks
- **Incident response**: Investigate endpoint communications during incidents
- **Baseline establishment**: Understand normal external communication patterns
- **IOC validation**: Verify threat intelligence indicators

### Integration Scenarios
- **SIEM integration**: Feed endpoint intelligence to SIEM systems
- **Threat intelligence platforms**: Enrich external data with Darktrace insights
- **Security orchestration**: Automate response based on endpoint risk scores
- **Network monitoring**: Correlate with network traffic analysis
- **Compliance reporting**: Document external communications for compliance

### Best Practices
- **Regular monitoring**: Periodically review high-risk endpoints
- **Whitelist management**: Maintain lists of approved external endpoints
- **Threshold tuning**: Adjust risk score thresholds based on environment
- **Investigation workflows**: Establish procedures for high-risk endpoint investigation
- **Documentation**: Maintain records of endpoint analysis and decisions

### Common Use Cases
- **External threat assessment**: Evaluate risk of external communications
- **IOC investigation**: Research specific IP addresses or domains
- **Communication mapping**: Understand external connectivity patterns
- **Risk scoring**: Prioritize security investigations based on endpoint risk
- **Compliance monitoring**: Track and document external communications
