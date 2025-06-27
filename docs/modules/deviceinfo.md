# DeviceInfo Module

The DeviceInfo module provides detailed connection information and communication patterns for specific devices in your network. This module allows you to analyze device connections, data transfer patterns, external communications, and compare similar devices for baseline analysis.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the deviceinfo module
deviceinfo = client.deviceinfo
```

## Methods Overview

The DeviceInfo module provides the following method:

- **`get()`** - Retrieve detailed connection information for a specific device

## Methods

### Get Device Information

Retrieve comprehensive connection information and communication patterns for a specific device, including time-series data for connections, data transfer volumes, and external communications.

```python
# Get basic connection information for a device
device_connections = deviceinfo.get(did=12345)

# Get data transfer out patterns
data_out = deviceinfo.get(
    did=12345,
    datatype="sizeout",
    intervalhours=4
)

# Get data transfer in patterns  
data_in = deviceinfo.get(
    did=12345,
    datatype="sizein",
    intervalhours=1
)

# Get connections to specific destination device
device_to_device = deviceinfo.get(
    did=12345,
    odid=67890,
    datatype="co"
)

# Get connections to specific port
port_connections = deviceinfo.get(
    did=12345,
    port=443,
    fulldevicedetails=True
)

# Get external domain communications
external_comms = deviceinfo.get(
    did=12345,
    externaldomain="google.com",
    datatype="co"
)

