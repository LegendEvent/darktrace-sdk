# Subnets Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.

The Subnets module retrieves the subnets processed by Darktrace (`GET /subnets`) and edits them (`POST /subnets`). It is useful for automating changes to a large number of subnets or for managing the quality of traffic across the network.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the subnets module
subnets = client.subnets
```

## Methods Overview

- **`get()`** - Retrieve subnet information (returns the parsed JSON, a list of subnet objects)
- **`post()`** - Edit a subnet by `sid` (returns the parsed JSON response)

## Methods

### Get Subnets

```python
# Get all subnets
all_subnets = subnets.get()

# Get one subnet by sid
subnet = subnets.get(sid=25)

# Get subnets seen in the last hour (or: seensince="3600")
active_subnets = subnets.get(seensince="1hour")

# Restrict the response to one top-level field
labels = subnets.get(responsedata="label")
```

#### Parameters

- `sid` (int, optional): Identification number of a subnet modeled in the Darktrace system
- `seensince` (str, optional): Relative offset for activity. Subnets with activity in the specified time period are returned. Either a number of seconds before the current time (e.g. `'3600'`) or a number with a modifier such as `'2min'`, `'1hour'`, `'6day'`, `'1week'` (`3min` = `3mins`, `5hour` = `5hours`, `6day` = `6days`, etc.). Minimum = 1 second, maximum = 6 months
- `responsedata` (str, optional): When given the name of a top-level field or object, restricts the returned JSON to only that field or object (one name)
- `subnet_id` (int, optional): Alias for `sid`. The API has no `/subnets/<id>` path; the value is sent as the `sid` query parameter. Prefer `sid`

The API does not support searching for subnets by anything other than `sid`. To find subnets by label, network, etc., download the full list first and filter the returned data yourself.

#### Response Structure

`get()` returns a list of subnet objects:

```python
[
  {
    "sid": 82,
    "auto": False,
    "dhcp": True,
    "firstSeen": 1585930090000,
    "label": "Test Subnet",
    "lastSeen": 1585930212000,
    "latitude": 12.0,
    "longitude": 0.0,
    "network": "10.12.32.0/24",
    "shid": 144,
    "uniqueHostnames": False,
    "uniqueUsernames": False,
    "confidence": 2,
    "dhcpQuality": 0,
    "kerberosQuality": 0,
    "recentTrafficPercent": 100,
    "clientDevices": 61,
    "mostRecentTraffic": 1585930942000
  }
]
```

| Field | Type | Description |
|---|---|---|
| `sid` | numeric | Unique subnet id |
| `auto` | boolean | The subnet was created automatically from processed traffic and not by modifying a network range on the Subnet Admin page |
| `dhcp` | boolean | Whether DHCP is enabled for the subnet |
| `firstSeen` / `lastSeen` | numeric | First / last time the subnet was seen on the network (epoch time, milliseconds) |
| `label` | string | Label assigned to the subnet in the Threat Visualizer |
| `latitude` / `longitude` | numeric | Location of the subnet as rendered on the Threat Visualizer |
| `network` | string | IP address range that describes the subnet |
| `shid` | numeric | Subnet history id; increments on edit |
| `uniqueHostnames` | boolean | Whether the subnet is tracking by hostname |
| `uniqueUsernames` | boolean | Whether the subnet is tracking by credential |
| `confidence` | numeric | A system field |
| `lastDHCP` | numeric | Timestamp of the last DHCP seen for the subnet |
| `dhcpCount` | numeric | Number of DHCP client devices in the last 7 days |
| `kerberosCount` | numeric | Number of Kerberos client devices in the last 7 days |
| `dhcpQuality` | numeric | Proportion of DHCP client devices compared to the overall number of client devices |
| `kerberosQuality` | numeric | Proportion of Kerberos client devices compared to the overall number of client devices |
| `recentTrafficPercent` | numeric | Percentage of processed traffic involving connections within this subnet; inter-subnet traffic counts for both subnets, so totals may exceed 100% |
| `clientDevices` | numeric | Number of client devices within the subnet |
| `serverDevices` | numeric | Number of server devices within the subnet |
| `icsDevices` | numeric | Number of industrial-type devices within the subnet |
| `mostRecentTraffic` | numeric | Most recent traffic seen for the subnet |

`serverDevices` and `icsDevices` were added alongside Threat Visualizer 6 / 6.1 and may be absent on older instances. Not every field is present in every response (e.g. `lastDHCP`, `dhcpCount` and `kerberosCount` are missing from the example above).

### Edit Subnet

Modify a subnet identified by `sid`. The `/editsubnet` endpoint is deprecated; `/subnets` accepts parameters or JSON (Threat Visualizer 6.0+), and the SDK sends a JSON body. The API guide describes `POST` as editing subnets and documents no response body, and it does not document creating new subnets; creating by posting an unknown `sid` is not covered by the guide.

```python
# Change a label
result = subnets.post(sid=25, label="GuestWifi")

