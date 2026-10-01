# Tags Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Tags module reviews, creates and deletes tags, and controls the tags applied to devices and credentials (`/tags`, `/tags/entities` and `/tags/[tid]/entities`).

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the tags module
tags = client.tags
```

## Permissions and rules

- POST and DELETE requests require the "Edit Tags" permission (granted automatically to users with the "Visualizer" or "SaaS Console" permission since Darktrace 5.2; global tokens from the System Config page should have it).
- Tags that are restricted (read-only, only modifiable or applicable by Darktrace) or referenced by model components cannot be deleted.
- Tags with `::` in the name are scoped (`[a]::[b]`, `a` determines the scope, `b` can be any text). Scoped tags are mutually exclusive: only one tag of a given scope can be present on a device at once.
- `responsedata` takes the name of ONE top-level field or object and restricts the returned JSON to it.
- All methods return the parsed JSON response of the API (a `dict` or a `list`), not a boolean.

## Methods

### Tag Management

#### get()

Retrieve all tags, or a single tag by `tid` or by name. `tag_id` and `tag` are alternatives (`/tags/[tid]` vs `/tags?tag=name`).

```python
# Get all tags (a list of tag objects)
all_tags = tags.get()

# Get specific tag by ID
specific_tag = tags.get(tag_id="5")

# Get tag by name
tag_by_name = tags.get(tag="active threat")

# Restrict the response to one top-level field
names = tags.get(responsedata="name")
```

**Parameters:**
- **tag_id** (str, optional): Tag ID (`tid`) to retrieve a specific tag
- **tag** (str, optional): Name of an existing tag
- **responsedata** (str, optional): Name of a top-level field or object to restrict the returned JSON to
- **timeout** (float or tuple, optional): Request timeout in seconds

**Returns:** `dict` for a single tag (`/tags/[tid]`), otherwise the parsed JSON (see the API guide for the exact shape of the full list).

#### create()

Create a new tag. The code sends a JSON body with `name` and a `data` object holding `color` and `description` (the API minimum is `name` plus an empty `data` object; `color` and `description` are optional but recommended).

```python
new_tag = tags.create(name="Suspicious Behavior")

colored_tag = tags.create(
    name="Suspicious Behavior",
    color=100,
    description="Device is behaving suspiciously"
)
print(colored_tag)
```

**Parameters:**
- **name** (str, required): Name for the created tag
- **color** (int, optional): Hue value (in HSL) used to color the tag in the Threat Visualizer UI
- **description** (str, optional): Description for the tag
- **timeout** (float or tuple, optional): Request timeout in seconds

**Returns:** `dict` with the created tag information.

#### delete()

Delete a tag by its tag ID (`DELETE /tags/[tid]`). Restricted tags and tags referenced by model components cannot be deleted.

```python
result = tags.delete(tag_id="89")
```

**Parameters:**
- **tag_id** (str, required): Tag ID (`tid`) to delete
- **timeout** (float or tuple, optional): Request timeout in seconds

**Returns:** `dict` - the parsed API response.

### Entity Tag Management (`/tags/entities`)

#### get_entities()

List the tags of a device, or the entities of a tag. A GET must include either `did` or `tag`; otherwise a `ValueError` is raised.

```python
# Tags applied to device 1 (a list of tag objects)
device_tags = tags.get_entities(did=1)
for t in device_tags:
    print(t["tid"], t["name"], t["data"]["color"])

# Tag-entity rows for a tag (a list)
rows = tags.get_entities(tag="High Risk")
for row in rows:
    print(row["teid"], row["entityType"], row["entityValue"])

