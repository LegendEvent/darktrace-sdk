import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Subnets(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self,
            subnet_id: Optional[int] = None,
            seensince: Optional[str] = None,
            sid: Optional[int] = None,
            responsedata: Optional[str] = None
        ):
        """
        Get subnet information from Darktrace.

        Args:
            subnet_id (int, optional): Specific subnet ID to retrieve (as path parameter).
            seensince (str, optional): Relative offset for activity (e.g., '2min', '1hour', '3600', '3min', '5hour', '6day').
                Minimum=1 second, Maximum=6 months. Subnets with activity in the specified time period are returned.
            sid (int, optional): Identification number of a subnet modeled in the Darktrace system.
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field(s) or object(s).

        Returns:
            list or dict: Subnet information from Darktrace.
        """
        endpoint = f'/subnets{f"/{subnet_id}" if subnet_id else ""}'
        url = f"{self.client.host}{endpoint}"

        params = dict()
        if seensince is not None:
            params['seensince'] = seensince
        if sid is not None:
            params['sid'] = sid
        if responsedata is not None:
            params['responsedata'] = responsedata

        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def post(self,
            sid: int,
            label: Optional[str] = None,
            network: Optional[str] = None,
            longitude: Optional[float] = None,
            latitude: Optional[float] = None,
            dhcp: Optional[bool] = None,
            uniqueUsernames: Optional[bool] = None,
            uniqueHostnames: Optional[bool] = None,
            excluded: Optional[bool] = None,
            modelExcluded: Optional[bool] = None,
            responsedata: Optional[str] = None
        ):
        """
        Create or update a subnet in Darktrace.

        Args:
            sid (int): Identification number of a subnet modeled in the Darktrace system.
            label (str, optional): An optional label to identify the subnet by. Do not use quotes around the string.
            network (str, optional): The IP address range that describes the subnet.
            longitude (float, optional): Longitude for the subnet's location (must be used with latitude). Whole values must be passed with a decimal point (e.g., 10.0).
            latitude (float, optional): Latitude for the subnet's location (must be used with longitude). Whole values must be passed with a decimal point (e.g., 10.0).
            dhcp (bool, optional): Whether DHCP is enabled for the subnet.
            uniqueUsernames (bool, optional): Whether the subnet is tracking by credential.
            uniqueHostnames (bool, optional): Whether the subnet is tracking by hostname.
            excluded (bool, optional): Whether traffic in this subnet should not be processed at all.
            modelExcluded (bool, optional): Whether devices within this subnet should be fully modeled. If true, the devices will be added to the Internal Traffic subnet.
            responsedata (str, optional): Restrict the returned JSON to only the specified top-level field(s) or object(s).

        Returns:
            dict: Result of the subnet creation or update operation.
        """
        endpoint = '/subnets'
        url = f"{self.client.host}{endpoint}"

        body = {'sid': sid}
        if label is not None:
            body['label'] = label
        if network is not None:
            body['network'] = network
        if longitude is not None:
            body['longitude'] = longitude
        if latitude is not None:
            body['latitude'] = latitude
        if dhcp is not None:
            body['dhcp'] = dhcp
        if uniqueUsernames is not None:
            body['uniqueUsernames'] = uniqueUsernames
        if uniqueHostnames is not None:
            body['uniqueHostnames'] = uniqueHostnames
        if excluded is not None:
            body['excluded'] = excluded
        if modelExcluded is not None:
            body['modelExcluded'] = modelExcluded
        if responsedata is not None:
            body['responsedata'] = responsedata

        headers, _ = self._get_headers(endpoint)
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        response.raise_for_status()
        return response.json()