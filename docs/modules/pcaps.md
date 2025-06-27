# PCAPs Module

The PCAPs module provides comprehensive packet capture functionality, allowing you to retrieve information about available packet captures, download PCAP files, and create new packet capture requests. This module is essential for detailed network forensics, incident investigation, and traffic analysis.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the pcaps module
pcaps = client.pcaps
```

## Methods Overview

The PCAPs module provides the following methods:

- **`get()`** - Retrieve PCAP information or download PCAP files
- **`create()`** - Create new packet capture requests

## Methods

### Get PCAPs

Retrieve PCAP information or download specific PCAP files from the Darktrace platform.

```python
# Get list of available PCAPs
available_pcaps = pcaps.get()

# Download specific PCAP file
pcap_data = pcaps.get(pcap_id="capture_20240127_143022.pcap")

# Get PCAP information with specific response data
pcap_info = pcaps.get(responsedata="filename,status,size")

# Get specific PCAP metadata
pcap_metadata = pcaps.get(
    pcap_id="network_incident_20240127.pcap",
    responsedata="creation_time,size,status"
)
```

#### Parameters

- `pcap_id` (str, optional): The filename of the PCAP to download. If not provided, returns a list of available PCAPs and their status
- `responsedata` (str, optional): Restrict returned JSON to only specified field(s) or object(s)

#### Response Structure

**List of PCAPs (when pcap_id not provided):**
```python
{
  "pcaps": [
    {
      "filename": "capture_20240127_143022.pcap",
      "creation_time": 1705324800,
      "size_bytes": 2147483648,
      "status": "ready",
      "duration_seconds": 300,
      "packet_count": 1547892,
      "capture_filters": {
        "source_ip": "192.168.1.100",
        "destination_ip": "203.0.113.50",
        "protocol": "tcp",
        "port_range": "80,443"
      },
      "capture_metadata": {
        "created_by": "incident_response",
        "incident_id": "INC-2024-001",
        "capture_reason": "suspicious_traffic_analysis",
        "retention_days": 30
      },
      "download_url": "/pcaps/capture_20240127_143022.pcap",
      "expires_at": 1708003200
    },
    {
      "filename": "network_baseline_20240126.pcap",
      "creation_time": 1705238400,
      "size_bytes": 524288000,
      "status": "processing",
      "progress": 75.5,
      "estimated_completion": 1705325400,
      "capture_filters": {
        "subnet": "192.168.1.0/24",
        "duration": 1800
      }
    }
  ],
  "storage_info": {
    "total_pcaps": 156,
    "total_size_gb": 1024.5,
    "available_space_gb": 2048.3,
    "retention_policy_days": 90,
    "auto_cleanup_enabled": true
  },
  "capture_capabilities": {
    "max_capture_duration": 3600,
    "max_file_size_gb": 10,
    "supported_protocols": ["tcp", "udp", "icmp"],
    "concurrent_captures": 5
  }
}
```

**Binary PCAP Data (when pcap_id provided):**
Returns raw binary PCAP file content for download.

### Create PCAP

Create a new packet capture request in the Darktrace system.

```python
# Create basic PCAP capture
new_capture = pcaps.create(
    ip1="192.168.1.100",
    start=1705324800,  # Start time (epoch seconds)
    end=1705325100     # End time (epoch seconds)
)

# Create targeted capture with specific parameters
targeted_capture = pcaps.create(
    ip1="192.168.1.100",      # Source IP
    ip2="203.0.113.50",       # Destination IP
    start=1705324800,
    end=1705325400,
    port1=12345,               # Source port
    port2=443,                 # Destination port
    protocol="tcp"             # Protocol filter
)

# Create bidirectional capture
bidirectional_capture = pcaps.create(
    ip1="10.0.1.50",
    ip2="10.0.1.100",
    start=1705324800,
    end=1705326600,
    protocol="udp"
)

