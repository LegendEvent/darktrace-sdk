from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any

__all__ = ["DarktraceAuth"]


class DarktraceAuth:
    """HMAC-SHA1 authentication for the Darktrace API.

    Generates request signatures using the public token, private token,
    and request details (path, query parameters, JSON body) as required
    by the Darktrace Threat Visualizer API.
    """

    def __init__(self, public_token: str, private_token: str) -> None:
        self.public_token = public_token
        self.private_token = private_token

    def __repr__(self) -> str:
        masked = self.public_token[:4] + "..." if len(self.public_token) > 4 else "***"
        return f"<DarktraceAuth public_token={masked}>"

    def get_headers(
        self,
        request_path: str,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Generate authentication headers and sorted parameters for Darktrace API requests.

        Args:
            request_path: The API endpoint path
            params: Optional query parameters to include in the signature
            json_body: Optional JSON body for POST requests to include in signature

        Returns:
            Dict containing:
            - 'headers': The required authentication headers
            - 'params': The sorted parameters (or original params if none)
        """
        # Use UTC time (Darktrace Server runs on UTC)
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        # Include query parameters in the signature if provided
        signature_path = request_path
        sorted_params = None

        if params and len(params) > 0:
            # Sort parameters alphabetically by key as required by Darktrace API
            sorted_params = dict(sorted(params.items()))
            query_string = "&".join(f"{k}={v}" for k, v in sorted_params.items())
            signature_path = f"{request_path}?{query_string}"

        # For POST requests with JSON body, include the JSON string directly as query parameter
        # as per Darktrace docs example: "/modelbreaches/101/comments?{"message":"Test Comment"}"
        if json_body:
            # Convert JSON body to string and append directly as query parameter
            # IMPORTANT: Must use same separators as in dt_breaches.py!
            json_string = json.dumps(json_body, separators=(",", ":"))  # No spaces in JSON
            separator = "&" if "?" in signature_path else "?"
            signature_path = f"{signature_path}{separator}{json_string}"

        signature = self.generate_signature(signature_path, date)

        return {
            "headers": {
                "DTAPI-Token": self.public_token,
                "DTAPI-Date": date,
                "DTAPI-Signature": signature,
                "Content-Type": "application/json",
            },
            "params": sorted_params or params,
        }

    def generate_signature(self, request_path: str, date: str) -> str:
        """
        Generate the HMAC signature for Darktrace API authentication.

        Args:
            request_path: The API endpoint path (including query parameters if any)
            date: The formatted date string

        Returns:
            The HMAC-SHA1 signature as a hexadecimal string
        """
        message = f"{request_path}\n{self.public_token}\n{date}"
        signature = hmac.new(self.private_token.encode("ASCII"), message.encode("ASCII"), hashlib.sha1).hexdigest()
        return signature
