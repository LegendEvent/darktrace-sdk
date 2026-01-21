# DeviceSummary Module

The DeviceSummary module provides comprehensive contextual information for specific devices, aggregating data from multiple sources including devices, similar devices, model breaches, device info, and connection details. This module creates a unified view of device status, behavior, and security posture.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the devicesummary module
devicesummary = client.devicesummary
```

## Methods Overview

The DeviceSummary module provides the following method:

- **`get()`** - Retrieve comprehensive summary information for a specific device

## Methods

### Get Device Summary

Retrieve comprehensive contextual information for a specific device, aggregating data from multiple Darktrace endpoints to provide a unified device view.

```python
# Get complete device summary
device_summary = devicesummary.get(did=123)

# Get specific data fields only
summary_info = devicesummary.get(
    did=123,
    responsedata="device_info"
)

# Get device summary with network context
network_summary = devicesummary.get(
    did=456,
    responsedata="network_activity"
)
```

#### Parameters

- `did` (int, **required**): Device identification number in the Darktrace system
- `responsedata` (str, optional): Restrict returned JSON to only this field/object for performance optimization

#### Response Structure

```python
{
  "device_info": {
    "did": 123,
    "ip": "192.168.1.100",
    "mac": "00:11:22:33:44:55",
    "hostname": "workstation-01.company.com",
    "device_type": "workstation",
    "operating_system": "Windows 10",
    "vendor": "Dell Inc.",
    "first_seen": 1640995200,
    "last_seen": 1705324800,
    "tags": ["critical", "finance"],
    "labels": ["user_device", "managed"],
    "credentials": ["user@company.com"],
    "location": "Office Building A",
    "department": "Finance"
  },
  "network_activity": {
    "total_connections": 15674,
    "unique_destinations": 234,
    "external_connections": 89,
    "data_transferred": {
      "sent_bytes": 2147483648,
      "received_bytes": 8589934592,
      "total_bytes": 10737418240
    },
    "recent_activity": {
      "last_24h_connections": 342,
      "peak_hour": "14:00-15:00",
      "busiest_protocols": ["HTTPS", "DNS", "SMB"]
    },
    "geo_distribution": [
      {
        "country": "United States",
        "connections": 150,
        "percentage": 43.8
      },
      {
        "country": "United Kingdom", 
        "connections": 89,
        "percentage": 26.0
      }
    ]
  },
  "security_assessment": {
    "risk_score": 0.25,
    "threat_level": "low",
    "active_breaches": 0,
    "total_breaches": 3,
    "recent_breaches": [
      {
        "breach_id": "mb_001",
        "model_name": "Unusual External Connection",
        "timestamp": 1705320000,
        "severity": 0.45,
        "status": "acknowledged",
        "details": "Connection to new external domain"
      }
    ],
    "compliance_status": "compliant",
    "vulnerabilities": {
      "critical": 0,
      "high": 1,
      "medium": 3,
      "low": 8
    }
  },
  "behavioral_analysis": {
    "anomaly_score": 0.15,
    "behavior_pattern": "consistent",
    "typical_usage_hours": "08:00-18:00",
    "weekend_activity": "minimal",
    "communication_patterns": {
      "internal_ratio": 0.75,
      "external_ratio": 0.25,
      "p2p_activity": "low",
      "server_interactions": "high"
    },
    "baseline_deviation": {
      "data_volume": 0.05,
      "connection_count": 0.12,
      "protocol_usage": 0.08,
      "timing_patterns": 0.03
    }
  },
  "similar_devices": [
    {
      "did": 456,
      "hostname": "workstation-02.company.com",
      "similarity_score": 0.89,
      "shared_characteristics": [
        "same_subnet",
        "similar_traffic_patterns",
        "same_os_version"
      ]
    },
    {
      "did": 789,
      "hostname": "workstation-03.company.com", 
      "similarity_score": 0.76,
      "shared_characteristics": [
        "same_department",
        "similar_applications",
        "same_user_profile"
      ]
    }
  ],
  "connection_details": {
    "established_connections": 23,
    "listening_ports": [80, 443, 22, 3389],
    "active_services": [
      {
        "port": 443,
        "protocol": "TCP",
        "service": "HTTPS",
        "connections": 156
      },
      {
        "port": 53,
        "protocol": "UDP", 
        "service": "DNS",
        "connections": 89
      }
    ],
    "external_endpoints": [
      {
        "ip": "203.0.113.10",
        "hostname": "api.service.com",
        "country": "United States",
        "reputation": "good",
        "connection_count": 45
      }
    ]
  },
  "compliance_info": {
    "data_classification": "confidential",
    "retention_policy": "7_years",
    "encryption_status": "enabled",
    "backup_status": "current",
    "patch_level": "up_to_date",
    "audit_requirements": ["SOX", "HIPAA"],
    "last_scan": 1705324800
  },
  "performance_metrics": {
    "cpu_usage": 35.2,
    "memory_usage": 68.5,
    "disk_usage": 78.3,
    "network_utilization": 15.7,
    "response_time": 45.2,
    "availability": 99.8
  }
}

