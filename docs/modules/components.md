# Components Module

The Components module provides access to Darktrace component information, allowing you to retrieve details about model components used in the Darktrace system for filtering and analysis.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the components module
components = client.components
```

## Methods Overview

The Components module provides the following method:

- **`get()`** - Retrieve component information with optional filtering

## Methods

### Get Components

Retrieve information about model components used in the Darktrace system. Components define the building blocks of models and provide filtering capabilities.

```python
# Get all components
all_components = components.get()

# Get specific component by ID
specific_component = components.get(cid=1234)

# Get only specific response data (e.g., filters)
filters_only = components.get(responsedata='filters')

# Get specific component with restricted response
component_filters = components.get(
    cid=1234,
    responsedata='filters'
)
```

#### Parameters

- `cid` (int, optional): Component ID to retrieve a specific component. If None, returns all components
- `responsedata` (str, optional): Restrict the returned JSON to only the specified top-level field or object

#### Response Structure

```python
# All components response
{
  "components": [
    {
      "cid": 1234,
      "name": "Component Name",
      "description": "Component description",
      "type": "component_type",
      "filters": [...],
      "metadata": {...}
    },
    // ... more components
  ]
}

# Single component response (when cid specified)
{
  "cid": 1234,
  "name": "Component Name", 
  "description": "Component description",
  "type": "component_type",
  "filters": [...],
  "metadata": {...}
}

# With responsedata='filters'
{
  "filters": [
    // Filter objects only
  ]
}
```

## Examples

### Basic Component Retrieval

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get all available components
all_components = client.components.get()

print(f"Total components: {len(all_components.get('components', []))}")

for component in all_components.get('components', []):
    print(f"Component {component.get('cid')}: {component.get('name')}")
    print(f"  Type: {component.get('type')}")
    print(f"  Description: {component.get('description', 'N/A')}")
```

### Component Analysis

```python
# Analyze component types and usage
components_data = client.components.get()

component_types = {}
for component in components_data.get('components', []):
    comp_type = component.get('type', 'Unknown')
    if comp_type not in component_types:
        component_types[comp_type] = []
    component_types[comp_type].append(component)

print("Component distribution by type:")
for comp_type, comps in component_types.items():
    print(f"  {comp_type}: {len(comps)} components")

# Get detailed info for a specific type
if 'filter' in component_types:
    print(f"\nFilter components:")
    for comp in component_types['filter']:
        print(f"  {comp.get('cid')}: {comp.get('name')}")
```

### Working with Specific Components

```python
# Get detailed information about a specific component
component_id = 1234
component_details = client.components.get(cid=component_id)

print(f"Component {component_id} details:")
print(f"  Name: {component_details.get('name')}")
print(f"  Type: {component_details.get('type')}")
print(f"  Description: {component_details.get('description')}")

# Check if component has filters
if 'filters' in component_details:
    print(f"  Available filters: {len(component_details['filters'])}")
    
    # Get only the filters for this component
    filters_only = client.components.get(
        cid=component_id,
        responsedata='filters'
    )
    
    print("  Filter details:")
    for filter_obj in filters_only.get('filters', []):
        print(f"    - {filter_obj.get('name', 'Unnamed filter')}")
```

### Component Discovery and Mapping

```python
# Create a mapping of component IDs to names for reference
components_data = client.components.get()
component_map = {}

for component in components_data.get('components', []):
    cid = component.get('cid')
    name = component.get('name', f'Component_{cid}')
    component_map[cid] = {
        'name': name,
        'type': component.get('type'),
        'description': component.get('description', '')
    }

# Function to lookup component details
def get_component_info(component_id):
    return component_map.get(component_id, {'name': 'Unknown', 'type': 'Unknown'})

# Example usage
example_id = 1234
info = get_component_info(example_id)
print(f"Component {example_id}: {info['name']} ({info['type']})")
```

## Error Handling

```python
try:
    # Attempt to get components
    components_data = client.components.get()
    
    # Process components
    for component in components_data.get('components', []):
        component_id = component.get('cid')
        
        # Get detailed info for each component
        try:
            detailed_info = client.components.get(cid=component_id)
            print(f"Component {component_id}: {detailed_info.get('name')}")
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Component {component_id} not found")
            else:
                print(f"Error retrieving component {component_id}: {e}")
                
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
        
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Usage Context
- Components are building blocks used in Darktrace models
- They define filtering and analysis capabilities
- Useful for understanding model composition and available filters

### Response Data
- Use `responsedata` parameter to limit response size for large component sets
- Common responsedata values: 'filters', 'metadata', 'description'
- Helps optimize API calls when only specific component information is needed

### Component Types
Components may include various types such as:
- **Filter components**: Provide filtering capabilities
- **Analysis components**: Define analysis methods
- **Detection components**: Specify detection mechanisms
- **Custom components**: Organization-specific components

### Best Practices
- Cache component information for reference during analysis workflows
- Use specific component IDs when you need detailed information
- Leverage responsedata parameter to reduce bandwidth for large queries
- Build component mappings for quick lookups in automated systems

## Examples

### Get All Componentss

```python
components_data = client.components.get()
for item in components_data.get("components", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    components_data = client.components.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
