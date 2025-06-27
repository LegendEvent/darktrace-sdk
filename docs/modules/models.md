# Models Module

The Models module provides access to Darktrace AI models and their configurations. This module allows you to retrieve information about the AI models that power Darktrace's threat detection capabilities, including model metadata, configurations, and parameters.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the models module
models = client.models
```

## Methods Overview

The Models module provides the following method:

- **`get()`** - Retrieve AI model information and configurations

## Methods

### Get Models

Retrieve information about Darktrace AI models and their configurations. This provides access to the models that power threat detection and analysis.

```python
# Get all models
all_models = models.get()

# Get specific model by UUID
specific_model = models.get(uuid="12345678-1234-1234-1234-123456789012")

# Get models with limited response data
model_names = models.get(responsedata="name,description")

# Get model configurations only
model_configs = models.get(responsedata="configuration")
```

#### Parameters

- `uuid` (str, optional): Universally unique identifier for a specific model. If provided, returns information for that model only
- `responsedata` (str, optional): Restrict returned JSON to specific fields or objects (comma-separated)

#### Response Structure

```python
# All models response
{
  "models": [
    {
      "uuid": "12345678-1234-1234-1234-123456789012",
      "pid": 123,
      "name": "Device / Anomalous Connection / External Destination",
      "description": "Detects unusual external connections from devices",
      "category": "Device",
      "subcategory": "Anomalous Connection",
      "active": true,
      "version": "1.2.3",
      "configuration": {
        "threshold": 0.85,
        "parameters": {...},
        "filters": [...]
      },
      "created": "2023-01-15T10:00:00Z",
      "modified": "2023-06-15T14:30:00Z",
      "author": "Darktrace",
      "tags": ["network", "external", "connection"],
      "severity": "medium"
    },
    // ... more models
  ]
}

# Single model response (when uuid specified)
{
  "uuid": "12345678-1234-1234-1234-123456789012",
  "pid": 123,
  "name": "Device / Anomalous Connection / External Destination",
  "description": "Detects unusual external connections from devices",
  "category": "Device", 
  "subcategory": "Anomalous Connection",
  "active": true,
  "version": "1.2.3",
  "configuration": {...},
  "created": "2023-01-15T10:00:00Z",
  "modified": "2023-06-15T14:30:00Z"
}

# With responsedata filtering
{
  "models": [
    {
      "name": "Device / Anomalous Connection / External Destination",
      "description": "Detects unusual external connections from devices"
    },
    // ... more models with only specified fields
  ]
}
```

## Examples

### Model Discovery and Analysis

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get all models for analysis
all_models = client.models.get()

print(f"Total models: {len(all_models.get('models', []))}")

# Analyze model distribution
category_stats = {}
active_count = 0
inactive_count = 0

for model in all_models.get('models', []):
    # Category analysis
    category = model.get('category', 'Unknown')
    category_stats[category] = category_stats.get(category, 0) + 1
    
    # Active/inactive analysis
    if model.get('active', False):
        active_count += 1
    else:
        inactive_count += 1
    
    # Display model information
    name = model.get('name', 'Unknown')
    description = model.get('description', 'No description')
    severity = model.get('severity', 'Unknown')
    
    print(f"\nModel: {name}")
    print(f"  Description: {description}")
    print(f"  Category: {category}")
    print(f"  Severity: {severity}")
    print(f"  Active: {model.get('active', False)}")

print(f"\nModel Statistics:")
print(f"Active models: {active_count}")
print(f"Inactive models: {inactive_count}")

print(f"\nCategory distribution:")
for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
    print(f"  {category}: {count} models")
```

### Model Configuration Analysis

```python
# Analyze model configurations and parameters
models_data = client.models.get()

print("Model Configuration Analysis:")
print("=" * 50)

# Analyze configuration patterns
threshold_distribution = {}
parameter_types = set()
filter_types = set()

for model in models_data.get('models', []):
    config = model.get('configuration', {})
    
    # Threshold analysis
    threshold = config.get('threshold')
    if threshold:
        threshold_range = f"{threshold:.1f}"
        threshold_distribution[threshold_range] = threshold_distribution.get(threshold_range, 0) + 1
    
    # Parameter analysis
    parameters = config.get('parameters', {})
    parameter_types.update(parameters.keys())
    
    # Filter analysis
    filters = config.get('filters', [])
    for filter_obj in filters:
        if isinstance(filter_obj, dict):
            filter_types.update(filter_obj.keys())

print(f"Threshold distribution:")
for threshold, count in sorted(threshold_distribution.items(), key=lambda x: float(x[0])):
    print(f"  {threshold}: {count} models")

print(f"\nCommon parameters: {', '.join(sorted(parameter_types))}")
print(f"Filter types: {', '.join(sorted(filter_types))}")
```

