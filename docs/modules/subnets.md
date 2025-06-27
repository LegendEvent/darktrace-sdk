# Subnets Module

The Subnets module provides comprehensive subnet information management capabilities, allowing you to retrieve, create, and update subnet configurations within the Darktrace system. This module is essential for network topology management, device organization, and traffic processing configuration.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the subnets module
subnets = client.subnets
```

## Methods Overview

The Subnets module provides the following methods:

- **`get()`** - Retrieve subnet information with various filtering options
- **`post()`** - Create or update subnet configurations

## Methods

### Get Subnets

Retrieve subnet information from the Darktrace platform with flexible filtering options.

```python
# Get all subnets
all_subnets = subnets.get()

# Get specific subnet by ID
specific_subnet = subnets.get(subnet_id=123)

# Get subnets with recent activity
active_subnets = subnets.get(seensince="1hour")

# Get specific subnet by SID
subnet_by_sid = subnets.get(sid=456)

# Get only specific response data
subnet_labels = subnets.get(responsedata="label")

# Combined filtering
recent_active = subnets.get(
    seensince="24hour",
    responsedata="network,label,devices"
)
```

#### Parameters

- `subnet_id` (int, optional): Specific subnet ID to retrieve (as path parameter)
- `seensince` (str, optional): Relative time offset for activity filtering (e.g., '2min', '1hour', '3600', '3min', '5hour', '6day'). Minimum=1 second, Maximum=6 months. Returns subnets with activity in the specified time period
- `sid` (int, optional): Identification number of a subnet modeled in the Darktrace system
- `responsedata` (str, optional): Restrict returned JSON to only specified top-level field(s) or object(s)

#### Response Structure

```python
{
  "subnets": [
    {
      "sid": 1,
      "label": "Corporate LAN",
      "network": "192.168.1.0/24",
      "longitude": -0.1276,
      "latitude": 51.5074,
      "dhcp": True,
      "uniqueUsernames": True,
      "uniqueHostnames": True,
      "excluded": False,
      "modelExcluded": False,
      "deviceCount": 245,
      "lastActivity": 1705324800,
      "devices": [
        {
          "did": 123,
          "hostname": "workstation-01",
          "ip": "192.168.1.100",
          "mac": "00:11:22:33:44:55",
          "lastSeen": 1705324800
        }
        // ... more devices
      ],
      "networkInfo": {
        "gateway": "192.168.1.1",
        "netmask": "255.255.255.0",
        "broadcast": "192.168.1.255",
        "usableHosts": 254,
        "usedAddresses": 89
      },
      "activityStats": {
        "totalConnections": 15432,
        "uniqueDestinations": 234,
        "dataTransferred": 2147483648,
        "protocolBreakdown": {
          "TCP": 78.5,
          "UDP": 15.2,
          "ICMP": 6.3
        }
      },
      "securityMetrics": {
        "riskScore": 0.35,
        "activeBreaches": 2,
        "vulnerableDevices": 5,
        "threatEvents": 12
      }
    }
    // ... more subnets
  ],
  "pagination": {
    "total": 25,
    "returned": 10,
    "hasMore": True
  }
}
```

### Create/Update Subnet

Create a new subnet or update an existing subnet configuration in the Darktrace system.

```python
# Create a new subnet
new_subnet = subnets.post(
    sid=100,
    label="Guest Network",
    network="10.0.100.0/24",
    dhcp=True,
    uniqueUsernames=False,
    uniqueHostnames=True,
    excluded=False,
    modelExcluded=False
)

# Update subnet with location
subnet_with_location = subnets.post(
    sid=101,
    label="Branch Office - London",
    network="172.16.1.0/24",
    longitude=-0.1276,
    latitude=51.5074,
    dhcp=True,
    uniqueUsernames=True,
    uniqueHostnames=True
)

# Create excluded subnet (traffic not processed)
excluded_subnet = subnets.post(
    sid=200,
    label="DMZ Network",
    network="203.0.113.0/24",
    excluded=True,
    dhcp=False
)

# Create model-excluded subnet (devices added to Internal Traffic)
internal_subnet = subnets.post(
    sid=300,
    label="Internal Infrastructure",
    network="10.0.0.0/16",
    modelExcluded=True,
    uniqueUsernames=True
)

