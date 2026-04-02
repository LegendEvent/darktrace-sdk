import json
from typing import Any, Dict, List, Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["IntelFeed"]


class IntelFeed(BaseEndpoint):
    """
    Interact with the /intelfeed endpoint of the Darktrace API.
    The /intelfeed endpoint provides programmatic access to Watched Domains (Customer Portal), a list of domains, IPs, and hostnames used by Darktrace, Inoculation, and STIX/TAXII integration.

    GET parameters:
        - sources (bool): If True, returns the current set of sources rather than the list of watched entries.
        - source (str): Restrict a retrieved list of entries to a particular source (label, max 64 chars).
        - fulldetails (bool): If True, returns full details about expiry time and description for each entry.
        - responsedata (str): Restrict the returned JSON to only the specified field/object (future compatibility).
        - **params: Additional query parameters (not officially supported).

    POST parameters (see update method):
        - addentry, addlist, description, expiry, hostname, removeall, removeentry, source, iagn

    Returns:
        list: List of watched domains, IPs, or hostnames, or list of sources, or detailed entry dicts.
    """

    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        sources: Optional[bool] = None,
        source: Optional[str] = None,
        fulldetails: Optional[bool] = None,
        responsedata: Optional[str] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
        **params,
    ):
        """
        Get the intelfeed list, sources, or detailed entries.

        Args:
            sources (bool, optional): If True, returns the current set of sources.
            source (str, optional): Restrict entries to a particular source.
            fulldetails (bool, optional): If True, returns full details for each entry.
            responsedata (str, optional): Restrict the returned JSON to only the specified field/object.
            **params: Additional query parameters (not officially supported).

        Returns:
            list: List of watched domains, IPs, hostnames, or sources, or detailed entry dicts.
        """
        endpoint = "/intelfeed"
        url = f"{self.client.host}{endpoint}"
        query_params = dict()
        if sources is not None:
            query_params["sources"] = str(sources).lower()
        if source:
            query_params["source"] = source
        if fulldetails:
            query_params["fulldetails"] = "true"
        if responsedata:
            query_params["responsedata"] = responsedata
        query_params.update(params)
        headers, sorted_params = self._get_headers(endpoint, query_params)
        resolved_timeout = self._resolve_timeout(timeout)

        response = self._make_request(
            "GET",
            url,
            headers=headers,
            params=sorted_params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_sources(self, timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET):  # type: ignore[assignment]
        """Get a list of sources for entries on the intelfeed list."""
        return self.get(sources=True, timeout=timeout)

    def get_by_source(self, source: str, timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET):  # type: ignore[assignment]
        """Get the intel feed list for all entries under a specific source."""
        return self.get(source=source, timeout=timeout)

    def get_with_details(self, timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET):  # type: ignore[assignment]
        """Get intel feed with full details about expiry time and description for each entry."""
        return self.get(fulldetails=True, timeout=timeout)

    def update(
        self,
        add_entry: Optional[str] = None,
        add_list: Optional[List[str]] = None,
        description: Optional[str] = None,
        source: Optional[str] = None,
        expiry: Optional[str] = None,
        is_hostname: bool = False,
        remove_entry: Optional[str] = None,
        remove_all: bool = False,
        enable_antigena: bool = False,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ):
        """Update the intel feed (watched domains) in Darktrace.

        Args:
            add_entry: Single entry to add (domain, hostname or IP address)
            add_list: List of entries to add (domains, hostnames or IP addresses)
            description: Description for added entries (must be under 256 characters)
            source: Source for added entries (must be under 64 characters)
            expiry: Expiration time for added items
            is_hostname: If True, treat added items as hostnames rather than domains
            remove_entry: Entry to remove (domain, hostname or IP address)
            remove_all: If True, remove all entries
            enable_antigena: If True, enable automatic Antigena Network actions
        """
        endpoint = "/intelfeed"
        url = f"{self.client.host}{endpoint}"

        # Build the request body
        body: Dict[str, Any] = {}

        if add_entry:
            body["addentry"] = add_entry
        if add_list:
            body["addlist"] = ",".join(add_list)
        if remove_entry:
            body["removeentry"] = remove_entry
        if remove_all:
            body["removeall"] = True
        if description:
            body["description"] = description
        if source:
            body["source"] = source
        if expiry:
            body["expiry"] = expiry
        if is_hostname:
            body["hostname"] = True
        if enable_antigena:
            body["iagn"] = True

        # For POST requests with JSON body, we need to include the body in the signature
        headers, _ = self._get_headers(endpoint, json_body=body)
        headers["Content-Type"] = "application/json"

        resolved_timeout = self._resolve_timeout(timeout)

        response = self._make_request(
            "POST",
            url,
            headers=headers,
            data=json.dumps(body, separators=(",", ":")),
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        self.client._debug(f"Response status: {response.status_code}")
        self.client._debug(f"Response text: {response.text}")
        response.raise_for_status()
        return response.json()
