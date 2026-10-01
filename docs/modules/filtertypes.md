# FilterTypes Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The FilterTypes module wraps the `/filtertypes` endpoint. It returns all internal Darktrace filters used in the Model Editor, their value type (for example `numeric` or `string`) and the comparators available for each filter.

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

- **`get()`** - Retrieve available filter types and their comparators (`GET /filtertypes`)

## Methods

### Get Filter Types

```python
# Get all filter types
all_filters = filtertypes.get()

# Restrict the response to one top-level field or object
comparators_only = filtertypes.get(responsedata="comparators")
```

#### Parameters

- `responsedata` (str, optional): When given the name of a top-level field or object, restricts the returned JSON to only that field or object. Pass a single name; the API guide does not document a comma-separated list.
- `timeout` (float or tuple, optional): Per-request timeout override.
- `**params`: Additional query parameters passed through unchanged (not officially documented).

#### Returns

The parsed JSON of the response (`list | dict`). Without `responsedata` this is a list of filter objects. The API guide does not show the response shape when `responsedata` is used, so inspect the result before processing it.

#### Response Structure

Each filter object has the fields below (the API guide abbreviates the list):

| Field | Type | Description |
|-------|------|-------------|
| `filtertype` | string | The filter name, for example `"Destination IP"` |
| `valuetype` | string | The data type expected by the filter, for example `"ipv4"` |
| `comparators` | array | The comparators available when creating model components or filtering using the filtertype |
| `graphable` | boolean | Optional. Only present (as `true`) if the filter can be used on a graph |

```python
[
  {
    "filtertype": "Product",
    "valuetype": "string",
    "comparators": [
      "matches",
      "does not match",
      "contains",
      "does not contain",
      "matches regular expression",
      "does not match regular expression",
      "is longer than",
      "is shorter than"
    ]
  },
  {
    "filtertype": "Volume Size",
    "valuetype": "numeric",
    "comparators": ["<", "<=", "=", "!=", ">=", ">"]
  },
  {
    "filtertype": "Tagged internal source",
    "valuetype": "id",
    "comparators": ["has tag", "does not have tag"]
  },
  {
    "filtertype": "HTTP no referrer",
    "valuetype": "flag",
    "comparators": ["is"]
  }
  # ... more filter types
]
```

## Examples

### List filters by value type

```python
all_filters = client.filtertypes.get()
print(f"Total filter types: {len(all_filters)}")

by_type = {}
for f in all_filters:
    by_type.setdefault(f.get("valuetype", "unknown"), []).append(f["filtertype"])

for value_type, names in sorted(by_type.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"{value_type}: {len(names)} filters")
```

### Graphable filters

`graphable` is only present when it is `true`, so test for the key rather than for `False`.

```python
graphable = [f["filtertype"] for f in client.filtertypes.get() if f.get("graphable")]
print(f"{len(graphable)} graphable filters")
for name in sorted(graphable)[:10]:
    print(f"  {name}")
```

### Comparators per filter

```python
usage = {}
for f in client.filtertypes.get():
    for comp in f.get("comparators", []):
        usage[comp] = usage.get(comp, 0) + 1

for comp, count in sorted(usage.items(), key=lambda x: x[1], reverse=True):
    print(f"{comp}: {count} filters")
```

### Validate a filter and comparator

```python
def validate_filter(filter_name, comparator):
    """Check that a filter exists and offers the given comparator."""
    for f in client.filtertypes.get():
        if f.get("filtertype") == filter_name:
            if comparator in f.get("comparators", []):
                return True, f"'{filter_name} {comparator}' is valid (value type: {f.get('valuetype')})"
            return False, f"Comparator '{comparator}' not available; choose from {f.get('comparators', [])}"
    return False, f"Filter '{filter_name}' not found"

print(validate_filter("Volume Size", ">="))
print(validate_filter("Volume Size", "contains"))
print(validate_filter("No such filter", "="))
```

### Export the filter reference

```python
import json

with open("darktrace_filters_reference.json", "w") as fh:
    json.dump(client.filtertypes.get(), fh, indent=2)
```

## Error Handling

```python
import requests

try:
    filter_types = client.filtertypes.get()
    print(f"Retrieved {len(filter_types)} filter types")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

- The endpoint is `GET` only. The API guide lists it under the permission group "Unrestricted Devices and Visualizer".
- Filter names are display names (for example `"Data ratio"`, `"Tagged internal source"`), not dotted identifiers.
- Value types seen in the API guide examples: `numeric`, `string`, `ipv4`, `id`, `flag`. The list is not stated to be exhaustive.
- Comparators seen in the API guide examples: `<`, `<=`, `=`, `!=`, `>=`, `>`, `matches`, `does not match`, `contains`, `does not contain`, `matches regular expression`, `does not match regular expression`, `is longer than`, `is shorter than`, `has tag`, `does not have tag`, `is`. Which ones apply depends on the filter.
- The filter list changes rarely, so it is reasonable to cache it.
