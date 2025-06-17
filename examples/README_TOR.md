# Tor Exit Nodes Example

This example demonstrates how to fetch Tor exit nodes from the Darktrace Intel Feed using the fixed authentication mechanism in the Darktrace SDK.

## Overview

The `tor_exit_nodes.py` script:

1. Connects to your Darktrace instance
2. Fetches Tor exit nodes from the Intel Feed
3. Formats the data into a consistent structure
4. Saves the results to a JSON file

This example specifically demonstrates the fixed authentication mechanism that properly handles query parameters in the API signature calculation.

## Usage

1. Update the script with your Darktrace instance and API credentials:

```python
host = "https://your-darktrace-instance"
public_token = "your-public-token"
private_token = "your-private-token"
```

2. Run the script:

```bash
python tor_exit_nodes.py
```

## Authentication Details

This example uses two query parameters:
- `source="Threat Intel::Tor::Exit Node"`
- `full_details=True`

The fixed authentication mechanism ensures that these parameters are:
1. Sorted alphabetically for the signature calculation
2. Used in the same sorted order in the actual request

This prevents API signature errors that were occurring in previous versions of the SDK.

## Output

The script will output:
- The number of Tor exit nodes found
- A sample of the first 5 nodes
- The total count of nodes

It also saves the complete results to a file named `tor_exit_nodes.json` with the following structure:

```json
{
  "total_nodes": 1234,
  "timestamp": "2023-07-01T12:34:56.789012+00:00",
  "nodes": [
    {
      "name": "1.2.3.4",
      "description": "Tor exit node",
      "expiry": "2023-12-31T23:59:59",
      "source": "Threat Intel::Tor::Exit Node"
    },
    ...
  ]
}
```

## Error Handling

If an error occurs, the script will display:
- The error message
- The HTTP status code (if available)
- The response text (if available)

This helps in diagnosing any issues with the API connection or authentication. 