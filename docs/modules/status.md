# Status Module

The Status module provides comprehensive system health and status information from the Darktrace platform, including appliance status, probe connectivity, system performance metrics, and operational health indicators.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the status module
status = client.status
```

## Methods Overview

The Status module provides the following method:

- **`get()`** - Retrieve detailed system health and status information

## Methods

### Get System Status

Retrieve comprehensive system health and status information from the Darktrace platform.

```python
# Get complete system status
full_status = status.get()

# Get status without probe information (faster)
quick_status = status.get(includechildren=False, fast=True)

# Get only specific status data
core_status = status.get(
    responsedata="version,uptime,appliance_status"
)

# Get status with probe details
detailed_status = status.get(
    includechildren=True,
    fast=False
)

# Fast status check for monitoring
monitoring_status = status.get(
    fast=True,
    responsedata="health,performance"
)
```

#### Parameters

- `includechildren` (bool, optional): Whether to include information about probes (children). True by default
- `fast` (bool, optional): When true, returns data faster but may omit subnet connectivity information if not cached
- `responsedata` (str, optional): Restrict returned JSON to only specified top-level field(s) or object(s)

#### Response Structure

```python
{
  "system_info": {
    "instancename": "darktrace-main",
    "version": "6.4.2",
    "build": "202401150900",
    "uptime": 2592000,  # seconds
    "hostname": "dt-appliance-01",
    "appliance_id": "12345-67890-abcdef",
    "deployment_type": "physical",
    "timezone": "UTC",
    "system_time": 1705324800
  },
  "appliance_status": {
    "overall_health": "healthy",
    "status": "operational",
    "cpu_usage": 35.2,
    "memory_usage": 68.4,
    "disk_usage": 45.7,
    "network_utilization": 12.3,
    "temperature": 42.5,
    "fan_speed": 2800,
    "power_status": "normal",
    "last_reboot": 1702732800
  },
  "performance_metrics": {
    "packets_per_second": 15432,
    "bytes_per_second": 125829120,
    "connections_per_second": 245,
    "analysis_throughput": 98.7,
    "queue_depth": 23,
    "processing_latency": 12.5,  # milliseconds
    "model_execution_time": 8.3
  },
  "license_info": {
    "license_type": "enterprise",
    "expiry_date": 1735689600,
    "days_until_expiry": 180,
    "features_enabled": [
      "threat_detection",
      "antigena_email",
      "antigena_network",
      "compliance_reporting"
    ],
    "device_limit": 5000,
    "current_devices": 2847,
    "utilization_percentage": 56.9
  },
  "connectivity_status": {
    "internet_connectivity": True,
    "dns_resolution": True,
    "ntp_sync": True,
    "time_drift": 0.03,  # seconds
    "external_services": {
      "darktrace_cloud": "connected",
      "threat_intelligence": "connected",
      "update_service": "connected"
    }
  },
  "probes": [
    {
      "probe_id": "probe-001",
      "hostname": "dt-probe-01",
      "status": "connected",
      "version": "6.4.2",
      "location": "Data Center A",
      "last_seen": 1705324750,
      "uptime": 1728000,
      "health": "healthy",
      "network_interfaces": [
        {
          "interface": "eth0",
          "status": "up",
          "speed": "1000Mbps",
          "utilization": 23.4
        }
      ],
      "performance": {
        "cpu_usage": 28.5,
        "memory_usage": 54.2,
        "packets_captured": 8934567,
        "packets_dropped": 23
      }
    }
  ],
  "services_status": {
    "threat_detection": {
      "status": "running",
      "last_update": 1705324700,
      "models_loaded": 847,
      "active_models": 832
    },
    "data_ingestion": {
      "status": "running",
      "ingestion_rate": "125.8 MB/s",
      "queue_size": 1024,
      "processing_lag": 2.1  # seconds
    },
    "ai_analyst": {
      "status": "running",
      "incidents_processed": 156,
      "average_processing_time": 45.2
    },
    "antigena": {
      "network_status": "enabled",
      "email_status": "enabled",
      "actions_taken": 23,
      "active_inhibitions": 5
    }
  },
  "storage_status": {
    "total_capacity": 10995116277760,  # bytes
    "used_capacity": 5026332344320,
    "free_capacity": 5968783933440,
    "usage_percentage": 45.7,
    "estimated_days_remaining": 145,
    "data_retention_days": 90,
    "compression_ratio": 3.2
  },
  "database_status": {
    "status": "healthy",
    "connection_pool": "optimal",
    "query_performance": "good",
    "replication_lag": 0.5,  # seconds
    "backup_status": "current",
    "last_backup": 1705238400
  },
  "alerts": [
    {
      "severity": "warning",
      "category": "performance",
      "message": "CPU usage above 80% for extended period",
      "timestamp": 1705324500,
      "acknowledged": False
    },
    {
      "severity": "info",
      "category": "maintenance",
      "message": "Scheduled maintenance window approaching",
      "timestamp": 1705320000,
      "acknowledged": True
    }
  ],
  "network_stats": {
    "interfaces": [
      {
        "name": "eth0",
        "status": "up",
        "speed": "10Gbps",
        "rx_bytes": 2147483648000,
        "tx_bytes": 1073741824000,
        "rx_packets": 1500000000,
        "tx_packets": 750000000,
        "errors": 0,
        "drops": 12
      }
    ],
    "total_bandwidth_utilization": 15.7,
    "peak_bandwidth": 8.9  # Gbps
  }
}