# Update only specific fields
updated_subnet = subnets.post(
    sid=101,
    label="Branch Office - London Updated",
    dhcp=False,
    responsedata="label,dhcp"
)
```

#### Parameters

- `sid` (int, **required**): Identification number of a subnet modeled in the Darktrace system
- `label` (str, optional): Optional label to identify the subnet (do not use quotes around the string)
- `network` (str, optional): IP address range that describes the subnet (CIDR notation)
- `longitude` (float, optional): Longitude for the subnet's location (must be used with latitude, whole values need decimal point e.g., 10.0)
- `latitude` (float, optional): Latitude for the subnet's location (must be used with longitude, whole values need decimal point e.g., 10.0)
- `dhcp` (bool, optional): Whether DHCP is enabled for the subnet
- `uniqueUsernames` (bool, optional): Whether the subnet is tracking by credential
- `uniqueHostnames` (bool, optional): Whether the subnet is tracking by hostname
- `excluded` (bool, optional): Whether traffic in this subnet should not be processed at all
- `modelExcluded` (bool, optional): Whether devices within this subnet should be fully modeled. If true, devices will be added to the Internal Traffic subnet
- `responsedata` (str, optional): Restrict returned JSON to only specified top-level field(s) or object(s)

#### Response Structure

```python
{
  "result": "success",
  "message": "Subnet updated successfully",
  "subnet": {
    "sid": 100,
    "label": "Guest Network",
    "network": "10.0.100.0/24",
    "longitude": null,
    "latitude": null,
    "dhcp": True,
    "uniqueUsernames": False,
    "uniqueHostnames": True,
    "excluded": False,
    "modelExcluded": False,
    "created": 1705324800,
    "modified": 1705324800
  },
  "affectedDevices": 0,
  "validationErrors": []
}
```

## Examples

### Network Topology Discovery

```python
from darktrace import DarktraceClient
from datetime import datetime, timedelta

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def discover_network_topology():
    """Discover and analyze network topology"""
    
    print("Network Topology Discovery")
    print("=" * 50)
    
    try:
        # Get all subnets
        all_subnets = client.subnets.get()
        subnets_data = all_subnets.get('subnets', [])
        
        print(f"Found {len(subnets_data)} subnets")
        
        topology = {
            'total_subnets': len(subnets_data),
            'total_devices': 0,
            'subnet_types': {},
            'geographic_distribution': {},
            'network_ranges': [],
            'dhcp_enabled': 0,
            'excluded_subnets': 0,
            'model_excluded': 0
        }
        
        # Analyze each subnet
        for subnet in subnets_data:
            sid = subnet.get('sid', 0)
            label = subnet.get('label', f'Subnet {sid}')
            network = subnet.get('network', 'Unknown')
            device_count = subnet.get('deviceCount', 0)
            
            print(f"\nSubnet: {label}")
            print(f"  SID: {sid}")
            print(f"  Network: {network}")
            print(f"  Devices: {device_count}")
            
            topology['total_devices'] += device_count
            topology['network_ranges'].append(network)
            
            # DHCP analysis
            if subnet.get('dhcp', False):
                topology['dhcp_enabled'] += 1
                print(f"  DHCP: Enabled")
            
            # Exclusion analysis
            if subnet.get('excluded', False):
                topology['excluded_subnets'] += 1
                print(f"  Status: Excluded from processing")
            elif subnet.get('modelExcluded', False):
                topology['model_excluded'] += 1
                print(f"  Status: Model excluded")
            
            # Geographic location
            longitude = subnet.get('longitude')
            latitude = subnet.get('latitude')
            if longitude is not None and latitude is not None:
                location = f"{latitude:.4f}, {longitude:.4f}"
                topology['geographic_distribution'][label] = location
                print(f"  Location: {location}")
            
            # Subnet classification
            if '192.168.' in network:
                subnet_type = 'Private Class C'
            elif '10.' in network:
                subnet_type = 'Private Class A'
            elif '172.' in network:
                subnet_type = 'Private Class B'
            elif any(public in network for public in ['203.', '8.8.', '1.1.']):
                subnet_type = 'Public'
            else:
                subnet_type = 'Unknown'
            
            topology['subnet_types'][subnet_type] = topology['subnet_types'].get(subnet_type, 0) + 1
            
            # Activity analysis
            activity_stats = subnet.get('activityStats', {})
            if activity_stats:
                connections = activity_stats.get('totalConnections', 0)
                data_gb = activity_stats.get('dataTransferred', 0) / (1024**3)
                print(f"  Activity: {connections:,} connections, {data_gb:.2f} GB")
            
            # Security metrics
            security = subnet.get('securityMetrics', {})
            if security:
                risk_score = security.get('riskScore', 0)
                active_breaches = security.get('activeBreaches', 0)
                print(f"  Security: Risk {risk_score:.3f}, {active_breaches} active breaches")
        
        # Summary analysis
        print(f"\n" + "="*50)
        print(f"TOPOLOGY SUMMARY:")
        print(f"  Total Subnets: {topology['total_subnets']}")
        print(f"  Total Devices: {topology['total_devices']:,}")
        print(f"  DHCP Enabled: {topology['dhcp_enabled']}/{topology['total_subnets']}")
        print(f"  Excluded from Processing: {topology['excluded_subnets']}")
        print(f"  Model Excluded: {topology['model_excluded']}")
        
        # Subnet type breakdown
        print(f"\nSUBNET TYPES:")
        for subnet_type, count in topology['subnet_types'].items():
            percentage = count / topology['total_subnets'] * 100
            print(f"  {subnet_type}: {count} ({percentage:.1f}%)")
        
        # Geographic distribution
        if topology['geographic_distribution']:
            print(f"\nGEOGRAPHIC LOCATIONS:")
            for subnet_name, location in topology['geographic_distribution'].items():
                print(f"  {subnet_name}: {location}")
        
        return topology
        
    except Exception as e:
        print(f"Error discovering topology: {e}")
        return None