# Compare with similar devices
similar_analysis = deviceinfo.get(
    did=12345,
    similardevices=5,
    fulldevicedetails=True,
    intervalhours=6
)
```

#### Parameters

- `did` (int, required): Device identification number
- `datatype` (str, optional): Data type to return - "co" (connections), "sizeout" (outbound data), "sizein" (inbound data). Default: "co"
- `odid` (int, optional): Destination device ID to filter connections
- `port` (int, optional): Specific port number to filter connections
- `externaldomain` (str, optional): Filter external communications by domain name
- `fulldevicedetails` (bool, optional): Include full device details for all referenced devices. Default: False
- `showallgraphdata` (bool, optional): Include zero-count intervals in time series. Default: True
- `similardevices` (int, optional): Include data for similar devices for comparison
- `intervalhours` (int, optional): Time interval grouping in hours. Default: 1

#### Response Structure

```python
{
  "device": {
    "did": 12345,
    "hostname": "workstation-01",
    "ip": "192.168.1.100",
    "mac": "00:11:22:33:44:55",
    "devicetype": 3,  # Laptop
    "os": 1,          # Windows
    "firstseen": 1640995200,
    "lastseen": 1705324800,
    "tags": ["corporate", "hr_department"]
  },
  
  # Connection data (datatype="co")
  "graphdata": [
    {
      "timestamp": 1705324800,
      "connections": 45,
      "unique_destinations": 12,
      "internal_connections": 35,
      "external_connections": 10,
      "protocols": {
        "TCP": 40,
        "UDP": 5
      },
      "ports": {
        "443": 25,
        "80": 10,
        "53": 5,
        "22": 3,
        "Other": 2
      }
    }
    // ... more time intervals
  ],
  
  # Data size out (datatype="sizeout")
  "graphdata": [
    {
      "timestamp": 1705324800,
      "bytes_out": 1048576,
      "packets_out": 1024,
      "sessions_out": 15,
      "top_destinations": [
        {
          "ip": "8.8.8.8",
          "bytes": 524288,
          "packets": 512
        }
      ]
    }
    // ... more intervals
  ],
  
  # Data size in (datatype="sizein")
  "graphdata": [
    {
      "timestamp": 1705324800,
      "bytes_in": 2097152,
      "packets_in": 2048, 
      "sessions_in": 20,
      "top_sources": [
        {
          "ip": "10.0.1.5",
          "bytes": 1048576,
          "packets": 1024
        }
      ]
    }
    // ... more intervals
  ],
  
  # Destination breakdown
  "destinations": [
    {
      "ip": "8.8.8.8",
      "hostname": "dns.google",
      "did": null,  # External
      "connections": 25,
      "first_connection": 1705320000,
      "last_connection": 1705324800,
      "bytes_sent": 524288,
      "bytes_received": 1048576,
      "ports": [53, 443],
      "protocols": ["UDP", "TCP"],
      "is_external": true,
      "country": "United States"
    },
    {
      "ip": "192.168.1.10",
      "hostname": "server-01",
      "did": 67890,
      "connections": 15,
      "first_connection": 1705322000,
      "last_connection": 1705324800,
      "bytes_sent": 262144,
      "bytes_received": 524288,
      "ports": [80, 443],
      "protocols": ["TCP"],
      "is_external": false
    }
  ],
  
  # With fulldevicedetails=True
  "devicedetails": {
    "12345": {
      "hostname": "workstation-01",
      "ip": "192.168.1.100",
      "mac": "00:11:22:33:44:55",
      "devicetype": 3,
      "os": 1,
      "vendor": "Dell Inc.",
      "model": "OptiPlex 7090",
      "location": "Building A, Floor 2",
      "owner": "john.doe@company.com",
      "compliance_tags": ["SOX", "GDPR"],
      "last_update": 1705324800
    },
    "67890": {
      "hostname": "server-01",
      "ip": "192.168.1.10",
      "mac": "aa:bb:cc:dd:ee:ff",
      "devicetype": 1,  # Server
      "os": 2,          # Linux
      "criticality": "high",
      "services": ["web", "database"]
    }
  },
  
  # With similardevices parameter
  "similar_devices": [
    {
      "did": 12346,
      "hostname": "workstation-02",
      "similarity_score": 0.92,
      "graphdata": [
        // Similar time series data structure
      ]
    },
    {
      "did": 12347,
      "hostname": "workstation-03", 
      "similarity_score": 0.87,
      "graphdata": [
        // Similar time series data structure
      ]
    }
  ],
  
  # Statistical summary
  "summary": {
    "total_connections": 1247,
    "unique_destinations": 89,
    "external_ratio": 0.15,
    "top_protocols": ["TCP", "UDP"],
    "top_ports": [443, 80, 53],
    "peak_activity_hour": 14,
    "data_transfer": {
      "total_bytes_out": 104857600,
      "total_bytes_in": 209715200,
      "avg_session_size": 1048576
    },
    "anomaly_indicators": [
      {
        "type": "unusual_port",
        "port": 8080,
        "confidence": 0.75,
        "description": "Uncommon port usage detected"
      }
    ]
  }
}
```

## Examples

### Comprehensive Device Connection Analysis

```python
from darktrace import DarktraceClient
from datetime import datetime, timedelta

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def analyze_device_connections(device_id, hours_back=24):
    """Comprehensive analysis of device connections"""
    
    print(f"Device Connection Analysis")
    print("=" * 50)
    print(f"Device ID: {device_id}")
    print(f"Analysis period: {hours_back} hours")
    
    try:
        # Get comprehensive connection data
        connection_data = client.deviceinfo.get(
            did=device_id,
            datatype="co",
            fulldevicedetails=True,
            showallgraphdata=True,
            intervalhours=1
        )
        
        device = connection_data.get('device', {})
        print(f"\nDEVICE INFORMATION:")
        print(f"  Hostname: {device.get('hostname', 'Unknown')}")
        print(f"  IP Address: {device.get('ip', 'Unknown')}")
        print(f"  MAC Address: {device.get('mac', 'Unknown')}")
        print(f"  Device Type: {device.get('devicetype', 'Unknown')}")
        print(f"  Operating System: {device.get('os', 'Unknown')}")
        
        # Analyze time series data
        graph_data = connection_data.get('graphdata', [])
        if graph_data:
            total_connections = sum(item.get('connections', 0) for item in graph_data)
            avg_connections = total_connections / len(graph_data) if graph_data else 0
            max_connections = max(item.get('connections', 0) for item in graph_data)
            
            print(f"\nCONNECTION STATISTICS:")
            print(f"  Total connections: {total_connections:,}")
            print(f"  Average per hour: {avg_connections:.1f}")
            print(f"  Peak connections: {max_connections:,}")
            
            # Protocol breakdown
            all_protocols = {}
            for item in graph_data:
                protocols = item.get('protocols', {})
                for protocol, count in protocols.items():
                    all_protocols[protocol] = all_protocols.get(protocol, 0) + count
            
            if all_protocols:
                print(f"\nPROTOCOL BREAKDOWN:")
                for protocol, count in sorted(all_protocols.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / total_connections * 100) if total_connections > 0 else 0
                    print(f"  {protocol}: {count:,} ({percentage:.1f}%)")
            
            # Port analysis
            all_ports = {}
            for item in graph_data:
                ports = item.get('ports', {})
                for port, count in ports.items():
                    all_ports[port] = all_ports.get(port, 0) + count
            
            if all_ports:
                print(f"\nTOP PORTS:")
                sorted_ports = sorted(all_ports.items(), key=lambda x: x[1], reverse=True)[:10]
                for port, count in sorted_ports:
                    percentage = (count / total_connections * 100) if total_connections > 0 else 0
                    print(f"  Port {port}: {count:,} ({percentage:.1f}%)")
        
        # Destination analysis
        destinations = connection_data.get('destinations', [])
        if destinations:
            print(f"\nDESTINATION ANALYSIS:")
            print(f"  Total unique destinations: {len(destinations)}")
            
            external_destinations = [d for d in destinations if d.get('is_external', False)]
            internal_destinations = [d for d in destinations if not d.get('is_external', True)]
            
            print(f"  External destinations: {len(external_destinations)}")
            print(f"  Internal destinations: {len(internal_destinations)}")
            
            # Top destinations by connections
            top_destinations = sorted(destinations, key=lambda x: x.get('connections', 0), reverse=True)[:10]
            print(f"\nTOP DESTINATIONS:")
            for dest in top_destinations:
                hostname = dest.get('hostname', dest.get('ip', 'Unknown'))
                connections = dest.get('connections', 0)
                is_external = "External" if dest.get('is_external', False) else "Internal"
                bytes_total = dest.get('bytes_sent', 0) + dest.get('bytes_received', 0)
                
                print(f"  {hostname}: {connections:,} connections ({is_external})")
                if bytes_total > 0:
                    if bytes_total >= 1073741824:  # GB
                        size_str = f"{bytes_total / 1073741824:.2f} GB"
                    elif bytes_total >= 1048576:  # MB
                        size_str = f"{bytes_total / 1048576:.2f} MB"
                    else:
                        size_str = f"{bytes_total / 1024:.2f} KB"
                    print(f"    Data transfer: {size_str}")
        
        # Summary analysis
        summary = connection_data.get('summary', {})
        if summary:
            print(f"\nSUMMARY ANALYSIS:")
            external_ratio = summary.get('external_ratio', 0)
            print(f"  External communication ratio: {external_ratio:.1%}")
            
            peak_hour = summary.get('peak_activity_hour')
            if peak_hour is not None:
                print(f"  Peak activity hour: {peak_hour:02d}:00")
            
            # Anomaly indicators
            anomalies = summary.get('anomaly_indicators', [])
            if anomalies:
                print(f"\nANOMALY INDICATORS:")
                for anomaly in anomalies:
                    anomaly_type = anomaly.get('type', 'Unknown')
                    confidence = anomaly.get('confidence', 0)
                    description = anomaly.get('description', 'No description')
                    print(f"  • {anomaly_type.replace('_', ' ').title()}: {description} (confidence: {confidence:.2%})")
        
        return connection_data
        
    except Exception as e:
        print(f"Error analyzing device connections: {e}")
        return None