# With fulldevicedetails the response is an object with "entities" and "devices"
detailed = tags.get_entities(tag="High Risk", fulldevicedetails=True)
print(detailed["entities"], detailed["devices"])
```

**Parameters:**
- **did** (int, optional): Device ID to list tags for a device
- **tag** (str, optional): Name of an existing tag to list its entities
- **responsedata** (str, optional): Name of a top-level field or object to restrict the returned JSON to
- **fulldevicedetails** (bool, optional): When true and a tag is queried, adds a `devices` object with more detailed device data (the standard expanded device format, see the `/devices` schema with `includetags=true`)
- **timeout** (float or tuple, optional): Request timeout in seconds

When `did` is used, the response mirrors `/tags` (a list of tag objects); when `tag` is used it mirrors `/tags/[tid]/entities`.

#### post_entities()

Add a tag to a device. This endpoint takes form parameters, not JSON; the module sends them form-encoded.

```python
# Apply the tag permanently
tags.post_entities(did=1, tag="Active Threat")

# Apply the tag for one hour
tags.post_entities(did=1, tag="Active Threat", duration=3600)
```

**Parameters:**
- **did** (int, required): Device ID to tag
- **tag** (str, required): Name of an existing tag
- **duration** (int, optional): How long the tag should be set for the device; it is removed once this duration has expired
- **timeout** (float or tuple, optional): Request timeout in seconds

**Returns:** `dict` - the parsed API response.

#### delete_entities()

Remove a tag from a device (`DELETE /tags/entities?tag=...&did=...`).

```python
result = tags.delete_entities(did=1, tag="Guest")
```

**Parameters:**
- **did** (int, required): Device ID to untag
- **tag** (str, required): Name of the tag to remove
- **timeout** (float or tuple, optional): Request timeout in seconds

**Returns:** `dict` - the parsed API response.

### Tag-ID based Entity Management (`/tags/[tid]/entities`)

#### get_tag_entities()

List the entities (devices or credentials) carrying a specific tag.

```python
rows = tags.get_tag_entities(tid=123)
for row in rows:
    print(row["teid"], row["entityType"], row["entityValue"])

# Full device details (adds a "devices" object)
detailed = tags.get_tag_entities(tid=123, fulldevicedetails=True)
```

**Parameters:**
- **tid** (int, required): Tag ID to query (retrievable from `get()`)
- **responsedata** (str, optional): Name of a top-level field or object to restrict the returned JSON to
- **fulldevicedetails** (bool, optional): When true, adds a `devices` object with more detailed device data
- **timeout** (float or tuple, optional): Request timeout in seconds

#### post_tag_entities()

Add a tag to one or more entities. This endpoint only supports JSON in POST requests. Device IDs are sent as strings (the module converts ints, and list items, with `str()`).

```python
# Tag several devices
tags.post_tag_entities(tid=1, entityType="Device", entityValue=["1", "2", "4"])

