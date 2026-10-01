# Components Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Components module provides access to the `/components` endpoint. Components are segments of model logic that are evaluated; each component is identified by its `cid`, which is referenced in the data attribute of model breaches. A component is a series of filters that an event or connection is assessed against as part of a larger model.

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

- **`get()`** - Retrieve all components or a single component by `cid`

## Methods

### Get Components

```python
# Get all components
all_components = components.get()

# Get specific component by ID
specific_component = components.get(cid=8977)

# Restrict the response to one top-level field
filters_only = components.get(responsedata='filters')

# Specific component, restricted to one field
component_filters = components.get(cid=8977, responsedata='filters')
```

#### Parameters

- `cid` (int, optional): Component ID. If omitted, all components are returned (`GET /components`); otherwise `GET /components/<cid>`
- `responsedata` (str, optional): Name of a single top-level field or object; the returned JSON is restricted to only that field or object
- `timeout` (float or tuple, optional): Per-request timeout override
- `**params`: Additional query parameters passed through to the API

The method returns the parsed JSON response (`dict` or `list`). The API guide only states that `/components` "returns a list of all component parts"; it does not show an example of the all-components response, so do not rely on a particular wrapper (the examples below handle both a bare list and a dict).

#### Response Structure

Single component (`/components/8977`, abridged from the API guide example):

```python
{
  "cid": 8977,
  "chid": 15524,
  "mlid": 33,
  "threshold": 5242880,
  "interval": 3600,
  "logic": {
    "data": {
      "left": "A",
      "operator": "AND",
      "right": {"left": "B", "operator": "AND", "right": "C"}
    },
    "version": "v0.1"
  },
  "filters": [
    {
      "id": "A",
      "cfid": 59205,
      "cfhid": 99603,
      "filtertype": "Direction",
      "comparator": "is",
      "arguments": {"value": "out"}
    },
    {
      "id": "d1",
      "cfid": 59210,
      "cfhid": 99608,
      "filtertype": "Connection hostname",
      "comparator": "display",
      "arguments": {}
    }
  ],
  "active": True
}
```

| Field | Description |
|---|---|
| `cid` | The component ID, a unique identifier |
| `chid` | The component history ID; increments when the component is edited |
| `mlid` | The metric logic ID of the metric used in the component |
| `threshold` | The threshold value the size must exceed for the component to breach |
| `interval` | Timeframe in seconds within which the threshold must be satisfied |
| `logic` | Object describing the component logic |
| `logic.data` | Logical relationship between the component filters (`left`, `operator`, `right`), referencing filters by their alphabetical ID |
| `logic.version` | Version of the component logic |
| `filters` | Array of the filters that make up the component |
| `filters[].id` | Filter identifier within the component: a capital letter (`A`, `F`, ...) for filters used in the model logic, or `d1`, `d4`, ... for display filters |
| `filters[].cfid` | The component filter ID, a unique identifier |
| `filters[].cfhid` | The component filter history ID; increments when the filter is edited |
| `filters[].filtertype` | The filtertype used (full list on the `/filtertypes` endpoint) |
| `filters[].comparator` | The comparator (valid comparators per filtertype are on the `/filtertypes` endpoint) |
| `filters[].arguments` | Object containing the value to compare (`arguments.value`); empty for display filters |
| `active` | Whether the component is currently active as part of a model |

With `responsedata`, only the named top-level field/object is returned (for example `responsedata='filters'` restricts the response to the `filters` field).

## Examples

### Listing Components

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def component_list(data):
    # The guide does not show the all-components shape: accept a bare list or a dict
    if isinstance(data, list):
        return data
    return data.get('components', [])

for component in component_list(client.components.get()):
    print(f"Component {component.get('cid')}: "
          f"{len(component.get('filters', []))} filters, "
          f"threshold {component.get('threshold')}, "
          f"interval {component.get('interval')}s, "
          f"active={component.get('active')}")
```

### Inspecting a Specific Component

```python
component = client.components.get(cid=8977)

print(f"Component {component['cid']} (mlid {component['mlid']}, active={component['active']})")

for f in component.get('filters', []):
    kind = "display" if f['id'].startswith('d') else "logic"
    print(f"  {f['id']} ({kind}): {f['filtertype']} {f['comparator']} {f['arguments'].get('value', '')}")
```

### Restricting the Response

```python
# Only the 'filters' field of one component
result = client.components.get(cid=8977, responsedata='filters')
for f in result.get('filters', []):
    print(f['id'], f['filtertype'], f['comparator'])
```

### Building a Component Lookup

```python
# Map each cid to a short summary for later lookups (e.g. from the cid values in model breach data)
component_map = {}
for component in component_list(client.components.get()):
    component_map[component['cid']] = {
        'mlid': component.get('mlid'),
        'threshold': component.get('threshold'),
        'interval': component.get('interval'),
        'active': component.get('active'),
    }

info = component_map.get(8977, {})
print(info)
```

### Counting Filtertypes

```python
from collections import Counter

# Count which filtertypes are used across all components
counts = Counter()
for component in component_list(client.components.get()):
    for f in component.get('filters', []):
        counts[f['filtertype']] += 1

for filtertype, n in counts.most_common():
    print(f"{filtertype}: {n}")
```

### Reading the Component Logic

```python
component = client.components.get(cid=8977)
logic = component['logic']['data']

def render(node):
    # A node is either a filter id (e.g. "A") or {"left", "operator", "right"}
    if isinstance(node, str):
        return node
    return f"({render(node['left'])} {node['operator']} {render(node['right'])})"

print(render(logic))   # e.g. (A AND (B AND C))
```

### Inspecting Several Components

```python
import requests

for cid in (8977, 8978):
    try:
        component = client.components.get(cid=cid)
    except requests.exceptions.HTTPError as e:
        print(f"Component {cid}: HTTP error {e}")
        continue
    print(cid, component.get('active'), [f['id'] for f in component.get('filters', [])])
```

## Error Handling

```python
import requests

try:
    component = client.components.get(cid=8977)
    print(component)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

- `responsedata` takes the name of ONE top-level field or object. Valid names are the top-level fields above: `cid`, `chid`, `mlid`, `threshold`, `interval`, `logic`, `filters`, `active`.
- For certain filtertypes, `arguments.value` is a numeric value corresponding to an enumerated type; see the `/enums` endpoint for the full list.
- Filtertypes and the comparators available for each are listed on the `/filtertypes` endpoint.
- Display filters (`d1`, `d4`, ...) are shown in the UI when a breach occurs and have no impact on the component logic.
