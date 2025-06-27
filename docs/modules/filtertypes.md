# FilterTypes Module

The FilterTypes module provides access to internal Darktrace filter definitions used in the Model Editor. This module returns information about available filters, their data types, and supported comparators, which is essential for building custom models and understanding the Darktrace filtering system.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the filtertypes module
filtertypes = client.filtertypes
```

## Methods Overview

The FilterTypes module provides the following method:

- **`get()`** - Retrieve available filter types and their specifications

## Methods

### Get Filter Types

Retrieve information about all internal Darktrace filters used in the Model Editor. This includes filter names, data types, available comparators, and graphing capabilities.

```python
# Get all filter types
all_filters = filtertypes.get()

# Get only comparators information
comparators_only = filtertypes.get(responsedata="comparators")

# Get filter types with custom parameters
custom_filters = filtertypes.get(responsedata="filtertype,valuetype")
```

#### Parameters

- `responsedata` (str, optional): Restrict returned JSON to specific fields or objects (comma-separated)

#### Response Structure

```python
[
  {
    "filtertype": "device.ip",
    "valuetype": "string",
    "comparators": ["=", "!=", "contains", "!contains", "regex", "!regex"],
    "graphable": true,
    "description": "Device IP address filter",
    "category": "device"
  },
  {
    "filtertype": "connection.port",
    "valuetype": "numeric",
    "comparators": ["=", "!=", "<", ">", "<=", ">=", "in", "!in"],
    "graphable": true,
    "description": "Connection port number filter",
    "category": "network"
  },
  {
    "filtertype": "device.activity",
    "valuetype": "boolean",
    "comparators": ["=", "!="],
    "graphable": false,
    "description": "Device activity status filter",
    "category": "device"
  },
  {
    "filtertype": "time.hour",
    "valuetype": "time",
    "comparators": ["=", "!=", "<", ">", "<=", ">=", "between"],
    "graphable": true,
    "description": "Time-based hour filter",
    "category": "temporal"
  },
  {
    "filtertype": "data.size",
    "valuetype": "bytes",
    "comparators": ["=", "!=", "<", ">", "<=", ">="],
    "graphable": true,
    "description": "Data size filter in bytes",
    "category": "data"
  }
  // ... more filter types
]

# With responsedata="comparators"
[
  {
    "comparators": ["=", "!=", "contains", "!contains", "regex", "!regex"]
  },
  {
    "comparators": ["=", "!=", "<", ">", "<=", ">=", "in", "!in"]
  },
  {
    "comparators": ["=", "!="]
  }
  // ... more comparator lists
]

# With responsedata="filtertype,valuetype"
[
  {
    "filtertype": "device.ip",
    "valuetype": "string"
  },
  {
    "filtertype": "connection.port", 
    "valuetype": "numeric"
  }
  // ... more filter types with only specified fields
]
```

## Examples

### Filter Types Discovery and Analysis

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get all available filter types
all_filters = client.filtertypes.get()

print("Darktrace Filter Types Analysis")
print("=" * 50)
print(f"Total filter types: {len(all_filters)}")

# Categorize filters by value type
value_type_stats = {}
graphable_count = 0
category_stats = {}

for filter_info in all_filters:
    # Value type analysis
    value_type = filter_info.get('valuetype', 'unknown')
    value_type_stats[value_type] = value_type_stats.get(value_type, 0) + 1
    
    # Graphable analysis
    if filter_info.get('graphable', False):
        graphable_count += 1
    
    # Category analysis (if available)
    category = filter_info.get('category', 'unknown')
    category_stats[category] = category_stats.get(category, 0) + 1
    
    # Display filter information
    filter_name = filter_info.get('filtertype', 'Unknown')
    comparators = filter_info.get('comparators', [])
    description = filter_info.get('description', 'No description')
    
    print(f"\nFilter: {filter_name}")
    print(f"  Type: {value_type}")
    print(f"  Graphable: {filter_info.get('graphable', False)}")
    print(f"  Comparators: {', '.join(comparators)}")
    if description != 'No description':
        print(f"  Description: {description}")

print(f"\nFilter Statistics:")
print(f"Value type distribution:")
for value_type, count in sorted(value_type_stats.items(), key=lambda x: x[1], reverse=True):
    print(f"  {value_type}: {count} filters")

print(f"\nGraphable filters: {graphable_count}/{len(all_filters)} ({graphable_count/len(all_filters)*100:.1f}%)")

if category_stats:
    print(f"\nCategory distribution:")
    for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} filters")
```

### Comparator Analysis