# Example usage
# network_topology = discover_network_topology()
```

### Subnet Configuration Management

```python
def manage_subnet_configurations():
    """Comprehensive subnet configuration management"""
    
    print("Subnet Configuration Management")
    print("=" * 60)
    
    try:
        # Define subnet configurations
        subnet_configs = [
            {
                'sid': 100,
                'label': 'Corporate LAN',
                'network': '192.168.1.0/24',
                'dhcp': True,
                'uniqueUsernames': True,
                'uniqueHostnames': True,
                'excluded': False,
                'modelExcluded': False
            },
            {
                'sid': 101,
                'label': 'Guest Network',
                'network': '10.0.100.0/24',
                'dhcp': True,
                'uniqueUsernames': False,
                'uniqueHostnames': False,
                'excluded': False,
                'modelExcluded': False
            },
            {
                'sid': 200,
                'label': 'DMZ Network',
                'network': '203.0.113.0/24',
                'dhcp': False,
                'uniqueUsernames': False,
                'uniqueHostnames': True,
                'excluded': True,
                'modelExcluded': False
            },
            {
                'sid': 300,
                'label': 'Server Farm',
                'network': '172.16.0.0/20',
                'longitude': -0.1276,
                'latitude': 51.5074,
                'dhcp': False,
                'uniqueUsernames': True,
                'uniqueHostnames': True,
                'excluded': False,
                'modelExcluded': False
            }
        ]
        
        # Create/update subnets
        results = []
        for config in subnet_configs:
            print(f"\nConfiguring subnet: {config['label']}")
            
            try:
                result = client.subnets.post(**config)
                results.append({
                    'config': config,
                    'result': result,
                    'status': 'success'
                })
                print(f"  ✅ Successfully configured")
                
                # Display result details
                subnet_info = result.get('subnet', {})
                print(f"     SID: {subnet_info.get('sid')}")
                print(f"     Network: {subnet_info.get('network')}")
                print(f"     DHCP: {subnet_info.get('dhcp')}")
                
            except Exception as e:
                results.append({
                    'config': config,
                    'error': str(e),
                    'status': 'failed'
                })
                print(f"  ❌ Failed: {e}")
        
        # Verify configurations
        print(f"\n" + "="*60)
        print(f"VERIFICATION:");
        
        for result in results:
            if result['status'] == 'success':
                config = result['config']
                sid = config['sid']
                
                # Verify the subnet was created/updated correctly
                try:
                    verification = client.subnets.get(sid=sid)
                    verified_subnets = verification.get('subnets', [])
                    
                    if verified_subnets:
                        verified_subnet = verified_subnets[0]
                        print(f"\n✅ Verified subnet {config['label']}:")
                        print(f"   SID: {verified_subnet.get('sid')}")
                        print(f"   Label: {verified_subnet.get('label')}")
                        print(f"   Network: {verified_subnet.get('network')}")
                        print(f"   DHCP: {verified_subnet.get('dhcp')}")
                        print(f"   Excluded: {verified_subnet.get('excluded')}")
                    else:
                        print(f"⚠️  Could not verify subnet {config['label']}")
                        
                except Exception as e:
                    print(f"❌ Verification failed for {config['label']}: {e}")
        
        return results
        
    except Exception as e:
        print(f"Error managing subnet configurations: {e}")
        return None

