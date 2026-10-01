# Device Search Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Device Search module wraps the `/devicesearch` endpoint, a highly filterable search over the devices Darktrace has seen on the network. It is better suited to inventory management and general queries than `/devices` because it provides sorting and string searching.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the device search module
devicesearch = client.devicesearch
```

## Methods Overview

- **`get()`** - Search for devices with filtering, sorting and pagination
- **`get_tag(tag)`**, **`get_type(type)`**, **`get_label(label)`**, **`get_vendor(vendor)`**, **`get_hostname(hostname)`**, **`get_ip(ip)`**, **`get_mac(mac)`** - Shortcuts that search on a single field filter. Each accepts the same extra keyword arguments as `get()` (`count`, `orderBy`, `order`, `offset`, `responsedata`, `seensince`, `timeout`).

All methods send a `GET` request and return the parsed JSON response (a `dict` for a normal search).

## Methods

### Search Devices

```python
# Basic device search (default: 100 devices, ordered by lastSeen ascending)
devices = devicesearch.get()

# Limit the number of devices
devices = devicesearch.get(count=50)

# Free-text search across all device fields
devices = devicesearch.get(query='"sarah"')

# Field filter with wildcard
devices = devicesearch.get(query='hostname:"server*"', count=100)

# Several space-separated filters
devices = devicesearch.get(
    query='tag:"Antigena*" ip:"10.0.1.*"',
    count=10,
    orderBy="priority",
    order="desc"
)

# Same filters through keyword arguments (do not combine with query)
devices = devicesearch.get(tag="Security Device", orderBy="lastSeen", order="asc")

# Devices with activity in the last hour
recent_devices = devicesearch.get(seensince="1hour")

# Paginated search
page1 = devicesearch.get(count=100, offset=0)
page2 = devicesearch.get(count=100, offset=100)

# Restrict the response to one top-level field
only_devices = devicesearch.get(query='tag:"critical"', responsedata="devices")

# Single-field helper
laptops = devicesearch.get_type("laptop", count=50)
```

#### Parameters

- `count` (int, optional): Number of devices to return (default: 100, maximum: 300)
- `orderBy` (str, optional): Field to order by (default: `lastSeen`). Valid values: `priority`, `hostname`, `ip`, `macaddress`, `vendor`, `os`, `firstSeen`, `lastSeen`, `devicelabel`, `typelabel`
- `order` (str, optional): `'asc'` or `'desc'` (default: ascending)
- `query` (str, optional): Search string, see Query Syntax below
- `offset` (int, optional): Offset for the results returned
- `responsedata` (str, optional): Name of ONE top-level field or object; restricts the returned JSON to only that field or object
- `seensince` (str, optional): Relative offset for activity; only devices with activity in that period are returned. Either a number of seconds before now (e.g. `'60'`) or a number with a modifier such as second, minute, hour, day or week (e.g. `'30minute'`, `'1hour'`). Minimum is 1 second. If unspecified, the time frame is four weeks (28 days).
- `tag`, `label`, `type`, `vendor`, `hostname`, `ip`, `mac` (str, optional): SDK convenience filters. Each value is turned into a `field:"value"` term and the terms are joined with spaces into the `query`. There is no `os` keyword argument; use `query='os:"..."'` instead.
- `timeout` (float or tuple, optional): Request timeout
- `**kwargs`: Additional parameters are passed through as query parameters

`query` and the convenience filters are mutually exclusive: setting both raises `ValueError`.

#### Query Syntax

`query` can be a plain string that is searched across all key/value pairs (`query='"value"'`) or be limited to one field with a filter. Valid field filters: `label`, `tag`, `type`, `hostname`, `ip`, `mac`, `vendor`, `os`, for example `label:"test"`.

- Wildcards (`*`) are supported, e.g. `ip:"10.0.1.*"`.
- Multiple queries can be separated by spaces, e.g. `tag:"*T*" label:"Test"`.
- Repeated filters on the same field are treated as "or", e.g. `type:"laptop" type:"desktop"` returns laptops and desktops.

The `priority` field is not included in the response for a device if its value is 0.

#### Response Structure

```python
{
  "totalCount": 2185,
  "devices": [
    {
      "did": 2719,
      "ip": "192.168.120.39",
      "ips": [
        {"ip": "192.168.120.39", "timems": 1581508800000, "time": "2020-02-12 12:00:00", "sid": 6}
      ],
      "sid": 6,
      "hostname": "sarah's iphone",
      "firstSeen": 1576581851000,
      "lastSeen": 1582131590000,
      "os": "Mac OS X",
      "typename": "mobile",
      "typelabel": "Mobile",
      "tags": [
        {
          "tid": 17,
          "expiry": 0,
          "thid": 17,
          "name": "iOS device",
          "restricted": False,
          "data": {"auto": False, "color": 181, "description": "", "visibility": "Public"},
          "isReferenced": True
        }
      ]
    }
  ]
}
```

- `totalCount`: total number of devices that meet the query parameters
- `devices`: array of matching devices. Per device: `did` (unique device id), `macaddress`, `vendor` (derived from the MAC address), `ip` (current IP), `ips` (historic IPs with `ip`, `timems`, `time`, `sid`), `sid` (current subnet id), `hostname`, `firstSeen` / `lastSeen` (epoch milliseconds), `os`, `devicelabel` (optional label), `typename` (system format), `typelabel` (readable format), `priority` (omitted when 0), `tags`
- `tags` entries: `tid`, `expiry`, `thid`, `name`, `restricted` (read-only tag), `data` (`auto`, `color`, `description`, `visibility`), `isReferenced`

Not every field is present on every device (for example `tags` only appears for tagged devices). See the Darktrace API guide for the full `/devicesearch` response schema. With `responsedata`, the response contains only the named field, so it is no longer shaped like the structure above.

## Examples

### Basic Device Discovery

```python
all_devices = client.devicesearch.get(count=300)  # Maximum count

