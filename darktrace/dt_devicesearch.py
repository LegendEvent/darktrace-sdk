import requests
from .dt_utils import debug_print, BaseEndpoint

class DeviceSearch(BaseEndpoint):
    """
    Interface for the /devicesearch endpoint.
    Provides highly filterable search for devices seen by Darktrace.

    Parameters (all optional, see Darktrace API docs):
        count (int): Number of devices to return (default 100, max 300)
        orderBy (str): Field to order by (priority, hostname, ip, macaddress, vendor, os, firstSeen, lastSeen, devicelabel, typelabel)
        order (str): asc or desc (default asc)
        query (str): String search, can use field filters (label, tag, type, hostname, ip, mac, vendor, os)
        offset (int): Offset for pagination
        responsedata (str): Restrict returned JSON to only this field/object
        seensince (str): Relative offset for activity (e.g. '1hour', '30minute', '60')
    """

    def __init__(self, client):
        super().__init__(client)

    def get(self, count=None, orderBy=None, order=None, query=None, offset=None, responsedata=None, seensince=None, **kwargs):
        """
        Search for devices using /devicesearch endpoint.

        Args:
            count (int): Number of devices to return (default 100, max 300)
            orderBy (str): Field to order by
            order (str): asc or desc
            query (str): String search, can use field filters
            offset (int): Offset for pagination
            responsedata (str): Restrict returned JSON to only this field/object
            seensince (str): Relative offset for activity
            **kwargs: Any additional parameters supported by the API

        Returns:
            dict: API response
        """
        endpoint = '/devicesearch'
        url = f"{self.client.host}{endpoint}"
        params = {}
        if count is not None:
            params['count'] = count
        if orderBy is not None:
            params['orderBy'] = orderBy
        if order is not None:
            params['order'] = order
        if query is not None:
            params['query'] = query
        if offset is not None:
            params['offset'] = offset
        if responsedata is not None:
            params['responsedata'] = responsedata
        if seensince is not None:
            params['seensince'] = seensince
        # Allow for future/undocumented params
        params.update(kwargs)

        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()