### Security Model Focus Analysis

```python
# Focus on security-related models
security_keywords = ['anomalous', 'suspicious', 'unusual', 'malicious', 'threat', 'attack']

security_models = []
all_models = client.models.get()

for model in all_models.get('models', []):
    name = model.get('name', '').lower()
    description = model.get('description', '').lower()
    
    # Check if model is security-related
    is_security = any(keyword in name or keyword in description for keyword in security_keywords)
    
    if is_security and model.get('active', False):
        security_models.append(model)

print(f"Active Security Models: {len(security_models)}")
print("=" * 50)

# Categorize security models
security_categories = {}
for model in security_models:
    category = model.get('category', 'Unknown')
    subcategory = model.get('subcategory', 'Unknown')
    full_category = f"{category} / {subcategory}"
    
    if full_category not in security_categories:
        security_categories[full_category] = []
    
    security_categories[full_category].append(model)

# Display security model categories
for category, models in sorted(security_categories.items()):
    print(f"\n{category}: {len(models)} models")
    for model in models[:3]:  # Show first 3 of each category
        print(f"  - {model.get('name', 'Unknown')}")
    if len(models) > 3:
        print(f"  ... and {len(models) - 3} more")
```

### Model Version and Maintenance Analysis

```python
# Analyze model versions and maintenance status
import datetime

models_data = client.models.get()

# Version analysis
version_stats = {}
recent_updates = []
old_models = []

current_time = datetime.datetime.now()

for model in models_data.get('models', []):
    # Version analysis
    version = model.get('version', 'Unknown')
    version_stats[version] = version_stats.get(version, 0) + 1
    
    # Modified date analysis
    modified_str = model.get('modified', '')
    if modified_str:
        try:
            modified_date = datetime.datetime.fromisoformat(modified_str.replace('Z', '+00:00'))
            days_since_update = (current_time - modified_date.replace(tzinfo=None)).days
            
            if days_since_update < 30:  # Updated in last 30 days
                recent_updates.append({
                    'name': model.get('name'),
                    'days_ago': days_since_update,
                    'version': version
                })
            elif days_since_update > 365:  # Not updated in over a year
                old_models.append({
                    'name': model.get('name'),
                    'days_ago': days_since_update,
                    'version': version
                })
        except:
            pass  # Skip invalid date formats

print("Model Maintenance Analysis:")
print("=" * 50)

print(f"Version distribution:")
for version, count in sorted(version_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {version}: {count} models")

print(f"\nRecently updated models ({len(recent_updates)}):")
for model in sorted(recent_updates, key=lambda x: x['days_ago'])[:10]:
    print(f"  {model['name']}: {model['days_ago']} days ago (v{model['version']})")

print(f"\nOldest models ({len(old_models)}):")
for model in sorted(old_models, key=lambda x: x['days_ago'], reverse=True)[:10]:
    print(f"  {model['name']}: {model['days_ago']} days ago (v{model['version']})")
```

### Specific Model Deep Dive

```python
# Deep dive into a specific model
model_uuid = "12345678-1234-1234-1234-123456789012"  # Replace with actual UUID

specific_model = client.models.get(uuid=model_uuid)

if specific_model:
    print(f"Model Deep Dive: {specific_model.get('name', 'Unknown')}")
    print("=" * 60)
    
    print(f"UUID: {specific_model.get('uuid')}")
    print(f"PID: {specific_model.get('pid')}")
    print(f"Description: {specific_model.get('description', 'No description')}")
    print(f"Category: {specific_model.get('category')} / {specific_model.get('subcategory')}")
    print(f"Version: {specific_model.get('version')}")
    print(f"Active: {specific_model.get('active')}")
    print(f"Severity: {specific_model.get('severity')}")
    print(f"Author: {specific_model.get('author')}")
    print(f"Created: {specific_model.get('created')}")
    print(f"Modified: {specific_model.get('modified')}")
    
    # Configuration details
    config = specific_model.get('configuration', {})
    if config:
        print(f"\nConfiguration:")
        print(f"  Threshold: {config.get('threshold', 'Not specified')}")
        
        parameters = config.get('parameters', {})
        if parameters:
            print(f"  Parameters:")
            for param, value in parameters.items():
                print(f"    {param}: {value}")
        
        filters = config.get('filters', [])
        if filters:
            print(f"  Filters: {len(filters)} configured")
    
    # Tags
    tags = specific_model.get('tags', [])
    if tags:
        print(f"\nTags: {', '.join(tags)}")
        
else:
    print(f"Model with UUID {model_uuid} not found")
```

### Model Export and Documentation

