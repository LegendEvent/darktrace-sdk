# Changelog

All notable changes to the Darktrace SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.0] - 2026-02-27

### Added
- **Connection Pooling**: Added `requests.Session()` for improved performance with multiple requests (4x faster on reused connections)
- **Context Manager Support**: `DarktraceClient` now supports `with` statement for proper resource cleanup
  ```python
  with DarktraceClient(host, public_token, private_token) as client:
      client.devices.get()
  ```
- **Automatic Retry Logic**: Transient failures (5xx, 429, connection errors) are automatically retried
  - Max 3 retries with 10 second wait between attempts
  - Client errors (4xx) are NOT retried
- **SSRF Protection**: URL scheme validation blocks dangerous schemes (`file://`, `ftp://`, `data://`, `javascript://`)
  - Note: Private IPs are explicitly ALLOWED for enterprise baremetal deployments
- **`_safe_json()` Helper**: Added to `BaseEndpoint` for JSON parsing with proper error handling
- **Configurable Request Timeout**: Added `timeout` parameter to `DarktraceClient` (default: None, uses requests default)
- **Compilation Test**: Added `tests/test_compilation.py` for full SDK validation without network calls

### Changed
- **SSL Verification Default**: Changed from `False` to `True` for security (verify_ssl=True by default)
- **Error Handling in ModelBreaches**: Methods now re-raise exceptions instead of returning `{"error": str}` dicts
  - `add_comment()`, `acknowledge()`, `unacknowledge()` now properly propagate exceptions
- **IntelFeed Parameter**: Fixed `fulldetails` parameter name (was incorrectly documented as `full_details` in examples)
- **Cleaned Up Imports**: Removed unused `timedelta` import from `auth.py`
- **Translated Comments**: German comments translated to English

### Fixed
- IntelFeed `get_with_details()` now correctly passes `fulldetails=True` to `get()`
- Examples and tests updated to use correct `fulldetails` parameter

### Security
- SSL certificate verification is now enabled by default
- URL scheme validation prevents SSRF attacks via non-HTTP schemes

### Removed
- Empty placeholder test file `tests/real/test_devicesearch_real.py`

---

## [0.8.55] - Previous Release

Initial stable release with 28 endpoint modules.