```json
{
  "status": {
    "instancename": "Darktrace Enterprise",
    "version": "5.2.0",
    "uptime": "10 days, 5 hours, 32 minutes",
    "lastupdate": "2023-06-15T10:11:12Z",
    "models": {
      "total": 120,
      "active": 118
    },
    "connections": {
      "total": 15000,
      "active": 8750
    }
  }
}
```

## Examples

### Get Basic Status Information

```python
# Get basic status information
status_info = client.status.get()

# Extract and print instance name and version
instance_name = status_info.get("status", {}).get("instancename", "Unknown")
version = status_info.get("status", {}).get("version", "Unknown")
print(f"Connected to: {instance_name}")
print(f"Version: {version}")
```

### Check System Uptime

```python
# Get status with uptime information
status_info = client.status.get(response_data="uptime")

# Extract and print uptime
uptime = status_info.get("status", {}).get("uptime", "Unknown")
print(f"System uptime: {uptime}")
```

### Get Detailed Status Information

```python
# Get full status information
detailed_status = client.status.get(response_data="full")

# Process and display the information
status_data = detailed_status.get("status", {})
print(f"Instance: {status_data.get('instancename', 'Unknown')}")
print(f"Version: {status_data.get('version', 'Unknown')}")
print(f"Uptime: {status_data.get('uptime', 'Unknown')}")
print(f"Last Update: {status_data.get('lastupdate', 'Unknown')}")

# Display model information
models = status_data.get("models", {})
print(f"Models: {models.get('active', 0)} active out of {models.get('total', 0)} total")

# Display connection information
connections = status_data.get("connections", {})
print(f"Connections: {connections.get('active', 0)} active out of {connections.get('total', 0)} total")
```

### System Health Dashboard

