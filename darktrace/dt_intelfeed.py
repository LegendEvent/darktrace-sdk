import requests
from typing import Optional, List, Dict, Any, Union
from .dt_utils import debug_print, BaseEndpoint

class IntelFeed(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, feed_type: Optional[str] = None, response_data: Optional[str] = None, 
            sources: Optional[bool] = None, source: Optional[str] = None, 
            full_details: Optional[bool] = None, **params):
        """Get intelligence feed data or details for a specific feed type.
        
        Args:
            feed_type: Optional feed type to filter by
            response_data: Optional response data format
            sources: If True, returns the current set of sources rather than the list of watched entries
            source: Optional source name to filter entries by
            full_details: If True, returns full details about expiry time and description for each entry
            **params: Additional parameters to pass to the API
        """
        endpoint = f'/intelfeed{f"/{feed_type}" if feed_type else ""}'
        url = f"{self.client.host}{endpoint}"
        
        # Build the query parameters
        query_params = {}
        if response_data:
            query_params['responsedata'] = response_data
        if sources is not None:
            query_params['sources'] = str(sources).lower()
        if source:
            query_params['source'] = source
        if full_details:
            query_params['fulldetails'] = 'true'
        # Add any additional parameters
        query_params.update(params)
        
        # Get headers and sorted parameters for consistent signature calculation
        headers, sorted_params = self._get_headers(endpoint, query_params)
            
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def get_sources(self):
        """Get a list of sources for entries on the intelfeed list."""
        return self.get(sources=True)
        
    def get_by_source(self, source: str):
        """Get the intel feed list for all entries under a specific source."""
        return self.get(source=source)
        
    def get_with_details(self):
        """Get intel feed with full details about expiry time and description for each entry."""
        return self.get(full_details=True)

    def update(self, add_entry: Optional[str] = None, add_list: Optional[List[str]] = None, 
               description: Optional[str] = None, source: Optional[str] = None, 
               expiry: Optional[str] = None, is_hostname: bool = False, 
               remove_entry: Optional[str] = None, remove_all: bool = False, 
               enable_antigena: bool = False):
        """Update the intel feed (watched domains) in Darktrace.
        
        Args:
            add_entry: Single entry to add (domain, hostname or IP address)
            add_list: List of entries to add (domains, hostnames or IP addresses)
            description: Description for added entries (must be under 256 characters)
            source: Source for added entries (must be under 64 characters)
            expiry: Expiration time for added items
            is_hostname: If True, treat added items as hostnames rather than domains
            remove_entry: Entry to remove (domain, hostname or IP address)
            remove_all: If True, remove all entries
            enable_antigena: If True, enable automatic Antigena Network actions
        """
        endpoint = '/intelfeed'
        url = f"{self.client.host}{endpoint}"
        
        # Build the request body
        body: Dict[str, Any] = {}
        
        if add_entry:
            body['addentry'] = add_entry
        if add_list:
            body['addlist'] = ','.join(add_list)
        if remove_entry:
            body['removeentry'] = remove_entry
        if remove_all:
            body['removeall'] = True
        if description:
            body['description'] = description
        if source:
            body['source'] = source
        if expiry:
            body['expiry'] = expiry
        if is_hostname:
            body['hostname'] = True
        if enable_antigena:
            body['iagn'] = True
        
        # For POST requests with JSON body, we don't include the body in the signature
        # But we still need to include any query parameters if present
        headers, _ = self._get_headers(endpoint)
            
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        response.raise_for_status()
        return response.json() 