## Examples

### Comprehensive Device Analysis

```python
from darktrace import DarktraceClient
from datetime import datetime

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def analyze_device_comprehensive(device_id):
    """Perform comprehensive analysis of a device"""
    
    print(f"Device Analysis Report")
    print("=" * 50)
    print(f"Device ID: {device_id}")
    
    try:
        # Get complete device summary
        summary = client.devicesummary.get(did=device_id)
        
        # Basic device information
        device_info = summary.get('device_info', {})
        print(f"\nDEVICE INFORMATION:")
        print(f"  Hostname: {device_info.get('hostname', 'Unknown')}")
        print(f"  IP Address: {device_info.get('ip', 'Unknown')}")
        print(f"  MAC Address: {device_info.get('mac', 'Unknown')}")
        print(f"  Device Type: {device_info.get('device_type', 'Unknown')}")
        print(f"  Operating System: {device_info.get('operating_system', 'Unknown')}")
        print(f"  Vendor: {device_info.get('vendor', 'Unknown')}")
        
        # Timestamps
        first_seen = device_info.get('first_seen', 0)
        last_seen = device_info.get('last_seen', 0)
        if first_seen:
            print(f"  First Seen: {datetime.fromtimestamp(first_seen)}")
        if last_seen:
            print(f"  Last Seen: {datetime.fromtimestamp(last_seen)}")
        
        # Tags and labels
        tags = device_info.get('tags', [])
        labels = device_info.get('labels', [])
        if tags:
            print(f"  Tags: {', '.join(tags)}")
        if labels:
            print(f"  Labels: {', '.join(labels)}")
        
        # Network activity analysis
        network_activity = summary.get('network_activity', {})
        if network_activity:
            print(f"\nNETWORK ACTIVITY:")
            print(f"  Total Connections: {network_activity.get('total_connections', 0):,}")
            print(f"  Unique Destinations: {network_activity.get('unique_destinations', 0):,}")
            print(f"  External Connections: {network_activity.get('external_connections', 0):,}")
            
            data_transferred = network_activity.get('data_transferred', {})
            if data_transferred:
                sent_gb = data_transferred.get('sent_bytes', 0) / (1024**3)
                received_gb = data_transferred.get('received_bytes', 0) / (1024**3)
                total_gb = data_transferred.get('total_bytes', 0) / (1024**3)
                print(f"  Data Sent: {sent_gb:.2f} GB")
                print(f"  Data Received: {received_gb:.2f} GB")
                print(f"  Total Data: {total_gb:.2f} GB")
            
            recent_activity = network_activity.get('recent_activity', {})
            if recent_activity:
                print(f"  Last 24h Connections: {recent_activity.get('last_24h_connections', 0):,}")
                print(f"  Peak Hour: {recent_activity.get('peak_hour', 'Unknown')}")
                protocols = recent_activity.get('busiest_protocols', [])
                if protocols:
                    print(f"  Top Protocols: {', '.join(protocols)}")
        
        # Security assessment
        security = summary.get('security_assessment', {})
        if security:
            print(f"\nSECURITY ASSESSMENT:")
            risk_score = security.get('risk_score', 0)
            threat_level = security.get('threat_level', 'unknown')
            print(f"  Risk Score: {risk_score:.3f}")
            print(f"  Threat Level: {threat_level.upper()}")
            print(f"  Active Breaches: {security.get('active_breaches', 0)}")
            print(f"  Total Breaches: {security.get('total_breaches', 0)}")
            
            vulnerabilities = security.get('vulnerabilities', {})
            if vulnerabilities:
                print(f"  Vulnerabilities:")
                for severity, count in vulnerabilities.items():
                    print(f"    {severity.title()}: {count}")
        
        # Behavioral analysis
        behavioral = summary.get('behavioral_analysis', {})
        if behavioral:
            print(f"\nBEHAVIORAL ANALYSIS:")
            anomaly_score = behavioral.get('anomaly_score', 0)
            pattern = behavioral.get('behavior_pattern', 'unknown')
            print(f"  Anomaly Score: {anomaly_score:.3f}")
            print(f"  Behavior Pattern: {pattern.title()}")
            print(f"  Typical Hours: {behavioral.get('typical_usage_hours', 'Unknown')}")
            print(f"  Weekend Activity: {behavioral.get('weekend_activity', 'Unknown')}")
            
            comm_patterns = behavioral.get('communication_patterns', {})
            if comm_patterns:
                internal_ratio = comm_patterns.get('internal_ratio', 0)
                external_ratio = comm_patterns.get('external_ratio', 0)
                print(f"  Internal Traffic: {internal_ratio:.1%}")
                print(f"  External Traffic: {external_ratio:.1%}")
        
        # Similar devices
        similar_devices = summary.get('similar_devices', [])
        if similar_devices:
            print(f"\nSIMILAR DEVICES:")
            for similar in similar_devices[:3]:  # Show top 3
                hostname = similar.get('hostname', 'Unknown')
                score = similar.get('similarity_score', 0)
                characteristics = similar.get('shared_characteristics', [])
                print(f"  • {hostname} (similarity: {score:.2f})")
                if characteristics:
                    print(f"    Shared: {', '.join(characteristics)}")
        
        # Performance metrics
        performance = summary.get('performance_metrics', {})
        if performance:
            print(f"\nPERFORMANCE METRICS:")
            print(f"  CPU Usage: {performance.get('cpu_usage', 0):.1f}%")
            print(f"  Memory Usage: {performance.get('memory_usage', 0):.1f}%")
            print(f"  Disk Usage: {performance.get('disk_usage', 0):.1f}%")
            print(f"  Network Utilization: {performance.get('network_utilization', 0):.1f}%")
            print(f"  Availability: {performance.get('availability', 0):.1f}%")
        
        # Risk assessment and recommendations
        print(f"\nRISK ASSESSMENT:")
        
        overall_risk = 0
        risk_factors = []
        
        # Calculate risk based on various factors
        if security.get('risk_score', 0) > 0.7:
            overall_risk += 0.4
            risk_factors.append("High security risk score")
        
        if behavioral.get('anomaly_score', 0) > 0.5:
            overall_risk += 0.3
            risk_factors.append("Anomalous behavior detected")
        
        if security.get('active_breaches', 0) > 0:
            overall_risk += 0.4
            risk_factors.append("Active security breaches")
        
        critical_vulns = security.get('vulnerabilities', {}).get('critical', 0)
        if critical_vulns > 0:
            overall_risk += 0.3
            risk_factors.append(f"{critical_vulns} critical vulnerabilities")
        
        # Determine risk level
        if overall_risk >= 0.8:
            risk_level = "🔴 CRITICAL RISK"
        elif overall_risk >= 0.6:
            risk_level = "🟡 HIGH RISK"
        elif overall_risk >= 0.3:
            risk_level = "🟠 MEDIUM RISK"
        else:
            risk_level = "🟢 LOW RISK"
        
        print(f"  Overall Risk: {risk_level}")
        print(f"  Risk Score: {overall_risk:.3f}")
        
        if risk_factors:
            print(f"  Risk Factors:")
            for factor in risk_factors:
                print(f"    • {factor}")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        
        recommendations = []
        
        if overall_risk >= 0.8:
            recommendations.append("• Immediate investigation required")
            recommendations.append("• Consider isolating device")
            recommendations.append("• Review all recent activities")
        elif overall_risk >= 0.6:
            recommendations.append("• Enhanced monitoring recommended")
            recommendations.append("• Security patch assessment needed")
        elif overall_risk >= 0.3:
            recommendations.append("• Regular monitoring sufficient")
            recommendations.append("• Address identified vulnerabilities")
        else:
            recommendations.append("• Device operating normally")
            recommendations.append("• Continue standard monitoring")
        
        # Specific recommendations based on data
        if critical_vulns > 0:
            recommendations.append(f"• Patch {critical_vulns} critical vulnerabilities immediately")
        
        if behavioral.get('anomaly_score', 0) > 0.5:
            recommendations.append("• Investigate behavioral anomalies")
        
        if security.get('active_breaches', 0) > 0:
            recommendations.append("• Review and respond to active breaches")
        
        external_ratio = behavioral.get('communication_patterns', {}).get('external_ratio', 0)
        if external_ratio > 0.8:
            recommendations.append("• Review high external communication volume")
        
        for rec in recommendations:
            print(f"  {rec}")
        
        return summary
        
    except Exception as e:
        print(f"Error analyzing device: {e}")
        return None

# Example usage
# device_analysis = analyze_device_comprehensive(123)
```

