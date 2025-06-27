# Metrics Module

The Metrics module provides access to available metrics and their metadata from Darktrace. This module allows you to discover what metrics are available for analysis, including their names, descriptions, data types, and configuration parameters.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the metrics module
metrics = client.metrics
```

## Methods Overview

The Metrics module provides the following method:

- **`get()`** - Retrieve available metrics information and metadata

## Methods

### Get Metrics

Retrieve information about available metrics from Darktrace. This includes metric definitions, data types, units, and configuration parameters that can be used with other modules like MetricData or Network.

```python
# Get all available metrics
all_metrics = metrics.get()

# Get specific metric by ID
specific_metric = metrics.get(metric_id=4)

# Get metrics with limited response data
metric_names = metrics.get(responsedata="mlid,name")

# Get metric descriptions only
metric_info = metrics.get(responsedata="name,description,unit")
```

#### Parameters

- `metric_id` (int, optional): The metric logic ID (mlid) for a specific metric. If provided, returns information for that metric only
- `responsedata` (str, optional): Restrict returned JSON to specific fields or objects (comma-separated)

#### Response Structure

```python
# All metrics response
[
  {
    "mlid": 1,
    "name": "bandwidth",
    "description": "Network bandwidth utilization in bytes per second",
    "unit": "bytes/sec",
    "datatype": "numeric",
    "category": "network",
    "aggregatable": true,
    "available_aggregations": ["sum", "avg", "max", "min"],
    "time_granularity": ["hour", "day", "week"],
    "requires_device": false,
    "requires_subnet": false,
    "parameters": {
      "direction": ["in", "out", "total"],
      "protocol": ["tcp", "udp", "all"]
    }
  },
  {
    "mlid": 2,
    "name": "connection_count",
    "description": "Number of network connections",
    "unit": "count",
    "datatype": "integer",
    "category": "network",
    "aggregatable": true,
    "available_aggregations": ["sum", "avg", "max"],
    "time_granularity": ["minute", "hour", "day"],
    "requires_device": true,
    "requires_subnet": false,
    "parameters": {
      "state": ["established", "syn_sent", "all"],
      "direction": ["inbound", "outbound", "all"]
    }
  },
  // ... more metrics
]

# Single metric response (when metric_id specified)
{
  "mlid": 4,
  "name": "device_activity",
  "description": "Device activity score based on network behavior",
  "unit": "score",
  "datatype": "float",
  "category": "device",
  "aggregatable": true,
  "available_aggregations": ["avg", "max", "min"],
  "time_granularity": ["hour", "day"],
  "requires_device": true,
  "requires_subnet": false,
  "parameters": {
    "include_internal": [true, false],
    "include_external": [true, false]
  }
}

# With responsedata filtering
[
  {
    "mlid": 1,
    "name": "bandwidth"
  },
  {
    "mlid": 2,
    "name": "connection_count"
  },
  // ... more metrics with only specified fields
]
```

## Examples

### Metrics Discovery and Catalog

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get all available metrics
all_metrics = client.metrics.get()

print(f"Available Metrics: {len(all_metrics)}")
print("=" * 50)

# Categorize metrics
metric_categories = {}
data_types = {}
aggregatable_count = 0

for metric in all_metrics:
    # Category analysis
    category = metric.get('category', 'unknown')
    if category not in metric_categories:
        metric_categories[category] = []
    metric_categories[category].append(metric)
    
    # Data type analysis
    datatype = metric.get('datatype', 'unknown')
    data_types[datatype] = data_types.get(datatype, 0) + 1
    
    # Aggregation capability
    if metric.get('aggregatable', False):
        aggregatable_count += 1
    
    # Display metric information
    mlid = metric.get('mlid')
    name = metric.get('name', 'Unknown')
    description = metric.get('description', 'No description')
    unit = metric.get('unit', 'N/A')
    
    print(f"\nMetric ID {mlid}: {name}")
    print(f"  Description: {description}")
    print(f"  Unit: {unit}")
    print(f"  Category: {category}")
    print(f"  Data Type: {datatype}")
    print(f"  Aggregatable: {metric.get('aggregatable', False)}")

print(f"\nMetric Statistics:")
print(f"Total metrics: {len(all_metrics)}")
print(f"Aggregatable metrics: {aggregatable_count}")

print(f"\nMetrics by category:")
for category, metrics_list in sorted(metric_categories.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"  {category}: {len(metrics_list)} metrics")

print(f"\nData type distribution:")
for dtype, count in sorted(data_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {dtype}: {count} metrics")
```