# Example analysis
# device_analysis = analyze_device_connections(12345, hours_back=24)
```

### Data Transfer Pattern Analysis

```python
def analyze_data_patterns(device_id, intervalhours=4):
    """Analyze data transfer patterns for a device"""
    
    print(f"Data Transfer Pattern Analysis")
    print("=" * 50)
    print(f"Device ID: {device_id}")
    print(f"Interval: {intervalhours} hours")
    
    try:
        # Get outbound data patterns
        data_out = client.deviceinfo.get(
            did=device_id,
            datatype="sizeout",
            fulldevicedetails=True,
            intervalhours=intervalhours
        )
        
        # Get inbound data patterns
        data_in = client.deviceinfo.get(
            did=device_id,
            datatype="sizein",
            fulldevicedetails=True,
            intervalhours=intervalhours
        )
        
        # Analyze outbound patterns
        out_graph = data_out.get('graphdata', [])
        if out_graph:
            total_out = sum(item.get('bytes_out', 0) for item in out_graph)
            avg_out = total_out / len(out_graph) if out_graph else 0
            max_out = max(item.get('bytes_out', 0) for item in out_graph)
            
            print(f"\nOUTBOUND DATA TRANSFER:")
            print(f"  Total data sent: {format_bytes(total_out)}")
            print(f"  Average per interval: {format_bytes(avg_out)}")
            print(f"  Peak interval: {format_bytes(max_out)}")
        
        # Analyze inbound patterns
        in_graph = data_in.get('graphdata', [])
        if in_graph:
            total_in = sum(item.get('bytes_in', 0) for item in in_graph)
            avg_in = total_in / len(in_graph) if in_graph else 0
            max_in = max(item.get('bytes_in', 0) for item in in_graph)
            
            print(f"\nINBOUND DATA TRANSFER:")
            print(f"  Total data received: {format_bytes(total_in)}")
            print(f"  Average per interval: {format_bytes(avg_in)}")
            print(f"  Peak interval: {format_bytes(max_in)}")
        
        # Calculate transfer ratio
        if total_out > 0 and total_in > 0:
            ratio = total_out / total_in
            print(f"\nTRANSFER RATIO:")
            print(f"  Out/In ratio: {ratio:.2f}")
            
            if ratio > 2.0:
                pattern = "Upload-heavy (potential data exfiltration)"
            elif ratio < 0.5:
                pattern = "Download-heavy (data consumption)"
            else:
                pattern = "Balanced transfer"
            
            print(f"  Pattern: {pattern}")
        
        # Analyze top destinations/sources
        print(f"\nTOP DATA DESTINATIONS:")
        for interval in out_graph[-5:]:  # Last 5 intervals
            top_destinations = interval.get('top_destinations', [])
            if top_destinations:
                timestamp = datetime.fromtimestamp(interval['timestamp'])
                print(f"  {timestamp.strftime('%Y-%m-%d %H:%M')}:")
                for dest in top_destinations[:3]:
                    print(f"    {dest['ip']}: {format_bytes(dest['bytes'])}")
        
        print(f"\nTOP DATA SOURCES:")
        for interval in in_graph[-5:]:  # Last 5 intervals
            top_sources = interval.get('top_sources', [])
            if top_sources:
                timestamp = datetime.fromtimestamp(interval['timestamp'])
                print(f"  {timestamp.strftime('%Y-%m-%d %H:%M')}:")
                for source in top_sources[:3]:
                    print(f"    {source['ip']}: {format_bytes(source['bytes'])}")
        
        return {
            'outbound': data_out,
            'inbound': data_in,
            'total_out': total_out,
            'total_in': total_in
        }
        
    except Exception as e:
        print(f"Error analyzing data patterns: {e}")
        return None