devices = all_devices.get('devices', [])
print(f"Returned {len(devices)} of {all_devices.get('totalCount')} devices")

for device in devices[:10]:
    print(f"Device: {device.get('hostname', 'Unknown')} ({device.get('ip', 'Unknown')})")
    print(f"  Vendor: {device.get('vendor', 'Unknown')}")
    print(f"  Type: {device.get('typelabel', 'Unknown')}")
    print(f"  Priority: {device.get('priority', 0)}")  # absent when 0
    print(f"  Last Seen: {device.get('lastSeen', 0)}")
```

### Advanced Search Queries

```python
# Tagged "Antigena*" devices in a subnet, highest priority first
antigena = client.devicesearch.get(
    query='tag:"Antigena*" ip:"10.0.1.*"',
    orderBy="priority",
    order="desc",
    count=10
)

# Windows devices
windows_devices = client.devicesearch.get(
    query='os:"Windows*"',
    orderBy="hostname",
    order="asc"
)

# Vendors Microsoft OR Dell (repeated field filter = or)
vendors = client.devicesearch.get(query='vendor:"Microsoft" vendor:"Dell"')

print(f"Matches: {vendors.get('totalCount')}")
```

### Device Inventory

```python
def create_device_inventory():
    inventory = {'by_vendor': {}, 'by_type': {}, 'by_os': {}}

    response = client.devicesearch.get(count=300)
    for device in response.get('devices', []):
        vendor = device.get('vendor', 'Unknown')
        inventory['by_vendor'][vendor] = inventory['by_vendor'].get(vendor, 0) + 1

        device_type = device.get('typelabel', 'Unknown')
        inventory['by_type'][device_type] = inventory['by_type'].get(device_type, 0) + 1

        os_name = device.get('os', 'Unknown')
        inventory['by_os'][os_name] = inventory['by_os'].get(os_name, 0) + 1

    return inventory

inventory = create_device_inventory()
for vendor, count in sorted(inventory['by_vendor'].items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {vendor}: {count}")
```

### Paginated Device Processing

Increment `offset` by `count` on each request. This is required to retrieve more than 300 devices.

```python
def process_all_devices():
    offset = 0
    page_size = 300  # Maximum allowed
    all_devices = []

    while True:
        page = client.devicesearch.get(
            count=page_size,
            offset=offset,
            orderBy="firstSeen",
            order="asc"
        )

        devices = page.get('devices', [])
        all_devices.extend(devices)

        if len(devices) < page_size:
            break

        offset += page_size

    return all_devices

all_devices = process_all_devices()
print(f"Total devices processed: {len(all_devices)}")
```

### Device Activity

```python
# Devices with activity in different time windows
for window in ["30minute", "1hour", "4hour", "1day"]:
    result = client.devicesearch.get(seensince=window, orderBy="lastSeen", order="desc", count=300)
    print(f"Active in last {window}: {result.get('totalCount')} devices")
```

## Error Handling

```python
import requests

try:
    devices = client.devicesearch.get(
        query='hostname:"server*"',
        count=100,
        orderBy="hostname",
        order="asc"
    )
    print(f"Found {len(devices.get('devices', []))} of {devices.get('totalCount')} devices")

except ValueError as e:
    # query combined with tag/label/type/vendor/hostname/ip/mac
    print(f"Invalid arguments: {e}")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
```

## Notes

- `count` is limited to 300 per request; use `offset` pagination for larger result sets.
- The default time frame is 28 days; widen or narrow it with `seensince`.
- `responsedata` takes the name of a single top-level field or object (e.g. `devices`).
- Use quotes for exact values (`hostname:"web-server-01"`) and `*` for wildcards (`hostname:"server*"`).
- The SDK puts convenience-filter values inside double quotes without escaping, so a value containing `"` must be passed through a hand-written `query` instead.