### Network Metrics Analysis

```python
# Focus on network-related metrics
network_metrics = []
all_metrics = client.metrics.get()

for metric in all_metrics:
    if metric.get('category') == 'network':
        network_metrics.append(metric)

print(f"Network Metrics Analysis: {len(network_metrics)} metrics")
print("=" * 60)

# Analyze network metric capabilities
bandwidth_metrics = []
connection_metrics = []
protocol_metrics = []

for metric in network_metrics:
    name = metric.get('name', '').lower()
    description = metric.get('description', '').lower()
    
    if 'bandwidth' in name or 'bytes' in name or 'throughput' in description:
        bandwidth_metrics.append(metric)
    elif 'connection' in name or 'session' in name:
        connection_metrics.append(metric)
    elif 'protocol' in name or 'tcp' in name or 'udp' in name:
        protocol_metrics.append(metric)

print(f"Bandwidth-related metrics: {len(bandwidth_metrics)}")
for metric in bandwidth_metrics:
    print(f"  - {metric.get('name')} (ID: {metric.get('mlid')}): {metric.get('unit', 'N/A')}")

print(f"\nConnection-related metrics: {len(connection_metrics)}")
for metric in connection_metrics:
    print(f"  - {metric.get('name')} (ID: {metric.get('mlid')}): {metric.get('unit', 'N/A')}")

print(f"\nProtocol-related metrics: {len(protocol_metrics)}")
for metric in protocol_metrics:
    print(f"  - {metric.get('name')} (ID: {metric.get('mlid')}): {metric.get('unit', 'N/A')}")

# Analyze time granularity options
time_granularities = {}
for metric in network_metrics:
    granularities = metric.get('time_granularity', [])
    for granularity in granularities:
        time_granularities[granularity] = time_granularities.get(granularity, 0) + 1

print(f"\nTime granularity support:")
for granularity, count in sorted(time_granularities.items(), key=lambda x: x[1], reverse=True):
    print(f"  {granularity}: {count} metrics")
```

### Device-Specific Metrics Discovery

```python
# Find metrics that require device specification
device_metrics = []
all_metrics = client.metrics.get()

for metric in all_metrics:
    if metric.get('requires_device', False):
        device_metrics.append(metric)

print(f"Device-Specific Metrics: {len(device_metrics)}")
print("=" * 50)

# Categorize device metrics
device_categories = {}
for metric in device_metrics:
    category = metric.get('category', 'unknown')
    if category not in device_categories:
        device_categories[category] = []
    device_categories[category].append(metric)

for category, metrics_list in sorted(device_categories.items()):
    print(f"\n{category.upper()} Device Metrics:")
    for metric in metrics_list:
        name = metric.get('name')
        mlid = metric.get('mlid')
        description = metric.get('description', 'No description')
        unit = metric.get('unit', 'N/A')
        
        print(f"  {name} (ID: {mlid})")
        print(f"    Description: {description}")
        print(f"    Unit: {unit}")
        
        # Show available parameters
        parameters = metric.get('parameters', {})
        if parameters:
            print(f"    Parameters:")
            for param, values in parameters.items():
                if isinstance(values, list):
                    print(f"      {param}: {', '.join(map(str, values))}")
                else:
                    print(f"      {param}: {values}")
```

### Metric Aggregation Capabilities