```python
# Analyze available comparators across filter types
def analyze_comparators():
    all_filters = client.filtertypes.get()
    
    print("Filter Comparator Analysis")
    print("=" * 50)
    
    # Collect all unique comparators
    all_comparators = set()
    comparator_usage = {}
    value_type_comparators = {}
    
    for filter_info in all_filters:
        comparators = filter_info.get('comparators', [])
        value_type = filter_info.get('valuetype', 'unknown')
        
        # Track all comparators
        all_comparators.update(comparators)
        
        # Track comparator usage
        for comp in comparators:
            comparator_usage[comp] = comparator_usage.get(comp, 0) + 1
        
        # Track comparators by value type
        if value_type not in value_type_comparators:
            value_type_comparators[value_type] = set()
        value_type_comparators[value_type].update(comparators)
    
    print(f"Total unique comparators: {len(all_comparators)}")
    print(f"Available comparators: {', '.join(sorted(all_comparators))}")
    
    print(f"\nComparator usage frequency:")
    for comp, count in sorted(comparator_usage.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(all_filters)) * 100
        print(f"  {comp}: {count} filters ({percentage:.1f}%)")
    
    print(f"\nComparators by value type:")
    for value_type, comparators in sorted(value_type_comparators.items()):
        print(f"  {value_type}: {', '.join(sorted(comparators))}")
    
    return {
        'all_comparators': all_comparators,
        'comparator_usage': comparator_usage,
        'value_type_comparators': value_type_comparators
    }

# Run comparator analysis
comparator_analysis = analyze_comparators()
```

### Model Editor Filter Reference

```python
# Create a reference for Model Editor filter usage
def create_filter_reference():
    all_filters = client.filtertypes.get()
    
    print("Model Editor Filter Reference")
    print("=" * 60)
    
    # Group filters by category or prefix
    filter_groups = {}
    
    for filter_info in all_filters:
        filter_name = filter_info.get('filtertype', 'unknown')
        
        # Group by prefix (e.g., device.*, connection.*, etc.)
        if '.' in filter_name:
            prefix = filter_name.split('.')[0]
        else:
            prefix = 'general'
        
        if prefix not in filter_groups:
            filter_groups[prefix] = []
        
        filter_groups[prefix].append(filter_info)
    
    # Display grouped filters
    for group_name, filters in sorted(filter_groups.items()):
        print(f"\n{group_name.upper()} FILTERS ({len(filters)} filters):")
        
        for filter_info in sorted(filters, key=lambda x: x.get('filtertype', '')):
            filter_name = filter_info.get('filtertype', 'Unknown')
            value_type = filter_info.get('valuetype', 'unknown')
            comparators = filter_info.get('comparators', [])
            graphable = filter_info.get('graphable', False)
            
            print(f"  {filter_name}")
            print(f"    Type: {value_type}")
            print(f"    Comparators: {', '.join(comparators)}")
            print(f"    Graphable: {'Yes' if graphable else 'No'}")
            
            # Show example usage
            example_comparator = comparators[0] if comparators else '='
            if value_type == 'string':
                example_value = '"example.com"'
            elif value_type == 'numeric':
                example_value = '80'
            elif value_type == 'boolean':
                example_value = 'true'
            elif value_type == 'time':
                example_value = '09:00'
            else:
                example_value = 'value'
            
            print(f"    Example: {filter_name} {example_comparator} {example_value}")
    
    return filter_groups

# Create filter reference
filter_reference = create_filter_reference()
```

### Filter Validation Helper

```python
# Create helper functions for filter validation
def validate_filter_usage(filter_name, comparator, value):
    """Validate if a filter, comparator, and value combination is valid"""
    
    all_filters = client.filtertypes.get()
    
    # Find the filter
    filter_info = None
    for f in all_filters:
        if f.get('filtertype') == filter_name:
            filter_info = f
            break
    
    if not filter_info:
        return {
            'valid': False,
            'error': f"Filter '{filter_name}' not found",
            'available_filters': [f.get('filtertype') for f in all_filters if f.get('filtertype')]
        }
    
    # Check comparator
    available_comparators = filter_info.get('comparators', [])
    if comparator not in available_comparators:
        return {
            'valid': False,
            'error': f"Comparator '{comparator}' not available for filter '{filter_name}'",
            'available_comparators': available_comparators
        }
    
    # Check value type
    value_type = filter_info.get('valuetype', 'unknown')
    value_valid = True
    value_error = None
    
    if value_type == 'numeric':
        try:
            float(value)
        except ValueError:
            value_valid = False
            value_error = f"Value '{value}' is not numeric"
    elif value_type == 'boolean':
        if str(value).lower() not in ['true', 'false', '1', '0']:
            value_valid = False
            value_error = f"Value '{value}' is not boolean (true/false)"
    elif value_type == 'time':
        # Basic time format validation
        if not isinstance(value, str) or ':' not in value:
            value_valid = False
            value_error = f"Value '{value}' is not a valid time format"
    
    if not value_valid:
        return {
            'valid': False,
            'error': value_error,
            'expected_type': value_type
        }
    
    return {
        'valid': True,
        'filter_info': filter_info,
        'message': f"Filter '{filter_name} {comparator} {value}' is valid"
    }

# Example validations
test_cases = [
    ('device.ip', '=', '192.168.1.1'),
    ('connection.port', '>', '80'),
    ('device.activity', '=', 'true'),
    ('invalid.filter', '=', 'value'),
    ('device.ip', 'invalid_op', '192.168.1.1'),
    ('connection.port', '>', 'not_a_number')
]

print("Filter Validation Examples")
print("=" * 50)

for filter_name, comparator, value in test_cases:
    result = validate_filter_usage(filter_name, comparator, value)
    
    print(f"\nTest: {filter_name} {comparator} {value}")
    if result['valid']:
        print(f"  ✅ {result['message']}")
    else:
        print(f"  ❌ {result['error']}")
        if 'available_filters' in result:
            print(f"     Available filters: {', '.join(result['available_filters'][:5])}...")
        elif 'available_comparators' in result:
            print(f"     Available comparators: {', '.join(result['available_comparators'])}")
        elif 'expected_type' in result:
            print(f"     Expected type: {result['expected_type']}")
```

