# MetricData Module

The MetricData module provides access to time-series metric data from Darktrace. This module allows you to retrieve actual metric values over time for analysis, monitoring, and reporting purposes. It works closely with the Metrics module to provide quantitative data for the metrics defined in your Darktrace deployment.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the metricdata module
metricdata = client.metricdata
```

## Methods Overview

The MetricData module provides the following method:

- **`get()`** - Retrieve time-series metric data with extensive filtering and aggregation options

## Methods

### Get Metric Data

Retrieve time-series metric data from Darktrace. This method provides comprehensive access to quantitative metrics with filtering by devices, protocols, ports, time ranges, and various aggregation options.

```python
# Get basic metric data
bandwidth_data = metricdata.get(
    metric="bandwidth",
    starttime=1705320000000,
    endtime=1705323600000
)

# Get multiple metrics at once
multi_metrics = metricdata.get(
    metrics=["bandwidth", "connection_count", "device_activity"],
    did=123,
    interval="5min"
)

# Get device-specific metric data
device_metrics = metricdata.get(
    metric="device_activity",
    did=123,
    from_=1705320000000,
    to=1705323600000,
    fulldevicedetails=True
)

# Get network protocol metrics
protocol_metrics = metricdata.get(
    metric="protocol_usage",
    protocol="tcp",
    destinationport=443,
    interval="1hour"
)

# Get metrics with breach correlation
breach_metrics = metricdata.get(
    metric="anomaly_score",
    did=123,
    breachtimes=True,
    interval="15min"
)

# Get metrics for multiple devices
multi_device = metricdata.get(
    metric="bandwidth",
    devices=["123", "456", "789"],
    interval="1hour"
)
```

#### Parameters

- `metric` (str, optional): Single metric name to retrieve (use this OR metrics parameter)
- `metrics` (List[str], optional): List of metric names to retrieve (use this OR metric parameter)
- `did` (int, optional): Device ID for device-specific metrics
- `ddid` (int, optional): Destination device ID for connection-based metrics
- `odid` (int, optional): Other device ID for multi-device metrics
- `port` (int, optional): Port number filter (matches source or destination)
- `sourceport` (int, optional): Source port number filter
- `destinationport` (int, optional): Destination port number filter
- `protocol` (str, optional): IP protocol filter (tcp, udp, icmp, etc.)
- `applicationprotocol` (str, optional): Application protocol filter (http, https, smtp, etc.)
- `starttime` (int, optional): Start time in milliseconds since epoch (UTC)
- `endtime` (int, optional): End time in milliseconds since epoch (UTC)
- `from_` (int, optional): Alternative start time parameter (epoch milliseconds)
- `to` (int, optional): Alternative end time parameter (epoch milliseconds)
- `interval` (str, optional): Time aggregation interval ('1min', '5min', '1hour', '1day', etc.)
- `breachtimes` (bool, optional): Include model breach times in the response
- `fulldevicedetails` (bool, optional): Include complete device information in response
- `devices` (List[str], optional): List of device IDs or names for multi-device queries

#### Response Structure

```python
# Single metric response
{
  "metric": "bandwidth",
  "interval": "5min",
  "unit": "bytes/sec",
  "datatype": "numeric",
  "timerange": {
    "start": 1705320000000,
    "end": 1705323600000
  },
  "data": [
    {
      "timestamp": 1705320000000,
      "value": 1048576,
      "device": {
        "did": 123,
        "ip": "192.168.1.100",
        "hostname": "workstation-01"
      }
    },
    {
      "timestamp": 1705320300000,
      "value": 2097152,
      "device": {
        "did": 123,
        "ip": "192.168.1.100",
        "hostname": "workstation-01"
      }
    }
    // ... more data points
  ]
}