def format_bytes(bytes_value):
    """Format bytes value for human readability"""
    if bytes_value >= 1073741824:  # GB
        return f"{bytes_value / 1073741824:.2f} GB"
    elif bytes_value >= 1048576:  # MB
        return f"{bytes_value / 1048576:.2f} MB"
    elif bytes_value >= 1024:  # KB
        return f"{bytes_value / 1024:.2f} KB"
    else:
        return f"{bytes_value} bytes"

# Example data pattern analysis
# data_patterns = analyze_data_patterns(12345, intervalhours=6)
```

### Device Comparison and Baseline Analysis

```python
def compare_similar_devices(device_id, num_similar=3):
    """Compare device with similar devices for baseline analysis"""
    
    print(f"Device Similarity Analysis")
    print("=" * 50)
    print(f"Primary Device ID: {device_id}")
    print(f"Comparing with {num_similar} similar devices")
    
    try:
        # Get device data with similar devices
        comparison_data = client.deviceinfo.get(
            did=device_id,
            datatype="co",
            similardevices=num_similar,
            fulldevicedetails=True,
            intervalhours=4
        )
        
        device = comparison_data.get('device', {})
        similar_devices = comparison_data.get('similar_devices', [])
        
        print(f"\nPRIMARY DEVICE:")
        print(f"  Hostname: {device.get('hostname', 'Unknown')}")
        print(f"  IP: {device.get('ip', 'Unknown')}")
        print(f"  Type: {device.get('devicetype', 'Unknown')}")
        
        # Analyze primary device metrics
        primary_graph = comparison_data.get('graphdata', [])
        primary_metrics = calculate_device_metrics(primary_graph)
        
        print(f"\nPRIMARY DEVICE METRICS:")
        print(f"  Total connections: {primary_metrics['total_connections']:,}")
        print(f"  Unique destinations: {primary_metrics['unique_destinations']}")
        print(f"  External ratio: {primary_metrics['external_ratio']:.2%}")
        print(f"  Peak connections: {primary_metrics['peak_connections']:,}")
        
        # Compare with similar devices
        print(f"\nSIMILAR DEVICES COMPARISON:")
        
        comparisons = []
        for similar in similar_devices:
            similar_metrics = calculate_device_metrics(similar.get('graphdata', []))
            
            comparison = {
                'device': similar,
                'metrics': similar_metrics,
                'similarity_score': similar.get('similarity_score', 0),
                'deviations': calculate_deviations(primary_metrics, similar_metrics)
            }
            comparisons.append(comparison)
        
        # Display comparisons
        for comp in comparisons:
            similar_device = comp['device']
            metrics = comp['metrics']
            deviations = comp['deviations']
            
            print(f"\n  Device: {similar_device.get('hostname', 'Unknown')} (ID: {similar_device.get('did')})")
            print(f"    Similarity Score: {comp['similarity_score']:.3f}")
            print(f"    Total Connections: {metrics['total_connections']:,}")
            print(f"    Unique Destinations: {metrics['unique_destinations']}")
            print(f"    External Ratio: {metrics['external_ratio']:.2%}")
            
            # Highlight significant deviations
            print(f"    Deviations from primary:")
            for metric, deviation in deviations.items():
                if abs(deviation) > 0.5:  # Significant deviation threshold
                    direction = "higher" if deviation > 0 else "lower"
                    print(f"      {metric}: {abs(deviation):.1f}x {direction}")
        
        # Baseline analysis
        print(f"\nBASELINE ANALYSIS:")
        
        # Calculate baseline from similar devices
        if comparisons:
            baseline_connections = sum(c['metrics']['total_connections'] for c in comparisons) / len(comparisons)
            baseline_destinations = sum(c['metrics']['unique_destinations'] for c in comparisons) / len(comparisons)
            baseline_external = sum(c['metrics']['external_ratio'] for c in comparisons) / len(comparisons)
            
            print(f"  Baseline connections: {baseline_connections:.0f}")
            print(f"  Baseline destinations: {baseline_destinations:.0f}")
            print(f"  Baseline external ratio: {baseline_external:.2%}")
            
            # Compare primary to baseline
            connection_deviation = (primary_metrics['total_connections'] / baseline_connections) if baseline_connections > 0 else 0
            destination_deviation = (primary_metrics['unique_destinations'] / baseline_destinations) if baseline_destinations > 0 else 0
            external_deviation = (primary_metrics['external_ratio'] / baseline_external) if baseline_external > 0 else 0
            
            print(f"\nPRIMARY vs BASELINE:")
            print(f"  Connection deviation: {connection_deviation:.2f}x")
            print(f"  Destination deviation: {destination_deviation:.2f}x")
            print(f"  External ratio deviation: {external_deviation:.2f}x")
            
            # Anomaly assessment
            anomalies = []
            if connection_deviation > 2.0:
                anomalies.append(f"Unusually high connection volume ({connection_deviation:.1f}x baseline)")
            elif connection_deviation < 0.5:
                anomalies.append(f"Unusually low connection volume ({connection_deviation:.1f}x baseline)")
            
            if destination_deviation > 2.0:
                anomalies.append(f"Unusually high destination diversity ({destination_deviation:.1f}x baseline)")
            
            if external_deviation > 2.0:
                anomalies.append(f"Unusually high external communication ({external_deviation:.1f}x baseline)")
            
            if anomalies:
                print(f"\nANOMALIES DETECTED:")
                for anomaly in anomalies:
                    print(f"  • {anomaly}")
            else:
                print(f"\nNo significant anomalies detected compared to baseline")
        
        return comparison_data
        
    except Exception as e:
        print(f"Error comparing devices: {e}")
        return None