# Create incident-specific capture
incident_capture = pcaps.create(
    ip1="172.16.1.25",
    start=1705324800,
    end=1705325700,
    port1=3389,                # RDP port
    protocol="tcp"
)
```

#### Parameters

- `ip1` (str, **required**): The source IP address
- `start` (int, **required**): Start time for packet capture (epoch seconds)
- `end` (int, **required**): End time for packet capture (epoch seconds)
- `ip2` (str, optional): The destination IP address
- `port1` (int, optional): The source port
- `port2` (int, optional): The destination port
- `protocol` (str, optional): Layer 3 protocol ("tcp" or "udp")

#### Response Structure

```python
{
  "result": "success",
  "capture_request": {
    "request_id": "cap_req_20240127_143500",
    "filename": "capture_20240127_143500.pcap",
    "status": "queued",
    "estimated_completion": 1705325400,
    "priority": "normal",
    "capture_parameters": {
      "source_ip": "192.168.1.100",
      "destination_ip": "203.0.113.50",
      "start_time": 1705324800,
      "end_time": 1705325100,
      "duration_seconds": 300,
      "source_port": 12345,
      "destination_port": 443,
      "protocol": "tcp"
    },
    "filters_applied": [
      "ip.src == 192.168.1.100",
      "ip.dst == 203.0.113.50",
      "tcp.port == 443"
    ],
    "estimated_size_mb": 25.6,
    "retention_expires": 1708003200
  },
  "queue_info": {
    "position": 3,
    "estimated_wait_minutes": 2,
    "concurrent_captures": 2
  }
}
```

## Examples

### Incident Response PCAP Analysis

```python
from darktrace import DarktraceClient
from datetime import datetime, timedelta
import os

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def incident_response_pcap_workflow(incident_id, suspicious_ip, time_range_hours=2):
    """Complete incident response workflow using PCAP captures"""
    
    print(f"Incident Response PCAP Workflow")
    print("=" * 50)
    print(f"Incident ID: {incident_id}")
    print(f"Suspicious IP: {suspicious_ip}")
    print(f"Time Range: {time_range_hours} hours")
    
    try:
        # Calculate time range
        end_time = int(datetime.now().timestamp())
        start_time = end_time - (time_range_hours * 3600)
        
        print(f"\nTime Range: {datetime.fromtimestamp(start_time)} to {datetime.fromtimestamp(end_time)}")
        
        # Step 1: Check existing PCAPs first
        print(f"\n1. CHECKING EXISTING PCAPS...")
        existing_pcaps = client.pcaps.get()
        
        relevant_pcaps = []
        if existing_pcaps.get('pcaps'):
            for pcap in existing_pcaps['pcaps']:
                # Check if PCAP covers our time range and IP
                pcap_time = pcap.get('creation_time', 0)
                if start_time <= pcap_time <= end_time:
                    # Check if it contains our suspicious IP
                    filters = pcap.get('capture_filters', {})
                    if (filters.get('source_ip') == suspicious_ip or 
                        filters.get('destination_ip') == suspicious_ip):
                        relevant_pcaps.append(pcap)
                        print(f"   📁 Found relevant PCAP: {pcap.get('filename', 'Unknown')}")
        
        if not relevant_pcaps:
            print(f"   No existing PCAPs found covering the incident timeframe")
        
        # Step 2: Create new PCAP captures if needed
        print(f"\n2. CREATING NEW PCAP CAPTURES...")
        
        capture_requests = []
        
        # Create comprehensive capture for suspicious IP
        print(f"   Creating capture for suspicious IP: {suspicious_ip}")
        comprehensive_capture = client.pcaps.create(
            ip1=suspicious_ip,
            start=start_time,
            end=end_time
        )
        capture_requests.append({
            'type': 'comprehensive',
            'request': comprehensive_capture,
            'description': f'All traffic from/to {suspicious_ip}'
        })
        
        # Create targeted captures for common attack vectors
        attack_vectors = [
            {'port': 22, 'protocol': 'tcp', 'description': 'SSH traffic'},
            {'port': 3389, 'protocol': 'tcp', 'description': 'RDP traffic'},
            {'port': 443, 'protocol': 'tcp', 'description': 'HTTPS traffic'},
            {'port': 53, 'protocol': 'udp', 'description': 'DNS traffic'}
        ]
        
        for vector in attack_vectors:
            print(f"   Creating targeted capture for {vector['description']}")
            try:
                targeted_capture = client.pcaps.create(
                    ip1=suspicious_ip,
                    start=start_time,
                    end=end_time,
                    port1=vector['port'],
                    protocol=vector['protocol']
                )
                capture_requests.append({
                    'type': 'targeted',
                    'request': targeted_capture,
                    'description': vector['description'],
                    'port': vector['port'],
                    'protocol': vector['protocol']
                })
            except Exception as e:
                print(f"     Warning: Could not create {vector['description']} capture: {e}")
        
        # Step 3: Monitor capture progress
        print(f"\n3. MONITORING CAPTURE PROGRESS...")
        
        import time
        capture_statuses = {}
        
        for i, capture_req in enumerate(capture_requests):
            request_data = capture_req['request']
            request_id = request_data.get('capture_request', {}).get('request_id', f'req_{i}')
            filename = request_data.get('capture_request', {}).get('filename', 'unknown.pcap')
            
            capture_statuses[request_id] = {
                'filename': filename,
                'description': capture_req['description'],
                'status': 'queued',
                'size': 0
            }
            
            print(f"   📊 {capture_req['description']}: {filename} (queued)")
        
        # Simulate monitoring (in real implementation, poll capture status)
        print(f"\n   Monitoring capture completion...")
        for _ in range(3):  # Check 3 times with delays
            time.sleep(2)  # Wait 2 seconds
            
            # Check status of captures
            updated_pcaps = client.pcaps.get()
            for pcap in updated_pcaps.get('pcaps', []):
                filename = pcap.get('filename', '')
                
                for req_id, status_info in capture_statuses.items():
                    if status_info['filename'] == filename:
                        current_status = pcap.get('status', 'unknown')
                        size_mb = pcap.get('size_bytes', 0) / (1024 * 1024)
                        
                        if current_status != status_info['status']:
                            status_info['status'] = current_status
                            status_info['size'] = size_mb
                            
                            status_icon = "✅" if current_status == 'ready' else "🔄" if current_status == 'processing' else "⏳"
                            print(f"     {status_icon} {status_info['description']}: {current_status} ({size_mb:.1f} MB)")
        
        # Step 4: Download and analyze ready PCAPs
        print(f"\n4. DOWNLOADING READY PCAPS...")
        
        download_results = []
        
        for req_id, status_info in capture_statuses.items():
            if status_info['status'] == 'ready':
                filename = status_info['filename']
                description = status_info['description']
                
                try:
                    print(f"   📥 Downloading {description}: {filename}")
                    
                    # Download PCAP data
                    pcap_data = client.pcaps.get(pcap_id=filename)
                    
                    # Save to local file
                    local_filename = f"incident_{incident_id}_{filename}"
                    
                    # In real implementation, save the binary data
                    # with open(local_filename, 'wb') as f:
                    #     f.write(pcap_data)
                    
                    download_results.append({
                        'filename': filename,
                        'local_file': local_filename,
                        'description': description,
                        'size_mb': status_info['size'],
                        'download_success': True
                    })
                    
                    print(f"     ✅ Downloaded successfully as {local_filename}")
                    
                except Exception as e:
                    print(f"     ❌ Download failed: {e}")
                    download_results.append({
                        'filename': filename,
                        'description': description,
                        'download_success': False,
                        'error': str(e)
                    })
        
        # Step 5: Generate incident report
        print(f"\n5. INCIDENT ANALYSIS SUMMARY:")
        print(f"   Incident ID: {incident_id}")
        print(f"   Suspicious IP: {suspicious_ip}")
        print(f"   Time Range: {time_range_hours} hours")
        print(f"   Capture Requests Created: {len(capture_requests)}")
        print(f"   Successful Downloads: {len([d for d in download_results if d.get('download_success')])}")
        
        total_size = sum(d.get('size_mb', 0) for d in download_results if d.get('download_success'))
        print(f"   Total PCAP Data: {total_size:.1f} MB")
        
        # Analysis recommendations
        print(f"\n   ANALYSIS RECOMMENDATIONS:")
        recommendations = [
            "• Analyze downloaded PCAPs using Wireshark or similar tools",
            "• Look for indicators of compromise (IoCs) in network traffic",
            "• Check for lateral movement patterns",
            "• Examine DNS queries for malicious domains",
            "• Analyze file transfers and data exfiltration attempts",
            "• Correlate timestamps with other security events",
            "• Document findings for incident report"
        ]
        
        for rec in recommendations:
            print(f"   {rec}")
        
        return {
            'incident_id': incident_id,
            'suspicious_ip': suspicious_ip,
            'time_range_hours': time_range_hours,
            'existing_pcaps': relevant_pcaps,
            'new_captures': capture_requests,
            'downloads': download_results,
            'total_size_mb': total_size
        }
        
    except Exception as e:
        print(f"Error in incident response workflow: {e}")
        return None

