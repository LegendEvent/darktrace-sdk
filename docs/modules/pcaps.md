# PCAPs Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.

The PCAPs module lets you list existing packet captures, request the creation of new ones, and download finished PCAP files.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the pcaps module
pcaps = client.pcaps
```

## Methods Overview

- **`get()`** - List PCAPs (`GET /pcaps`) or download one PCAP file (`GET /pcaps/<filename>`)
- **`create()`** - Request a new PCAP (`POST /pcaps`)

Permissions: `create()` needs the *Create PCAPs* permission; downloading a file needs *Create PCAPs* and *Download PCAPs*.

## Methods

### Get PCAPs

```python
# List all PCAPs and their status
pcap_list = pcaps.get()

# Download a finished PCAP (returns bytes)
data = pcaps.get(pcap_id="DCIP_20210330063306_20210330063307_10_36_39_131_35860_10_2_3_4_53_udp_Lx5blz.pcap")
with open("capture.pcap", "wb") as f:
    f.write(data)
```

#### Parameters

- `pcap_id` (str, optional): Filename of the PCAP to download. If omitted, the list of PCAPs is returned.
- `responsedata` (str, optional): Sent as the `responsedata` query parameter. The API guide does not document this parameter for `/pcaps`, so its effect is unverified.
- `timeout` (float | tuple, optional): Per-request timeout override.

#### Return value

- Without `pcap_id`: a **list** of PCAP objects (parsed JSON).
- With `pcap_id`: the raw **binary** PCAP content (`bytes`).

**Filename prefix:** the list returns `filename` with a `/tm` prefix (for example `/tm/DCIP_....pcap`). Omit that prefix when requesting the file, i.e. pass only `DCIP_....pcap` as `pcap_id`. The SDK also strips a leading `/tm/` for you.

A file can only be retrieved once its `state` is `"finished"`.

#### Response Structure (list)

Each item (the guide marks the response as abbreviated):

```python
[
  {
    "tmqid": 98,
    "startTime": 1605262128,
    "endTime": 1605262137,
    "filename": "/tm/DCIP_20201112220038_20201112220039_10_0_18_224_3379_192_168_72_4_53_udp_Kjktpo_m.pcap",
    "index": "connection4",
    "l3proto": "udp",
    "ip1": "10.0.18.224",
    "port1": 3379,
    "ip2": "192.168.72.4",
    "port2": 53,
    "start": 1605218438,
    "end": 1605218439,
    "state": "finished"
  }
]
```

| Field | Description |
|-------|-------------|
| `tmqid` | Unique tm query ID of the capture |
| `startTime` / `endTime` | Epoch time at which generation of the PCAP began / completed |
| `filename` | Filename used to retrieve the PCAP (strip the `/tm` prefix) |
| `index` | System field |
| `l3proto` | Layer 3 protocol, if specified at creation |
| `ip1` | Source IP of the connections in the capture |
| `port1` | Source port, if specified at creation |
| `ip2` / `port2` | Destination IP / port, if specified at creation |
| `start` / `end` | Start / end time of the packet capture (epoch seconds) |
| `state` | Current status of the request, e.g. `pending`, `finished` |

### Create PCAP

```python
# Source IP only
req = pcaps.create(ip1="10.36.39.131", start=1605222041, end=1605222281)

# Source and destination IP
req = pcaps.create(ip1="10.2.3.4", ip2="8.8.8.8", start=1598258905, end=1598258910)

# With protocol (requires ip2 AND port2)
req = pcaps.create(
    ip1="10.0.18.224", ip2="8.8.8.8", port2=53,
    start=1598258905, end=1598258910, protocol="udp"
)

# Fully specified
req = pcaps.create(
    ip1="10.2.3.4", port1=43723, ip2="8.8.8.8", port2=53,
    start=1598258905, end=1598258910, protocol="udp"
)
```

#### Parameters

- `ip1` (str, **required**): The source IP
- `start` (int, **required**): Start time of the capture, epoch seconds
- `end` (int, **required**): End time of the capture, epoch seconds
- `ip2` (str, optional): The destination IP
- `port1` (int, optional): The specific port for the source IP
- `port2` (int, optional): The specific port for the destination IP
- `protocol` (str, optional): Layer 3 protocol, `"tcp"` or `"udp"`
- `timeout` (float | tuple, optional): Per-request timeout override

The request is sent as a JSON body (query parameters are not supported by the endpoint).

Rules from the API guide:

- The maximum timeframe for PCAP creation is **30 minutes** (`end - start`).
- To use `protocol`, both `ip2` and `port2` must be specified.
- The guide lists four valid body formats: `ip1` + times; `ip1` + `ip2` + times; `ip1` + `ip2` + `port2` + times + `protocol`; and `ip1` + `port1` + `ip2` + `port2` + times + `protocol`.

The SDK does not validate these rules client-side; the Darktrace API rejects invalid requests.

#### Response Structure

`create()` returns the parsed JSON describing the creation request:

```python
{
  "tmqid": 101,
  "startTime": 1605262345,
  "filename": "DCIP_20200824084825_20200824084830_10_2_3_4_8_8_8_8_80_tcp_loBSz0_m.pcap",
  "index": "connection3",
  "l3proto": "tcp",
  "ip1": "10.2.3.4",
  "ip2": "8.8.8.8",
  "port2": 80,
  "start": 1598258905,
  "end": 1598258910,
  "state": "pending"
}
```

## Examples

### Create a PCAP, wait for it, and download it

```python
import time
from datetime import datetime

end_time = int(datetime.now().timestamp())
start_time = end_time - 15 * 60          # must be <= 30 minutes

req = client.pcaps.create(ip1="10.0.18.224", ip2="8.8.8.8", port2=53,
                          start=start_time, end=end_time, protocol="udp")
name = req["filename"]                   # no /tm prefix in the create response

# Poll the list until the capture is finished
for _ in range(30):
    for p in client.pcaps.get():
        # listed filenames carry a /tm prefix
        if p["filename"].removeprefix("/tm/") == name and p["state"] == "finished":
            data = client.pcaps.get(pcap_id=name)
            with open(name, "wb") as f:
                f.write(data)
            raise SystemExit(f"saved {name}")
    time.sleep(10)
```

### Find existing PCAPs for an IP

```python
finished = [
    p for p in client.pcaps.get()
    if p["state"] == "finished" and "10.0.18.224" in (p["ip1"], p.get("ip2"))
]
for p in finished:
    print(p["filename"], p["start"], p["end"], p.get("l3proto"))
```

## Error Handling

```python
from darktrace.exceptions import DarktraceError  # base exception of the SDK

try:
    pcap_list = client.pcaps.get()
    req = client.pcaps.create(ip1="10.2.3.4", ip2="8.8.8.8", port2=80,
                              start=1598258905, end=1598258910, protocol="tcp")
except DarktraceError as e:
    print(f"API error: {e}")
```

## Notes

- `GET /pcaps` returns a list; use list iteration, not `.get(...)` on the result.
- Downloads return binary data directly; write it to a file in `"wb"` mode.
- Required permissions are listed under Methods Overview.
