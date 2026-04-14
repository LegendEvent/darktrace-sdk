from typing import Any, Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Models"]


class Models(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        uuid: Optional[str] = None,
        responsedata: Optional[str] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
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