```python
from darktrace import DarktraceClient
from datetime import datetime, timedelta

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def create_system_health_dashboard():
    """Create comprehensive system health dashboard"""
    
    print("Darktrace System Health Dashboard")
    print("=" * 60)
    
    try:
        # Get complete system status
        system_status = client.status.get()
        
        # System Information
        system_info = system_status.get('system_info', {})
        print(f"\n🖥️  SYSTEM INFORMATION:")
        print(f"   Instance: {system_info.get('instancename', 'Unknown')}")
        print(f"   Version: {system_info.get('version', 'Unknown')}")
        print(f"   Build: {system_info.get('build', 'Unknown')}")
        print(f"   Hostname: {system_info.get('hostname', 'Unknown')}")
        print(f"   Deployment: {system_info.get('deployment_type', 'Unknown')}")
        
        # Uptime calculation
        uptime_seconds = system_info.get('uptime', 0)
        uptime_days = uptime_seconds // 86400
        uptime_hours = (uptime_seconds % 86400) // 3600
        uptime_minutes = (uptime_seconds % 3600) // 60
        print(f"   Uptime: {uptime_days}d {uptime_hours}h {uptime_minutes}m")
        
        # Appliance Status
        appliance_status = system_status.get('appliance_status', {})
        overall_health = appliance_status.get('overall_health', 'unknown')
        
        if overall_health == 'healthy':
            health_icon = "🟢"
        elif overall_health == 'warning':
            health_icon = "🟡"
        elif overall_health == 'critical':
            health_icon = "🔴"
        else:
            health_icon = "⚪"
        
        print(f"\n{health_icon} APPLIANCE STATUS: {overall_health.upper()}")
        print(f"   Status: {appliance_status.get('status', 'Unknown')}")
        print(f"   CPU Usage: {appliance_status.get('cpu_usage', 0):.1f}%")
        print(f"   Memory Usage: {appliance_status.get('memory_usage', 0):.1f}%")
        print(f"   Disk Usage: {appliance_status.get('disk_usage', 0):.1f}%")
        print(f"   Network Utilization: {appliance_status.get('network_utilization', 0):.1f}%")
        print(f"   Temperature: {appliance_status.get('temperature', 0):.1f}°C")
        
        # Performance Metrics
        performance = system_status.get('performance_metrics', {})
        if performance:
            print(f"\n📊 PERFORMANCE METRICS:")
            print(f"   Packets/sec: {performance.get('packets_per_second', 0):,}")
            
            bytes_per_sec = performance.get('bytes_per_second', 0)
            mbps = bytes_per_sec * 8 / 1_000_000  # Convert to Mbps
            print(f"   Throughput: {mbps:.1f} Mbps")
            
            print(f"   Connections/sec: {performance.get('connections_per_second', 0):,}")
            print(f"   Analysis Throughput: {performance.get('analysis_throughput', 0):.1f}%")
            print(f"   Queue Depth: {performance.get('queue_depth', 0)}")
            print(f"   Processing Latency: {performance.get('processing_latency', 0):.1f}ms")
        
        # License Information
        license_info = system_status.get('license_info', {})
        if license_info:
            expiry_timestamp = license_info.get('expiry_date', 0)
            days_until_expiry = license_info.get('days_until_expiry', 0)
            
            if days_until_expiry <= 30:
                license_icon = "🔴"
            elif days_until_expiry <= 90:
                license_icon = "🟡"
            else:
                license_icon = "🟢"
            
            print(f"\n{license_icon} LICENSE STATUS:")
            print(f"   Type: {license_info.get('license_type', 'Unknown')}")
            print(f"   Days until expiry: {days_until_expiry}")
            
            if expiry_timestamp:
                expiry_date = datetime.fromtimestamp(expiry_timestamp)
                print(f"   Expires: {expiry_date.strftime('%Y-%m-%d')}")
            
            current_devices = license_info.get('current_devices', 0)
            device_limit = license_info.get('device_limit', 0)
            utilization = license_info.get('utilization_percentage', 0)
            
            print(f"   Device Usage: {current_devices:,}/{device_limit:,} ({utilization:.1f}%)")
        
        # Connectivity Status
        connectivity = system_status.get('connectivity_status', {})
        if connectivity:
            print(f"\n🌐 CONNECTIVITY:")
            
            statuses = [
                ("Internet", connectivity.get('internet_connectivity', False)),
                ("DNS", connectivity.get('dns_resolution', False)),
                ("NTP Sync", connectivity.get('ntp_sync', False))
            ]
            
            for service, status in statuses:
                status_icon = "✅" if status else "❌"
                print(f"   {status_icon} {service}")
            
            time_drift = connectivity.get('time_drift', 0)
            if time_drift > 5:
                drift_icon = "⚠️"
            else:
                drift_icon = "✅"
            print(f"   {drift_icon} Time Drift: {time_drift:.2f}s")
        
        # Probe Status
        probes = system_status.get('probes', [])
        if probes:
            print(f"\n🔗 PROBES ({len(probes)} total):")
            
            connected_probes = 0
            for probe in probes:
                probe_status = probe.get('status', 'unknown')
                health = probe.get('health', 'unknown')
                hostname = probe.get('hostname', 'Unknown')
                
                if probe_status == 'connected':
                    connected_probes += 1
                    status_icon = "🟢"
                else:
                    status_icon = "🔴"
                
                print(f"   {status_icon} {hostname} ({probe_status}, {health})")
                
                # Show performance for connected probes
                if probe_status == 'connected':
                    perf = probe.get('performance', {})
                    cpu = perf.get('cpu_usage', 0)
                    memory = perf.get('memory_usage', 0)
                    dropped = perf.get('packets_dropped', 0)
                    print(f"      CPU: {cpu:.1f}%, Mem: {memory:.1f}%, Dropped: {dropped}")
            
            probe_health = (connected_probes / len(probes)) * 100 if probes else 0
            print(f"   Probe Health: {connected_probes}/{len(probes)} connected ({probe_health:.1f}%)")
        
        # Storage Status
        storage = system_status.get('storage_status', {})
        if storage:
            print(f"\n💾 STORAGE:")
            
            total_gb = storage.get('total_capacity', 0) / (1024**3)
            used_gb = storage.get('used_capacity', 0) / (1024**3)
            free_gb = storage.get('free_capacity', 0) / (1024**3)
            usage_pct = storage.get('usage_percentage', 0)
            
            if usage_pct >= 90:
                storage_icon = "🔴"
            elif usage_pct >= 80:
                storage_icon = "🟡"
            else:
                storage_icon = "🟢"
            
            print(f"   {storage_icon} Usage: {used_gb:.1f}GB / {total_gb:.1f}GB ({usage_pct:.1f}%)")
            print(f"   Free Space: {free_gb:.1f}GB")
            
            days_remaining = storage.get('estimated_days_remaining', 0)
            if days_remaining < 30:
                days_icon = "🔴"
            elif days_remaining < 90:
                days_icon = "🟡"
            else:
                days_icon = "🟢"
            print(f"   {days_icon} Estimated Days Remaining: {days_remaining}")
        
        # Active Alerts
        alerts = system_status.get('alerts', [])
        if alerts:
            print(f"\n🚨 ACTIVE ALERTS ({len(alerts)} total):")
            
            for alert in alerts[:5]:  # Show top 5 alerts
                severity = alert.get('severity', 'info')
                message = alert.get('message', 'No message')
                acknowledged = alert.get('acknowledged', False)
                
                if severity == 'critical':
                    severity_icon = "🔴"
                elif severity == 'warning':
                    severity_icon = "🟡"
                else:
                    severity_icon = "🔵"
                
                ack_icon = "✅" if acknowledged else "❗"
                print(f"   {severity_icon}{ack_icon} {message}")
        
        # Overall System Assessment
        print(f"\n" + "="*60)
        print(f"OVERALL SYSTEM ASSESSMENT:")
        
        # Calculate overall health score
        health_score = 100
        issues = []
        
        if appliance_status.get('cpu_usage', 0) > 80:
            health_score -= 20
            issues.append("High CPU usage")
        
        if appliance_status.get('memory_usage', 0) > 90:
            health_score -= 20
            issues.append("High memory usage")
        
        if storage.get('usage_percentage', 0) > 90:
            health_score -= 25
            issues.append("Storage nearly full")
        
        if license_info.get('days_until_expiry', 365) <= 30:
            health_score -= 15
            issues.append("License expiring soon")
        
        if probes and (connected_probes / len(probes)) < 0.8:
            health_score -= 20
            issues.append("Probe connectivity issues")
        
        if not connectivity.get('internet_connectivity', True):
            health_score -= 30
            issues.append("Internet connectivity issues")
        
        # Overall health assessment
        if health_score >= 90:
            overall_icon = "🟢"
            overall_status = "EXCELLENT"
        elif health_score >= 75:
            overall_icon = "🟡"
            overall_status = "GOOD"
        elif health_score >= 50:
            overall_icon = "🟠"
            overall_status = "FAIR"
        else:
            overall_icon = "🔴"
            overall_status = "POOR"
        
        print(f"  {overall_icon} System Health: {overall_status} ({health_score}/100)")
        
        if issues:
            print(f"  Issues Detected:")
            for issue in issues:
                print(f"    • {issue}")
        else:
            print(f"  ✅ No critical issues detected")
        
        return system_status
        
    except Exception as e:
        print(f"Error creating dashboard: {e}")
        return None

# Example usage
# dashboard_data = create_system_health_dashboard()
```