```python
# Analyze aggregation capabilities across metrics
aggregation_analysis = {}
all_metrics = client.metrics.get()

for metric in all_metrics:
    if metric.get('aggregatable', False):
        aggregations = metric.get('available_aggregations', [])
        category = metric.get('category', 'unknown')
        
        if category not in aggregation_analysis:
            aggregation_analysis[category] = {
                'metrics': [],
                'aggregation_types': set()
            }
        
        aggregation_analysis[category]['metrics'].append(metric)
        aggregation_analysis[category]['aggregation_types'].update(aggregations)

print("Metric Aggregation Capabilities")
print("=" * 50)

for category, analysis in sorted(aggregation_analysis.items()):
    metrics_count = len(analysis['metrics'])
    aggregation_types = sorted(analysis['aggregation_types'])
    
    print(f"\n{category.upper()} ({metrics_count} aggregatable metrics):")
    print(f"  Available aggregations: {', '.join(aggregation_types)}")
    
    # Show examples of aggregatable metrics in this category
    for metric in analysis['metrics'][:3]:  # Show first 3
        name = metric.get('name')
        unit = metric.get('unit', 'N/A')
        metric_aggregations = metric.get('available_aggregations', [])
        print(f"    - {name} ({unit}): {', '.join(metric_aggregations)}")
    
    if len(analysis['metrics']) > 3:
        print(f"    ... and {len(analysis['metrics']) - 3} more")

# Global aggregation type popularity
all_aggregation_types = {}
for metric in all_metrics:
    if metric.get('aggregatable', False):
        for agg_type in metric.get('available_aggregations', []):
            all_aggregation_types[agg_type] = all_aggregation_types.get(agg_type, 0) + 1

print(f"\nMost Common Aggregation Types:")
for agg_type, count in sorted(all_aggregation_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {agg_type}: {count} metrics")
```

### Detailed Metric Inspection

```python
# Deep dive into a specific metric
metric_id = 4  # Replace with actual metric ID of interest

specific_metric = client.metrics.get(metric_id=metric_id)

if specific_metric:
    print(f"Detailed Metric Analysis: {specific_metric.get('name', 'Unknown')}")
    print("=" * 70)
    
    print(f"Metric ID (MLID): {specific_metric.get('mlid')}")
    print(f"Name: {specific_metric.get('name')}")
    print(f"Description: {specific_metric.get('description', 'No description')}")
    print(f"Category: {specific_metric.get('category', 'Unknown')}")
    print(f"Data Type: {specific_metric.get('datatype', 'Unknown')}")
    print(f"Unit: {specific_metric.get('unit', 'N/A')}")
    print(f"Aggregatable: {specific_metric.get('aggregatable', False)}")
    
    # Requirements
    print(f"\nRequirements:")
    print(f"  Requires Device: {specific_metric.get('requires_device', False)}")
    print(f"  Requires Subnet: {specific_metric.get('requires_subnet', False)}")
    
    # Time granularity
    time_granularities = specific_metric.get('time_granularity', [])
    if time_granularities:
        print(f"\nSupported Time Granularities: {', '.join(time_granularities)}")
    
    # Aggregation options
    aggregations = specific_metric.get('available_aggregations', [])
    if aggregations:
        print(f"Available Aggregations: {', '.join(aggregations)}")
    
    # Parameters
    parameters = specific_metric.get('parameters', {})
    if parameters:
        print(f"\nConfigurable Parameters:")
        for param, values in parameters.items():
            if isinstance(values, list):
                print(f"  {param}: {', '.join(map(str, values))}")
            else:
                print(f"  {param}: {values}")
    
    # Usage examples
    print(f"\nUsage Examples:")
    metric_name = specific_metric.get('name')
    
    if specific_metric.get('requires_device'):
        print(f"  # Get {metric_name} for specific device")
        print(f"  data = client.metricdata.get(metric='{metric_name}', did=123)")
    else:
        print(f"  # Get {metric_name} for all devices")
        print(f"  data = client.metricdata.get(metric='{metric_name}')")
    
    if aggregations:
        print(f"  # Get aggregated {metric_name}")
        example_agg = aggregations[0]
        print(f"  data = client.metricdata.get(metric='{metric_name}', aggregation='{example_agg}')")
        
else:
    print(f"Metric with ID {metric_id} not found")
```

### Metrics Compatibility Matrix

