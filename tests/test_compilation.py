#!/usr/bin/env python3
"""
Compilation test for the Darktrace SDK.

This test verifies that ALL SDK modules import correctly and have the expected structure.
No network calls are made - this is purely a static validation test.

Run: pytest tests/test_compilation.py -v
"""

import pytest
import sys
import importlib
from typing import List, Tuple


class TestSDKCompilation:
    """Test that all SDK modules compile and import correctly."""

    def test_version_module(self):
        """Test _version module exists and has __version__."""
        from darktrace._version import __version__

        assert isinstance(__version__, str)
        assert len(__version__) > 0
        # Should be semantic version format
        parts = __version__.split(".")
        assert len(parts) >= 2, (
            f"Version should have at least major.minor: {__version__}"
        )

    def test_auth_module(self):
        """Test auth module imports and has DarktraceAuth class."""
        from darktrace.auth import DarktraceAuth

        assert DarktraceAuth is not None

    def test_utils_module(self):
        """Test dt_utils module has required components."""
        from darktrace.dt_utils import (
            BaseEndpoint,
            debug_print,
            encode_query,
            TimeoutType,
            _UNSET,
            _MAX_RETRIES,
            _INITIAL_RETRY_WAIT_SECONDS,
            _RETRY_STATUS_CODES,
        )

        assert BaseEndpoint is not None
        assert _MAX_RETRIES == 3
        assert _INITIAL_RETRY_WAIT_SECONDS == 3

    def test_client_module(self):
        """Test client module has DarktraceClient with all endpoints."""
        from darktrace.client import DarktraceClient

        # Check class exists
        assert DarktraceClient is not None

        # Check it has context manager support
        assert hasattr(DarktraceClient, "__enter__")
        assert hasattr(DarktraceClient, "__exit__")
        assert hasattr(DarktraceClient, "close")

    def test_all_endpoint_modules_import(self):
        """Test that all 27 endpoint modules can be imported."""
        endpoint_modules = [
            "darktrace.dt_advanced_search",
            "darktrace.dt_analyst",
            "darktrace.dt_antigena",
            "darktrace.dt_breaches",
            "darktrace.dt_components",
            "darktrace.dt_cves",
            "darktrace.dt_details",
            "darktrace.dt_devices",
            "darktrace.dt_deviceinfo",
            "darktrace.dt_devicesearch",
            "darktrace.dt_devicesummary",
            "darktrace.dt_email",
            "darktrace.dt_endpointdetails",
            "darktrace.dt_enums",
            "darktrace.dt_filtertypes",
            "darktrace.dt_intelfeed",
            "darktrace.dt_mbcomments",
            "darktrace.dt_metricdata",
            "darktrace.dt_metrics",
            "darktrace.dt_models",
            "darktrace.dt_network",
            "darktrace.dt_pcaps",
            "darktrace.dt_similardevices",
            "darktrace.dt_status",
            "darktrace.dt_subnets",
            "darktrace.dt_summarystatistics",
            "darktrace.dt_tags",
        ]

        failed = []
        for module_name in endpoint_modules:
            try:
                importlib.import_module(module_name)
            except Exception as e:
                failed.append((module_name, str(e)))

        assert len(failed) == 0, f"Failed to import modules: {failed}"

    def test_all_endpoint_classes_in_client(self):
        """Test that DarktraceClient has all 27 endpoint attributes."""
        from darktrace import DarktraceClient

        # Create a client (no actual connection)
        client = DarktraceClient(
            host="https://test.example.com",
            public_token="test_public",
            private_token="test_private",
        )

        expected_endpoints = [
            "advanced_search",
            "analyst",
            "antigena",
            "breaches",  # ModelBreaches
            "components",
            "cves",
            "details",
            "devices",
            "deviceinfo",
            "devicesearch",
            "devicesummary",
            "email",
            "endpointdetails",
            "enums",
            "filtertypes",
            "intelfeed",
            "mbcomments",
            "metricdata",
            "metrics",
            "models",
            "network",
            "pcaps",
            "similardevices",
            "status",
            "subnets",
            "summarystatistics",
            "tags",
        ]

        missing = []
        for endpoint in expected_endpoints:
            if not hasattr(client, endpoint):
                missing.append(endpoint)

        assert len(missing) == 0, f"Missing endpoints in DarktraceClient: {missing}"

        # Cleanup
        client.close()

    def test_all_exports_in_init(self):
        """Test that __init__.py exports all public classes."""
        import darktrace

        expected_exports = [
            "DarktraceClient",
            "DarktraceAuth",
            # Endpoint classes
            "AdvancedSearch",
            "Analyst",
            "Antigena",
            "ModelBreaches",
            "Components",
            "CVEs",
            "Details",
            "Devices",
            "DeviceInfo",
            "DeviceSearch",
            "DeviceSummary",
            "DarktraceEmail",
            "EndpointDetails",
            "Enums",
            "FilterTypes",
            "IntelFeed",
            "MBComments",
            "MetricData",
            "Metrics",
            "Models",
            "Network",
            "PCAPs",
            "SimilarDevices",
            "Status",
            "Subnets",
            "SummaryStatistics",
            "Tags",
        ]

        missing = []
        for name in expected_exports:
            if not hasattr(darktrace, name):
                missing.append(name)

        assert len(missing) == 0, f"Missing exports in __init__.py: {missing}"

    def test_package_metadata(self):
        """Test package has proper metadata."""
        import darktrace

        # Should have __version__
        assert hasattr(darktrace, "__version__")
        assert isinstance(darktrace.__version__, str)

    def test_no_syntax_errors(self):
        """Compile all Python files to check for syntax errors."""
        import py_compile
        import os

        errors = []
        darktrace_dir = os.path.dirname(__import__("darktrace").__file__)

        for filename in os.listdir(darktrace_dir):
            if filename.endswith(".py"):
                filepath = os.path.join(darktrace_dir, filename)
                try:
                    py_compile.compile(filepath, doraise=True)
                except py_compile.PyCompileError as e:
                    errors.append((filename, str(e)))

        assert len(errors) == 0, f"Syntax errors found: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