### System Monitoring Script

```python
def monitor_system_health(alert_thresholds=None, monitoring_interval=300):
    """Continuous system monitoring with alerting"""
    
    import time
    from datetime import datetime
    
    if alert_thresholds is None:
        alert_thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 90.0,
            'disk_usage': 85.0,
            'storage_usage': 90.0,
            'license_days': 30,
            'probe_health': 80.0,
            'processing_latency': 50.0
        }
    
    print(f"System Health Monitoring Started")
    print(f"Monitoring interval: {monitoring_interval}s")
    print(f"Alert thresholds: {alert_thresholds}")
    print("=" * 60)
    
    alert_history = []
    
    def send_alert(severity, message, metric_value=None):
        """Send alert notification"""
        timestamp = datetime.now()
        alert = {
            'timestamp': timestamp,
            'severity': severity,
            'message': message,
            'metric_value': metric_value
        }
        alert_history.append(alert)
        
        # Print alert (in real implementation, send to monitoring system)
        severity_icons = {'critical': '🔴', 'warning': '🟡', 'info': '🔵'}
        icon = severity_icons.get(severity, '⚪')
        print(f"{icon} ALERT [{timestamp.strftime('%H:%M:%S')}] {severity.upper()}: {message}")
        if metric_value is not None:
            print(f"    Current value: {metric_value}")
    
    try:
        while True:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking system health...")
            
            try:
                # Get system status
                status = client.status.get(fast=True)
                
                # Check appliance metrics
                appliance = status.get('appliance_status', {})
                
                cpu_usage = appliance.get('cpu_usage', 0)
                if cpu_usage > alert_thresholds['cpu_usage']:
                    send_alert('warning', f'High CPU usage detected', f"{cpu_usage:.1f}%")
                
                memory_usage = appliance.get('memory_usage', 0)
                if memory_usage > alert_thresholds['memory_usage']:
                    send_alert('critical', f'High memory usage detected', f"{memory_usage:.1f}%")
                
                disk_usage = appliance.get('disk_usage', 0)
                if disk_usage > alert_thresholds['disk_usage']:
                    send_alert('warning', f'High disk usage detected', f"{disk_usage:.1f}%")
                
                # Check storage
                storage = status.get('storage_status', {})
                storage_usage = storage.get('usage_percentage', 0)
                if storage_usage > alert_thresholds['storage_usage']:
                    send_alert('critical', f'Storage nearly full', f"{storage_usage:.1f}%")
                
                # Check license
                license_info = status.get('license_info', {})
                days_until_expiry = license_info.get('days_until_expiry', 365)
                if days_until_expiry <= alert_thresholds['license_days']:
                    send_alert('warning', f'License expiring soon', f"{days_until_expiry} days")
                
                # Check probe health
                probes = status.get('probes', [])
                if probes:
                    connected_probes = sum(1 for p in probes if p.get('status') == 'connected')
                    probe_health = (connected_probes / len(probes)) * 100
                    if probe_health < alert_thresholds['probe_health']:
                        send_alert('warning', f'Probe connectivity issues', f"{probe_health:.1f}%")
                
                # Check performance
                performance = status.get('performance_metrics', {})
                latency = performance.get('processing_latency', 0)
                if latency > alert_thresholds['processing_latency']:
                    send_alert('warning', f'High processing latency', f"{latency:.1f}ms")
                
                # Check connectivity
                connectivity = status.get('connectivity_status', {})
                if not connectivity.get('internet_connectivity', True):
                    send_alert('critical', 'Internet connectivity lost')
                
                if not connectivity.get('ntp_sync', True):
                    send_alert('warning', 'NTP synchronization failed')
                
                # Status summary
                print(f"✅ Health check completed - CPU: {cpu_usage:.1f}%, Mem: {memory_usage:.1f}%, Disk: {disk_usage:.1f}%")
                
            except Exception as e:
                send_alert('critical', f'Health check failed: {e}')
                print(f"❌ Health check error: {e}")
            
            # Wait for next check
            time.sleep(monitoring_interval)
            
    except KeyboardInterrupt:
        print(f"\nMonitoring stopped by user")
        
        # Show alert summary
        if alert_history:
            print(f"\nAlert Summary ({len(alert_history)} alerts):")
            for alert in alert_history[-10:]:  # Show last 10 alerts
                timestamp = alert['timestamp'].strftime('%H:%M:%S')
                print(f"  {timestamp} {alert['severity'].upper()}: {alert['message']}")
    
    except Exception as e:
        print(f"Monitoring error: {e}")

# Example usage (commented to prevent automatic execution)
# monitor_system_health()
```