### Graphable Filters Analysis

```python
# Analyze filters that can be used for graphing
def analyze_graphable_filters():
    all_filters = client.filtertypes.get()
    
    graphable_filters = [f for f in all_filters if f.get('graphable', False)]
    non_graphable_filters = [f for f in all_filters if not f.get('graphable', False)]
    
    print("Graphable Filters Analysis")
    print("=" * 50)
    print(f"Graphable filters: {len(graphable_filters)}")
    print(f"Non-graphable filters: {len(non_graphable_filters)}")
    
    # Analyze graphable filters by value type
    graphable_by_type = {}
    for filter_info in graphable_filters:
        value_type = filter_info.get('valuetype', 'unknown')
        if value_type not in graphable_by_type:
            graphable_by_type[value_type] = []
        graphable_by_type[value_type].append(filter_info)
    
    print(f"\nGraphable filters by value type:")
    for value_type, filters in sorted(graphable_by_type.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {value_type}: {len(filters)} filters")
        
        # Show example filters
        for filter_info in filters[:3]:  # Show first 3
            filter_name = filter_info.get('filtertype', 'Unknown')
            print(f"    - {filter_name}")
        
        if len(filters) > 3:
            print(f"    ... and {len(filters) - 3} more")
    
    # Recommend best filters for graphing
    print(f"\nRecommended filters for graphing:")
    recommended_categories = ['device', 'connection', 'data', 'time']
    
    for category in recommended_categories:
        category_filters = [
            f for f in graphable_filters 
            if f.get('filtertype', '').startswith(category + '.')
        ]
        
        if category_filters:
            print(f"  {category.upper()} category:")
            for filter_info in category_filters[:5]:  # Show top 5
                filter_name = filter_info.get('filtertype', 'Unknown')
                value_type = filter_info.get('valuetype', 'unknown')
                print(f"    - {filter_name} ({value_type})")
    
    return {
        'graphable': graphable_filters,
        'non_graphable': non_graphable_filters,
        'by_type': graphable_by_type
    }

# Run graphable analysis
graphable_analysis = analyze_graphable_filters()
```

### Export Filter Documentation

```python
# Export comprehensive filter documentation
def export_filter_documentation():
    all_filters = client.filtertypes.get()
    
    documentation = {
        'summary': {
            'total_filters': len(all_filters),
            'value_types': {},
            'graphable_count': 0,
            'categories': {}
        },
        'filters_by_category': {},
        'comparator_reference': {},
        'detailed_filters': []
    }
    
    # Process each filter
    for filter_info in all_filters:
        # Summary statistics
        value_type = filter_info.get('valuetype', 'unknown')
        documentation['summary']['value_types'][value_type] = documentation['summary']['value_types'].get(value_type, 0) + 1
        
        if filter_info.get('graphable', False):
            documentation['summary']['graphable_count'] += 1
        
        # Category grouping
        filter_name = filter_info.get('filtertype', 'unknown')
        category = filter_name.split('.')[0] if '.' in filter_name else 'general'
        documentation['summary']['categories'][category] = documentation['summary']['categories'].get(category, 0) + 1
        
        if category not in documentation['filters_by_category']:
            documentation['filters_by_category'][category] = []
        
        documentation['filters_by_category'][category].append({
            'filtertype': filter_info.get('filtertype'),
            'valuetype': filter_info.get('valuetype'),
            'comparators': filter_info.get('comparators', []),
            'graphable': filter_info.get('graphable', False)
        })
        
        # Comparator reference
        comparators = filter_info.get('comparators', [])
        for comp in comparators:
            if comp not in documentation['comparator_reference']:
                documentation['comparator_reference'][comp] = []
            documentation['comparator_reference'][comp].append(filter_name)
        
        # Detailed filter information
        documentation['detailed_filters'].append(filter_info)
    
    return documentation

# Generate and display documentation
doc = export_filter_documentation()

print("Filter Documentation Export")
print("=" * 50)
print(f"Total filters: {doc['summary']['total_filters']}")
print(f"Graphable filters: {doc['summary']['graphable_count']}")

print(f"\nValue types:")
for value_type, count in sorted(doc['summary']['value_types'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {value_type}: {count}")

print(f"\nCategories:")
for category, count in sorted(doc['summary']['categories'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {category}: {count}")

print(f"\nComparator usage:")
for comparator, filters in sorted(doc['comparator_reference'].items(), key=lambda x: len(x[1]), reverse=True)[:10]:
    print(f"  {comparator}: {len(filters)} filters")

# Export to file (example)
import json
with open('darktrace_filters_reference.json', 'w') as f:
    json.dump(doc, f, indent=2)
    
print(f"\nFilter reference exported to: darktrace_filters_reference.json")
```