def calculate_device_metrics(graph_data):
    """Calculate metrics from graph data"""
    if not graph_data:
        return {
            'total_connections': 0,
            'unique_destinations': 0,
            'external_ratio': 0,
            'peak_connections': 0
        }
    
    total_connections = sum(item.get('connections', 0) for item in graph_data)
    total_external = sum(item.get('external_connections', 0) for item in graph_data)
    peak_connections = max(item.get('connections', 0) for item in graph_data)
    
    # Calculate unique destinations (approximation)
    unique_destinations = sum(item.get('unique_destinations', 0) for item in graph_data) / len(graph_data)
    
    external_ratio = (total_external / total_connections) if total_connections > 0 else 0
    
    return {
        'total_connections': total_connections,
        'unique_destinations': int(unique_destinations),
        'external_ratio': external_ratio,
        'peak_connections': peak_connections
    }

def calculate_deviations(primary_metrics, similar_metrics):
    """Calculate deviations between primary and similar device metrics"""
    deviations = {}
    
    for metric in primary_metrics:
        primary_value = primary_metrics[metric]
        similar_value = similar_metrics[metric]
        
        if similar_value > 0:
            deviation = (primary_value - similar_value) / similar_value
            deviations[metric] = deviation
        else:
            deviations[metric] = 0
    
    return deviations

