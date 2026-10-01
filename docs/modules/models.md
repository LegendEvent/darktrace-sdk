# Models Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Models module provides read access to the models that exist on the Darktrace Threat Visualizer (`/models`), including custom and de-activated models.

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

- **`get()`** - Retrieve the list of models, or a single model by `uuid`

## Methods

### Get Models

```python
# Get all models (returns a list of model objects)
all_models = models.get()

# Get a specific model by UUID
specific_model = models.get(uuid="80010119-6d7f-0000-0305-5e0000000420")

# Restrict the response to ONE top-level field
model_names = models.get(responsedata="name")
```

#### Parameters

- `uuid` (str, optional): Universally unique identifier (128-bit hexadecimal) of a model. If provided, only that model is returned
- `responsedata` (str, optional): When given the name of **one** top-level field or object, restricts the returned JSON to only that field or object. A comma-separated list of fields is not supported
- `timeout` (float or tuple, optional): Per-request timeout override

#### Return value

The parsed JSON of the response. Without `uuid` this is a list of model objects; with `uuid` the matching model object is returned.

Notes from the API guide:

- The returned JSON does **not** contain the full model logic. `logic.data` holds numeric component IDs (`cid`s) that can be looked up through the `/components` endpoint.
- Only `uuid` is supported as a filter. To search by any other attribute (name, category, tag, ...), retrieve the full list and filter it client-side.
- `uuid` is consistent across instances; `pid` is specific to the instance.
- Since Threat Visualizer 6, models mapped to MITRE ATT&CK include a `mitre` object. It only appears on mapped models.

#### Response Structure

Abbreviated example of one model object (see the API guide for the complete field list):

```python
{
  "name": "Anomalous Connection::New Internal TCP Callback",
  "pid": 219,
  "phid": 21888,
  "uuid": "8aafe33f-eb10-45fe-9ace-66dda23f0cfa",
  "logic": {"data": [23938, 23937], "type": "componentList", "version": 1},
  "throttle": 3600,
  "sharedEndpoints": True,
  "actions": {
    "alert": True,
    "antigena": {},
    "breach": True,
    "model": True,
    "setPriority": False,
    "setTag": False,
    "setType": False
  },
  "tags": ["AP: Lateral Movement"],
  "interval": 30,
  "delay": 0,
  "sequenced": True,
  "active": True,
  "modified": "2022-07-27 16:06:12",
  "activeTimes": {"devices": {...}, "tags": {}, "type": "exclusions", "version": 2},
  "autoUpdatable": True,
  "autoUpdate": False,
  "autoSuppress": True,
  "description": "A device received an incoming connection, ...",
  "behaviour": "decreasing",
  "defeats": [],
  "created": {"by": "System"},
  "edited": {"by": "darktrace", "userID": 2},
  "history": [{"modified": "2022-05-19 17:00:03", "active": False, "message": "...", "by": "System", "phid": 19612}],
  "message": "User set update to false via bulk edit.",
  "version": 25,
  "mitre": {"tactics": ["command-and-control", "lateral-movement"], "techniques": ["T1203", "T1210"]},
  "priority": 2,
  "category": "Informational",
  "compliance": False
}
```

Field notes (from the API guide):

- `pid` is the model's "policy id"; `phid` is the "policy history id" and increments when the model is modified.
- `active` indicates whether the model is enabled or disabled; `modified` is a UTC string (`YYYY-MM-DD HH:MM:SS`).
- `actions.breach` generates a model breach in the threat tray; `actions.alert` pushes alerts to external systems; `actions.model` creates an event in the device's event log without a breach.
- `priority` is numeric: 0-3 equate to informational, 4 to suspicious and 5 to critical. `category` is the matching string. If `compliance` is true, it takes priority over `category`.
- `activeTimes.type` is `"restrictions"` for a blacklist and `"exclusions"` for a whitelist.
- `version` is the model version and increments on edit.

With `responsedata` the list contains only that field or object per model, for example `models.get(responsedata="name")` returns `[{"name": "..."}, ...]`.

## Examples

### Model Overview

```python
from collections import Counter

all_models = client.models.get()  # list of dicts

print(f"Total models: {len(all_models)}")

active = [m for m in all_models if m.get("active")]
print(f"Active models: {len(active)}")
print(f"Inactive models: {len(all_models) - len(active)}")

# Distribution by behavior category (string field)
categories = Counter(m.get("category", "Unknown") for m in all_models)
for category, count in categories.most_common():
    print(f"  {category}: {count} models")
```

### Filtering Client-Side

The API can only filter on `uuid`, so everything else is done on the returned list.

```python
all_models = client.models.get()

# Active models with a given tag
lateral = [
    m for m in all_models
    if m.get("active") and "AP: Lateral Movement" in m.get("tags", [])
]

# Models mapped to MITRE ATT&CK (mitre only exists on mapped models)
mapped = [m for m in all_models if "mitre" in m]
for m in mapped[:10]:
    print(m["name"], m["mitre"]["tactics"], m["mitre"]["techniques"])

# Models that raise breaches and are critical (priority 5)
critical = [m for m in all_models if m.get("priority") == 5 and m.get("actions", {}).get("breach")]
print(f"Critical breach-producing models: {len(critical)}")
```

### Recently Modified Models

```python
import datetime

all_models = client.models.get()
cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=30)

for m in all_models:
    modified = datetime.datetime.strptime(m["modified"], "%Y-%m-%d %H:%M:%S")  # UTC
    if modified > cutoff:
        print(f"{m['name']} (v{m['version']}) modified {m['modified']} by {m.get('edited', {}).get('by')}")
```

### Single Model Details

```python
model = client.models.get(uuid="80010119-6d7f-0000-0305-5e0000000420")

print(f"Name: {model.get('name')}")
print(f"PID: {model.get('pid')}  PHID: {model.get('phid')}")
print(f"Active: {model.get('active')}")
print(f"Category: {model.get('category')} (priority {model.get('priority')})")
print(f"Version: {model.get('version')}")
print(f"Created by: {model.get('created', {}).get('by')}")
print(f"Component IDs: {model.get('logic', {}).get('data')}")  # look up via /components
print(f"Tags: {', '.join(model.get('tags', []))}")
```

### Single Field Only

```python
# responsedata accepts one top-level field name
names = [m["name"] for m in client.models.get(responsedata="name")]
```

## Error Handling

```python
import requests

try:
    models_data = client.models.get()
    for model in models_data:
        print(model.get("name"))
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Notes

- **UUID vs PID**: `uuid` is consistent across instances; `pid` is instance-specific.
- **Full logic**: use the `/components` endpoint with the `logic.data` values as `cid`s.
- **Filtering**: only `uuid` is supported server-side; use client-side filtering for everything else.
- **Caching**: the full model list is large; cache it rather than fetching repeatedly.
