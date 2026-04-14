"""Darktrace SDK utilities — base endpoint, sentinel, retry logic, and helpers."""

from __future__ import annotations

import base64
import json
import logging
import time
from typing import Any, Optional, Tuple, Union

import requests

from .exceptions import _raise_for_status

__all__ = ["BaseEndpoint", "TimeoutType", "debug_print", "encode_query"]
logger = logging.getLogger("darktrace")

# Type alias for timeout parameter — can be None, float, or tuple of (connect, read)
TimeoutType = Optional[Union[float, Tuple[float, float]]]


class _Unset:
    """Sentinel value for unset timeout parameters.

    Allows distinguishing between "not specified" (use client default)
    and "explicitly None" (no timeout). This class is a singleton —
    use the ``_UNSET`` module-level instance.
    """

    _instance = None

    def __new__(cls) -> _Unset:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "<UNSET>"

    def __bool__(self) -> bool:
        return False


_UNSET = _Unset()

# Internal type alias that includes _Unset sentinel for _resolve_timeout's parameter
_InternalTimeoutType = Union[_Unset, None, float, Tuple[float, float]]

# Retry configuration
_MAX_RETRIES = 3
_INITIAL_RETRY_WAIT_SECONDS = 3  # Exponential backoff: 3s, 6s, 12s
_RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})  # Rate limit + 5xx


def debug_print(message: str, debug: bool = False) -> None:
    """Log a debug message when debug mode is enabled.

    Args:
        message: The message to log.
        debug: Whether debug mode is enabled.
    """
    if debug:
        logger.debug(message)


def _format_timing(elapsed_seconds: float) -> str:
    """Format elapsed time as human-readable string.

    Args:
        elapsed_seconds: Time elapsed in seconds.

    Returns:
        Formatted string like "123ms" for <1s or "1.23s" for >=1s.
    """
    elapsed_ms = elapsed_seconds * 1000
    if elapsed_ms < 1000:
        return f"{elapsed_ms:.0f}ms"
    return f"{elapsed_seconds:.2f}s"