# Example usage
# config_results = manage_subnet_configurations()
```

### Subnet Activity Monitoring

```python
def monitor_subnet_activity(time_window="1hour"):
    """Monitor subnet activity over a specified time window"""
    
    print(f"Subnet Activity Monitoring")
    print("=" * 50)
    print(f"Time window: {time_window}")
    
    try:
        # Get subnets with recent activity
        active_subnets = client.subnets.get(seensince=time_window)
        subnets_data = active_subnets.get('subnets', [])
        
        if not subnets_data:
            print(f"No subnet activity detected in the last {time_window}")
            return None
        
        print(f"\nFound {len(subnets_data)} subnets with activity")
        
        activity_summary = {
            'total_active_subnets': len(subnets_data),
            'total_connections': 0,
            'total_data_transfer': 0,
            'high_activity_subnets': [],
            'security_concerns': [],
            'protocol_distribution': {}
        }
        
        # Analyze each active subnet
        for subnet in subnets_data:
            label = subnet.get('label', f"Subnet {subnet.get('sid', 'Unknown')}")
            network = subnet.get('network', 'Unknown')
            
            print(f"\n📊 {label} ({network}):")
            
            # Activity statistics
            activity_stats = subnet.get('activityStats', {})
            if activity_stats:
                connections = activity_stats.get('totalConnections', 0)
                destinations = activity_stats.get('uniqueDestinations', 0)
                data_bytes = activity_stats.get('dataTransferred', 0)
                data_mb = data_bytes / (1024**2)
                
                activity_summary['total_connections'] += connections
                activity_summary['total_data_transfer'] += data_bytes
                
                print(f"   Connections: {connections:,}")
                print(f"   Unique Destinations: {destinations:,}")
                print(f"   Data Transfer: {data_mb:.2f} MB")
                
                # High activity detection
                if connections > 10000 or data_mb > 1000:
                    activity_summary['high_activity_subnets'].append({
                        'subnet': label,
                        'connections': connections,
                        'data_mb': data_mb
                    })
                    print(f"   🔥 HIGH ACTIVITY DETECTED")
                
                # Protocol analysis
                protocol_breakdown = activity_stats.get('protocolBreakdown', {})
                for protocol, percentage in protocol_breakdown.items():
                    activity_summary['protocol_distribution'][protocol] = \
                        activity_summary['protocol_distribution'].get(protocol, 0) + percentage
                    print(f"   {protocol}: {percentage:.1f}%")
            
            # Security analysis
            security_metrics = subnet.get('securityMetrics', {})
            if security_metrics:
                risk_score = security_metrics.get('riskScore', 0)
                active_breaches = security_metrics.get('activeBreaches', 0)
                threat_events = security_metrics.get('threatEvents', 0)
                
                print(f"   Risk Score: {risk_score:.3f}")
                print(f"   Active Breaches: {active_breaches}")
                print(f"   Threat Events: {threat_events}")
                
                # Security concern detection
                if risk_score > 0.7 or active_breaches > 0:
                    activity_summary['security_concerns'].append({
                        'subnet': label,
                        'risk_score': risk_score,
                        'active_breaches': active_breaches,
                        'threat_events': threat_events
                    })
                    print(f"   🚨 SECURITY CONCERN")
            
            # Device information
            device_count = subnet.get('deviceCount', 0)
            if device_count > 0:
                print(f"   Active Devices: {device_count}")
        
        # Summary report
        print(f"\n" + "="*50)
        print(f"ACTIVITY SUMMARY:")
        print(f"  Active Subnets: {activity_summary['total_active_subnets']}")
        print(f"  Total Connections: {activity_summary['total_connections']:,}")
        
        total_data_gb = activity_summary['total_data_transfer'] / (1024**3)
        print(f"  Total Data Transfer: {total_data_gb:.2f} GB")
        
        # High activity subnets
        if activity_summary['high_activity_subnets']:
            print(f"\nHIGH ACTIVITY SUBNETS:")
            for subnet_info in activity_summary['high_activity_subnets']:
                print(f"  🔥 {subnet_info['subnet']}")
                print(f"     Connections: {subnet_info['connections']:,}")
                print(f"     Data: {subnet_info['data_mb']:.2f} MB")
        
        # Security concerns
        if activity_summary['security_concerns']:
            print(f"\nSECURITY CONCERNS:")
            for concern in activity_summary['security_concerns']:
                print(f"  🚨 {concern['subnet']}")
                print(f"     Risk: {concern['risk_score']:.3f}")
                print(f"     Breaches: {concern['active_breaches']}")
                print(f"     Threats: {concern['threat_events']}")
        
        # Protocol distribution
        print(f"\nPROTOCOL DISTRIBUTION:")
        total_protocols = sum(activity_summary['protocol_distribution'].values())
        for protocol, total_percentage in activity_summary['protocol_distribution'].items():
            avg_percentage = total_percentage / len(subnets_data) if len(subnets_data) > 0 else 0
            print(f"  {protocol}: {avg_percentage:.1f}% (average)")
        
        return activity_summary
        
    except Exception as e:
        print(f"Error monitoring subnet activity: {e}")
        return None

