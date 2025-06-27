import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class SimilarDevices(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(
        self,
        device_id: Optional[str] = None,
        count: Optional[int] = None,
        fulldevicedetails: Optional[bool] = None,
        token: Optional[str] = None,
        responsedata: Optional[str] = None,
        **kwargs
    ):
        """
        Get similar devices information from Darktrace.

        Args:
            device_id (str, optional): Device ID to find similar devices for. If not provided, returns all similar devices.
            count (int, optional): Number of similar devices to return.
            fulldevicedetails (bool, optional): Whether to include full device details in the response.
            token (str, optional): Pagination token for large result sets.
            responsedata (str, optional): Restrict the returned JSON to only the specified field(s).
            **kwargs: Additional parameters for future compatibility.

        Returns:
            list or dict: Similar devices information from Darktrace.
        """
        endpoint = f'/similardevices{f"/{device_id}" if device_id else ""}'
        url = f"{self.client.host}{endpoint}"

        params = dict()
        if count is not None:
            params['count'] = count
        if fulldevicedetails is not None:
            params['fulldevicedetails'] = fulldevicedetails
        if token is not None:
            params['token'] = token
        if responsedata is not None:
            params['responsedata'] = responsedata
        # Allow passing extra params for forward compatibility
        params.update(kwargs)

        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        try:
            return response.json()
        except Exception as e:
            # Return a dict with error info if response is not JSON (e.g., HTML login page)
            return {"error": f"Non-JSON response: {str(e)}", "content": response.text[:500]}