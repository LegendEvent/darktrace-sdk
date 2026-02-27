import base64
import json
import time
from typing import Dict, Any, Optional, Tuple, Union

import requests

# Type alias for timeout parameter - can be None, float, or tuple of (connect, read)
TimeoutType = Optional[Union[float, Tuple[float, float]]]

# Sentinel value for unset timeout - allows distinguishing between
# "not specified" (use client default) and "explicitly None" (no timeout)
_UNSET = object()

# Retry configuration
_MAX_RETRIES = 3
_RETRY_WAIT_SECONDS = 10
_RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})  # Rate limit + 5xx

def debug_print(message: str, debug: bool = False):
    if debug:
        print(f"DEBUG: {message}")

def _format_timing(elapsed_seconds: float) -> str:
    """Format elapsed time as human-readable string.
    
    Args:
        elapsed_seconds: Time elapsed in seconds
        
    Returns:
        Formatted string like "123ms" for <1s or "1.23s" for >=1s
    """
    elapsed_ms = elapsed_seconds * 1000
    if elapsed_ms < 1000:
        return f"{elapsed_ms:.0f}ms"
    else:
        return f"{elapsed_seconds:.2f}s"

class BaseEndpoint:
    """Base class for all Darktrace API endpoint modules."""

    def __init__(self, client):
        self.client = client

    def _resolve_timeout(self, timeout: TimeoutType = _UNSET) -> TimeoutType:  # type: ignore[assignment]
        """Resolve timeout value, using client default if not specified.

        Args:
            timeout: Per-request timeout. _UNSET (default) uses client.timeout.
                     None means no timeout. Float or tuple sets specific timeout.
        """
        if timeout is not _UNSET:
            return timeout
        return getattr(self.client, 'timeout', None)
    
    def _get_headers(self, endpoint: str, params: Optional[Dict[str, Any]] = None, json_body: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, str], Optional[Dict[str, Any]]]:
        """
        Get authentication headers and sorted parameters for API requests.
        
        Args:
            endpoint: The API endpoint path
            params: Optional query parameters to include in the signature
            json_body: Optional JSON body for POST requests to include in signature
            
        Returns:
            Tuple containing:
            - Dict with the required authentication headers
            - Dict with sorted parameters (or None if no params)
        """
        result = self.client.auth.get_headers(endpoint, params, json_body)
        return result['headers'], result['params']

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an HTTP request with retry logic and timing logged in debug mode.
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            url: Full URL to request
            **kwargs: Additional arguments passed to requests.request()
            
        Returns:
            requests.Response object
            
        Raises:
            requests.RequestException: After max retries exhausted
        """
        last_exception: Optional[Exception] = None
        
        for attempt in range(_MAX_RETRIES + 1):  # 1 initial + 3 retries
            start = time.perf_counter()
            try:
                response = self.client._session.request(method, url, **kwargs)
                elapsed = time.perf_counter() - start
                
                if self.client.debug:
                    timing_str = _format_timing(elapsed)
                    self.client._debug(f"{method} {url} [{timing_str}]")
                
                # Check if we should retry based on status code
                if response.status_code in _RETRY_STATUS_CODES and attempt < _MAX_RETRIES:
                    if self.client.debug:
                        self.client._debug(f"Retry {attempt + 1}/{_MAX_RETRIES}: HTTP {response.status_code}")
                    time.sleep(_RETRY_WAIT_SECONDS)
                    continue
                
                return response
                
            except (requests.ConnectionError, requests.Timeout) as e:
                elapsed = time.perf_counter() - start
                last_exception = e
                
                if self.client.debug:
                    timing_str = _format_timing(elapsed)
                    self.client._debug(f"{method} {url} FAILED [{timing_str}]: {e}")
                
                if attempt < _MAX_RETRIES:
                    if self.client.debug:
                        self.client._debug(f"Retry {attempt + 1}/{_MAX_RETRIES}: Connection error")
                    time.sleep(_RETRY_WAIT_SECONDS)
                    continue
                else:
                    raise
        
        # Should not reach here, but raise last exception if we do
        if last_exception:
            raise last_exception
        
        return response  # type: ignore[unreachable]


def encode_query(query: dict) -> str:
    query_json = json.dumps(query)
    return base64.b64encode(query_json.encode()).decode() 