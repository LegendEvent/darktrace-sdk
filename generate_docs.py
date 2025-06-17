#!/usr/bin/env python3
"""
Generate documentation templates for Darktrace SDK modules
"""

import os
import re
from pathlib import Path

# List of modules that already have documentation
DOCUMENTED_MODULES = [
    'antigena',
    'auth',
    'breaches',
    'devices',
    'status'
]

# Template for module documentation
DOC_TEMPLATE = """# {title} Module

The {title} module provides access to {description}.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the {module_name} module
{module_var} = client.{module_name}
```

## Methods

### Get {title}

Retrieve {description_lower} from the Darktrace platform.

```python
# Get all {module_name_plural}
all_{module_name_plural} = {module_var}.get()

# Get a specific number of {module_name_plural}
recent_{module_name_plural} = {module_var}.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{{
  "{module_name_plural}": [
    {{
      // {title} data
    }},
    // ... more items
  ]
}}
```

## Examples

### Get All {title}s

```python
{module_name_plural}_data = client.{module_name}.get()
for item in {module_name_plural}_data.get("{module_name_plural}", []):
    print(f"Item: {{item}}")
```

## Error Handling

```python
try:
    {module_name_plural}_data = client.{module_name}.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {{e}}")
except Exception as e:
    print(f"An error occurred: {{e}}")
```
"""

def get_module_description(module_name):
    """Get a description for a module based on its name"""
    descriptions = {
        'advanced_search': 'advanced search functionality',
        'analyst': 'AI Analyst incidents and investigations',
        'components': 'Darktrace component information',
        'cves': 'CVE information related to devices',
        'details': 'detailed information about specific entities',
        'deviceinfo': 'detailed device information',
        'devicesearch': 'device search functionality',
        'devicesummary': 'summarized device information',
        'email': 'Darktrace Email security features',
        'endpointdetails': 'endpoint-specific information',
        'enums': 'enumeration values used in the Darktrace platform',
        'filtertypes': 'available filter types for searches',
        'intelfeed': 'threat intelligence feed information',
        'mbcomments': 'model breach comments',
        'metricdata': 'time-series metric data',
        'metrics': 'available metrics and their information',
        'models': 'Darktrace models and their configurations',
        'network': 'network information and statistics',
        'pcaps': 'packet capture functionality',
        'similardevices': 'similar device detection',
        'subnets': 'subnet information and management',
        'summarystatistics': 'overall system statistics',
        'tags': 'tag management for devices and entities'
    }
    
    return descriptions.get(module_name, f"{module_name} functionality")

def generate_doc_for_module(module_name):
    """Generate documentation for a module"""
    # Skip already documented modules
    if module_name in DOCUMENTED_MODULES:
        print(f"Skipping {module_name} - already documented")
        return
    
    # Create title from module name
    title = ' '.join(word.capitalize() for word in module_name.split('_'))
    
    # Get description
    description = get_module_description(module_name)
    description_lower = description[0].lower() + description[1:]
    
    # Create plural form of module name (simple rule, may need adjustments)
    module_name_plural = module_name + 's'
    if module_name.endswith('s'):
        module_name_plural = module_name
    elif module_name.endswith('y'):
        module_name_plural = module_name[:-1] + 'ies'
    
    # Create variable name (typically the same as module_name)
    module_var = module_name
    
    # Generate documentation content
    doc_content = DOC_TEMPLATE.format(
        title=title,
        module_name=module_name,
        module_var=module_var,
        module_name_plural=module_name_plural,
        description=description,
        description_lower=description_lower
    )
    
    # Create the file
    doc_path = Path(f"docs/modules/{module_name}.md")
    doc_path.write_text(doc_content)
    print(f"Generated documentation for {module_name} at {doc_path}")

def main():
    """Main function to generate documentation"""
    # Ensure the docs/modules directory exists
    os.makedirs("docs/modules", exist_ok=True)
    
    # Get all module files
    module_files = Path('darktrace').glob('dt_*.py')
    
    # Process each module file
    for module_file in module_files:
        # Extract module name from filename (remove dt_ prefix and .py extension)
        module_name = module_file.stem.replace('dt_', '')
        
        # Skip utils module
        if module_name == 'utils':
            continue
        
        # Generate documentation
        generate_doc_for_module(module_name)

if __name__ == "__main__":
    main() 