# Example usage
# incident_analysis = incident_response_pcap_workflow("INC-2024-001", "192.168.1.100", 4)
```

### PCAP Management and Analysis

```python
def manage_pcap_storage_and_analysis():
    """Comprehensive PCAP storage management and analysis"""
    
    print(f"PCAP Storage Management and Analysis")
    print("=" * 60)
    
    try:
        # Get current PCAP inventory
        pcap_inventory = client.pcaps.get()
        
        if not pcap_inventory.get('pcaps'):
            print("No PCAPs available for analysis")
            return None
        
        pcaps = pcap_inventory['pcaps']
        storage_info = pcap_inventory.get('storage_info', {})
        
        print(f"PCAP INVENTORY OVERVIEW:")
        print(f"  Total PCAPs: {storage_info.get('total_pcaps', len(pcaps))}")
        print(f"  Total Storage: {storage_info.get('total_size_gb', 0):.1f} GB")
        print(f"  Available Space: {storage_info.get('available_space_gb', 0):.1f} GB")
        print(f"  Retention Policy: {storage_info.get('retention_policy_days', 0)} days")
        
        # Categorize PCAPs by status
        status_categories = {}
        size_analysis = {'total_size': 0, 'largest_pcap': 0, 'average_size': 0}
        age_analysis = {'newest': None, 'oldest': None}
        
        current_time = int(datetime.now().timestamp())
        
        for pcap in pcaps:
            status = pcap.get('status', 'unknown')
            size_bytes = pcap.get('size_bytes', 0)
            creation_time = pcap.get('creation_time', 0)
            filename = pcap.get('filename', 'unknown')
            
            # Status categorization
            status_categories[status] = status_categories.get(status, 0) + 1
            
            # Size analysis
            size_analysis['total_size'] += size_bytes
            size_analysis['largest_pcap'] = max(size_analysis['largest_pcap'], size_bytes)
            
            # Age analysis
            age_days = (current_time - creation_time) / 86400 if creation_time > 0 else 0
            
            if age_analysis['newest'] is None or age_days < age_analysis['newest']:
                age_analysis['newest'] = age_days
            if age_analysis['oldest'] is None or age_days > age_analysis['oldest']:
                age_analysis['oldest'] = age_days
        
        # Calculate averages
        if pcaps:
            size_analysis['average_size'] = size_analysis['total_size'] / len(pcaps)
        
        print(f"\nPCAP STATUS BREAKDOWN:")
        for status, count in status_categories.items():
            percentage = (count / len(pcaps)) * 100
            print(f"  {status.title()}: {count} ({percentage:.1f}%)")
        
        print(f"\nSIZE ANALYSIS:")
        print(f"  Total Size: {size_analysis['total_size'] / (1024**3):.2f} GB")
        print(f"  Average Size: {size_analysis['average_size'] / (1024**2):.1f} MB")
        print(f"  Largest PCAP: {size_analysis['largest_pcap'] / (1024**2):.1f} MB")
        
        print(f"\nAGE ANALYSIS:")
        print(f"  Newest PCAP: {age_analysis['newest']:.1f} days old")
        print(f"  Oldest PCAP: {age_analysis['oldest']:.1f} days old")
        
        # Identify PCAPs for different purposes
        print(f"\nPCAP CATEGORIZATION:")
        
        # Large PCAPs (potential for detailed analysis)
        large_pcaps = [p for p in pcaps if p.get('size_bytes', 0) > 100 * 1024 * 1024]  # > 100MB
        print(f"  Large PCAPs (>100MB): {len(large_pcaps)}")
        
        # Recent PCAPs (last 7 days)
        recent_pcaps = [p for p in pcaps if (current_time - p.get('creation_time', 0)) / 86400 <= 7]
        print(f"  Recent PCAPs (≤7 days): {len(recent_pcaps)}")
        
        # Ready for analysis
        ready_pcaps = [p for p in pcaps if p.get('status') == 'ready']
        print(f"  Ready for Analysis: {len(ready_pcaps)}")
        
        # Processing PCAPs
        processing_pcaps = [p for p in pcaps if p.get('status') == 'processing']
        print(f"  Currently Processing: {len(processing_pcaps)}")
        
        # Show processing progress
        if processing_pcaps:
            print(f"\n  PROCESSING PROGRESS:")
            for pcap in processing_pcaps:
                filename = pcap.get('filename', 'unknown')
                progress = pcap.get('progress', 0)
                estimated_completion = pcap.get('estimated_completion', 0)
                
                print(f"    📊 {filename}: {progress:.1f}%")
                if estimated_completion > 0:
                    completion_time = datetime.fromtimestamp(estimated_completion)
                    print(f"       ETA: {completion_time.strftime('%H:%M:%S')}")
        
        # Detailed analysis of ready PCAPs
        if ready_pcaps:
            print(f"\nREADY PCAPS ANALYSIS:")
            
            # Sort by size for analysis priority
            ready_pcaps_sorted = sorted(ready_pcaps, key=lambda x: x.get('size_bytes', 0), reverse=True)
            
            print(f"  Top 5 PCAPs by Size:")
            for i, pcap in enumerate(ready_pcaps_sorted[:5], 1):
                filename = pcap.get('filename', 'unknown')
                size_mb = pcap.get('size_bytes', 0) / (1024**2)
                packet_count = pcap.get('packet_count', 0)
                duration = pcap.get('duration_seconds', 0)
                
                print(f"    {i}. {filename}")
                print(f"       Size: {size_mb:.1f} MB, Packets: {packet_count:,}, Duration: {duration}s")
                
                # Show capture filters if available
                filters = pcap.get('capture_filters', {})
                if filters:
                    filter_desc = []
                    if filters.get('source_ip'):
                        filter_desc.append(f"src:{filters['source_ip']}")
                    if filters.get('destination_ip'):
                        filter_desc.append(f"dst:{filters['destination_ip']}")
                    if filters.get('protocol'):
                        filter_desc.append(f"proto:{filters['protocol']}")
                    if filter_desc:
                        print(f"       Filters: {', '.join(filter_desc)}")
        
        # Storage optimization recommendations
        print(f"\nSTORAGE OPTIMIZATION:")
        
        # Calculate storage utilization
        total_storage_gb = storage_info.get('total_size_gb', 0)
        available_space_gb = storage_info.get('available_space_gb', 0)
        used_space_gb = total_storage_gb
        total_capacity_gb = used_space_gb + available_space_gb
        
        if total_capacity_gb > 0:
            utilization_pct = (used_space_gb / total_capacity_gb) * 100
            print(f"  Storage Utilization: {utilization_pct:.1f}%")
            
            if utilization_pct > 90:
                print(f"  🔴 CRITICAL: Storage nearly full")
            elif utilization_pct > 80:
                print(f"  🟡 WARNING: High storage usage")
            else:
                print(f"  🟢 Storage usage normal")
        
        # Retention analysis
        retention_days = storage_info.get('retention_policy_days', 90)
        old_pcaps = [p for p in pcaps if (current_time - p.get('creation_time', 0)) / 86400 > retention_days]
        
        if old_pcaps:
            print(f"  PCAPs exceeding retention ({retention_days} days): {len(old_pcaps)}")
            old_size_gb = sum(p.get('size_bytes', 0) for p in old_pcaps) / (1024**3)
            print(f"  Space recoverable: {old_size_gb:.2f} GB")
        
        # Analysis recommendations
        print(f"\nANALYSIS RECOMMENDATIONS:")
        
        recommendations = []
        
        if len(large_pcaps) > 0:
            recommendations.append(f"• Prioritize analysis of {len(large_pcaps)} large PCAPs")
        
        if len(recent_pcaps) > 10:
            recommendations.append(f"• Review {len(recent_pcaps)} recent PCAPs for current threats")
        
        if utilization_pct > 85:
            recommendations.append("• Consider archiving or deleting old PCAPs")
        
        if len(processing_pcaps) > 5:
            recommendations.append("• Monitor processing queue - high load detected")
        
        recommendations.extend([
            "• Implement automated PCAP analysis workflows",
            "• Use threat intelligence to prioritize PCAP analysis",
            "• Consider compression for long-term PCAP storage",
            "• Regular cleanup of expired PCAPs"
        ])
        
        for rec in recommendations:
            print(f"  {rec}")
        
        return {
            'inventory_summary': {
                'total_pcaps': len(pcaps),
                'status_breakdown': status_categories,
                'size_analysis': size_analysis,
                'age_analysis': age_analysis
            },
            'categorization': {
                'large_pcaps': len(large_pcaps),
                'recent_pcaps': len(recent_pcaps),
                'ready_pcaps': len(ready_pcaps),
                'processing_pcaps': len(processing_pcaps)
            },
            'storage_info': storage_info,
            'recommendations': recommendations
        }
        
    except Exception as e:
        print(f"Error in PCAP management: {e}")
        return None