### Device Fleet Overview

```python
def analyze_device_fleet(device_ids):
    """Analyze multiple devices for fleet management"""
    
    print(f"Device Fleet Analysis")
    print("=" * 60)
    print(f"Analyzing {len(device_ids)} devices")
    
    fleet_summary = {
        'total_devices': len(device_ids),
        'high_risk_devices': 0,
        'active_breaches': 0,
        'total_vulnerabilities': 0,
        'average_risk_score': 0,
        'device_types': {},
        'operating_systems': {},
        'network_activity': {
            'total_connections': 0,
            'total_data_transfer': 0
        }
    }
    
    risk_scores = []
    problem_devices = []
    
    for device_id in device_ids:
        try:
            print(f"\nAnalyzing device {device_id}...")
            summary = client.devicesummary.get(did=device_id)
            
            # Extract key metrics
            device_info = summary.get('device_info', {})
            security = summary.get('security_assessment', {})
            network = summary.get('network_activity', {})
            
            # Device classification
            device_type = device_info.get('device_type', 'unknown')
            fleet_summary['device_types'][device_type] = fleet_summary['device_types'].get(device_type, 0) + 1
            
            os = device_info.get('operating_system', 'unknown')
            fleet_summary['operating_systems'][os] = fleet_summary['operating_systems'].get(os, 0) + 1
            
            # Security metrics
            risk_score = security.get('risk_score', 0)
            risk_scores.append(risk_score)
            
            if risk_score > 0.7:
                fleet_summary['high_risk_devices'] += 1
                problem_devices.append({
                    'device_id': device_id,
                    'hostname': device_info.get('hostname', 'Unknown'),
                    'risk_score': risk_score,
                    'active_breaches': security.get('active_breaches', 0)
                })
            
            fleet_summary['active_breaches'] += security.get('active_breaches', 0)
            
            # Vulnerability count
            vulnerabilities = security.get('vulnerabilities', {})
            device_vuln_total = sum(vulnerabilities.values())
            fleet_summary['total_vulnerabilities'] += device_vuln_total
            
            # Network activity
            fleet_summary['network_activity']['total_connections'] += network.get('total_connections', 0)
            data_transfer = network.get('data_transferred', {}).get('total_bytes', 0)
            fleet_summary['network_activity']['total_data_transfer'] += data_transfer
            
        except Exception as e:
            print(f"Error analyzing device {device_id}: {e}")
    
    # Calculate averages
    if risk_scores:
        fleet_summary['average_risk_score'] = sum(risk_scores) / len(risk_scores)
    
    # Display fleet summary
    print(f"\n" + "="*60)
    print(f"FLEET SUMMARY:")
    print(f"  Total Devices: {fleet_summary['total_devices']}")
    print(f"  High Risk Devices: {fleet_summary['high_risk_devices']} ({fleet_summary['high_risk_devices']/fleet_summary['total_devices']*100:.1f}%)")
    print(f"  Average Risk Score: {fleet_summary['average_risk_score']:.3f}")
    print(f"  Active Breaches: {fleet_summary['active_breaches']}")
    print(f"  Total Vulnerabilities: {fleet_summary['total_vulnerabilities']}")
    
    # Data transfer summary
    total_tb = fleet_summary['network_activity']['total_data_transfer'] / (1024**4)
    print(f"  Total Data Transfer: {total_tb:.2f} TB")
    print(f"  Total Connections: {fleet_summary['network_activity']['total_connections']:,}")
    
    # Device type breakdown
    print(f"\nDEVICE TYPES:")
    for device_type, count in sorted(fleet_summary['device_types'].items()):
        percentage = count / fleet_summary['total_devices'] * 100
        print(f"  {device_type.title()}: {count} ({percentage:.1f}%)")
    
    # Operating system breakdown
    print(f"\nOPERATING SYSTEMS:")
    for os, count in sorted(fleet_summary['operating_systems'].items()):
        percentage = count / fleet_summary['total_devices'] * 100
        print(f"  {os}: {count} ({percentage:.1f}%)")
    
    # Problem devices
    if problem_devices:
        print(f"\nHIGH RISK DEVICES:")
        for device in sorted(problem_devices, key=lambda x: x['risk_score'], reverse=True)[:10]:
            print(f"  🚨 {device['hostname']} (ID: {device['device_id']})")
            print(f"     Risk Score: {device['risk_score']:.3f}, Active Breaches: {device['active_breaches']}")
    
    return fleet_summary

# Example usage
# device_list = [123, 456, 789, 101, 112, 131]
# fleet_analysis = analyze_device_fleet(device_list)
```