# Example device comparison
# device_comparison = compare_similar_devices(12345, num_similar=5)
```

### External Communication Analysis

```python
def analyze_external_communications(device_id, domain=None):
    """Analyze external communications for security assessment"""
    
    print(f"External Communication Analysis")
    print("=" * 50)
    print(f"Device ID: {device_id}")
    if domain:
        print(f"Filtering domain: {domain}")
    
    try:
        # Get external communication data
        if domain:
            external_data = client.deviceinfo.get(
                did=device_id,
                datatype="co",
                externaldomain=domain,
                fulldevicedetails=True
            )
        else:
            external_data = client.deviceinfo.get(
                did=device_id,
                datatype="co",
                fulldevicedetails=True
            )
        
        device = external_data.get('device', {})
        destinations = external_data.get('destinations', [])
        
        # Filter for external destinations only
        external_destinations = [d for d in destinations if d.get('is_external', False)]
        
        print(f"\nDEVICE: {device.get('hostname', 'Unknown')}")
        print(f"External destinations: {len(external_destinations)}")
        
        if not external_destinations:
            print("No external communications found")
            return None
        
        # Analyze external communications
        total_external_connections = sum(d.get('connections', 0) for d in external_destinations)
        
        print(f"\nEXTERNAL COMMUNICATION OVERVIEW:")
        print(f"  Total external connections: {total_external_connections:,}")
        print(f"  Unique external destinations: {len(external_destinations)}")
        
        # Country analysis
        countries = {}
        for dest in external_destinations:
            country = dest.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + dest.get('connections', 0)
        
        print(f"\nCOUNTRY BREAKDOWN:")
        sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
        for country, connections in sorted_countries[:10]:
            percentage = (connections / total_external_connections * 100) if total_external_connections > 0 else 0
            print(f"  {country}: {connections:,} ({percentage:.1f}%)")
        
        # Domain analysis
        domains = {}
        for dest in external_destinations:
            hostname = dest.get('hostname', '')
            if hostname and '.' in hostname:
                # Extract domain
                parts = hostname.split('.')
                if len(parts) >= 2:
                    domain = '.'.join(parts[-2:])  # Get last two parts
                    domains[domain] = domains.get(domain, 0) + dest.get('connections', 0)
        
        if domains:
            print(f"\nTOP EXTERNAL DOMAINS:")
            sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)
            for domain_name, connections in sorted_domains[:15]:
                percentage = (connections / total_external_connections * 100) if total_external_connections > 0 else 0
                print(f"  {domain_name}: {connections:,} ({percentage:.1f}%)")
        
        # Port analysis for external communications
        external_ports = {}
        for dest in external_destinations:
            ports = dest.get('ports', [])
            for port in ports:
                external_ports[port] = external_ports.get(port, 0) + dest.get('connections', 0)
        
        if external_ports:
            print(f"\nEXTERNAL PORTS:")
            sorted_ports = sorted(external_ports.items(), key=lambda x: x[1], reverse=True)
            for port, connections in sorted_ports[:10]:
                percentage = (connections / total_external_connections * 100) if total_external_connections > 0 else 0
                service = get_common_service(port)
                print(f"  Port {port} ({service}): {connections:,} ({percentage:.1f}%)")
        
        # Risk assessment
        print(f"\nRISK ASSESSMENT:")
        
        risk_factors = []
        risk_score = 0
        
        # High-risk countries
        high_risk_countries = ['Unknown', 'China', 'Russia', 'North Korea']
        high_risk_connections = sum(countries.get(country, 0) for country in high_risk_countries)
        if high_risk_connections > 0:
            risk_factors.append(f"Connections to high-risk countries: {high_risk_connections:,}")
            risk_score += 0.3
        
        # Unusual ports
        unusual_ports = [p for p in external_ports.keys() if p not in [80, 443, 53, 25, 110, 143, 993, 995]]
        if unusual_ports:
            unusual_connections = sum(external_ports[p] for p in unusual_ports)
            risk_factors.append(f"Unusual port usage: {len(unusual_ports)} ports, {unusual_connections:,} connections")
            risk_score += 0.2
        
        # High volume to single destination
        max_connections_to_single = max(d.get('connections', 0) for d in external_destinations)
        if max_connections_to_single > total_external_connections * 0.5:
            risk_factors.append(f"High concentration to single destination: {max_connections_to_single:,} connections")
            risk_score += 0.2
        
        # Many unique destinations
        if len(external_destinations) > 100:
            risk_factors.append(f"High number of unique destinations: {len(external_destinations)}")
            risk_score += 0.2
        
        # Display risk assessment
        if risk_score >= 0.7:
            risk_level = "🔴 HIGH RISK"
        elif risk_score >= 0.4:
            risk_level = "🟡 MEDIUM RISK"
        elif risk_score >= 0.2:
            risk_level = "🟠 LOW RISK"
        else:
            risk_level = "🟢 MINIMAL RISK"
        
        print(f"  Risk Level: {risk_level}")
        print(f"  Risk Score: {risk_score:.2f}")
        
        if risk_factors:
            print(f"  Risk Factors:")
            for factor in risk_factors:
                print(f"    • {factor}")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        recommendations = []
        
        if risk_score >= 0.5:
            recommendations.append("• Investigate high-risk external communications immediately")
            recommendations.append("• Consider blocking or monitoring suspicious destinations")
        
        if len(unusual_ports) > 5:
            recommendations.append("• Review unusual port usage and validate business need")
        
        if high_risk_connections > 0:
            recommendations.append("• Review connections to high-risk geographic locations")
        
        if len(external_destinations) > 200:
            recommendations.append("• Consider implementing stricter egress filtering")
        
        if not recommendations:
            recommendations.append("• External communications appear normal")
            recommendations.append("• Continue regular monitoring")
        
        for rec in recommendations:
            print(f"  {rec}")
        
        return external_data
        
    except Exception as e:
        print(f"Error analyzing external communications: {e}")
        return None