# Example usage
# pcap_management = manage_pcap_storage_and_analysis()
```

### Automated PCAP Collection for Threat Hunting

```python
def automated_threat_hunting_pcaps(threat_indicators, time_window_hours=24):
    """Automated PCAP collection based on threat indicators"""
    
    print(f"Automated Threat Hunting PCAP Collection")
    print("=" * 60)
    print(f"Time Window: {time_window_hours} hours")
    print(f"Threat Indicators: {len(threat_indicators)}")
    
    try:
        # Calculate time range
        end_time = int(datetime.now().timestamp())
        start_time = end_time - (time_window_hours * 3600)
        
        collection_results = {
            'threat_indicators': threat_indicators,
            'time_range': {'start': start_time, 'end': end_time},
            'capture_requests': [],
            'existing_relevant_pcaps': [],
            'collection_summary': {}
        }
        
        print(f"\nTime Range: {datetime.fromtimestamp(start_time)} to {datetime.fromtimestamp(end_time)}")
        
        # Step 1: Check existing PCAPs for relevant data
        print(f"\n1. CHECKING EXISTING PCAPS...")
        
        existing_pcaps = client.pcaps.get()
        
        for pcap in existing_pcaps.get('pcaps', []):
            pcap_time = pcap.get('creation_time', 0)
            
            # Check if PCAP is within our time window
            if start_time <= pcap_time <= end_time:
                filters = pcap.get('capture_filters', {})
                
                # Check if PCAP contains any of our threat indicators
                for indicator in threat_indicators:
                    if indicator['type'] == 'ip_address':
                        ip = indicator['value']
                        if (filters.get('source_ip') == ip or 
                            filters.get('destination_ip') == ip):
                            collection_results['existing_relevant_pcaps'].append({
                                'pcap': pcap,
                                'matched_indicator': indicator,
                                'relevance': 'direct_ip_match'
                            })
                    
                    elif indicator['type'] == 'port':
                        port = indicator['value']
                        if (filters.get('port1') == port or 
                            filters.get('port2') == port):
                            collection_results['existing_relevant_pcaps'].append({
                                'pcap': pcap,
                                'matched_indicator': indicator,
                                'relevance': 'port_match'
                            })
        
        if collection_results['existing_relevant_pcaps']:
            print(f"   Found {len(collection_results['existing_relevant_pcaps'])} relevant existing PCAPs")
        else:
            print(f"   No existing PCAPs match threat indicators")
        
        # Step 2: Create targeted captures for each threat indicator
        print(f"\n2. CREATING TARGETED CAPTURES...")
        
        for i, indicator in enumerate(threat_indicators):
            indicator_type = indicator['type']
            indicator_value = indicator['value']
            priority = indicator.get('priority', 'medium')
            
            print(f"\n   Indicator {i+1}: {indicator_type} = {indicator_value} (priority: {priority})")
            
            try:
                if indicator_type == 'ip_address':
                    # Create comprehensive capture for suspicious IP
                    capture_request = client.pcaps.create(
                        ip1=indicator_value,
                        start=start_time,
                        end=end_time
                    )
                    
                    collection_results['capture_requests'].append({
                        'indicator': indicator,
                        'capture_type': 'ip_comprehensive',
                        'request': capture_request,
                        'description': f'All traffic for IP {indicator_value}'
                    })
                    
                    # Also create protocol-specific captures for high-priority IPs
                    if priority == 'high':
                        for protocol in ['tcp', 'udp']:
                            try:
                                protocol_capture = client.pcaps.create(
                                    ip1=indicator_value,
                                    start=start_time,
                                    end=end_time,
                                    protocol=protocol
                                )
                                
                                collection_results['capture_requests'].append({
                                    'indicator': indicator,
                                    'capture_type': f'ip_{protocol}',
                                    'request': protocol_capture,
                                    'description': f'{protocol.upper()} traffic for IP {indicator_value}'
                                })
                            except Exception as e:
                                print(f"     Warning: Could not create {protocol} capture: {e}")
                
                elif indicator_type == 'domain':
                    # Create DNS captures for domain indicators
                    # Note: This would require DNS resolution to get IPs
                    print(f"     Domain indicators require DNS resolution (not implemented in this example)")
                
                elif indicator_type == 'port':
                    # Create port-specific captures
                    port = int(indicator_value)
                    
                    # Determine likely protocol based on port
                    tcp_ports = [22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389]
                    udp_ports = [53, 67, 68, 69, 123, 161, 162, 500, 4500]
                    
                    protocols_to_capture = []
                    if port in tcp_ports or port > 1024:
                        protocols_to_capture.append('tcp')
                    if port in udp_ports or port > 1024:
                        protocols_to_capture.append('udp')
                    
                    if not protocols_to_capture:
                        protocols_to_capture = ['tcp', 'udp']  # Default to both
                    
                    for protocol in protocols_to_capture:
                        try:
                            port_capture = client.pcaps.create(
                                ip1="0.0.0.0",  # Any IP
                                start=start_time,
                                end=end_time,
                                port1=port,
                                protocol=protocol
                            )
                            
                            collection_results['capture_requests'].append({
                                'indicator': indicator,
                                'capture_type': f'port_{protocol}',
                                'request': port_capture,
                                'description': f'Port {port}/{protocol.upper()} traffic'
                            })
                        except Exception as e:
                            print(f"     Warning: Could not create port {port}/{protocol} capture: {e}")
                
                elif indicator_type == 'subnet':
                    # Create subnet-wide captures
                    subnet = indicator_value
                    print(f"     Subnet captures require network-wide collection (not implemented)")
                
                print(f"     ✅ Capture requests created for {indicator_type} indicator")
                
            except Exception as e:
                print(f"     ❌ Failed to create captures for {indicator_type} {indicator_value}: {e}")
        
        # Step 3: Monitor and prioritize captures
        print(f"\n3. CAPTURE PRIORITIZATION AND MONITORING...")
        
        # Sort captures by priority
        high_priority_captures = [
            cr for cr in collection_results['capture_requests']
            if cr['indicator'].get('priority') == 'high'
        ]
        
        medium_priority_captures = [
            cr for cr in collection_results['capture_requests']
            if cr['indicator'].get('priority') == 'medium'
        ]
        
        low_priority_captures = [
            cr for cr in collection_results['capture_requests']
            if cr['indicator'].get('priority') == 'low'
        ]
        
        print(f"   High Priority Captures: {len(high_priority_captures)}")
        print(f"   Medium Priority Captures: {len(medium_priority_captures)}")
        print(f"   Low Priority Captures: {len(low_priority_captures)}")
        
        # Step 4: Generate collection summary
        print(f"\n4. COLLECTION SUMMARY:")
        
        total_captures = len(collection_results['capture_requests'])
        total_existing = len(collection_results['existing_relevant_pcaps'])
        
        collection_results['collection_summary'] = {
            'total_indicators': len(threat_indicators),
            'new_captures_created': total_captures,
            'existing_relevant_pcaps': total_existing,
            'high_priority_captures': len(high_priority_captures),
            'coverage_assessment': 'comprehensive' if total_captures > 0 else 'limited'
        }
        
        print(f"   Total Threat Indicators: {len(threat_indicators)}")
        print(f"   New Capture Requests: {total_captures}")
        print(f"   Existing Relevant PCAPs: {total_existing}")
        print(f"   High Priority Captures: {len(high_priority_captures)}")
        
        # Step 5: Analysis workflow recommendations
        print(f"\n5. ANALYSIS WORKFLOW RECOMMENDATIONS:")
        
        recommendations = []
        
        if high_priority_captures:
            recommendations.append("• Prioritize analysis of high-priority indicator captures")
        
        if total_existing > 0:
            recommendations.append("• Start analysis with existing relevant PCAPs while new captures process")
        
        if total_captures > 10:
            recommendations.append("• Consider parallel analysis workflows for large capture sets")
        
        recommendations.extend([
            "• Correlate PCAP findings with SIEM and log data",
            "• Look for lateral movement patterns across captures",
            "• Extract and analyze file transfers from PCAP data",
            "• Document IoCs found for threat intelligence feeds",
            "• Update threat hunting rules based on findings"
        ])
        
        for rec in recommendations:
            print(f"   {rec}")
        
        # Step 6: Automation suggestions
        print(f"\n6. AUTOMATION OPPORTUNITIES:")
        
        automation_suggestions = [
            "• Automate PCAP creation based on threat intelligence feeds",
            "• Implement automatic IoC extraction from completed PCAPs",
            "• Set up alerts for high-priority capture completion",
            "• Create automated correlation with other security data sources",
            "• Develop playbooks for common threat hunting scenarios"
        ]
        
        for suggestion in automation_suggestions:
            print(f"   {suggestion}")
        
        return collection_results
        
    except Exception as e:
        print(f"Error in automated threat hunting PCAP collection: {e}")
        return None