## Error Handling

```python
try:
    # Attempt to get filter types
    filter_types = client.filtertypes.get()
    
    print(f"Retrieved {len(filter_types)} filter types")
    
    # Process filter types
    for filter_info in filter_types[:5]:  # Process first 5
        filter_name = filter_info.get('filtertype', 'Unknown')
        value_type = filter_info.get('valuetype', 'unknown')
        comparators = filter_info.get('comparators', [])
        
        print(f"Filter: {filter_name}")
        print(f"  Type: {value_type}")
        print(f"  Comparators: {', '.join(comparators)}")
        
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 403:
            print("Access denied - check API permissions for filtertypes endpoint")
        elif e.response.status_code == 404:
            print("Filter types endpoint not found - check Darktrace version compatibility")
        else:
            print(f"Response: {e.response.text}")
            
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Filter Types and Categories
- **Device filters**: Filters related to device properties (IP, hostname, type, etc.)
- **Connection filters**: Network connection-related filters (port, protocol, etc.)
- **Data filters**: Data transfer and content-related filters (size, type, etc.)
- **Time filters**: Temporal filters for time-based conditions
- **General filters**: Miscellaneous filters not fitting other categories

### Value Types
- **string**: Text-based values, support string comparators
- **numeric**: Numerical values, support mathematical comparators
- **boolean**: True/false values, limited to equality comparators
- **time**: Time-based values with time-specific comparators
- **bytes**: Data size values with size-specific comparators

### Comparator Types
- **Equality**: `=`, `!=` for exact matches
- **Numerical**: `<`, `>`, `<=`, `>=` for numeric comparisons
- **String**: `contains`, `!contains` for substring matching
- **Pattern**: `regex`, `!regex` for pattern matching
- **Set**: `in`, `!in` for membership testing
- **Range**: `between` for range-based filtering

### Graphable Capability
- **Graph visualization**: Graphable filters can be used in visual representations
- **Analytics support**: Enables creation of charts and graphs in Model Editor
- **Performance consideration**: Graphable filters may have optimized indexing
- **UI integration**: These filters appear in graphing interfaces

### Model Editor Integration
- **Filter validation**: Use filter types to validate model conditions
- **Comparator selection**: Choose appropriate comparators for each value type
- **Performance optimization**: Understand which filters support efficient querying
- **User interface**: Filter types drive Model Editor UI components

### Response Data Filtering
Use `responsedata` parameter to optimize queries:
- `"filtertype"`: Get only filter names
- `"comparators"`: Get only available comparators
- `"valuetype,graphable"`: Get specific attributes only
- Custom combinations for specific use cases

### Best Practices
- **Cache filter definitions**: Filter types change infrequently
- **Validate inputs**: Use filter type information to validate user inputs
- **Optimize queries**: Choose efficient filters for performance-critical models
- **Documentation**: Maintain local documentation of commonly used filters
- **Testing**: Validate filter combinations before deploying models

### Common Use Cases
- **Model development**: Understanding available filters for custom models
- **UI development**: Building interfaces for filter selection
- **Validation**: Ensuring filter expressions are syntactically correct
- **Documentation**: Creating user guides for filter usage
- **Integration**: Connecting external tools with Darktrace filtering system

### Performance Considerations
- **Filter complexity**: Some filters may be more computationally expensive
- **Graphable optimization**: Graphable filters may have better performance for visualization
- **Caching strategy**: Cache filter type information to reduce API calls
- **Validation overhead**: Consider performance impact of extensive validation

### Integration Patterns
- **Model Editor**: Primary use case for creating and editing detection models
- **Advanced Search**: Filter types inform advanced search capabilities  
- **Custom Applications**: External applications can use filter definitions
- **Validation Libraries**: Build reusable validation components
- **Documentation Generation**: Automatically generate filter reference materials
