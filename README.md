
# 🚀 Darktrace Python SDK *(Work in Progress)*

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/darktrace-sdk)
![GitHub License](https://img.shields.io/github/license/LegendEvent/darktrace-sdk)
![GitHub Repo stars](https://img.shields.io/github/stars/LegendEvent/darktrace-sdk?style=social)


> **A modern, Pythonic SDK for the Darktrace Threat Visualizer API.**
> 
> **⚠️ Work in progress – not 100% production ready. Breaking changes and incomplete features may exist.**

---

## 🆕 Latest Updates (v1.0.5)

- **Critical Authentication Fix**: Fixed parameter order mismatch between signature calculation and request URLs
- **Consistent Parameter Ordering**: Ensured parameters are sorted alphabetically in both signature calculation and requests
- **Improved BaseEndpoint Class**: Updated to handle parameter sorting consistently across all API calls
- **Fixed AI Analyst Module**: Updated authentication handling in the analyst module
- **Enhanced Examples**: Added comprehensive examples for Intel Feed module

---


## ✨ Features

- **Extensive API Coverage**: Most endpoints, parameters, and actions from the official Darktrace API Guide are implemented.
- **Modular & Maintainable**: Each endpoint group is a separate Python module/class.
- **Easy Authentication**: Secure HMAC-SHA1 signature generation and token management.
- **Async-Ready**: Designed for easy extension to async workflows.
- **Type Hints & Docstrings**: Full typing and documentation for all public methods.
- **Comprehensive Documentation**: Detailed documentation for every module and endpoint.
- **⚠️ Not yet production ready**: Some features may be incomplete or subject to change.

---

## 📦 Installation

```bash
pip install darktrace-sdk
```

After installation, you'll import it in Python as `darktrace`:

```python
from darktrace import DarktraceClient
```

Or clone this repository:

```bash
git clone https://github.com/yourusername/darktrace.git
cd darktrace
pip install .
```

---

## 🚦 Quick Start

```python
from darktrace import DarktraceClient

# Initialize the client
client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access endpoint groups
devices = client.devices
all_devices = devices.get()

antigena = client.antigena
actions = antigena.get_actions()

print(all_devices)
print(actions)
```

---

## 📚 Documentation

Comprehensive documentation is available in the [docs](docs/) directory:

- [Main Documentation](docs/README.md) - Overview and getting started
- [Authentication](docs/modules/auth.md) - How authentication works
- [Antigena](docs/modules/antigena.md) - Managing Antigena actions
- [Devices](docs/modules/devices.md) - Working with device information
- [Model Breaches](docs/modules/breaches.md) - Handling model breach alerts
- [Status](docs/modules/status.md) - System status information

And [many more modules](docs/modules/) covering every aspect of the Darktrace API.

See the [EXAMPLES.md](EXAMPLES.md) file for additional usage examples.

---


## 🛡️ Endpoint Coverage

This SDK aims to cover **all endpoints** in the Darktrace API Guide, including:

- `/advancedsearch` (search, analyze, graph)
- `/aianalyst` (incidentevents, groups, acknowledge, pin, comments, stats, investigations, incidents)
- `/antigena` (actions, manual, summary)
- `/components`, `/cves`, `/details`, `/deviceinfo`, `/devices`, `/devicesearch`, `/devicesummary`
- `/endpointdetails`, `/enums`, `/filtertypes`, `/intelfeed`, `/mbcomments`, `/metricdata`, `/metrics`, `/models`, `/modelbreaches`, `/network`, `/pcaps`, `/similardevices`, `/status`, `/subnets`, `/summarystatistics`, `/tags`, and all `/agemail` endpoints


> **If you find a missing endpoint, open an issue or PR and it will be added!**
> 
> **⚠️ This SDK is a work in progress and not yet 100% production ready.**

---

## ⚠️ Known Issues

### Advanced Search POST Requests
POST requests to the Advanced Search API (`/advancedsearch/api/search`) are currently not working due to unresolved authentication signature calculation issues. The Darktrace API documentation specifies that POST parameters should be included in the signature calculation as query string parameters, but multiple implementation attempts following the official documentation have resulted in "API SIGNATURE ERROR" responses.

**Workaround**: Use GET requests for Advanced Search queries, which work correctly and support all the same functionality. The SDK automatically defaults to GET requests for the Advanced Search module.

**Status**: Tracked as [issue #1](https://github.com/LegendEvent/darktrace-sdk/issues/1). GET requests remain fully functional for all use cases.

### /devicesummary Endpoint Returns HTTP 500
The `/devicesummary` endpoint may return a `500 Internal Server Error` when accessed with API tokens, even though it works in the browser or with session/cookie authentication. This is a known limitation of the Darktrace API backend and not a bug in the SDK or your code.

**Workaround**: There is currently no programmatic workaround. If you require this endpoint, please contact Darktrace support or use browser-based access where possible.

**Status**: Tracked as [issue #37](https://github.com/LegendEvent/darktrace-sdk/issues/37). If you encounter this, please reference the issue for updates.

---

## 📝 Contributing

Contributions are welcome! Please:

1. Fork the repo and create your branch.
2. Write clear, tested code following PEP8 and clean code principles.
3. Add/Update docstrings and type hints.
4. Submit a pull request with a detailed description.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- Inspired by the official Darktrace API Guide
- Community contributions welcome!

---

> Made with ❤️ for the Darktrace community.