# Tag a credential for one hour
tags.post_tag_entities(
    tid=1,
    entityType="Credential",
    entityValue="benjamin.ash",
    expiryDuration=3600
)
```

**Parameters:**
- **tid** (int, required): Tag ID to apply
- **entityType** (str, required): `"Device"` or `"Credential"`
- **entityValue** (str or list, required): For devices, the numeric `did` (as a string); for credentials, the credential value. An array is also accepted
- **expiryDuration** (int, optional): Duration in seconds the tag should be applied for
- **timeout** (float or tuple, optional): Request timeout in seconds

**Returns:** `dict` - the parsed API response (it contains the `teid` of the new tag-to-entity relationship; see the API guide for the exact shape).

#### delete_tag_entity()

Remove a tag from an entity via the tag entity ID (`teid`) of the tag-to-entity relationship (`DELETE /tags/[tid]/entities/[teid]`). The `teid` appears in the data returned by `get_tag_entities()` and in the response when a tag is added.

```python
rows = tags.get_tag_entities(tid=1)
teid = rows[0]["teid"]
result = tags.delete_tag_entity(tid=1, teid=teid)
```

**Parameters:**
- **tid** (int, required): Tag ID
- **teid** (int, required): Tag entity ID
- **timeout** (float or tuple, optional): Request timeout in seconds

**Returns:** `dict` - the parsed API response.

## Response Structures

### Tag object (`/tags/[tid]`, `/tags?tag=`, and the items returned by `/tags/entities?did=`)

```json
{
  "tid": 24,
  "expiry": 0,
  "thid": 24,
  "name": "DNS Server",
  "restricted": false,
  "data": {
    "auto": false,
    "color": 112,
    "description": "Devices receiving and making DNS queries",
    "visibility": "Public"
  },
  "isReferenced": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `tid` | numeric | The tag ID, a unique value |
| `expiry` | numeric | Default expiry time for the tag when applied to a device |
| `thid` | numeric | Tag history ID, increments if the tag is edited |
| `name` | string | Tag label shown in the UI |
| `restricted` | boolean | Read-only tag; can only be modified or applied by Darktrace |
| `data.auto` | boolean | Whether the tag was auto-generated |
| `data.color` | numeric | Hue value (in HSL) used to color the tag in the UI |
| `data.description` | string | Optional description |
| `data.visibility` | string | A system field |
| `isReferenced` | boolean | Whether the tag is used by one or more model components |

### Tag-entity rows (`/tags/entities?tag=` and `/tags/[tid]/entities`)

```json
[
  {
    "teid": 325684,
    "tehid": 325684,
    "tid": 123,
    "entityType": "Credential",
    "entityValue": "b.ash@holdingsinc.com",
    "valid": true,
    "expiry": 1702038492000
  },
  {
    "teid": 325614,
    "tehid": 325614,
    "tid": 123,
    "entityType": "Device",
    "entityValue": "400",
    "valid": true
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `teid` | numeric | Tag entity ID of the tag-to-entity relationship; used in DELETE requests |
| `tehid` | numeric | Tag entity history ID, a system field |
| `tid` | numeric | The tag ID |
| `entityType` | string | Type of entity the tag is applied to (device or credential) |
| `entityValue` | string | For devices the `did`, for credentials the credential value |
| `valid` | boolean | A system field |
| `expiry` | numeric | Expiry time of the tag on the entity (only present when an expiry is set) |

With `fulldevicedetails=true` and a tag, the response is an object with an `entities` array (rows as above) and a `devices` array of devices in the standard expanded format.

## Examples

### Tag a device temporarily and clean up

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Create a tag; the response is the tag object, so tid is a top-level key
tag = client.tags.create(name="Under Investigation", color=240, description="Temporary tag")
tid = tag["tid"]

# Apply it to device 123 for one hour (form-encoded POST by name)
client.tags.post_entities(did=123, tag="Under Investigation", duration=3600)

# Tags on the device: a list of tag objects
for t in client.tags.get_entities(did=123):
    print(t["tid"], t["name"])

# Tag-entity rows for the tag: a list; teid identifies each relationship
for row in client.tags.get_tag_entities(tid=tid):
    print(row["teid"], row["entityType"], row["entityValue"])

# Remove the tag from the device, then delete the tag itself
client.tags.delete_entities(did=123, tag="Under Investigation")
client.tags.delete(tag_id=str(tid))
```

### Find unused tags

```python
for tag in client.tags.get():
    rows = client.tags.get_tag_entities(tid=tag["tid"])
    if not rows and not tag["restricted"] and not tag["isReferenced"]:
        print("unused:", tag["name"])
```

## Error Handling

```python
import requests

try:
    new_tag = client.tags.create(name="test_tag", color=120, description="Test tag")
    client.tags.post_entities(did=123, tag="test_tag", duration=3600)
    device_tags = client.tags.get_entities(did=123)
    client.tags.delete_entities(did=123, tag="test_tag")
    client.tags.delete(tag_id=str(new_tag["tid"]))

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")

except requests.exceptions.Timeout as e:
    print(f"Request timeout: {e}")

except ValueError as e:
    # e.g. get_entities() called without did or tag
    print(f"Value error: {e}")
```
