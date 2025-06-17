# Darktrace SDK Documentation

This documentation provides detailed information about each module in the Darktrace SDK and how to use them.

## Getting Started

```python
from darktrace import DarktraceClient

# Initialize the client
client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN",
    debug=False  # Set to True for verbose output
)
```

## Available Modules

The Darktrace SDK provides access to all Darktrace API endpoints through the following modules:

1. [Advanced Search](modules/advanced_search.md) - Complex search operations across the Darktrace platform
2. [AI Analyst](modules/analyst.md) - AI Analyst incidents and investigations
3. [Antigena](modules/antigena.md) - Antigena actions and configurations
4. [Model Breaches](modules/breaches.md) - Model breach alerts and information
5. [Components](modules/components.md) - Darktrace component information
6. [CVEs](modules/cves.md) - CVE information related to devices
7. [Details](modules/details.md) - Detailed information about specific entities
8. [Device Info](modules/deviceinfo.md) - Detailed device information
9. [Devices](modules/devices.md) - Device management and information
10. [Device Search](modules/devicesearch.md) - Search for devices with specific criteria
11. [Device Summary](modules/devicesummary.md) - Summarized device information
12. [Email](modules/email.md) - Darktrace Email security features
13. [Endpoint Details](modules/endpointdetails.md) - Endpoint-specific information
14. [Enums](modules/enums.md) - Enumeration values used in the Darktrace platform
15. [Filter Types](modules/filtertypes.md) - Available filter types for searches
16. [Intel Feed](modules/intelfeed.md) - Threat intelligence feed information
17. [Model Breach Comments](modules/mbcomments.md) - Comments on model breaches
18. [Metric Data](modules/metricdata.md) - Time-series metric data
19. [Metrics](modules/metrics.md) - Available metrics and their information
20. [Models](modules/models.md) - Darktrace models and their configurations
21. [Network](modules/network.md) - Network information and statistics
22. [PCAPs](modules/pcaps.md) - Packet capture functionality
23. [Similar Devices](modules/similardevices.md) - Find devices similar to a given device
24. [Status](modules/status.md) - System status information
25. [Subnets](modules/subnets.md) - Subnet information and management
26. [Summary Statistics](modules/summarystatistics.md) - Overall system statistics
27. [Tags](modules/tags.md) - Tag management for devices and entities

## Authentication

The SDK handles authentication automatically using the provided public and private tokens. See [Authentication](modules/auth.md) for more details.

## Error Handling

```python
try:
    devices = client.devices.get()
except Exception as e:
    print(f"Error: {e}")
```

## Debugging

Enable debug mode to see detailed API requests and responses:

```python
client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN",
    debug=True  # Enable debug output
)
``` 