# Multiple metrics response
{
  "metrics": ["bandwidth", "connection_count", "device_activity"],
  "interval": "5min",
  "timerange": {
    "start": 1705320000000,
    "end": 1705323600000
  },
  "data": {
    "bandwidth": [
      {
        "timestamp": 1705320000000,
        "value": 1048576,
        "unit": "bytes/sec",
        "device": {"did": 123, "ip": "192.168.1.100"}
      }
      // ... more data points
    ],
    "connection_count": [
      {
        "timestamp": 1705320000000,
        "value": 25,
        "unit": "count",
        "device": {"did": 123, "ip": "192.168.1.100"}
      }
      // ... more data points
    ],
    "device_activity": [
      {
        "timestamp": 1705320000000,
        "value": 7.2,
        "unit": "score",
        "device": {"did": 123, "ip": "192.168.1.100"}
      }
      // ... more data points
    ]
  }
}

# With fulldevicedetails=True
{
  "metric": "device_activity",
  "data": [
    {
      "timestamp": 1705320000000,
      "value": 7.2,
      "device": {
        "did": 123,
        "ip": "192.168.1.100",
        "hostname": "workstation-01",
        "devicelabel": "Employee Workstation",
        "macaddress": "00:1B:44:11:3A:B7",
        "vendor": "Dell Inc.",
        "os": "Windows 10",
        "devicetype": "desktop",
        "tags": ["corporate", "finance-dept"]
      }
    }
    // ... more data points
  ]
}

# With breachtimes=True
{
  "metric": "anomaly_score",
  "data": [
    {
      "timestamp": 1705320000000,
      "value": 0.85,
      "device": {"did": 123},
      "breaches": [
        {
          "breach_id": "uuid-breach-123",
          "model_name": "Device / Anomalous Activity",
          "score": 0.95,
          "time": 1705320060000
        }
      ]
    }
    // ... more data points
  ]
}

# Multi-device response
{
  "metric": "bandwidth",
  "devices": ["123", "456", "789"],
  "data": [
    {
      "timestamp": 1705320000000,
      "values": [
        {"device_id": "123", "value": 1048576},
        {"device_id": "456", "value": 2097152},
        {"device_id": "789", "value": 512000}
      ]
    }
    // ... more timestamps
  ]
}
```

## Examples

### Basic Metric Time Series Analysis

```python
from darktrace import DarktraceClient
import datetime

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get bandwidth data for the last 24 hours
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(hours=24)

bandwidth_data = client.metricdata.get(
    metric="bandwidth",
    starttime=int(start_time.timestamp() * 1000),
    endtime=int(end_time.timestamp() * 1000),
    interval="1hour"
)

print("Bandwidth Analysis (Last 24 Hours)")
print("=" * 50)

