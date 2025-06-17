# Cves Module

The Cves module provides access to CVE information related to devices.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the cves module
cves = client.cves
```

## Methods

### Get Cves

Retrieve cVE information related to devices from the Darktrace platform.

```python
# Get all cves
all_cves = cves.get()

# Get a specific number of cves
recent_cves = cves.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "cves": [
    {
      // Cves data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Cvess

```python
cves_data = client.cves.get()
for item in cves_data.get("cves", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    cves_data = client.cves.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