### Performance Analysis

```python
def analyze_system_performance(duration_hours=24):
    """Analyze system performance over time"""
    
    print(f"System Performance Analysis")
    print("=" * 50)
    print(f"Analysis period: {duration_hours} hours")
    
    try:
        # Get current status for baseline
        current_status = client.status.get()
        
        # Extract performance metrics
        performance = current_status.get('performance_metrics', {})
        appliance = current_status.get('appliance_status', {})
        
        print(f"\nCURRENT PERFORMANCE SNAPSHOT:")
        print(f"  CPU Usage: {appliance.get('cpu_usage', 0):.1f}%")
        print(f"  Memory Usage: {appliance.get('memory_usage', 0):.1f}%")
        print(f"  Network Utilization: {appliance.get('network_utilization', 0):.1f}%")
        
        pps = performance.get('packets_per_second', 0)
        bps = performance.get('bytes_per_second', 0)
        cps = performance.get('connections_per_second', 0)
        
        print(f"  Packets/sec: {pps:,}")
        print(f"  Bytes/sec: {bps:,} ({bps*8/1_000_000:.1f} Mbps)")
        print(f"  Connections/sec: {cps:,}")
        
        analysis_throughput = performance.get('analysis_throughput', 0)
        queue_depth = performance.get('queue_depth', 0)
        latency = performance.get('processing_latency', 0)
        
        print(f"  Analysis Throughput: {analysis_throughput:.1f}%")
        print(f"  Queue Depth: {queue_depth}")
        print(f"  Processing Latency: {latency:.1f}ms")
        
        # Performance assessment
        print(f"\nPERFORMANCE ASSESSMENT:")
        
        performance_score = 100
        issues = []
        recommendations = []
        
        # CPU assessment
        cpu_usage = appliance.get('cpu_usage', 0)
        if cpu_usage > 90:
            performance_score -= 30
            issues.append("Critical CPU usage")
            recommendations.append("• Consider hardware upgrade or load balancing")
        elif cpu_usage > 75:
            performance_score -= 15
            issues.append("High CPU usage")
            recommendations.append("• Monitor CPU trends and consider optimization")
        
        # Memory assessment
        memory_usage = appliance.get('memory_usage', 0)
        if memory_usage > 95:
            performance_score -= 25
            issues.append("Critical memory usage")
            recommendations.append("• Immediate memory optimization required")
        elif memory_usage > 85:
            performance_score -= 10
            issues.append("High memory usage")
            recommendations.append("• Monitor memory usage trends")
        
        # Throughput assessment
        if analysis_throughput < 80:
            performance_score -= 20
            issues.append("Low analysis throughput")
            recommendations.append("• Check model performance and queue management")
        
        # Latency assessment
        if latency > 100:
            performance_score -= 20
            issues.append("High processing latency")
            recommendations.append("• Optimize processing pipeline and check queue depth")
        elif latency > 50:
            performance_score -= 10
            issues.append("Elevated processing latency")
            recommendations.append("• Monitor latency trends")
        
        # Queue depth assessment
        if queue_depth > 1000:
            performance_score -= 15
            issues.append("High queue depth")
            recommendations.append("• Investigate processing bottlenecks")
        
        # Overall performance rating
        if performance_score >= 90:
            perf_rating = "🟢 EXCELLENT"
        elif performance_score >= 75:
            perf_rating = "🟡 GOOD"
        elif performance_score >= 60:
            perf_rating = "🟠 FAIR"
        else:
            perf_rating = "🔴 POOR"
        
        print(f"  Overall Performance: {perf_rating} ({performance_score}/100)")
        
        if issues:
            print(f"\n  Issues Detected:")
            for issue in issues:
                print(f"    • {issue}")
        
        if recommendations:
            print(f"\n  Recommendations:")
            for rec in recommendations:
                print(f"    {rec}")
        
        # Network interface analysis
        network_stats = current_status.get('network_stats', {})
        interfaces = network_stats.get('interfaces', [])
        
        if interfaces:
            print(f"\nNETWORK INTERFACE ANALYSIS:")
            
            for interface in interfaces:
                name = interface.get('name', 'Unknown')
                status = interface.get('status', 'unknown')
                speed = interface.get('speed', 'Unknown')
                
                rx_bytes = interface.get('rx_bytes', 0)
                tx_bytes = interface.get('tx_bytes', 0)
                errors = interface.get('errors', 0)
                drops = interface.get('drops', 0)
                
                print(f"  {name} ({status}, {speed}):")
                print(f"    RX: {rx_bytes/1_000_000_000:.2f} GB")
                print(f"    TX: {tx_bytes/1_000_000_000:.2f} GB")
                print(f"    Errors: {errors}, Drops: {drops}")
                
                if errors > 0 or drops > 100:
                    print(f"    ⚠️  Network issues detected")
        
        # Storage performance
        storage = current_status.get('storage_status', {})
        if storage:
            print(f"\nSTORAGE PERFORMANCE:")
            
            compression_ratio = storage.get('compression_ratio', 1.0)
            retention_days = storage.get('data_retention_days', 0)
            
            print(f"  Compression Ratio: {compression_ratio:.1f}:1")
            print(f"  Data Retention: {retention_days} days")
            
            if compression_ratio < 2.0:
                print(f"  📈 Consider enabling higher compression")
        
        return {
            'performance_score': performance_score,
            'issues': issues,
            'recommendations': recommendations,
            'current_metrics': performance
        }
        
    except Exception as e:
        print(f"Error analyzing performance: {e}")
        return None

# Example usage
# performance_analysis = analyze_system_performance()
```