# Analyze bandwidth trends
data_points = bandwidth_data.get('data', [])
if data_points:
    total_bandwidth = 0
    peak_bandwidth = 0
    peak_time = None
    hourly_averages = []
    
    for point in data_points:
        timestamp = point.get('timestamp', 0)
        value = point.get('value', 0)
        
        total_bandwidth += value
        hourly_averages.append(value)
        
        if value > peak_bandwidth:
            peak_bandwidth = value
            peak_time = datetime.datetime.fromtimestamp(timestamp / 1000)
    
    avg_bandwidth = total_bandwidth / len(data_points) if data_points else 0
    
    print(f"Total data points: {len(data_points)}")
    print(f"Average bandwidth: {avg_bandwidth:,.0f} bytes/sec")
    print(f"Peak bandwidth: {peak_bandwidth:,.0f} bytes/sec")
    if peak_time:
        print(f"Peak time: {peak_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show hourly breakdown
    print(f"\nHourly Bandwidth Breakdown:")
    for i, point in enumerate(data_points[-12:]):  # Last 12 hours
        timestamp = point.get('timestamp', 0)
        value = point.get('value', 0)
        time_str = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%H:%M')
        print(f"  {time_str}: {value:,.0f} bytes/sec")
```

### Device Performance Monitoring

```python
# Monitor specific device performance metrics
device_id = 123

# Get multiple performance metrics for the device
performance_data = client.metricdata.get(
    metrics=["bandwidth", "connection_count", "cpu_usage", "memory_usage"],
    did=device_id,
    starttime=int((datetime.datetime.now() - datetime.timedelta(hours=4)).timestamp() * 1000),
    endtime=int(datetime.datetime.now().timestamp() * 1000),
    interval="15min",
    fulldevicedetails=True
)

print(f"Device Performance Analysis (DID: {device_id})")
print("=" * 60)

# Extract device information
device_info = None
data = performance_data.get('data', {})

if data:
    # Get device info from first metric's first data point
    for metric_name, metric_data in data.items():
        if metric_data and len(metric_data) > 0:
            first_point = metric_data[0]
            device_info = first_point.get('device', {})
            break
    
    if device_info:
        print(f"Device: {device_info.get('hostname', 'Unknown')} ({device_info.get('ip', 'Unknown IP')})")
        print(f"Label: {device_info.get('devicelabel', 'No label')}")
        print(f"Type: {device_info.get('devicetype', 'Unknown')}")
        print(f"OS: {device_info.get('os', 'Unknown')}")

# Analyze each metric
for metric_name, metric_data in data.items():
    if not metric_data:
        continue
    
    print(f"\n{metric_name.upper()} Analysis:")
    
    values = [point.get('value', 0) for point in metric_data if point.get('value') is not None]
    
    if values:
        avg_value = sum(values) / len(values)
        max_value = max(values)
        min_value = min(values)
        
        # Get unit from first data point
        unit = metric_data[0].get('unit', 'N/A') if metric_data else 'N/A'
        
        print(f"  Average: {avg_value:.2f} {unit}")
        print(f"  Maximum: {max_value:.2f} {unit}")
        print(f"  Minimum: {min_value:.2f} {unit}")
        print(f"  Data points: {len(values)}")
        
        # Show trend (last 4 values)
        if len(values) >= 4:
            recent_values = values[-4:]
            print(f"  Recent trend: {' → '.join([f'{v:.1f}' for v in recent_values])}")

# Performance correlation analysis
if 'bandwidth' in data and 'connection_count' in data:
    print(f"\nPerformance Correlation Analysis:")
    
    bandwidth_values = [p.get('value', 0) for p in data['bandwidth'] if p.get('value') is not None]
    connection_values = [p.get('value', 0) for p in data['connection_count'] if p.get('value') is not None]
    
    if len(bandwidth_values) == len(connection_values) and len(bandwidth_values) > 0:
        # Simple correlation calculation
        correlations = []
        for i in range(len(bandwidth_values)):
            if connection_values[i] > 0:
                ratio = bandwidth_values[i] / connection_values[i]
                correlations.append(ratio)
        
        if correlations:
            avg_bytes_per_connection = sum(correlations) / len(correlations)
            print(f"  Average bytes per connection: {avg_bytes_per_connection:,.0f}")
```

### Network Protocol Analysis

```python
# Analyze network protocol metrics
protocol_metrics = ["tcp_connections", "udp_traffic", "http_requests", "https_requests"]

protocol_data = client.metricdata.get(
    metrics=protocol_metrics,
    starttime=int((datetime.datetime.now() - datetime.timedelta(hours=8)).timestamp() * 1000),
    endtime=int(datetime.datetime.now().timestamp() * 1000),
    interval="30min"
)

print("Network Protocol Analysis")
print("=" * 50)

data = protocol_data.get('data', {})

# Analyze each protocol metric
protocol_stats = {}
for metric_name, metric_data in data.items():
    if not metric_data:
        continue
    
    values = [point.get('value', 0) for point in metric_data if point.get('value') is not None]
    
    if values:
        protocol_stats[metric_name] = {
            'total': sum(values),
            'average': sum(values) / len(values),
            'peak': max(values),
            'data_points': len(values)
        }

# Display protocol statistics
for protocol, stats in sorted(protocol_stats.items(), key=lambda x: x[1]['total'], reverse=True):
    print(f"\n{protocol.upper()}:")
    print(f"  Total: {stats['total']:,.0f}")
    print(f"  Average: {stats['average']:,.1f}")
    print(f"  Peak: {stats['peak']:,.0f}")
    print(f"  Data points: {stats['data_points']}")

# Protocol distribution analysis
if protocol_stats:
    total_across_protocols = sum(stats['total'] for stats in protocol_stats.values())
    
    print(f"\nProtocol Distribution:")
    for protocol, stats in sorted(protocol_stats.items(), key=lambda x: x[1]['total'], reverse=True):
        percentage = (stats['total'] / total_across_protocols) * 100 if total_across_protocols > 0 else 0
        print(f"  {protocol}: {percentage:.1f}% of total traffic")
```

### Security Metrics and Breach Correlation

```python
# Analyze security metrics with breach correlation
security_metrics = client.metricdata.get(
    metrics=["anomaly_score", "threat_level", "model_alerts"],
    did=123,
    starttime=int((datetime.datetime.now() - datetime.timedelta(hours=12)).timestamp() * 1000),
    endtime=int(datetime.datetime.now().timestamp() * 1000),
    interval="10min",
    breachtimes=True
)

print("Security Metrics Analysis with Breach Correlation")
print("=" * 70)

data = security_metrics.get('data', {})

# Analyze security trends
for metric_name, metric_data in data.items():
    if not metric_data:
        continue
    
    print(f"\n{metric_name.upper()} Analysis:")
    
    # Extract values and breach information
    values = []
    breach_count = 0
    breach_times = []
    
    for point in metric_data:
        value = point.get('value')
        if value is not None:
            values.append(value)
        
        # Check for breaches
        breaches = point.get('breaches', [])
        if breaches:
            breach_count += len(breaches)
            for breach in breaches:
                breach_times.append({
                    'time': breach.get('time'),
                    'model': breach.get('model_name'),
                    'score': breach.get('score')
                })
    
    if values:
        avg_value = sum(values) / len(values)
        max_value = max(values)
        min_value = min(values)
        
        print(f"  Average score: {avg_value:.3f}")
        print(f"  Maximum score: {max_value:.3f}")
        print(f"  Minimum score: {min_value:.3f}")
        print(f"  Associated breaches: {breach_count}")
        
        # High-risk periods
        high_risk_threshold = 0.8  # Adjust based on your environment
        high_risk_count = sum(1 for v in values if v > high_risk_threshold)
        
        if high_risk_count > 0:
            print(f"  High-risk periods (>{high_risk_threshold}): {high_risk_count}")
    
    # Breach details
    if breach_times:
        print(f"  Recent breaches:")
        for breach in sorted(breach_times, key=lambda x: x.get('time', 0), reverse=True)[:5]:
            breach_time = datetime.datetime.fromtimestamp(breach.get('time', 0) / 1000)
            model_name = breach.get('model', 'Unknown')
            score = breach.get('score', 0)
            print(f"    {breach_time.strftime('%H:%M:%S')} - {model_name} (Score: {score:.3f})")

# Security trend analysis
if 'anomaly_score' in data:
    anomaly_data = data['anomaly_score']
    
    print(f"\nSecurity Trend Analysis:")
    
    # Calculate rolling average for trend
    window_size = 6  # 1 hour window with 10-minute intervals
    rolling_averages = []
    
    for i in range(len(anomaly_data) - window_size + 1):
        window_values = [
            anomaly_data[j].get('value', 0) 
            for j in range(i, i + window_size)
            if anomaly_data[j].get('value') is not None
        ]
        if window_values:
            rolling_averages.append(sum(window_values) / len(window_values))
    
    if len(rolling_averages) >= 2:
        trend_direction = "increasing" if rolling_averages[-1] > rolling_averages[0] else "decreasing"
        trend_magnitude = abs(rolling_averages[-1] - rolling_averages[0])
        
        print(f"  Overall trend: {trend_direction}")
        print(f"  Trend magnitude: {trend_magnitude:.3f}")
        
        if rolling_averages[-1] > 0.7:
            print(f"  ⚠️  Current risk level: HIGH")
        elif rolling_averages[-1] > 0.4:
            print(f"  ⚠️  Current risk level: MEDIUM")
        else:
            print(f"  ✅ Current risk level: LOW")
```

### Multi-Device Comparison

```python
# Compare metrics across multiple devices
device_ids = ["123", "456", "789"]  # Replace with actual device IDs

multi_device_data = client.metricdata.get(
    metric="bandwidth",
    devices=device_ids,
    starttime=int((datetime.datetime.now() - datetime.timedelta(hours=6)).timestamp() * 1000),
    endtime=int(datetime.datetime.now().timestamp() * 1000),
    interval="30min",
    fulldevicedetails=True
)

print(f"Multi-Device Bandwidth Comparison")
print("=" * 60)

data_points = multi_device_data.get('data', [])

if data_points:
    # Aggregate data by device
    device_stats = {}
    
    for point in data_points:
        timestamp = point.get('timestamp', 0)
        values = point.get('values', [])
        
        for device_value in values:
            device_id = device_value.get('device_id')
            value = device_value.get('value', 0)
            
            if device_id not in device_stats:
                device_stats[device_id] = {
                    'values': [],
                    'total': 0,
                    'count': 0
                }
            
            device_stats[device_id]['values'].append(value)
            device_stats[device_id]['total'] += value
            device_stats[device_id]['count'] += 1
    
    # Calculate statistics and compare
    print(f"Device Bandwidth Statistics:")
    
    for device_id, stats in sorted(device_stats.items()):
        values = stats['values']
        if values:
            avg_bandwidth = stats['total'] / stats['count']
            max_bandwidth = max(values)
            min_bandwidth = min(values)
            
            print(f"\n  Device {device_id}:")
            print(f"    Average: {avg_bandwidth:,.0f} bytes/sec")
            print(f"    Maximum: {max_bandwidth:,.0f} bytes/sec")
            print(f"    Minimum: {min_bandwidth:,.0f} bytes/sec")
            print(f"    Data points: {len(values)}")
    
    # Identify top consumers
    if device_stats:
        top_consumer = max(device_stats.items(), key=lambda x: x[1]['total'])
        print(f"\n  Top bandwidth consumer: Device {top_consumer[0]}")
        print(f"    Total consumption: {top_consumer[1]['total']:,.0f} bytes")
```

### Custom Time Interval Analysis

```python
# Analyze metrics with different time intervals
metric_name = "connection_count"
device_id = 123

# Define different intervals to compare
intervals = ["1min", "15min", "1hour"]
interval_data = {}

for interval in intervals:
    data = client.metricdata.get(
        metric=metric_name,
        did=device_id,
        starttime=int((datetime.datetime.now() - datetime.timedelta(hours=3)).timestamp() * 1000),
        endtime=int(datetime.datetime.now().timestamp() * 1000),
        interval=interval
    )
    
    interval_data[interval] = data.get('data', [])

print(f"Time Interval Analysis: {metric_name}")
print("=" * 60)

# Compare data granularity and patterns
for interval, data in interval_data.items():
    if data:
        values = [point.get('value', 0) for point in data if point.get('value') is not None]
        
        print(f"\n{interval.upper()} Interval:")
        print(f"  Data points: {len(values)}")
        
        if values:
            avg_value = sum(values) / len(values)
            max_value = max(values)
            min_value = min(values)
            
            print(f"  Average: {avg_value:.1f}")
            print(f"  Range: {min_value:.1f} - {max_value:.1f}")
            
            # Calculate variance to understand data volatility
            variance = sum((x - avg_value) ** 2 for x in values) / len(values)
            std_dev = variance ** 0.5
            print(f"  Volatility (std dev): {std_dev:.2f}")
            
            # Show recent trend
            if len(values) >= 3:
                recent_values = values[-3:]
                print(f"  Recent trend: {' → '.join([f'{v:.1f}' for v in recent_values])}")

# Recommend optimal interval based on analysis
print(f"\nInterval Recommendation:")
print(f"  • Use 1min for real-time monitoring and immediate response")
print(f"  • Use 15min for operational monitoring and trend analysis")
print(f"  • Use 1hour for capacity planning and long-term trends")
```

## Error Handling

```python
try:
    # Attempt to get metric data
    metric_data = client.metricdata.get(
        metric="bandwidth",
        did=123,
        starttime=int((datetime.datetime.now() - datetime.timedelta(hours=1)).timestamp() * 1000),
        endtime=int(datetime.datetime.now().timestamp() * 1000),
        interval="5min"
    )
    
    # Process metric data
    data_points = metric_data.get('data', [])
    print(f"Retrieved {len(data_points)} data points")
    
    for point in data_points:
        timestamp = point.get('timestamp', 0)
        value = point.get('value', 0)
        time_str = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%H:%M:%S')
        
        print(f"  {time_str}: {value}")
        
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check metric name and parameter values")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for metricdata endpoint")
        elif e.response.status_code == 404:
            print("Metric not found - verify metric name exists")
        elif e.response.status_code == 422:
            print("Invalid parameters - check time ranges and filter values")
        else:
            print(f"Response: {e.response.text}")
            
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Metric Names and Discovery
- **Use Metrics module**: Query the `/metrics` endpoint to discover available metric names
- **Metric validation**: Ensure metric names exist before querying metric data
- **Case sensitivity**: Metric names are typically case-sensitive
- **Multiple metrics**: Use `metrics` parameter for batch retrieval

