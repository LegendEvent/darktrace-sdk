# 🚀 Darktrace Python SDK

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/darktrace-sdk)
![GitHub License](https://img.shields.io/github/license/LegendEvent/darktrace-sdk)
![GitHub Repo stars](https://img.shields.io/github/stars/LegendEvent/darktrace-sdk?style=social)

> **A modern, fully-featured, and Pythonic SDK for the entire Darktrace Threat Visualizer API.**

---

## ✨ Features

- **100% API Coverage**: Every endpoint, every parameter, every action from the official Darktrace API Guide is implemented.
- **Modular & Maintainable**: Each endpoint group is a separate Python module/class.
- **Easy Authentication**: Secure HMAC-SHA1 signature generation and token management.
- **Async-Ready**: Designed for easy extension to async workflows.
- **Type Hints & Docstrings**: Full typing and documentation for all public methods.
- **Production-Ready**: Suitable for SIEM/SOC integration, automation, and research.

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
from darktrace import DarktraceClient, Devices, Antigena

# Initialize the client
client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access endpoint groups
devices = Devices(client)
all_devices = devices.get()

antigena = Antigena(client)
actions = antigena.get_actions()

print(all_devices)
print(actions)
```

---

## 🛡️ 100% Endpoint Coverage

This SDK covers **every endpoint** in the Darktrace API Guide, including:

- `/advancedsearch` (search, analyze, graph)
- `/aianalyst` (incidentevents, groups, acknowledge, pin, comments, stats, investigations, incidents)
- `/antigena` (actions, manual, summary)
- `/components`, `/cves`, `/details`, `/deviceinfo`, `/devices`, `/devicesearch`, `/devicesummary`
- `/endpointdetails`, `/enums`, `/filtertypes`, `/intelfeed`, `/mbcomments`, `/metricdata`, `/metrics`, `/models`, `/modelbreaches`, `/network`, `/pcaps`, `/similardevices`, `/status`, `/subnets`, `/summarystatistics`, `/tags`, and all `/agemail` endpoints

> **If you find a missing endpoint, open an issue or PR and it will be added!**

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