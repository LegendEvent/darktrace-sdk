import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Models(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, uuid: Optional[str] = None, responsedata: Optional[str] = None):
        """
        Get model information from Darktrace.

        Args:
            uuid (str, optional): Universally unique identifier for a model. If provided, filters to a specific model.
            responsedata (str, optional): Restrict the returned JSON to only the specified field(s) or object(s).

        Returns:
            list or dict: Model information from Darktrace. Returns a list of models or a dict for a single model.
        """
        endpoint = '/models'
        url = f"{self.client.host}{endpoint}"
        params = dict()
        if uuid is not None:
            params['uuid'] = uuid
        if responsedata is not None:
            params['responsedata'] = responsedata
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()