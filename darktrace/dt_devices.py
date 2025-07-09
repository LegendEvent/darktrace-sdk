import requests
import json
from typing import List, Dict, Any
from .dt_utils import debug_print, BaseEndpoint


class Devices(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, 
            did: int = None, 
            ip: str = None, 
            iptime: str = None, 
            mac: str = None, 
            seensince: str = None,
            sid: int = None,
            count: int = None,
            includetags: bool = None,
            responsedata: str = None,
            cloudsecurity: bool = None,
            saasfilter: Any = None
            ):
        """
        Get device information from Darktrace.

        Args:
            did (int, optional): Device ID.
            ip (str, optional): Device IP address.
            iptime (str, optional): Returns the device which had the IP at a given time.
            mac (str, optional): Returns the device with this MAC address.
            seensince (str, optional): Relative offset for activity (e.g., '2min', '1hour', '3600').
            sid (int, optional): Subnet ID.
            count (int, optional): Number of devices to return.
            includetags (bool, optional): Whether to include tags applied to the device in the response.
            responsedata (str, optional): Restrict the returned JSON to only the specified field(s).
            cloudsecurity (bool, optional): When true, limits the devices returned to those identified by Darktrace Cloud Security.
            saasfilter (str or list of str, optional): Limit returned devices to specific SaaS/Cloud/Zero Trust module users. Can be repeated.

        Returns:
            dict or list: Device information from Darktrace.
        """
        endpoint = '/devices'
        url = f"{self.client.host}{endpoint}"

        # Build parameters dictionary
        params = dict()
        if did is not None:
            params['did'] = did
        if ip is not None:
            params['ip'] = ip
        if iptime is not None:
            params['iptime'] = iptime
        if mac is not None:
            params['mac'] = mac
        if seensince is not None:
            params['seensince'] = seensince
        if sid is not None:
            params['sid'] = sid
        if count is not None:
            params['count'] = count
        if includetags is not None:
            params['includetags'] = includetags
        if responsedata is not None:
            params['responsedata'] = responsedata
        if cloudsecurity is not None:
            params['cloudsecurity'] = cloudsecurity
        # saasfilter can be a string or list of strings; only wrap in list if input is a list/tuple
        if saasfilter is not None:
            if isinstance(saasfilter, (list, tuple)):
                params['saasfilter'] = saasfilter
            else:
                params['saasfilter'] = saasfilter

        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")

        response = requests.get(
            url,
            headers=headers,
            params=sorted_params,
            verify=False
        )
        response.raise_for_status()
        return response.json()

    def update(self, did: int, **kwargs) -> dict:
        """Update device properties in Darktrace.
        
        Args:
            did (int): Device ID to update
            **kwargs: Device properties to update
                label (str): Device label
                priority (int): Device priority (-5 to 5)
                type (int): Device type enum
        """
        endpoint = '/devices'
        url = f"{self.client.host}{endpoint}"
        
        # Prepare request body
        body: Dict[str, Any] = {"did": did}
        body.update(kwargs)
        
        # Get headers with JSON body for signature generation
        headers, sorted_params = self._get_headers(endpoint, json_body=body)
        self.client._debug(f"POST {url} body={body}")
        
        # Send JSON as raw data with consistent formatting (same as signature generation)
        json_data = json.dumps(body, separators=(',', ':'))
        response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()