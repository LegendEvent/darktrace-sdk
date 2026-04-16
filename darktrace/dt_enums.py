from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Enums"]


class Enums(BaseEndpoint):
    """
    Interact with the /enums endpoint of the Darktrace API.
    The /enums endpoint returns string values for numeric codes (enumerated types) used in many API responses.
    The list of enums can be filtered using the responsedata parameter.
    """

    def get(
        self,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
        """
        Get enum values for all types or restrict to a specific field/object.

        Args:
            responsedata (str, optional): When given the name of a top-level field or object, restricts the returned JSON to only that field or object (e.g., 'countries').
            **params: Additional API parameters (not officially documented).

        Returns:
            dict: Enum values from the Darktrace API.
        """
        query_params = {}
        if responsedata:
            query_params["responsedata"] = responsedata
        query_params.update(params)
        return self._get("/enums", params=query_params, timeout=timeout)