### Device Monitoring Dashboard

```python
def create_device_monitoring_dashboard(device_id, refresh_interval=300):
    """Create a monitoring dashboard for a specific device"""
    
    import time
    from datetime import datetime
    
    def display_dashboard():
        print("\033[2J\033[H")  # Clear screen
        print(f"Device Monitoring Dashboard")
        print("=" * 70)
        print(f"Device ID: {device_id}")
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Refresh Interval: {refresh_interval}s")
        
        try:
            summary = client.devicesummary.get(did=device_id)
            
            # Device status header
            device_info = summary.get('device_info', {})
            hostname = device_info.get('hostname', 'Unknown')
            ip = device_info.get('ip', 'Unknown')
            
            print(f"\nDEVICE: {hostname} ({ip})")
            
            # Security status
            security = summary.get('security_assessment', {})
            risk_score = security.get('risk_score', 0)
            threat_level = security.get('threat_level', 'unknown')
            active_breaches = security.get('active_breaches', 0)
            
            if risk_score >= 0.8:
                status_icon = "🔴"
            elif risk_score >= 0.5:
                status_icon = "🟡"
            else:
                status_icon = "🟢"
            
            print(f"{status_icon} SECURITY STATUS: {threat_level.upper()}")
            print(f"   Risk Score: {risk_score:.3f}")
            print(f"   Active Breaches: {active_breaches}")
            
            # Network activity
            network = summary.get('network_activity', {})
            recent_activity = network.get('recent_activity', {})
            connections_24h = recent_activity.get('last_24h_connections', 0)
            
            print(f"\n📊 NETWORK ACTIVITY:")
            print(f"   Connections (24h): {connections_24h:,}")
            print(f"   External Connections: {network.get('external_connections', 0):,}")
            
            # Performance metrics
            performance = summary.get('performance_metrics', {})
            cpu = performance.get('cpu_usage', 0)
            memory = performance.get('memory_usage', 0)
            disk = performance.get('disk_usage', 0)
            
            print(f"\n⚡ PERFORMANCE:")
            print(f"   CPU: {cpu:.1f}% | Memory: {memory:.1f}% | Disk: {disk:.1f}%")
            
            # Create simple bar charts
            def create_bar(value, max_val=100, width=20):
                filled = int((value / max_val) * width)
                return "█" * filled + "░" * (width - filled)
            
            print(f"   CPU  [{create_bar(cpu)}] {cpu:.1f}%")
            print(f"   MEM  [{create_bar(memory)}] {memory:.1f}%")
            print(f"   DISK [{create_bar(disk)}] {disk:.1f}%")
            
            # Recent breaches
            recent_breaches = security.get('recent_breaches', [])
            if recent_breaches:
                print(f"\n🚨 RECENT BREACHES:")
                for breach in recent_breaches[:3]:
                    breach_time = datetime.fromtimestamp(breach.get('timestamp', 0))
                    model_name = breach.get('model_name', 'Unknown')
                    severity = breach.get('severity', 0)
                    print(f"   • {model_name} (severity: {severity:.2f})")
                    print(f"     {breach_time.strftime('%H:%M:%S')}")
            
            # Connection details
            connection_details = summary.get('connection_details', {})
            active_connections = connection_details.get('established_connections', 0)
            
            print(f"\n🔗 CONNECTIONS:")
            print(f"   Active: {active_connections}")
            
            listening_ports = connection_details.get('listening_ports', [])
            if listening_ports:
                ports_str = ', '.join(map(str, listening_ports[:5]))
                if len(listening_ports) > 5:
                    ports_str += f", +{len(listening_ports)-5} more"
                print(f"   Listening Ports: {ports_str}")
            
            print(f"\n" + "="*70)
            print(f"Press Ctrl+C to stop monitoring")
            
        except Exception as e:
            print(f"Error updating dashboard: {e}")
    
    # Main monitoring loop
    try:
        while True:
            display_dashboard()
            time.sleep(refresh_interval)
    except KeyboardInterrupt:
        print(f"\nMonitoring stopped.")

# Example usage (commented to prevent automatic execution)
# create_device_monitoring_dashboard(123, refresh_interval=60)
```

