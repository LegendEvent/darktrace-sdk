"""Darktrace SDK exception hierarchy.

All exceptions subclass :class:`requests.HTTPError` for backward compatibility
with existing ``except requests.HTTPError`` handlers.

Hierarchy::

    requests.HTTPError
    └── DarktraceError
        ├── BadRequestError        (400)
        ├── AuthenticationError    (401)
        ├── ForbiddenError         (403)
        ├── NotFoundError          (404)
        ├── RateLimitError         (429)
        ├── ServerError            (5xx)
        └── ConnectionError        (network-level failures)
"""

from __future__ import annotations

import requests


class DarktraceError(requests.HTTPError):
    """Base exception for all Darktrace SDK errors.

    Subclasses :class:`requests.HTTPError` so that existing
    ``except requests.HTTPError`` handlers still catch SDK exceptions.
    """

    def __init__(
        self,
        message: str = "",
        response: requests.Response | None = None,
        method: str | None = None,
        url: str | None = None,
    ) -> None:
        self.method = method
        self.url = url
        super().__init__(message, response=response)

    @property
    def status_code(self) -> int | None:
        """HTTP status code from the response, or ``None``."""
        if self.response is not None:
            return self.response.status_code
        return None


class BadRequestError(DarktraceError):
    """400 Bad Request — invalid parameters or malformed request."""


class AuthenticationError(DarktraceError):
    """401 Unauthorized — invalid tokens or HMAC signature mismatch."""


class ForbiddenError(DarktraceError):
    """403 Forbidden — insufficient permissions."""


class NotFoundError(DarktraceError):
    """404 Not Found — resource or endpoint does not exist."""


class RateLimitError(DarktraceError):
    """429 Too Many Requests — rate limit exceeded."""

    def __init__(
        self,
        message: str = "",
        response: requests.Response | None = None,
        method: str | None = None,
        url: str | None = None,
    ) -> None:
        super().__init__(message, response=response, method=method, url=url)
        self.retry_after: str | None = None
        if response is not None:
            self.retry_after = response.headers.get("Retry-After")


class ServerError(DarktraceError):
    """5xx Server Error — Darktrace backend issue."""


class ConnectionError(DarktraceError):
    """Network-level connection failure.

    Raised when the SDK cannot reach the Darktrace instance
    (DNS failure, refused connection, timeout, etc.).
    """


_STATUS_MAP: dict[int, type[DarktraceError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: ForbiddenError,
    404: NotFoundError,
    429: RateLimitError,
}


def _raise_for_status(
    response: requests.Response,
    method: str | None = None,
    url: str | None = None,
) -> None:
    """Raise a typed SDK exception for HTTP error responses.

    Maps status codes to specific :class:`DarktraceError` subclasses.
    Falls back to :class:`ServerError` for 5xx codes not otherwise mapped,
    and to :class:`DarktraceError` for any other error status.

    Does nothing if the response indicates success (2xx).

    Args:
        response: The HTTP response to check.
        method: HTTP method used for the request.
        url: Full URL that was requested.
    """
    status_code = response.status_code

    if status_code < 400:
        return

    exc_class = _STATUS_MAP.get(status_code)

    if exc_class is None and 500 <= status_code < 600:
        exc_class = ServerError

    if exc_class is None:
        exc_class = DarktraceError

    message = f"{status_code} {response.reason} for url: {response.url}"

    raise exc_class(message=message, response=response, method=method, url=url)
