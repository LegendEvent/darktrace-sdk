from typing import Optional, Union, Tuple
from .dt_utils import debug_print, BaseEndpoint, _UNSET


class Components(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        cid: Optional[int] = None,
        responsedata: Optional[str] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
        **params,
    ):  # type: ignore[assignment]
        """
        Get information about model components.

        Parameters:
            cid (int, optional): Component ID to retrieve a specific component. If None, returns all components.
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field or object.
            **params: Additional parameters for future compatibility.

        Returns:
            dict or list: API response containing component(s) data.

        Example:
            get()                # Get all components
            get(cid=1234)        # Get component with ID 1234
            get(responsedata='filters')  # Only return the 'filters' field for all components
        """
        endpoint = f"/components{f'/{cid}' if cid is not None else ''}"
        # Add responsedata to params if provided
        if responsedata is not None:
            params["responsedata"] = responsedata
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)

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