## Error Handling

```python
try:
    # Get system status
    system_status = client.status.get()
    print("System status retrieved successfully")
    
    # Get fast status
    quick_status = client.status.get(fast=True, includechildren=False)
    print("Quick status check completed")
    
    # Get specific status data
    core_metrics = client.status.get(
        responsedata="appliance_status,performance_metrics"
    )
    print("Core metrics retrieved")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check parameters")
        elif e.response.status_code == 401:
            print("Authentication failed - check tokens")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions")
        elif e.response.status_code == 404:
            print("Status endpoint not found")
        elif e.response.status_code == 429:
            print("Rate limit exceeded - reduce request frequency")
        elif e.response.status_code == 503:
            print("Service unavailable - system may be under heavy load")
        else:
            print(f"Response: {e.response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
    print("Check network connectivity and host URL")

except requests.exceptions.Timeout as e:
    print(f"Request timeout: {e}")
    print("System may be under heavy load, try fast=True parameter")

except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
    print("The response might not be valid JSON")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### System Monitoring
- **Real-time status**: Provides current system health and operational status
- **Performance metrics**: Detailed performance indicators for system optimization
- **Probe management**: Monitor and manage distributed probe deployments
- **Resource utilization**: Track CPU, memory, disk, and network usage

### Health Assessment
- **Overall health**: Comprehensive health scoring based on multiple metrics
- **Alert generation**: Identify and alert on system health issues
- **Trend analysis**: Monitor system performance trends over time
- **Capacity planning**: Use metrics for capacity planning and scaling decisions

### License Management
- **License tracking**: Monitor license usage and expiration dates
- **Feature availability**: Track enabled features and capabilities
- **Usage monitoring**: Monitor device count against license limits
- **Compliance**: Ensure license compliance and plan renewals

### Connectivity Monitoring
- **External services**: Monitor connectivity to external services
- **Network health**: Track network interface status and performance
- **Time synchronization**: Monitor NTP synchronization and time drift
- **Service dependencies**: Monitor critical service dependencies

### Performance Optimization
- **Throughput monitoring**: Track packet processing and analysis throughput
- **Latency tracking**: Monitor processing latency and queue depths
- **Resource optimization**: Identify resource bottlenecks and optimization opportunities
- **Capacity management**: Plan capacity based on current and projected usage

### Operational Intelligence
- **Proactive monitoring**: Identify issues before they become critical
- **Automated alerting**: Generate alerts based on configurable thresholds
- **Historical analysis**: Track system performance trends and patterns
- **Maintenance planning**: Use metrics for maintenance window planning

### Fast Mode Benefits
- **Reduced latency**: Faster response times for frequent status checks
- **Lower overhead**: Reduced system load for monitoring operations
- **Selective data**: Option to exclude detailed probe information
- **Monitoring integration**: Ideal for integration with monitoring systems

### Response Data Filtering
- **Bandwidth optimization**: Reduce data transfer by selecting specific fields
- **Performance improvement**: Faster responses with targeted data retrieval
- **Integration efficiency**: Optimize API calls for specific use cases
- **Resource conservation**: Reduce network and processing overhead

### Use Cases
- **System administration**: Comprehensive system health monitoring and management
- **Performance monitoring**: Real-time performance tracking and optimization
- **Capacity planning**: Resource usage analysis for capacity planning
- **Compliance monitoring**: License and feature compliance tracking
- **Incident response**: System status during incident investigation
- **Maintenance planning**: System health assessment for maintenance scheduling
- **Integration monitoring**: Monitor system health from external monitoring systems