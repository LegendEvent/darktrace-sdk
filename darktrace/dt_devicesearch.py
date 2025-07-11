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
    
    def get_tag(self, tag: str, **kwargs):
        """
        Search for devices with a specific tag.

        Args:
            tag (str): The tag to search for.
            **kwargs: Additional parameters for the search.

        Returns:
            dict: API response
        """
        query = f'tag:"{tag}"'
        return self.get(query=query, **kwargs)

    def get_type(self, type_label: str, **kwargs):
        """
        Search for devices with a specific type.

        Args:
            type_label (str): The type to search for.
            **kwargs: Additional parameters for the search.

        Returns:
            dict: API response
        """
        query = f'type:"{type_label}"'
        return self.get(query=query, **kwargs)

    def get_label(self, label: str, **kwargs):
        """
        Search for devices with a specific label.

        Args:
            label (str): The label to search for.
            **kwargs: Additional parameters for the search.

        Returns:
            dict: API response
        """
        query = f'label:"{label}"'
        return self.get(query=query, **kwargs)

    def get_vendor(self, vendor: str, **kwargs):
        """
        Search for devices with a specific vendor.

        Args:
            vendor (str): The vendor to search for.
            **kwargs: Additional parameters for the search.

        Returns:
            dict: API response
        """
        query = f'vendor:"{vendor}"'
        return self.get(query=query, **kwargs)

    def get_hostname(self, hostname: str, **kwargs):
        """
        Search for devices with a specific hostname.

        Args:
            hostname (str): The hostname to search for.
            **kwargs: Additional parameters for the search.

        Returns:
            dict: API response
        """
        query = f'hostname:"{hostname}"'
        return self.get(query=query, **kwargs)

    def get_ip(self, ip: str, **kwargs):
        """
        Search for devices with a specific IP address.

        Args:
            ip (str): The IP address to search for.
            **kwargs: Additional parameters for the search.

        Returns:
            dict: API response
        """
        query = f'ip:"{ip}"'
        return self.get(query=query, **kwargs)

    def get_mac(self, mac: str, **kwargs):
        """
        Search for devices with a specific MAC address.

        Args:
            mac (str): The MAC address to search for.
            **kwargs: Additional parameters for the search.

        Returns:
            dict: API response
        """
        query = f'mac:"{mac}"'
        return self.get(query=query, **kwargs)