# Darktrace SDK Examples

This directory contains example scripts demonstrating how to use various features of the Darktrace SDK.

## Intel Feed Module Fix

### Issue

The Intel Feed module was encountering a `400 Bad Request` error when using the `sources=true` parameter. This was due to two issues:

1. Incorrect parameter handling in the module
2. Query parameters were not included in the API signature calculation

The error message was:
```
Error accessing API: 400 Client Error: Bad request for URL: https://instance/intelfeed?sources=true
```

### Fix

The issue was fixed by:

1. Properly handling the `sources` parameter in the Intel Feed module:
   - Added explicit parameters for `sources`, `source`, and `full_details` in the `get()` method
   - Fixed parameter handling to convert boolean values to lowercase strings (`'true'` or `'false'`)
   - Added convenience methods for common operations

2. Fixing the authentication mechanism to include query parameters in the signature calculation:
   - Updated the `DarktraceAuth` class to accept query parameters and include them in the signature
   - Created a `BaseEndpoint` class that all endpoint modules inherit from
   - Updated all endpoint modules to use the new authentication method

### Authentication Details

The Darktrace API requires that query parameters be included in the signature calculation. The correct signature format is:

```
message = f"{endpoint}?{sorted_query_params}\n{public_token}\n{date}"
```

For example, with the endpoint `/intelfeed` and the parameter `sources=true`, the signature should be calculated using:

```
message = "/intelfeed?sources=true\npublic_token\ndate"
```

### Usage

To use the fixed Intel Feed module:

```python
from darktrace import DarktraceClient

# Initialize client
client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Get sources
sources = client.intelfeed.get_sources()

# Get entries for a specific source
source_entries = client.intelfeed.get_by_source("SourceName")

# Get all entries with full details
detailed_entries = client.intelfeed.get_with_details()
```

See the `intelfeed_example.py` script for a complete example. 