class BaseEndpoint:
    """Base class for all Darktrace API endpoint modules.

    Provides authenticated request helpers with retry logic, timeout
    resolution, and structured debug logging via Python's ``logging`` module.
    """

    def __init__(self, client: Any) -> None:
        self.client = client

    def __repr__(self) -> str:
        host = getattr(self.client, "host", "unknown")
        return f"<{self.__class__.__name__} host={host!r}>"

    def _resolve_timeout(self, timeout: _InternalTimeoutType = _UNSET) -> TimeoutType:
        """Resolve timeout value, using client default if not specified.

        Args:
            timeout: Per-request timeout. ``_UNSET`` (default) uses client.timeout.
                     ``None`` means no timeout. Float or tuple sets specific timeout.

        Returns:
            Resolved timeout value.
        """
        if timeout is not _UNSET:
            return timeout
        return getattr(self.client, "timeout", None)

    def _get_headers(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> tuple[dict[str, str], dict[str, Any] | None]:
        """Get authentication headers and sorted parameters for API requests.

        Args:
            endpoint: The API endpoint path.
            params: Optional query parameters to include in the signature.
            json_body: Optional JSON body for POST requests to include in signature.

        Returns:
            Tuple of (headers dict, sorted params dict or None).
        """
        result = self.client.auth.get_headers(endpoint, params, json_body)
        return result["headers"], result["params"]

    def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        timeout: _InternalTimeoutType = _UNSET,
    ) -> Any:
        """Make an authenticated GET request.

        Args:
            endpoint: The API endpoint path (e.g. "/devices").
            params: Optional query parameters.
            timeout: Per-request timeout override.

        Returns:
            Parsed JSON response.
        """
        headers, sorted_params = self._get_headers(endpoint, params)
        url = f"{self.client.host}{endpoint}"
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "GET",
            url,
            headers=headers,
            params=sorted_params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        _raise_for_status(response, method="GET", url=url)
        return response.json()

    def _post_json(
        self,
        endpoint: str,
        body: dict[str, Any],
        params: dict[str, Any] | None = None,
        timeout: _InternalTimeoutType = _UNSET,
    ) -> Any:
        """Make an authenticated POST request with a JSON body.

        The body is JSON-serialized with compact separators (no whitespace)
        to match the HMAC signature computation in ``auth.get_headers``.

        Args:
            endpoint: The API endpoint path (e.g. "/antigena").
            body: JSON-serializable dict to send as request body.
            params: Optional additional query parameters.
            timeout: Per-request timeout override.

        Returns:
            Parsed JSON response.
        """
        headers, sorted_params = self._get_headers(endpoint, params, body)
        url = f"{self.client.host}{endpoint}"
        json_data = json.dumps(body, separators=(",", ":"))
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "POST",
            url,
            headers=headers,
            params=sorted_params,
            data=json_data,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        if self.client.debug:
            logger.debug("POST %s [%d]", endpoint, response.status_code)
        _raise_for_status(response, method="POST", url=url)
        return response.json()

    def _post_form(
        self,
        endpoint: str,
        form_data: dict[str, Any],
        params: dict[str, Any] | None = None,
        timeout: _InternalTimeoutType = _UNSET,
    ) -> Any:
        """Make an authenticated POST request with form-encoded data.

        Args:
            endpoint: The API endpoint path.
            form_data: Dict of form fields to send.
            params: Optional additional query parameters.
            timeout: Per-request timeout override.

        Returns:
            Parsed JSON response.
        """
        headers, sorted_params = self._get_headers(endpoint, params)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        url = f"{self.client.host}{endpoint}"
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "POST",
            url,
            headers=headers,
            params=sorted_params,
            data=form_data,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        _raise_for_status(response, method="POST", url=url)
        return response.json()

    def _delete(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        timeout: _InternalTimeoutType = _UNSET,
    ) -> Any:
        """Make an authenticated DELETE request.

        Args:
            endpoint: The API endpoint path (e.g. "/tags/123").
            params: Optional query parameters.
            timeout: Per-request timeout override.

        Returns:
            Parsed JSON response.
        """
        headers, sorted_params = self._get_headers(endpoint, params)
        url = f"{self.client.host}{endpoint}"
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "DELETE",
            url,
            headers=headers,
            params=sorted_params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        _raise_for_status(response, method="DELETE", url=url)
        return response.json()

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an HTTP request with retry logic and timing logged in debug mode.

        Retries on transient failures (429, 5xx status codes, connection errors)
        with exponential backoff (3s, 6s, 12s).

        Args:
            method: HTTP method (GET, POST, DELETE, etc.).
            url: Full URL to request.
            **kwargs: Additional arguments passed to ``requests.request()``.

        Returns:
            ``requests.Response`` object.

        Raises:
            requests.RequestException: After max retries exhausted.
        """
        last_exception: Exception | None = None

        for attempt in range(_MAX_RETRIES + 1):  # 1 initial + 3 retries
            start = time.perf_counter()
            try:
                response = self.client._session.request(method, url, **kwargs)
                elapsed = time.perf_counter() - start

                if self.client.debug:
                    timing_str = _format_timing(elapsed)
                    logger.debug("%s %s [%s]", method, url, timing_str)

                # Check if we should retry based on status code
                if response.status_code in _RETRY_STATUS_CODES and attempt < _MAX_RETRIES:
                    wait_time = _INITIAL_RETRY_WAIT_SECONDS * (2**attempt)
                    logger.debug(
                        "Retry %d/%d: HTTP %d, waiting %ds",
                        attempt + 1,
                        _MAX_RETRIES,
                        response.status_code,
                        wait_time,
                    )
                    response.close()  # Free connection before sleeping
                    time.sleep(wait_time)
                    continue

                return response

            except (requests.ConnectionError, requests.Timeout) as e:
                elapsed = time.perf_counter() - start
                last_exception = e

                if self.client.debug:
                    timing_str = _format_timing(elapsed)
                    logger.debug("%s %s FAILED [%s]: %s", method, url, timing_str, e)

                if attempt < _MAX_RETRIES:
                    wait_time = _INITIAL_RETRY_WAIT_SECONDS * (2**attempt)
                    logger.debug(
                        "Retry %d/%d: Connection error, waiting %ds",
                        attempt + 1,
                        _MAX_RETRIES,
                        wait_time,
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    raise

        # Should not reach here, but raise last exception if we do
        if last_exception:
            raise last_exception

        raise RuntimeError("Unexpected state in retry loop")  # pragma: no cover


def encode_query(query: dict) -> str:
    """Encode a query dict as a base64-encoded JSON string.

    Args:
        query: The query dictionary to encode.

    Returns:
        Base64-encoded JSON string.
    """
    query_json = json.dumps(query)
    return base64.b64encode(query_json.encode()).decode()
