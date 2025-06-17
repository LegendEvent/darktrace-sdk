# Threat Intelligence Integration Example

This example demonstrates how to integrate multiple Darktrace SDK modules to create a comprehensive threat intelligence workflow.

## Overview

The `threat_intelligence.py` script demonstrates a complete threat intelligence workflow:

1. Fetches threat intelligence from the Darktrace Intel Feed
2. Identifies devices potentially communicating with known threats
3. Retrieves model breaches related to those devices
4. Generates a comprehensive threat intelligence report

This example showcases the fixed authentication mechanism that properly handles multiple query parameters in the API signature calculation.

## Key Features Demonstrated

- **Intel Feed Module**: Using the fixed authentication with multiple query parameters (`source` and `full_details`)
- **Devices Module**: Retrieving device information
- **Model Breaches Module**: Fetching breaches with time-based filtering and device filtering
- **Multiple Parameter Handling**: Proper parameter ordering in API requests
- **Error Handling**: Proper HTTP error handling with response details
- **Report Generation**: Creating structured JSON output

## Usage

1. Update the script with your Darktrace instance and API credentials:

```python
DARKTRACE_HOST = "https://your-darktrace-instance"
PUBLIC_TOKEN = "your-public-token"
PRIVATE_TOKEN = "your-private-token"
```

2. Configure the threat intelligence source and time period:

```python
THREAT_INTEL_SOURCE = "Threat Intel::Tor::Exit Node"  # Change as needed
DAYS_TO_CHECK = 7  # Number of days to look back for model breaches
```

3. Run the script:

```bash
python threat_intelligence.py
```

## Authentication Details

This example uses multiple query parameters in different API calls:

1. Intel Feed module:
   - `source="Threat Intel::Tor::Exit Node"`
   - `full_details=True`

2. Model Breaches module:
   - `from_time=<timestamp>`
   - `devices=<comma-separated-device-ids>`

The fixed authentication mechanism ensures that these parameters are:
1. Sorted alphabetically for the signature calculation
2. Used in the same sorted order in the actual request

## Output

The script generates a JSON report with the following structure:

```json
{
  "timestamp": "2023-07-01T12:34:56.789012+00:00",
  "summary": {
    "threats_count": 123,
    "affected_devices_count": 5,
    "model_breaches_count": 42
  },
  "threats": [
    {
      "name": "1.2.3.4",
      "description": "Tor exit node",
      "expiry": "2023-12-31T23:59:59",
      "source": "Threat Intel::Tor::Exit Node"
    },
    ...
  ],
  "affected_devices": [
    {
      "did": 12345,
      "hostname": "workstation01",
      "ip": "192.168.1.100"
    },
    ...
  ],
  "model_breaches": [
    {
      "pid": "abcdef123456",
      "time": 1688213696000,
      "model": "Device / Unusual External Connections",
      "score": 0.85,
      "device": "workstation01"
    },
    ...
  ]
}
```

The report is saved to a file named `threat_intelligence_report.json` in the current directory. 