```python
# Export model information for documentation
def export_model_documentation():
    models_data = client.models.get()
    
    # Create structured documentation
    documentation = {
        'summary': {
            'total_models': len(models_data.get('models', [])),
            'active_models': 0,
            'categories': {}
        },
        'models_by_category': {},
        'model_details': []
    }
    
    for model in models_data.get('models', []):
        # Summary statistics
        if model.get('active', False):
            documentation['summary']['active_models'] += 1
        
        category = model.get('category', 'Unknown')
        documentation['summary']['categories'][category] = documentation['summary']['categories'].get(category, 0) + 1
        
        # Group by category
        if category not in documentation['models_by_category']:
            documentation['models_by_category'][category] = []
        
        documentation['models_by_category'][category].append({
            'name': model.get('name'),
            'description': model.get('description'),
            'active': model.get('active'),
            'severity': model.get('severity'),
            'uuid': model.get('uuid')
        })
        
        # Detailed model information
        documentation['model_details'].append({
            'name': model.get('name'),
            'uuid': model.get('uuid'),
            'category': f"{model.get('category')} / {model.get('subcategory')}",
            'description': model.get('description'),
            'active': model.get('active'),
            'version': model.get('version'),
            'severity': model.get('severity'),
            'configuration': model.get('configuration', {})
        })
    
    return documentation

# Generate documentation
doc = export_model_documentation()

print(f"Model Documentation Export")
print("=" * 50)
print(f"Total models: {doc['summary']['total_models']}")
print(f"Active models: {doc['summary']['active_models']}")

print(f"\nModels by category:")
for category, count in sorted(doc['summary']['categories'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {category}: {count}")

# Export to file (example)
import json
with open('darktrace_models_export.json', 'w') as f:
    json.dump(doc, f, indent=2)
    
print(f"\nDocumentation exported to: darktrace_models_export.json")
```

## Error Handling

```python
try:
    # Attempt to get all models
    models_data = client.models.get()
    
    # Process model information
    for model in models_data.get('models', []):
        model_uuid = model.get('uuid')
        model_name = model.get('name', 'Unknown')
        
        print(f"Processing model: {model_name}")
        
        # Get detailed information for specific model
        try:
            detailed_model = client.models.get(uuid=model_uuid)
            
            if detailed_model:
                config = detailed_model.get('configuration', {})
                print(f"  Configuration: {len(config)} parameters")
            else:
                print(f"  No detailed information available")
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"  Model {model_uuid} not found in detailed lookup")
            else:
                print(f"  Error retrieving model details: {e}")
                
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 403:
            print("Access denied - check API permissions for models endpoint")
        elif e.response.status_code == 404:
            print("Models endpoint not found - check Darktrace version compatibility")
        else:
            print(f"Response: {e.response.text}")
            
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Model Information
- **UUID**: Unique identifier for each model across Darktrace instances
- **PID**: Internal model ID specific to the instance
- **Categories**: Hierarchical organization (Category / Subcategory)
- **Versions**: Model version for tracking updates and changes
- **Active status**: Whether the model is currently enabled for detection

### Model Categories
Common model categories include:
- **Device**: Device behavior and activity models
- **Network**: Network traffic and connection models  
- **Data**: Data movement and access models
- **User**: User behavior and authentication models
- **Compliance**: Regulatory and policy compliance models
- **Threat**: Specific threat detection models

### Configuration Parameters
Model configurations may include:
- **Thresholds**: Detection sensitivity settings
- **Parameters**: Model-specific tuning parameters
- **Filters**: Conditions and criteria for model application
- **Time windows**: Analysis timeframes and lookback periods

### Response Data Filtering
Use `responsedata` parameter to optimize queries:
- `"name,description"`: Basic model information
- `"configuration"`: Model settings and parameters only
- `"uuid,pid,active"`: Minimal identification data
- `"category,subcategory"`: Classification information

### Best Practices
- **Cache model data**: Model information changes infrequently
- **Use UUID for specific lookups**: More reliable than name-based searches
- **Filter response data**: Reduce bandwidth for large model sets
- **Monitor active models**: Focus on enabled detection capabilities
- **Track model versions**: Important for change management

### Common Use Cases
- **Security assessments**: Understand enabled detection capabilities
- **Model management**: Track active/inactive models and configurations
- **Documentation generation**: Create model inventories and references
- **Performance tuning**: Analyze model parameters and thresholds
- **Compliance reporting**: Document detection coverage and capabilities

### Integration Considerations
- **Model UUIDs are consistent** across Darktrace updates
- **Configuration format may vary** by model type and version
- **Active status changes** affect detection capabilities
- **Version tracking** helps with troubleshooting and optimization

## Examples

### Get All Modelss

```python
models_data = client.models.get()
for item in models_data.get("models", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    models_data = client.models.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