### Time Parameters and Ranges
- **Time formats**: Use epoch milliseconds for `starttime`/`endtime` or `from_`/`to`
- **UTC timezone**: All timestamps are interpreted as UTC
- **Range limits**: Large time ranges may result in timeouts or sampling
- **Default behavior**: Without time parameters, returns recent data

### Interval Specifications
Common interval formats:
- **Minutes**: '1min', '5min', '15min', '30min'
- **Hours**: '1hour', '2hour', '6hour', '12hour'
- **Days**: '1day', '7day'
- **Automatic**: Darktrace may adjust intervals based on time range

### Device and Protocol Filtering
- **Device requirements**: Some metrics require specific device IDs (`did`)
- **Multi-device queries**: Use `devices` parameter for comparing multiple devices
- **Protocol filtering**: Filter by IP protocol (`tcp`, `udp`) or application protocol (`http`, `https`)
- **Port filtering**: Filter by specific ports for network-related metrics

### Data Aggregation and Processing
- **Automatic aggregation**: Intervals automatically aggregate raw data points
- **Missing data**: Handle null values and gaps in time series
- **Data volume**: Consider response size for large time ranges
- **Sampling**: High-frequency data may be sampled for large queries

### Breach Correlation
- **Breach timing**: `breachtimes=True` correlates metrics with model breaches
- **Security context**: Useful for understanding metric spikes in security context
- **Performance impact**: Breach correlation increases query complexity