```python
# Create a compatibility matrix for metrics usage
def create_metrics_compatibility_matrix():
    all_metrics = client.metrics.get()
    
    compatibility_matrix = {
        'network_compatible': [],
        'device_required': [],
        'subnet_compatible': [],
        'time_series': [],
        'aggregatable': [],
        'real_time': []
    }
    
    for metric in all_metrics:
        name = metric.get('name')
        mlid = metric.get('mlid')
        category = metric.get('category', 'unknown')
        
        # Network module compatibility
        if category in ['network', 'traffic', 'connection']:
            compatibility_matrix['network_compatible'].append({
                'name': name,
                'mlid': mlid,
                'category': category
            })
        
        # Device requirement
        if metric.get('requires_device', False):
            compatibility_matrix['device_required'].append({
                'name': name,
                'mlid': mlid,
                'unit': metric.get('unit', 'N/A')
            })
        
        # Subnet compatibility
        if metric.get('requires_subnet', False) or not metric.get('requires_device', True):
            compatibility_matrix['subnet_compatible'].append({
                'name': name,
                'mlid': mlid
            })
        
        # Time series capability
        time_granularities = metric.get('time_granularity', [])
        if time_granularities:
            compatibility_matrix['time_series'].append({
                'name': name,
                'mlid': mlid,
                'granularities': time_granularities
            })
        
        # Aggregation capability
        if metric.get('aggregatable', False):
            compatibility_matrix['aggregatable'].append({
                'name': name,
                'mlid': mlid,
                'aggregations': metric.get('available_aggregations', [])
            })
    
    return compatibility_matrix

# Generate compatibility matrix
matrix = create_metrics_compatibility_matrix()

print("Metrics Compatibility Matrix")
print("=" * 50)

print(f"Network Module Compatible: {len(matrix['network_compatible'])} metrics")
for metric in matrix['network_compatible'][:5]:
    print(f"  - {metric['name']} (ID: {metric['mlid']}, Category: {metric['category']})")

print(f"\nDevice-Required Metrics: {len(matrix['device_required'])} metrics")
for metric in matrix['device_required'][:5]:
    print(f"  - {metric['name']} (ID: {metric['mlid']}, Unit: {metric['unit']})")

print(f"\nTime Series Capable: {len(matrix['time_series'])} metrics")
for metric in matrix['time_series'][:5]:
    granularities = ', '.join(metric['granularities'])
    print(f"  - {metric['name']} (ID: {metric['mlid']}, Granularities: {granularities})")

print(f"\nAggregatable Metrics: {len(matrix['aggregatable'])} metrics")
for metric in matrix['aggregatable'][:5]:
    aggregations = ', '.join(metric['aggregations'])
    print(f"  - {metric['name']} (ID: {metric['mlid']}, Types: {aggregations})")
```

### Export Metrics Documentation

```python
# Export comprehensive metrics documentation
def export_metrics_documentation():
    all_metrics = client.metrics.get()
    
    documentation = {
        'summary': {
            'total_metrics': len(all_metrics),
            'categories': {},
            'data_types': {},
            'aggregatable_count': 0,
            'device_required_count': 0
        },
        'metrics_by_category': {},
        'detailed_metrics': []
    }
    
    for metric in all_metrics:
        # Summary statistics
        category = metric.get('category', 'unknown')
        datatype = metric.get('datatype', 'unknown')
        
        documentation['summary']['categories'][category] = documentation['summary']['categories'].get(category, 0) + 1
        documentation['summary']['data_types'][datatype] = documentation['summary']['data_types'].get(datatype, 0) + 1
        
        if metric.get('aggregatable', False):
            documentation['summary']['aggregatable_count'] += 1
        if metric.get('requires_device', False):
            documentation['summary']['device_required_count'] += 1
        
        # Group by category
        if category not in documentation['metrics_by_category']:
            documentation['metrics_by_category'][category] = []
        
        documentation['metrics_by_category'][category].append({
            'mlid': metric.get('mlid'),
            'name': metric.get('name'),
            'description': metric.get('description'),
            'unit': metric.get('unit'),
            'requires_device': metric.get('requires_device', False)
        })
        
        # Detailed metric information
        documentation['detailed_metrics'].append(metric)
    
    return documentation

# Generate and display documentation
doc = export_metrics_documentation()

print("Metrics Documentation Export")
print("=" * 50)
print(f"Total metrics: {doc['summary']['total_metrics']}")
print(f"Aggregatable metrics: {doc['summary']['aggregatable_count']}")
print(f"Device-required metrics: {doc['summary']['device_required_count']}")

print(f"\nMetrics by category:")
for category, count in sorted(doc['summary']['categories'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {category}: {count}")

print(f"\nData types:")
for dtype, count in sorted(doc['summary']['data_types'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {dtype}: {count}")

# Export to file (example)
import json
with open('darktrace_metrics_catalog.json', 'w') as f:
    json.dump(doc, f, indent=2)
    
print(f"\nMetrics catalog exported to: darktrace_metrics_catalog.json")
```