# Example threat indicators
example_threat_indicators = [
    {
        'type': 'ip_address',
        'value': '203.0.113.50',
        'priority': 'high',
        'description': 'Known C2 server'
    },
    {
        'type': 'ip_address',
        'value': '198.51.100.25',
        'priority': 'medium',
        'description': 'Suspicious external IP'
    },
    {
        'type': 'port',
        'value': '4444',
        'priority': 'high',
        'description': 'Common reverse shell port'
    },
    {
        'type': 'port',
        'value': '8080',
        'priority': 'medium',
        'description': 'Alternative HTTP port'
    },
    {
        'type': 'domain',
        'value': 'malicious-domain.com',
        'priority': 'high',
        'description': 'Known malicious domain'
    }
]

# Example usage
# threat_hunting_results = automated_threat_hunting_pcaps(example_threat_indicators, 24)
```

## Error Handling

```python
try:
    # Get PCAP list
    pcap_list = client.pcaps.get()
    print("PCAP list retrieved successfully")
    
    # Download specific PCAP
    pcap_data = client.pcaps.get(pcap_id="capture_20240127.pcap")
    print("PCAP downloaded successfully")
    
    # Create new PCAP capture
    new_capture = client.pcaps.create(
        ip1="192.168.1.100",
        start=1705324800,
        end=1705325100,
        protocol="tcp"
    )
    print("PCAP capture request created successfully")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check parameters (IP addresses, time range, protocol)")
        elif e.response.status_code == 401:
            print("Authentication failed - check tokens")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for PCAP operations")
        elif e.response.status_code == 404:
            print("PCAP not found - check PCAP ID/filename")
        elif e.response.status_code == 409:
            print("Conflict - capture request may overlap with existing capture")
        elif e.response.status_code == 413:
            print("Request too large - time range or capture scope too broad")
        elif e.response.status_code == 429:
            print("Rate limit exceeded - too many capture requests")
        elif e.response.status_code == 503:
            print("Service unavailable - PCAP system may be overloaded")
        else:
            print(f"Response: {e.response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
    print("Check network connectivity and host URL")

except requests.exceptions.Timeout as e:
    print(f"Request timeout: {e}")
    print("PCAP operations may take time - consider increasing timeout")

except ValueError as e:
    print(f"Value error: {e}")
    print("Check parameter types - IPs (string), ports (int), times (int)")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Packet Capture Operations
- **Real-time capture**: Create packet captures for specific time ranges and filters
- **Historical analysis**: Access previously captured packet data
- **Targeted collection**: Filter captures by IP, port, protocol, and time
- **Bulk operations**: Manage multiple capture requests and downloads

### Forensic Analysis
- **Incident response**: Capture network traffic for security incident investigation
- **Threat hunting**: Proactive capture of potentially malicious traffic
- **Compliance**: Capture traffic for regulatory compliance requirements
- **Network troubleshooting**: Detailed packet analysis for network issues

### Capture Filtering
- **IP filtering**: Capture traffic to/from specific IP addresses
- **Port filtering**: Focus on specific network services or protocols
- **Protocol filtering**: Separate TCP, UDP, or other protocol traffic
- **Bidirectional capture**: Capture both directions of network communication

### Storage Management
- **Retention policies**: Automatic cleanup based on age and storage limits
- **Compression**: Efficient storage of packet capture data
- **Capacity planning**: Monitor and manage PCAP storage utilization
- **Archive strategies**: Long-term retention and archival of important captures

### Performance Considerations
- **Capture duration**: Balance detail level with storage and processing requirements
- **Network impact**: Minimize impact on network performance during captures
- **Processing queues**: Manage concurrent capture and processing operations
- **Resource allocation**: Optimize system resources for capture operations

### Integration Workflows
- **SIEM integration**: Correlate PCAP data with security events
- **Threat intelligence**: Use threat feeds to prioritize capture targets
- **Incident response**: Integrate PCAP collection into IR workflows
- **Automated analysis**: Develop automated PCAP analysis pipelines

### Analysis Tools
- **Wireshark compatibility**: Export PCAPs for analysis in standard tools
- **Custom analysis**: Develop custom packet analysis scripts and tools
- **IoC extraction**: Automatically extract indicators of compromise
- **Pattern recognition**: Identify recurring network patterns and anomalies

### Security Considerations
- **Data sensitivity**: Handle captured data according to privacy requirements
- **Access controls**: Restrict PCAP access to authorized personnel
- **Encryption**: Protect stored PCAP data with appropriate encryption
- **Audit trails**: Maintain records of PCAP access and analysis activities

### Use Cases
- **Security incident response**: Detailed network forensics for security events
- **Threat hunting**: Proactive search for indicators of compromise
- **Compliance auditing**: Network traffic analysis for regulatory compliance
- **Performance analysis**: Network performance troubleshooting and optimization
- **Malware analysis**: Network behavior analysis of malicious software
- **Data leak investigation**: Investigation of unauthorized data transfers
- **Network baseline establishment**: Capture normal traffic patterns for comparison