## Error Handling

```python
try:
    # Get device summary
    device_summary = client.devicesummary.get(did=123)
    print("Device summary retrieved successfully")
    
    # Get specific response data
    network_only = client.devicesummary.get(
        did=123,
        responsedata="network_activity"
    )
    print("Network activity data retrieved")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check device ID parameter")
        elif e.response.status_code == 401:
            print("Authentication failed - check tokens")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions")
        elif e.response.status_code == 404:
            print("Device not found - check device ID")
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
    print("Check that device ID is a valid integer")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes
 
 ### Known Limitations
 
 ⚠️ **HTTP 500 Error with API Token Authentication**
 
 The `/devicesummary` endpoint may return HTTP 500 Internal Server Error when accessed with API tokens, even though it works in the browser or with session/cookie authentication.
 
 **Root Cause**: This is a Darktrace API backend limitation (not an SDK bug).
 
 - The SDK implementation is correct and uses the same authentication mechanism as other endpoints (`/devices`, `/details`, `/deviceinfo`) which work properly with API tokens.
 - Only `/devicesummary` returns HTTP 500 when accessed with API token authentication.
 - The endpoint works correctly when accessed via browser or with session cookies.
 
 **Status**: Confirmed as Darktrace API backend limitation (tested with SDK v0.8.54 on Darktrace v6.3.18). See [issue #37](https://github.com/LegendEvent/darktrace-sdk/issues/37) for details.
 
 **Workaround**: There is currently no programmatic workaround. If you require this endpoint, please contact Darktrace support or use browser-based access where possible.
 
 **Alternative**: You can call the underlying endpoints directly and aggregate the data yourself:
 - `/devices` - Device inventory
 - `/similardevices` - Similar device analysis
 - `/modelbreaches` - Breach information
 - `/deviceinfo` - Detailed device information
 - `/details` - Connection details
 
 ### Data Aggregation
- **Multiple sources**: Combines data from devices, similardevices, modelbreaches, deviceinfo, and details endpoints
- **Unified view**: Provides comprehensive device context in a single response
- **Performance optimization**: Single API call instead of multiple separate requests
- **Contextual analysis**: Cross-references data for enhanced insights

### Device Context
- **Comprehensive profiling**: Complete device characterization including hardware, software, and behavior
- **Real-time status**: Current device state and recent activity
- **Historical perspective**: Long-term trends and baseline behavior
- **Relationship mapping**: Similar devices and network relationships

### Security Integration
- **Risk assessment**: Calculated risk scores based on multiple factors
- **Threat correlation**: Links security events with device behavior
- **Vulnerability tracking**: Comprehensive vulnerability assessment
- **Breach monitoring**: Active and historical breach information

### Performance Monitoring
- **Resource utilization**: CPU, memory, disk, and network usage
- **Availability tracking**: Device uptime and responsiveness
- **Performance trends**: Historical performance data
- **Capacity planning**: Resource usage patterns for planning

### Network Analysis
- **Communication patterns**: Internal vs external traffic analysis
- **Protocol usage**: Application and protocol breakdown
- **Geographic distribution**: Geographic analysis of connections
- **Anomaly detection**: Unusual network behavior identification

### Behavioral Analytics
- **Pattern recognition**: Normal behavior pattern establishment
- **Anomaly scoring**: Quantified behavioral deviation measurement
- **Temporal analysis**: Time-based usage patterns
- **Baseline comparison**: Deviation from established baselines

### Similar Device Analysis
- **Device clustering**: Groups devices with similar characteristics
- **Comparison metrics**: Quantified similarity scoring
- **Shared attributes**: Common characteristics identification
- **Fleet management**: Device grouping for management purposes

### Response Data Optimization
- **Selective retrieval**: Use responsedata parameter to limit data transfer
- **Performance tuning**: Reduce API response time and bandwidth usage
- **Targeted analysis**: Focus on specific data aspects
- **Bandwidth conservation**: Important for limited bandwidth environments

### Use Cases
- **Security operations**: Comprehensive device security assessment
- **Incident response**: Detailed device analysis during incidents
- **Compliance monitoring**: Regulatory compliance status tracking
- **Fleet management**: Large-scale device management and monitoring
- **Performance optimization**: Resource usage analysis and optimization
- **Risk assessment**: Quantified device risk evaluation

### Integration Patterns
- **SIEM integration**: Feed device data into security information systems
- **Asset management**: Comprehensive asset inventory and tracking
- **Monitoring systems**: Real-time device monitoring and alerting
- **Compliance reporting**: Automated compliance status reporting
- **Dashboard development**: Rich device information for dashboards
