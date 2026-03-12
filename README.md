# 🚀 Darktrace Python SDK

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/darktrace-sdk)
![GitHub License](https://img.shields.io/github/license/LegendEvent/darktrace-sdk)
![GitHub Repo stars](https://img.shields.io/github/stars/LegendEvent/darktrace-sdk?style=social)

> **A modern, Pythonic SDK for the Darktrace Threat Visualizer API.**

---

## 🆕 Latest Updates (v0.9.0)

### New Features
- **Connection Pooling**: Automatic HTTP connection pooling via `requests.Session()` for 4x faster requests on reused connections
- **Context Manager Support**: Use `with DarktraceClient(...) as client:` for proper resource cleanup
- **Automatic Retry Logic**: Transient failures (5xx, 429, connection errors) are automatically retried (3 retries with exponential backoff: 3s, 6s, 12s)
- **SSRF Protection**: URL scheme validation blocks dangerous schemes (`file://`, `ftp://`, `data://`, `javascript://`)
- **Configurable Timeout**: New `timeout` parameter on `DarktraceClient`

### Improvements
- **Error Handling**: `ModelBreaches` methods now properly re-raise exceptions instead of returning error dicts
- **SSL Verification**: Enabled by default for security (verify_ssl=True)

### Bug Fixes
- Fixed IntelFeed `fulldetails` parameter name in examples

> For previous updates, see [GitHub Releases](https://github.com/LegendEvent/darktrace-sdk/releases) or [CHANGELOG.md](CHANGELOG.md).

---


## ✨ Features

- **Extensive API Coverage**: Most endpoints, parameters, and actions from the official Darktrace API Guide are implemented.
- **Modular & Maintainable**: Each endpoint group is a separate Python module/class.
- **Easy Authentication**: Secure HMAC-SHA1 signature generation and token management.
- **SSL Verification**: SSL certificate verification is enabled by default for secure connections.
- **Async-Ready**: Designed for easy extension to async workflows.
- **Type Hints & Docstrings**: Full typing and documentation for all public methods.
- **Comprehensive Documentation**: Detailed documentation for every module and endpoint.

---

## 🔒 SSL Certificate Verification

**SSL verification is enabled by default (`verify_ssl=True`)** for secure connections to your Darktrace instance.

For development or testing environments with self-signed certificates, you can disable verification:

```python
client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN",
    verify_ssl=False  # Only for development/testing
)
```

> ⚠️ **Warning**: Disabling SSL verification exposes your connection to man-in-the-middle attacks. Never disable in production environments.

### Using Self-Signed Certificates with verify_ssl=True

For production environments with self-signed certificates, add the certificate to your system trust store instead of disabling verification:

```bash
# 1. Get the certificate from your Darktrace instance
openssl s_client -showcerts -connect your-darktrace-instance:443 </dev/null 2>/dev/null | openssl x509 -outform PEM > ~/darktrace-cert.pem

# 2. Copy to system CA store (Linux/Ubuntu/Debian)
sudo cp ~/darktrace-cert.pem /usr/local/share/ca-certificates/darktrace-cert.crt
sudo update-ca-certificates

# 3. Now verify_ssl=True will work
```

**Alternative (no sudo required):**
```bash
# Create a custom CA bundle and set environment variable
cat /etc/ssl/certs/ca-certificates.crt ~/darktrace-cert.pem > ~/.custom-ca-bundle.pem
export REQUESTS_CA_BUNDLE=~/.custom-ca-bundle.pem
```

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

# Initialize the client (SSL verification enabled by default)
client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# For development with self-signed certificates, disable SSL verification:
# client = DarktraceClient(
#     host="https://your-darktrace-instance",
#     public_token="YOUR_PUBLIC_TOKEN",
#     private_token="YOUR_PRIVATE_TOKEN",
#     verify_ssl=False  # Not recommended for production
# )

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
The `/devicesummary` endpoint returns a `500 Internal Server Error` when accessed with API tokens, even though it works in the browser or with session/cookie authentication. This is a known limitation of the Darktrace API backend and not a bug in the SDK or your code.

**Status**: Confirmed as Darktrace API backend limitation (tested with SDK v0.8.54 on instance v6.3.18). The SDK implementation is correct and uses the same authentication pattern as other endpoints that work with API tokens.

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