# Enable tracking by hostname and DHCP
result = subnets.post(
    sid=25,
    uniqueUsernames=False,
    uniqueHostnames=True,
    dhcp=True
)

# Update the location (longitude and latitude must be given together)
result = subnets.post(sid=25, latitude=51.5, longitude=-0.1)
```

#### Parameters

- `sid` (int, **required**): Identification number of a subnet modeled in the Darktrace system
- `label` (str, optional): Label to identify the subnet. Do not use quotes around the string, this results in a double-quoted string
- `network` (str, optional): IP address range that describes the subnet
- `longitude` (float, optional): Longitude of the subnet location as rendered on the Threat Visualizer. When updating the location, both `longitude` and `latitude` must be specified; whole values must be passed with a decimal point (e.g. `10.0`)
- `latitude` (float, optional): Latitude, same rules as `longitude`
- `dhcp` (bool, optional): Whether DHCP is enabled for the subnet
- `uniqueUsernames` (bool, optional): Whether the subnet is tracking by credential
- `uniqueHostnames` (bool, optional): Whether the subnet is tracking by hostname
- `excluded` (bool, optional): Whether traffic in this subnet should not be processed at all
- `modelExcluded` (bool, optional): Whether devices within this subnet should be fully modeled. If true, the devices will be added to the `Internal Traffic` subnet
- `responsedata` (str, optional): Restrict the returned JSON to a single top-level field or object (sent in the JSON body; the guide does not show it for POST bodies)

#### Response

The guide documents no POST response schema; see the API guide. `post()` returns whatever JSON the API sends back.

## Examples

### List Subnets and Find by Label

```python
subnets_list = client.subnets.get()   # list of dicts

for subnet in subnets_list:
    print(subnet["sid"], subnet.get("label"), subnet.get("network"),
          "client devices:", subnet.get("clientDevices"))

# Searching by label is not supported by the API: filter locally
guest = [s for s in subnets_list if s.get("label") == "Guest Network"]
```

### Subnets with Recent Activity

```python
recent = client.subnets.get(seensince="24hour")
for subnet in recent:
    print(subnet["sid"], subnet.get("label"), subnet.get("mostRecentTraffic"))
```

### Edit and Verify

```python
client.subnets.post(sid=25, label="GuestWifi", dhcp=True)

# GET with sid returns a list (normally with one element)
result = client.subnets.get(sid=25)
if result:
    print(result[0].get("label"), result[0].get("dhcp"))
```

### Locations and Tracking Flags

```python
for subnet in client.subnets.get():
    lat, lon = subnet.get("latitude"), subnet.get("longitude")
    flags = [name for name in ("auto", "dhcp", "uniqueHostnames", "uniqueUsernames")
             if subnet.get(name)]
    print(subnet["sid"], subnet.get("network"), (lat, lon), flags)
```

## Error Handling

```python
import requests

try:
    all_subnets = client.subnets.get()
    one_subnet = client.subnets.get(sid=25)
    client.subnets.post(sid=25, label="GuestWifi")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")

except ValueError as e:
    print(f"Value error (e.g. a non-JSON response): {e}")
```

## Notes

- `get()` returns a plain list of subnet objects, not a dict.
- Timestamps in the response are epoch time in milliseconds.
- Use `seensince` to limit results to recently active subnets and `responsedata` to reduce the response to one top-level field.
- Booleans are sent lowercase (`true`/`false`) to the API.
