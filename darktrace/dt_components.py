from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Components"]


class Components(BaseEndpoint):
    def __init__(self, client) -> None:
        super().__init__(client)

    def get(
        self,
        cid: int | None = None,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
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
        if responsedata is not None:
            params["responsedata"] = responsedata
        return self._get(endpoint, params=params if params else None, timeout=timeout)