## Error Handling

```python
try:
    # Attempt to get all metrics
    all_metrics = client.metrics.get()
    
    print(f"Retrieved {len(all_metrics)} metrics")
    
    # Process each metric
    for metric in all_metrics:
        mlid = metric.get('mlid')
        name = metric.get('name', 'Unknown')
        
        print(f"Processing metric {mlid}: {name}")
        
        # Get detailed information for specific metric
        try:
            detailed_metric = client.metrics.get(metric_id=mlid)
            
            if detailed_metric:
                description = detailed_metric.get('description', 'No description')
                print(f"  Description: {description}")
            else:
                print(f"  No detailed information available")
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"  Metric {mlid} not found in detailed lookup")
            else:
                print(f"  Error retrieving metric details: {e}")
                
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 403:
            print("Access denied - check API permissions for metrics endpoint")
        elif e.response.status_code == 404:
            print("Metrics endpoint not found - check Darktrace version compatibility")
        else:
            print(f"Response: {e.response.text}")
            
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Metric Logic IDs (MLIDs)
- **Unique identifiers**: Each metric has a unique MLID across Darktrace instances
- **Consistency**: MLIDs remain consistent across different API calls and modules
- **Reference usage**: Use MLIDs when referencing metrics in other modules like MetricData

### Metric Categories
Common metric categories include:
- **network**: Network traffic, bandwidth, and connectivity metrics
- **device**: Device-specific behavior and activity metrics
- **security**: Security-related scoring and threat metrics
- **performance**: System and application performance metrics
- **compliance**: Regulatory and policy compliance metrics

### Data Types and Units
- **Numeric types**: integer, float, double for quantitative measurements
- **Text types**: string for categorical or descriptive data
- **Boolean types**: boolean for true/false states
- **Units**: bytes/sec, count, percentage, score, etc.

### Aggregation Capabilities
Available aggregation types typically include:
- **sum**: Total values over time period
- **avg**: Average values over time period
- **max**: Maximum value in time period
- **min**: Minimum value in time period
- **count**: Number of data points

### Time Granularity
Supported time granularities:
- **minute**: Per-minute data points
- **hour**: Hourly aggregated data
- **day**: Daily aggregated data  
- **week**: Weekly aggregated data
- **month**: Monthly aggregated data

### Requirements and Dependencies
- **Device requirement**: Some metrics require a specific device (did parameter)
- **Subnet requirement**: Some metrics require subnet context
- **Time dependency**: Most metrics require time range specification
- **Parameter dependencies**: Some metrics require specific parameters

### Response Data Filtering
Use `responsedata` parameter to optimize queries:
- `"mlid,name"`: Basic metric identification
- `"name,description,unit"`: Metric overview information
- `"category,datatype"`: Classification data
- `"aggregatable,available_aggregations"`: Aggregation capabilities

### Common Use Cases
- **Metric discovery**: Understanding what data is available for analysis
- **Integration planning**: Determining metric compatibility with other modules
- **Dashboard design**: Selecting appropriate metrics for visualization
- **API optimization**: Understanding metric requirements and capabilities
- **Data analysis**: Choosing correct aggregation methods and time granularities

### Best Practices
- **Cache metric definitions**: Metric metadata changes infrequently
- **Use MLIDs for references**: More reliable than name-based references
- **Check requirements**: Verify device/subnet requirements before using metrics
- **Validate aggregations**: Ensure chosen aggregation type is supported
- **Consider time granularity**: Choose appropriate resolution for analysis needs

### Integration with Other Modules
- **MetricData**: Use metric names/MLIDs to retrieve actual metric values
- **Network**: Many network metrics can be filtered by network module parameters
- **Devices**: Device-specific metrics require device IDs from devices module
- **Subnets**: Subnet-scoped metrics work with subnet module data

### Performance Considerations
- **Metric catalog size**: Large numbers of metrics may impact response time
- **Response filtering**: Use responsedata to reduce payload size
- **Caching strategy**: Cache metric definitions to reduce API calls
- **Selective queries**: Query specific metrics when possible rather than all metrics