# Example usage
# activity_report = monitor_subnet_activity("24hour")
```

### Subnet Security Analysis

```python
def analyze_subnet_security():
    """Comprehensive security analysis of all subnets"""
    
    print("Subnet Security Analysis")
    print("=" * 50)
    
    try:
        # Get all subnets
        all_subnets = client.subnets.get()
        subnets_data = all_subnets.get('subnets', [])
        
        security_analysis = {
            'total_subnets': len(subnets_data),
            'high_risk_subnets': [],
            'vulnerable_subnets': [],
            'breach_affected_subnets': [],
            'excluded_subnets': [],
            'dhcp_insecure_subnets': [],
            'overall_risk_score': 0,
            'security_recommendations': []
        }
        
        total_risk = 0
        
        for subnet in subnets_data:
            sid = subnet.get('sid', 0)
            label = subnet.get('label', f'Subnet {sid}')
            network = subnet.get('network', 'Unknown')
            
            print(f"\n🔍 Analyzing {label} ({network}):")
            
            # Security metrics analysis
            security_metrics = subnet.get('securityMetrics', {})
            risk_score = security_metrics.get('riskScore', 0)
            active_breaches = security_metrics.get('activeBreaches', 0)
            vulnerable_devices = security_metrics.get('vulnerableDevices', 0)
            threat_events = security_metrics.get('threatEvents', 0)
            
            total_risk += risk_score
            
            print(f"   Risk Score: {risk_score:.3f}")
            print(f"   Active Breaches: {active_breaches}")
            print(f"   Vulnerable Devices: {vulnerable_devices}")
            print(f"   Threat Events: {threat_events}")
            
            # Risk categorization
            if risk_score >= 0.8:
                security_analysis['high_risk_subnets'].append({
                    'subnet': label,
                    'network': network,
                    'risk_score': risk_score,
                    'active_breaches': active_breaches
                })
                print(f"   🔴 HIGH RISK SUBNET")
            
            # Vulnerability analysis
            if vulnerable_devices > 0:
                security_analysis['vulnerable_subnets'].append({
                    'subnet': label,
                    'network': network,
                    'vulnerable_devices': vulnerable_devices,
                    'risk_score': risk_score
                })
                print(f"   ⚠️  {vulnerable_devices} vulnerable devices")
            
            # Breach analysis
            if active_breaches > 0:
                security_analysis['breach_affected_subnets'].append({
                    'subnet': label,
                    'network': network,
                    'active_breaches': active_breaches,
                    'threat_events': threat_events
                })
                print(f"   🚨 {active_breaches} active breaches")
            
            # Configuration security analysis
            excluded = subnet.get('excluded', False)
            model_excluded = subnet.get('modelExcluded', False)
            dhcp_enabled = subnet.get('dhcp', False)
            unique_usernames = subnet.get('uniqueUsernames', False)
            unique_hostnames = subnet.get('uniqueHostnames', False)
            
            if excluded:
                security_analysis['excluded_subnets'].append({
                    'subnet': label,
                    'network': network,
                    'reason': 'Traffic not processed'
                })
                print(f"   ⭕ Excluded from processing")
            
            if model_excluded:
                security_analysis['excluded_subnets'].append({
                    'subnet': label,
                    'network': network,
                    'reason': 'Model excluded'
                })
                print(f"   ⭕ Model excluded")
            
            # DHCP security concerns
            if dhcp_enabled and not unique_usernames and not unique_hostnames:
                security_analysis['dhcp_insecure_subnets'].append({
                    'subnet': label,
                    'network': network,
                    'issue': 'DHCP enabled without unique tracking'
                })
                print(f"   ⚠️  DHCP without unique tracking")
            
            # Geographic security (if applicable)
            longitude = subnet.get('longitude')
            latitude = subnet.get('latitude')
            if longitude is not None and latitude is not None:
                print(f"   📍 Location: {latitude:.4f}, {longitude:.4f}")
        
        # Calculate overall risk
        if len(subnets_data) > 0:
            security_analysis['overall_risk_score'] = total_risk / len(subnets_data)
        
        # Generate security recommendations
        recommendations = []
        
        if security_analysis['high_risk_subnets']:
            recommendations.append("• Immediate investigation of high-risk subnets required")
            recommendations.append("• Consider implementing additional monitoring for high-risk networks")
        
        if security_analysis['vulnerable_subnets']:
            recommendations.append("• Patch vulnerable devices in affected subnets")
            recommendations.append("• Implement vulnerability scanning schedule")
        
        if security_analysis['breach_affected_subnets']:
            recommendations.append("• Respond to active breaches immediately")
            recommendations.append("• Review incident response procedures")
        
        if security_analysis['dhcp_insecure_subnets']:
            recommendations.append("• Enable unique username/hostname tracking for DHCP subnets")
            recommendations.append("• Review DHCP security configurations")
        
        if security_analysis['excluded_subnets']:
            recommendations.append("• Review exclusion policies for network segments")
            recommendations.append("• Ensure excluded subnets don't contain critical assets")
        
        if not recommendations:
            recommendations.append("• Continue current security monitoring practices")
            recommendations.append("• Regular security assessment recommended")
        
        security_analysis['security_recommendations'] = recommendations
        
        # Display security summary
        print(f"\n" + "="*50)
        print(f"SECURITY SUMMARY:")
        print(f"  Total Subnets: {security_analysis['total_subnets']}")
        print(f"  Overall Risk Score: {security_analysis['overall_risk_score']:.3f}")
        print(f"  High Risk Subnets: {len(security_analysis['high_risk_subnets'])}")
        print(f"  Vulnerable Subnets: {len(security_analysis['vulnerable_subnets'])}")
        print(f"  Breach Affected: {len(security_analysis['breach_affected_subnets'])}")
        print(f"  Excluded Subnets: {len(security_analysis['excluded_subnets'])}")
        
        # Detailed findings
        if security_analysis['high_risk_subnets']:
            print(f"\nHIGH RISK SUBNETS:")
            for subnet_info in security_analysis['high_risk_subnets']:
                print(f"  🔴 {subnet_info['subnet']} ({subnet_info['network']})")
                print(f"     Risk: {subnet_info['risk_score']:.3f}")
                print(f"     Breaches: {subnet_info['active_breaches']}")
        
        if security_analysis['breach_affected_subnets']:
            print(f"\nBREACH AFFECTED SUBNETS:")
            for subnet_info in security_analysis['breach_affected_subnets']:
                print(f"  🚨 {subnet_info['subnet']} ({subnet_info['network']})")
                print(f"     Active Breaches: {subnet_info['active_breaches']}")
                print(f"     Threat Events: {subnet_info['threat_events']}")
        
        # Security recommendations
        print(f"\nSECURITY RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"  {rec}")
        
        return security_analysis
        
    except Exception as e:
        print(f"Error analyzing subnet security: {e}")
        return None

# Example usage
# security_report = analyze_subnet_security()
```

## Error Handling

```python
try:
    # Get all subnets
    all_subnets = client.subnets.get()
    print("Subnets retrieved successfully")
    
    # Get specific subnet
    specific_subnet = client.subnets.get(subnet_id=123)
    print("Specific subnet retrieved")
    
    # Create new subnet
    new_subnet = client.subnets.post(
        sid=999,
        label="Test Subnet",
        network="10.0.99.0/24",
        dhcp=True
    )
    print("Subnet created successfully")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check parameters and network format")
        elif e.response.status_code == 401:
            print("Authentication failed - check tokens")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions")
        elif e.response.status_code == 404:
            print("Subnet not found - check subnet ID")
        elif e.response.status_code == 409:
            print("Conflict - subnet may already exist")
        elif e.response.status_code == 422:
            print("Validation error - check network CIDR format and parameters")
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
    print("Check that SID is a valid integer and coordinates are valid floats")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Subnet Management
- **Network organization**: Organize devices into logical network segments
- **Traffic processing**: Control how Darktrace processes traffic from different network segments
- **Device modeling**: Configure device modeling behavior per subnet
- **Geographic tracking**: Associate subnets with physical locations

### Configuration Options
- **DHCP tracking**: Enable/disable DHCP environment handling
- **Unique tracking**: Configure username and hostname uniqueness tracking
- **Exclusion policies**: Exclude subnets from processing or modeling
- **Location mapping**: Associate subnets with geographic coordinates

### Activity Monitoring
- **Time-based filtering**: Monitor subnet activity over specified time periods
- **Real-time analysis**: Current activity and connection statistics
- **Protocol breakdown**: Understand traffic composition by protocol
- **Data transfer tracking**: Monitor bandwidth usage and data flow

### Security Integration
- **Risk assessment**: Calculate and track subnet-level risk scores
- **Breach monitoring**: Track security breaches and threat events per subnet
- **Vulnerability tracking**: Monitor vulnerable devices within subnets
- **Threat intelligence**: Correlate subnet activity with threat indicators

### Network Topology
- **Visual representation**: Build network topology maps from subnet data
- **Relationship mapping**: Understand device-to-subnet relationships
- **Capacity planning**: Monitor subnet utilization and growth
- **Segmentation analysis**: Evaluate network segmentation effectiveness

### Performance Considerations
- **Filtering optimization**: Use seensince parameter to limit activity queries
- **Response data selection**: Use responsedata parameter to reduce bandwidth
- **Batch operations**: Process multiple subnet configurations efficiently
- **Caching strategies**: Cache subnet information for improved performance

### Best Practices
- **Consistent labeling**: Use descriptive labels for subnet identification
- **Geographic accuracy**: Ensure accurate coordinate information for location tracking
- **Security policies**: Align subnet configurations with security policies
- **Regular review**: Periodically review and update subnet configurations
- **Documentation**: Maintain documentation of subnet purposes and configurations

### Integration Patterns
- **CMDB integration**: Synchronize subnet information with configuration management databases
- **Network monitoring**: Integrate with network monitoring and management systems
- **Security tools**: Feed subnet context into security information systems
- **Asset management**: Use subnet information for asset inventory and management
- **Compliance reporting**: Generate compliance reports based on subnet configurations

### Use Cases
- **Network segmentation**: Implement and manage network segmentation strategies
- **Security monitoring**: Monitor network segments for security threats
- **Compliance management**: Ensure network configurations meet compliance requirements
- **Capacity planning**: Plan network capacity based on subnet utilization
- **Incident response**: Use subnet context for incident investigation and response
- **Asset discovery**: Discover and catalog network assets by subnet
