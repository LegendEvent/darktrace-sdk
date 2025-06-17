# Intel Feed Module

The Intel Feed module provides access to the Darktrace Watched Domains feature, allowing you to retrieve and manage domains, IPs, and hostnames used by Darktrace for threat intelligence.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the intelfeed module
intelfeed = client.intelfeed
```

## Methods

### Get Intel Feed

Retrieve watched domains information from the Darktrace platform.

```python
# Get all watched domains
all_domains = intelfeed.get()

# Get list of sources
sources = intelfeed.get_sources()

# Get watched domains from a specific source
source_domains = intelfeed.get_by_source("CustomSource")

# Get full details about watched domains
detailed_domains = intelfeed.get_with_details()
```

#### Parameters

- `feed_type` (str, optional): Optional feed type to filter by
- `response_data` (str, optional): Optional response data format
- `sources` (bool, optional): If True, returns the current set of sources rather than the list of watched entries
- `source` (str, optional): Optional source name to filter entries by
- `full_details` (bool, optional): If True, returns full details about expiry time and description for each entry

#### Response

For a basic request, the response is an array of domains:

```json
[
  "example1.com",
  "example2.com",
  "0.0.0.0"
]
```

With `full_details=True`, the response includes additional information:

```json
[
  {
    "name": "example1.com",
    "description": "Test"
  },
  {
    "name": "example2.com",
    "description": "Test"
  },
  {
    "name": "example3.com",
    "description": "Test",
    "strength": "100",
    "iagn": true,
    "expiry": "2020-04-03 15:23:20"
  }
]
```

### Update Intel Feed

Update the watched domains in Darktrace by adding or removing entries.

```python
# Add a single domain
intelfeed.update(add_entry="example.com", description="Test domain", source="test")

# Add multiple domains
intelfeed.update(
    add_list=["example1.com", "example2.com", "example3.com"],
    description="Test domains",
    source="ThreatIntel"
)

# Remove a domain
intelfeed.update(remove_entry="example.com", source="test")

# Remove all domains
intelfeed.update(remove_all=True)
```

#### Parameters

- `add_entry` (str, optional): Single entry to add (domain, hostname or IP address)
- `add_list` (List[str], optional): List of entries to add (domains, hostnames or IP addresses)
- `description` (str, optional): Description for added entries (must be under 256 characters)
- `source` (str, optional): Source for added entries (must be under 64 characters)
- `expiry` (str, optional): Expiration time for added items
- `is_hostname` (bool, optional): If True, treat added items as hostnames rather than domains
- `remove_entry` (str, optional): Entry to remove (domain, hostname or IP address)
- `remove_all` (bool, optional): If True, remove all entries
- `enable_antigena` (bool, optional): If True, enable automatic Antigena Network actions

## Examples

### Get All Watched Domains

```python
domains = client.intelfeed.get()
for domain in domains:
    print(f"Domain: {domain}")
```

### Get Sources

```python
sources = client.intelfeed.get_sources()
print(f"Available sources: {sources}")
```

### Get Domains from a Specific Source

```python
source_domains = client.intelfeed.get_by_source("ThreatIntel")
print(f"Domains from ThreatIntel source: {source_domains}")
```

### Get Full Details

```python
detailed_domains = client.intelfeed.get_with_details()
for domain in detailed_domains:
    print(f"Domain: {domain['name']}")
    if 'description' in domain:
        print(f"  Description: {domain['description']}")
    if 'expiry' in domain:
        print(f"  Expires: {domain['expiry']}")
```

### Add Domains

```python
# Add a single domain
client.intelfeed.update(
    add_entry="malicious-site.com",
    description="Known malicious site",
    source="CustomThreatFeed"
)

# Add multiple domains
client.intelfeed.update(
    add_list=["threat1.com", "threat2.com", "threat3.com"],
    description="Threat intelligence feed",
    source="ExternalThreatFeed",
    expiry="2023-12-31T23:59:59"
)
```

## Error Handling

```python
try:
    domains = client.intelfeed.get()
    # Process the domains
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
