# Changelog

All notable changes to the Darktrace SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed (verified against the official API guide and read-only against a live 7.0.42 instance)
- `MetricData.get(metrics=[...])` sent one comma-joined `metric=a,b` (the server returned unrelated data); it now sends `metric1=`, `metric2=`, ... as the guide specifies. `from_`/`to` are typed as `YYYY-MM-DD HH:MM:SS` strings, `interval` as seconds, and unpaired time parameters raise `ValueError`. The `devices` parameter (never in the guide, rejected by the server) is removed.
- `SimilarDevices.get(device_id=...)` used `/similardevices/<id>`, which the server answers with a non-JSON error; it now sends `?did=`.
- `Subnets.get(subnet_id=...)` now sends `sid=` instead of the non-existent `/subnets/<id>` path; `MBComments.get(comment_id=...)` (same dead path) raises `ValueError`.
- `MBComments.post` now posts to `/modelbreaches/<pbid>/comments` with `{"message": ...}`; `/mbcomments` is GET only in the guide.
- Boolean query parameters are sent as `true`/`false` (guide format) instead of `True`/`False`.
- `Antigena.activate_action` accepts the guide's optional `duration`; `Details.get(did=0)` is no longer rejected; `Tags.get_entities` requires `did` or `tag`; `Tags.post_tag_entities` sends device ids as strings; `IntelFeed.update(add_list=...)` also accepts a string.

## [0.10.1] - 2026-10-01

### Fixed
- `Analyst.acknowledge/unacknowledge/pin/unpin` and `Tags.post_entities` failed with `API SIGNATURE ERROR`: `_post_form` now signs exactly the url-encoded body it sends (#59, #60).
- GET parameters are signed as sent: list values as repeated keys, `None` dropped, UTF-8; `ModelBreaches.get` no longer collapses a `saasfilter` list (#63, #61).

### Documentation
- `Analyst.add_comment` is accepted but not stored on Threat Visualizer 7.x; use `breaches.add_comment` (#62).
- `saasfilter` is documented as the API guide specifies: a wildcard matched against `SaaS::[platform]` with a trailing `*` (e.g. `office365*`), repeatable as a list.

## [0.9.0] - 2026-02-27

### Added
- **Connection Pooling**: Added `requests.Session()` for improved performance with multiple requests (4x faster on reused connections)
- **Context Manager Support**: `DarktraceClient` now supports `with` statement for proper resource cleanup
  ```python
  with DarktraceClient(host, public_token, private_token) as client:
      client.devices.get()
  ```
- **Automatic Retry Logic**: Transient failures (5xx, 429, connection errors) are automatically retried
  - Max 3 retries with exponential backoff (3s, 6s, 12s between attempts)
  - Client errors (4xx) are NOT retried
- **SSRF Protection**: URL scheme validation blocks dangerous schemes (`file://`, `ftp://`, `data://`, `javascript://`)
  - Note: Private IPs are explicitly ALLOWED for enterprise baremetal deployments
- **Configurable Request Timeout**: Added `timeout` parameter to `DarktraceClient` (default: None, uses requests default)
- **Compilation Test**: Added `tests/test_compilation.py` for full SDK validation without network calls
- **Read-Only Test**: Added `tests/test_sdk_readonly.py` for comprehensive testing against real Darktrace instances
- **CHANGELOG.md**: This changelog file

### Changed
- **SSL Verification Default**: Changed from `False` to `True` for security (verify_ssl=True by default)
- **Error Handling in ModelBreaches**: Methods now re-raise exceptions instead of returning `{"error": str}` dicts
  - `add_comment()`, `acknowledge()`, `unacknowledge()` now properly propagate exceptions
- **IntelFeed Parameter**: Fixed `fulldetails` parameter name (was incorrectly documented as `full_details` in examples)
- **Cleaned Up Imports**: Removed unused `timedelta` import from `auth.py`
- **Translated Comments**: German comments translated to English
- **Documentation Updated**: Added v0.9.0 features to README.md and docs/README.md

### Fixed
- IntelFeed `get_with_details()` now correctly passes `fulldetails=True` to `get()`
- Examples and tests updated to use correct `fulldetails` parameter

### Security
- SSL certificate verification is now enabled by default
- URL scheme validation prevents SSRF attacks via non-HTTP schemes

### Removed
- Mocked test file `tests/test_devicesearch.py` (replaced by compilation + readonly tests)

---

## [0.8.55] - Previous Release

Initial stable release with 27 endpoint modules.