def get_common_service(port):
    """Get common service name for port number"""
    common_ports = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
        80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 993: 'IMAPS',
        995: 'POP3S', 3389: 'RDP', 5060: 'SIP', 8080: 'HTTP-Alt'
    }
    return common_ports.get(port, 'Unknown')

# Example external communication analysis
# external_analysis = analyze_external_communications(12345)
# domain_analysis = analyze_external_communications(12345, domain="google.com")
```

## Error Handling

```python
try:
    # Attempt to get device information
    device_info = client.deviceinfo.get(
        did=12345,
        datatype="co",
        fulldevicedetails=True,
        intervalhours=2
    )
    
    # Process device information
    device = device_info.get('device', {})
    print(f"Device: {device.get('hostname', 'Unknown')}")
    
    # Process graph data
    graph_data = device_info.get('graphdata', [])
    if graph_data:
        total_connections = sum(item.get('connections', 0) for item in graph_data)
        print(f"Total connections: {total_connections:,}")
    
    # Process destinations
    destinations = device_info.get('destinations', [])
    print(f"Unique destinations: {len(destinations)}")
    
    # Process device details if available
    device_details = device_info.get('devicedetails', {})
    for did, details in device_details.items():
        print(f"Device {did}: {details.get('hostname', 'Unknown')}")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check device ID and parameters")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for deviceinfo endpoint")
        elif e.response.status_code == 404:
            print("Device not found or no data available")
        elif e.response.status_code == 429:
            print("Rate limit exceeded - reduce request frequency")
        else:
            print(f"Response: {e.response.text}")
            
