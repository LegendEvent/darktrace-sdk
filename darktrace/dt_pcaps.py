import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class PCAPs(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, pcap_id: Optional[str] = None, responsedata: Optional[str] = None):
        """
        Retrieve PCAP information or download a specific PCAP file from Darktrace.

        Args:
            pcap_id (str, optional): The filename of the PCAP to download. If not provided, returns a list of available PCAPs and their status.
            responsedata (str, optional): Restrict the returned JSON to only the specified field(s) or object(s).

        Returns:
            list, dict, or bytes: List of PCAPs, details of a specific PCAP, or binary PCAP file content.
        """
        endpoint = f'/pcaps{f"/{pcap_id}" if pcap_id else ""}'
        url = f"{self.client.host}{endpoint}"
        params = dict()
        if responsedata is not None:
            params['responsedata'] = responsedata
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        # Return JSON if possible, else return raw content (for PCAP file download)
        return response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.content

    def create(self, ip1: str, start: int, end: int, ip2: Optional[str] = None, port1: Optional[int] = None, port2: Optional[int] = None, protocol: Optional[str] = None):
        """
        Create a new PCAP capture request in Darktrace.

        Args:
            ip1 (str): The source IP address (required).
            start (int): The start time for the packet capture (epoch seconds, required).
            end (int): The end time for the packet capture (epoch seconds, required).
            ip2 (str, optional): The destination IP address.
            port1 (int, optional): The source port.
            port2 (int, optional): The destination port.
            protocol (str, optional): Layer 3 protocol ("tcp" or "udp").

        Returns:
            dict: Details of the PCAP creation request (including filename, state, etc.).
        """
        endpoint = '/pcaps'
        url = f"{self.client.host}{endpoint}"
        body = {"ip1": ip1, "start": start, "end": end}
        if ip2 is not None:
            body["ip2"] = ip2
        if port1 is not None:
            body["port1"] = port1
        if port2 is not None:
            body["port2"] = port2
        if protocol is not None:
            body["protocol"] = protocol
        headers, _ = self._get_headers(endpoint)
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        response.raise_for_status()
        return response.json()