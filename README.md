
# 🚀 Darktrace Python SDK

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/darktrace-sdk)
![GitHub License](https://img.shields.io/github/license/LegendEvent/darktrace-sdk)
![GitHub Repo stars](https://img.shields.io/github/stars/LegendEvent/darktrace-sdk?style=social)


> **A modern, Pythonic SDK for the Darktrace Threat Visualizer API.**


---


## 🆕 Latest Updates (v0.8.52)

- **Batch operations for breaches**: `acknowledge`, `unacknowledge`, and `get_comments` now support lists of IDs and return aggregated results.
- **Helper methods for DeviceSearch**: Added `get_tag`, `get_type`, `get_label`, `get_vendor`, `get_hostname`, `get_ip`, and `get_mac` for easier device filtering.
- **Direct filter parameters for DeviceSearch**: The `get` method now accepts direct parameters like `tag`, `type`, `hostname`, etc., and auto-builds the query if no explicit query is given.
- **Improved error handling**: A runtime error is raised if both `query` and filter parameters are set. A Sphinx warning is included in the docstring for better IDE/documentation feedback.
- **Best practices**: SDK methods return Python objects, not JSON strings.
- **Bugfixes**: Improved JSON compatibility and response formats.

---


## ✨ Features

- **Extensive API Coverage**: Most endpoints, parameters, and actions from the official Darktrace API Guide are implemented.
- **Modular & Maintainable**: Each endpoint group is a separate Python module/class.
- **Easy Authentication**: Secure HMAC-SHA1 signature generation and token management.
- **Async-Ready**: Designed for easy extension to async workflows.
- **Type Hints & Docstrings**: Full typing and documentation for all public methods.
- **Comprehensive Documentation**: Detailed documentation for every module and endpoint.

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

# Use Advanced Search with POST requests (Darktrace 6.1+)
advanced_search = client.advanced_search
query = {
    "search": "@type:\"ssl\" AND @fields.dest_port:\"443\"",
    "fields": [],
    "offset": 0,
    "timeframe": "3600"  # 1 hour
}
results = advanced_search.search(query=query, post_request=True)

print(all_devices)
print(actions)
print(results)
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

---

## ⚠️ Known Issues

### /devicesummary Endpoint Returns HTTP 500
The `/devicesummary` endpoint may return a `500 Internal Server Error` when accessed with API tokens, even though it works in the browser or with session/cookie authentication. This is a known limitation of the Darktrace API backend and not a bug in the SDK or your code.

**Workaround**: There is currently no programmatic workaround. If you require this endpoint, please contact Darktrace support or use browser-based access where possible.

**Status**: Tracked as [issue #37](https://github.com/LegendEvent/darktrace-sdk/issues/37). If you encounter this, please reference the issue for updates.

---

## 📝 Contributing

Contributions are welcome! Please:

1. Fork the repo and create your branch.
2. Write clear, tested code and clean code principles.
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
