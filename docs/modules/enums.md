# Enums Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Enums module wraps the `/enums` endpoint, which returns the string values for the numeric codes (enumerated types) used in many API responses. Because enums are derived for use in models, the set of enums and enum categories returned depends on your environment and the modules and integrations deployed.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the enums module
enums = client.enums
```

## Methods Overview

- **`get()`** - Retrieve enumerations for all types or restricted to one top-level field/object (`GET /enums`)

## Methods

### Get Enumeration Values

```python
# All enumerated types
all_enums = enums.get()

# Restrict to one top-level field/object
countries = enums.get(responsedata="countries")
```

#### Parameters

- `responsedata` (str, optional): When given the name of a top-level field or object, restricts the returned JSON to only that field or object. Takes a single name.
- `timeout` (float | tuple[float, float], optional): Per-request timeout override.
- `**params`: Additional query parameters passed through as-is (not documented in the API guide).

Using extensions (`/enums/[category]`) is no longer supported by the API and is not used by the SDK.

#### Return Type

Returns the parsed JSON: a `dict` or a `list`, depending on the response. Per the API guide, enum data is made of arrays of objects with a `code` and a `name` (both strings); entries may also carry `"hidden": true`:

```python
[
  {"code": "0", "name": "None", "hidden": True},
  {"code": "1", "name": "Unknown"},
  {"code": "2", "name": "Laptop"},
  {"code": "3", "name": "Mobile"},
  # ... response is abbreviated in the guide
]
```

The response schema in the guide lists named categories (for example `Country`, `Matching metrics`, `DNS response code`, `Proxied connection`, `Trusted hostname`), each an array of `{code, name}` objects, e.g. a country entry `{"code": "AD", "name": "Andorra"}` or a metric entry `{"code": "activeconnections", "name": "Active Connections"}`. Codes are strings and are not necessarily numeric. The names of some keys may change with product taxonomy (for example `AGE Model` is now `Darktrace/Email Model`) and are specific to your environment. Note that the guide's example request uses `responsedata=countries` while its schema names the key `Country`; check the exact key names against your own instance. For the full list of categories see the API guide.

## Examples

### Inspect what your instance returns

```python
data = client.enums.get()
print(type(data))

if isinstance(data, dict):
    for category, entries in data.items():
        print(category, len(entries))
else:
    print(f"{len(data)} entries")
    for entry in data[:5]:
        print(entry["code"], entry["name"], entry.get("hidden", False))
```

### Build a code to name lookup

```python
def build_lookup(entries):
    """Map code -> name for one list of {"code": ..., "name": ...} objects."""
    return {e["code"]: e["name"] for e in entries}

countries = client.enums.get(responsedata="countries")
# Depending on the instance the category list may be returned directly or
# nested under its key; handle both.
if isinstance(countries, dict):
    countries = countries.get("countries", countries.get("Country", []))

lookup = build_lookup(countries)
print(lookup.get("AD", "Unknown"))   # codes are strings
```

### Find a category by name and list its visible entries

Category key names vary by environment, so match them case-insensitively instead of hard-coding one spelling. Entries flagged `"hidden": true` can be skipped when you only want the selectable values.

```python
def find_category(data, wanted):
    """Return the entries of the first dict key matching `wanted` (case-insensitive)."""
    if not isinstance(data, dict):
        return []
    for key, entries in data.items():
        if key.lower() == wanted.lower():
            return entries
    return []

data = client.enums.get()
for entry in find_category(data, "Country")[:10]:
    if not entry.get("hidden", False):
        print(entry["code"], entry["name"])
```

### Translate codes found in another response

Fetch the enums once, build lookups per category, then resolve the codes you meet elsewhere (codes are compared as strings):

```python
data = client.enums.get()

lookups = {
    category: {e["code"]: e["name"] for e in entries}
    for category, entries in data.items()
} if isinstance(data, dict) else {}

def name_for(category, code, default="Unknown"):
    return lookups.get(category, {}).get(str(code), default)

print(name_for("Country", "AD"))
```

For endpoints that support it (for example `/modelbreaches`), the guide also describes an `expandenums` parameter that returns full strings instead of numeric codes in certain nested lists, which can remove the need for a manual lookup.

### Caching

Enum data changes rarely, so fetch it once and reuse it:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def get_enums(responsedata=None):
    return client.enums.get(responsedata=responsedata)
```

To refresh periodically instead of keeping the data for the whole process, store a timestamp next to it:

```python
import time

_cache = {"data": None, "fetched": 0.0}

def get_enums_ttl(max_age=3600):
    if _cache["data"] is None or time.time() - _cache["fetched"] > max_age:
        _cache["data"] = client.enums.get()
        _cache["fetched"] = time.time()
    return _cache["data"]
```

## Error Handling

```python
import requests

try:
    all_enums = client.enums.get()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

## Notes

- Only `GET` is supported. The only documented parameter is `responsedata`.
- `code` and `name` are strings; do not assume integer codes.
- Category availability varies by environment and deployed modules.
- Entries marked `"hidden": true` are present in the response but flagged as hidden.
