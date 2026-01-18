# Tests Directory

This directory contains test suites for the Darktrace SDK.

## Structure

```
tests/
├── fixtures/              # Mock API response fixtures for unit tests
│   ├── devicesearch_multi_param_response.json
│   ├── devicesearch_single_param_type_response.json
│   ├── devicesearch_single_param_mac_response.json
│   └── devicesearch_empty_response.json
├── real/                 # Real-environment tests (skipped by default)
│   └── test_devicesearch_real.py
└── test_devicesearch.py  # Mocked unit tests for DeviceSearch
```

## Test Types

### Mocked Unit Tests (`test_*.py`)
- Use mocked API responses from `fixtures/`
- Run without requiring a live Darktrace instance
- Fast, reliable, and isolated
- **Run with**: `pytest tests/test_*.py`

### Real Environment Tests (`real/test_*.py`)
- Require live Darktrace instance with valid credentials
- Skipped by default using `@pytest.mark.skip`
- Only run on work machines with API access
- **Run with**:
  ```bash
  pytest tests/real/test_devicesearch_real.py \
      --host=https://your-instance.darktrace.com \
      --public-token=YOUR_PUBLIC_TOKEN \
      --private-token=YOUR_PRIVATE_TOKEN
  ```

## Running Tests

### All Mocked Tests
```bash
pytest tests/
```

### Specific Test File
```bash
pytest tests/test_devicesearch.py -v
```

### Real Environment Tests
```bash
pytest tests/real/test_devicesearch_real.py \
    --host=... --public-token=... --private-token=...
```

### Existing Integration Tests (Root Directory)
The root `test_darktrace_sdk.py` file contains integration tests that require
a live Darktrace instance. These tests are separate from the new mocked tests.

## Issue #45 Fix

The mocked tests in `test_devicesearch.py` specifically test the fix for Issue #45:
- Multi-parameter search now uses space-separated criteria (PDF spec compliant)
- Previously used explicit ` AND ` operator which caused 0 results
- All 17 tests validate various search scenarios

## Adding New Tests

1. Create fixture JSON in `fixtures/` matching PDF response structure
2. Add test in appropriate `test_*.py` file
3. For real environment tests, add to `real/` directory with `@pytest.mark.skip`
4. Update this README with new test descriptions
