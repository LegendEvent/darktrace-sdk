from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Models"]


class Models(BaseEndpoint):
    def get(
        self,
        uuid: str | None = None,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
    ) -> dict | list:
        """
        Get model information from Darktrace.

        Args:
            uuid (str, optional): Universally unique identifier for a model. If provided, filters to a specific model.
            responsedata (str, optional): Restrict the returned JSON to only the specified field(s) or object(s).

        Returns:
            list or dict: Model information from Darktrace. Returns a list of models or a dict for a single model.
        """
        params = {}
        if uuid is not None:
            params["uuid"] = uuid
        if responsedata is not None:
            params["responsedata"] = responsedata
        return self._get("/models", params=params, timeout=timeout)