except ValueError as e:
    print(f"Value error: {e}")
    print("Check that device ID is a valid integer")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Data Types
- **"co" (connections)**: Connection count data with protocol and port breakdowns
- **"sizeout"**: Outbound data transfer volumes and top destinations  
- **"sizein"**: Inbound data transfer volumes and top sources
- **Time series data**: All data types provide time-series information for trend analysis

### Device Identification
- **Device ID (did)**: Primary device identifier (required parameter)
- **Destination device (odid)**: Filter connections to specific internal device
- **External filtering**: Use externaldomain to focus on specific external services
- **Port filtering**: Analyze connections to specific ports or services

### Time Series Configuration
- **Interval hours**: Configurable time grouping (1, 2, 4, 6, 12, 24 hours)
- **Show all data**: Option to include zero-count intervals for complete timeline
- **Historical analysis**: Data availability depends on retention settings
- **Real-time updates**: Recent data reflects current network activity

### Device Details
- **Full device details**: Enhanced information about all referenced devices
- **Device metadata**: Hostname, IP, MAC, type, OS, tags, and custom attributes
- **Relationship mapping**: Understanding connections between specific devices
- **Asset inventory**: Comprehensive device information for asset management

### Similarity Analysis
- **Behavioral baselines**: Compare device behavior with similar devices
- **Anomaly detection**: Identify deviations from peer group behavior
- **Risk assessment**: Understand normal vs abnormal communication patterns
- **Clustering insights**: Group devices by communication patterns

### External Communication Monitoring
- **Domain filtering**: Focus analysis on specific external services
- **Geographic analysis**: Understand communication patterns by country
- **Risk assessment**: Evaluate external communications for security threats
- **Compliance monitoring**: Track external data flows for regulatory compliance

### Performance Considerations
- **Time range impact**: Longer time ranges require more processing
- **Data volume**: Full device details increase response size
- **Similar devices**: Comparing multiple devices increases computation
- **Selective filtering**: Use specific parameters to focus analysis

### Security Applications
- **Threat hunting**: Identify suspicious communication patterns
- **Baseline establishment**: Understand normal device behavior
- **Incident investigation**: Detailed analysis during security incidents
- **Compliance monitoring**: Track and document network communications
- **Risk assessment**: Evaluate device communication risks

### Integration Scenarios
- **SIEM integration**: Feed device communication data to SIEM systems
- **Network monitoring**: Enhance network monitoring with behavioral analysis
- **Asset management**: Correlate with asset inventory systems
- **Security orchestration**: Automate responses based on communication patterns
- **Compliance reporting**: Generate reports for regulatory requirements

### Best Practices
- **Regular baselines**: Establish and update communication baselines regularly
- **Anomaly thresholds**: Define appropriate thresholds for anomaly detection
- **Historical analysis**: Use historical data for trend analysis and forecasting
- **Correlation analysis**: Correlate with other security data sources
- **Performance monitoring**: Monitor API performance and optimize queries

### Common Use Cases
- **Device profiling**: Understand device communication patterns and behavior
- **Threat detection**: Identify potential security threats in device communications
- **Network optimization**: Analyze traffic patterns for network optimization
- **Compliance auditing**: Document and report on network communications
- **Incident response**: Investigate device communications during security incidents