### Response Data Optimization
- **Device details**: Use `fulldevicedetails=False` to reduce payload size
- **Selective metrics**: Query only needed metrics to improve performance
- **Time range optimization**: Use appropriate time ranges for use case
- **Interval selection**: Choose intervals that match analysis requirements

### Common Use Cases
- **Performance monitoring**: Track system and network performance metrics
- **Capacity planning**: Analyze usage trends for resource planning
- **Security analysis**: Monitor security metrics and breach correlation
- **Troubleshooting**: Investigate metric anomalies and patterns
- **Compliance reporting**: Generate metric reports for audit purposes

### Best Practices
- **Cache metric definitions**: Use Metrics module to understand available metrics
- **Handle missing data**: Account for null values and data gaps
- **Optimize time ranges**: Balance data granularity with query performance
- **Use appropriate intervals**: Match interval to analysis timeframe
- **Monitor query performance**: Large queries may impact system performance

### Integration Considerations
- **Metrics dependency**: Requires metrics to be defined and active
- **Device correlation**: Works with Devices module for device-specific analysis
- **Time synchronization**: Ensure consistent time handling across modules
- **Data retention**: Historical data availability depends on Darktrace configuration

### Performance Considerations
- **Query optimization**: Use filters to reduce data volume
- **Batch processing**: Process large datasets in smaller time chunks
- **Caching strategy**: Cache frequently accessed metric data
- **Rate limiting**: Consider API rate limits for high-frequency queries
