# Darktrace SDK Examples

This document provides examples of how to use the Darktrace SDK.

## Installation

The Darktrace SDK can be installed from PyPI:

```bash
pip install darktrace-sdk
```

After installation, you'll import it in Python as `darktrace`:

```python
from darktrace import DarktraceClient
```

## Running the Example Script

The `example.py` script demonstrates basic functionality of the SDK. Before running it, you'll need to:

1. Edit the example script to include your actual Darktrace instance URL and API tokens.
2. Make sure you have the Darktrace SDK installed.

```bash
# Edit the example script
nano example.py  # or use any text editor

# Run the example
python example.py
```

## Running the Test Script

The `test_darktrace_sdk.py` script is a more comprehensive test script that can be used to verify your connection and check multiple endpoints.

```bash
python test_darktrace_sdk.py --host https://your-darktrace-instance --public-token YOUR_PUBLIC_TOKEN --private-token YOUR_PRIVATE_TOKEN
```

Add `--debug` for verbose output:

```bash
python test_darktrace_sdk.py --host https://your-darktrace-instance --public-token YOUR_PUBLIC_TOKEN --private-token YOUR_PRIVATE_TOKEN --debug
```

## Specialized Examples

The `examples` directory contains specialized examples for specific use cases:

- `tor_exit_nodes.py` - Demonstrates how to fetch Tor exit nodes from the Intel Feed
- `threat_intelligence.py` - Shows how to use multiple modules together for threat intelligence integration
- `intelfeed_example.py` - Comprehensive example of using the Intel Feed module

Each example includes detailed comments explaining the code and can be run directly after updating the credentials.

## Common Issues

1. **Import Error**: If you get an import error like `ModuleNotFoundError: No module named 'darktrace'`, check that you've installed the package using `pip install darktrace-sdk`.

2. **Authentication Errors**: Make sure your API tokens are correct and that your user account has API access enabled in Darktrace.

3. **SSL Verification**: The SDK disables SSL verification by default for testing. In production, you should properly handle SSL certificates.

## Next Steps

For more advanced usage, you can refer to the modules in the SDK that correspond to different Darktrace API endpoints:

- `client.antigena` - Antigena actions and settings
- `client.analyst` - AI Analyst incidents and events
- `client.breaches` - Model breach alerts
- `client.devices` - Device information and management
- `client.email` - Darktrace/Email endpoints
- `client.intelfeed` - Intel Feed for threat intelligence integration

Each module has methods corresponding to the available API endpoints, with docstrings explaining the parameters. 

## Intel Feed Examples

The Intel Feed module allows you to work with threat intelligence data in Darktrace:

```python
# Get all available sources
sources = client.intelfeed.get_sources()

# Get entries from a specific source
entries = client.intelfeed.get(source="Threat Intel::Tor::Exit Node")

# Get detailed information about entries
detailed_entries = client.intelfeed.get(source="Threat Intel::Tor::Exit Node", full_details=True)

# Add entries to the Intel Feed
client.intelfeed.update(
    add_entry="malicious-domain.com",
    description="Known malicious domain",
    source="Custom Threat Feed"
)
```

For more detailed examples, see the `examples/intelfeed_example.py` and `examples/tor_exit_nodes.py` files. 