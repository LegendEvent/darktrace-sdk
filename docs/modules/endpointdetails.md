# EndpointDetails Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The EndpointDetails module wraps the `/endpointdetails` API endpoint. It returns location, IP address and (optionally) device connection information for external IPs and hostnames, and can be used to get intel about endpoints and the devices that have been seen accessing them.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the endpointdetails module
endpointdetails = client.endpointdetails
```

## Methods Overview

- **`get()`** - Retrieve details for an external IP address or hostname

## Methods

### Get Endpoint Details

`GET /endpointdetails`. Returns the parsed JSON response (a `dict`).

```python
# Details for a specific IP address
ip_details = endpointdetails.get(ip="8.8.8.8")

# Details for a hostname, including devices that connected to it
hostname_details = endpointdetails.get(hostname="darktrace.com", devices=True)

# Restrict the response to one top-level field
asn_only = endpointdetails.get(ip="8.8.8.8", responsedata="asn")
```

#### Parameters

- `ip` (str, optional): Return data for this IP address.
- `hostname` (str, optional): Return data for this hostname.
- `additionalinfo` (bool, optional): Return additional information about the endpoint.
- `devices` (bool, optional): Return a list of devices which have recently connected to the endpoint.
- `score` (bool, optional): Return rarity data for this endpoint.
- `responsedata` (str, optional): When given the name of a **single** top-level field or object, restricts the returned JSON to only that field or object.
- `timeout` (float or tuple, optional): Per-request timeout override.

Parameters left as `None` are not sent.

#### Notes from the API guide

- The "popularity" score = 100 - (IP or domain) rarity score.
- For hostname queries, `additionalinfo=True` adds an `ips` object and a `locations` object with details of the IP addresses Darktrace has seen associated with the hostname and the physical locations of those IPs where derivable.
- Queries for IPs that are internal (or treated as such) return `"name": "internal_ip"` and different key/value fields.
- The structure of the `additionalinfo` and `score` data is not described in detail in the API guide; inspect the returned JSON or see the API guide.

#### Response Structure

IP query (`ip=...`, `devices=False`):

```python
{
  "ip": "172.217.169.36",
  "firsttime": 1528807105000,        # first time seen on the network, epoch ms
  "country": "United States",
  "asn": "AS15169 Google LLC",
  "city": "",
  "region": "North America",
  "name": "",                        # "internal_ip" for internal IPs
  "longitude": -97.822,
  "latitude": 37.751
}
```

IP query with `devices=True` adds a `devices` array (fields as in the hostname example below, plus `macaddress` and `vendor` in the guide example).

Hostname query (`hostname=...`, `devices=False`):

```python
{
  "hostname": "darktrace.com",
  "firsttime": 1528807217000
}
```

Hostname query with `devices=True`:

```python
{
  "hostname": "darktrace.com",
  "firsttime": 1528807217000,
  "devices": [
    {
      "did": 316,                     # device id
      "ip": "10.0.56.12",             # current IP
      "ips": [                        # historic IPs
        {"ip": "10.0.56.12", "timems": 1581508800000, "time": "2020-02-12 12:00:00", "sid": 23}
      ],
      "sid": 23,                      # subnet id
      "hostname": "Sarah Development",
      "firstSeen": 1528807078000,     # epoch ms
      "lastSeen": 1581960902000,      # epoch ms
      "os": "Linux 3.11 and newer",
      "typename": "desktop",
      "typelabel": "Desktop"
    }
  ]
}
```

## Examples

### Devices That Connected to an Endpoint

```python
details = client.endpointdetails.get(hostname="darktrace.com", devices=True)

print(f"Hostname: {details.get('hostname')}")
print(f"First seen: {details.get('firsttime')}")

for device in details.get("devices", []):
    print(f"  did={device['did']} {device.get('hostname')} ({device.get('ip')}) "
          f"lastSeen={device.get('lastSeen')}")
```

### IP Location and ASN

```python
details = client.endpointdetails.get(ip="8.8.8.8")

if details.get("name") == "internal_ip":
    print("Internal IP - different fields are returned")
else:
    print(f"{details.get('ip')}: {details.get('asn')}")
    print(f"Location: {details.get('city') or 'n/a'}, {details.get('region')}, {details.get('country')}")
    print(f"Lat/Lon: {details.get('latitude')}, {details.get('longitude')}")
```

### Restricting the Response

```python
# responsedata takes ONE top-level field or object name
devices_only = client.endpointdetails.get(
    hostname="darktrace.com",
    devices=True,
    responsedata="devices"
)
```

## Error Handling

```python
import requests

try:
    details = client.endpointdetails.get(ip="8.8.8.8", devices=True)
    print(f"Endpoint: {details.get('ip')} ({details.get('country')})")
    print(f"Connected devices: {len(details.get('devices', []))}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```
