import requests
import json
from typing import Dict, Any, Optional, Union
from datetime import datetime
from .dt_utils import debug_print, BaseEndpoint

class ModelBreaches(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self, **params):
        """
        Get model breach alerts from the /modelbreaches endpoint.

        Parameters (all optional, see API docs for details):
            deviceattop (bool): Return device JSON at top-level (default: True)
            did (int): Device ID to filter by
            endtime (int): End time in milliseconds since epoch
            expandenums (bool): Expand numeric enums to strings
            from_time (str): Start time in YYYY-MM-DD HH:MM:SS format
            historicmodelonly (bool): Return only historic model details
            includeacknowledged (bool): Include acknowledged breaches
            includebreachurl (bool): Include breach URLs in response
            minimal (bool): Reduce data returned (default: False for API)
            minscore (float): Minimum breach score filter
            pbid (int): Specific breach ID to return
            pid (int): Filter by model ID
            starttime (int): Start time in milliseconds since epoch
            to_time (str): End time in YYYY-MM-DD HH:MM:SS format
            uuid (str): Filter by model UUID
            responsedata (str): Restrict response to specific fields
            saasonly (bool): Return only SaaS breaches
            group (str): Group results (e.g. 'device')
            includesuppressed (bool): Include suppressed breaches
            saasfilter (str or list): Filter by SaaS platform (can be repeated)
            creationtime (bool): Use creation time for filtering
            fulldevicedetails (bool): Return full device/component info (if supported)

        Returns:
            list or dict: API response containing model breach data

        Notes:
            - Time parameters must always be specified in pairs.
            - When minimal=true, response is reduced.
            - See API docs for full parameter details and response schema.
        """
        endpoint = '/modelbreaches'

        # Handle special parameter names for API compatibility
        if 'from_time' in params:
            params['from'] = params.pop('from_time')
        if 'to_time' in params:
            params['to'] = params.pop('to_time')

        # Support multiple saasfilter values
        if 'saasfilter' in params and isinstance(params['saasfilter'], list):
            # requests will handle repeated params if passed as a list of tuples
            saasfilters = params.pop('saasfilter')
            params_list = list(params.items()) + [("saasfilter", v) for v in saasfilters]
        else:
            params_list = list(params.items())

        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, dict(params_list))
        self.client._debug(f"GET {url} params={sorted_params}")

        response = requests.get(
            url,
            headers=headers,
            params=sorted_params,
            verify=False
        )
        response.raise_for_status()
        return response.json()

    def get_comments(self, pbid: int, **params):
        """
        Get comments for a specific model breach alert.

        Args:
            pbid (int): Policy breach ID of the model breach.
            responsedata (str, optional): Restrict response to specific fields.
        Returns:
            list: List of comment objects (see API docs for schema)
        """
        endpoint = f'/modelbreaches/{pbid}/comments'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def add_comment(self, pbid: int, message: str, **params) -> bool:
        """
        Add a comment to a model breach alert.

        Args:
            pbid (int): Policy breach ID of the model breach.
            message (str): The comment text to add.
            params: Additional parameters for the API call (future-proofing, e.g., responsedata)
        Returns:
            bool: True if comment was added successfully, False otherwise.
        """
        print(f"DEBUG BREACHES: add_comment called with:")
        print(f"  - pbid: {pbid}")
        print(f"  - message: '{message}'")
        print(f"  - params: {params}")
        
        endpoint = f'/modelbreaches/{pbid}/comments'
        url = f"{self.client.host}{endpoint}"
        body: Dict[str, Any] = {'message': message}
        
        print(f"DEBUG BREACHES: Calling _get_headers with:")
        print(f"  - endpoint: '{endpoint}'")
        print(f"  - params: {params}")
        print(f"  - body: {body}")
        
        headers, sorted_params = self._get_headers(endpoint, params, body)
        
        print(f"DEBUG BREACHES: Received from _get_headers:")
        print(f"  - headers: {headers}")
        print(f"  - sorted_params: {sorted_params}")
        
        self.client._debug(f"POST {url} params={sorted_params} body={body}")
        
        try:
            # Send JSON as raw data, not as json parameter (as per Darktrace docs)
            # IMPORTANT: Must use same JSON formatting as in signature generation!
            json_data = json.dumps(body, separators=(',', ':'))
            print(f"DEBUG BREACHES: JSON data to send: '{json_data}'")
            print(f"DEBUG BREACHES: Making POST request to: {url}")
            print(f"DEBUG BREACHES: With headers: {headers}")
            print(f"DEBUG BREACHES: With params: {sorted_params}")
            print(f"DEBUG BREACHES: With data: '{json_data}'")
            
            response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
            self.client._debug(f"Response Status: {response.status_code}")
            self.client._debug(f"Response Text: {response.text}")
            
            print(f"DEBUG BREACHES: Response status: {response.status_code}")
            print(f"DEBUG BREACHES: Response headers: {dict(response.headers)}")
            print(f"DEBUG BREACHES: Response text: '{response.text}'")
            
            if response.status_code == 200:
                self.client._debug("Comment added successfully")
                return True
            else:
                self.client._debug(f"Failed to add comment. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.client._debug(f"Exception occurred while adding comment: {str(e)}")
            print(f"DEBUG BREACHES: Exception: {str(e)}")
            return False

    def acknowledge(self, pbid: int, **params) -> bool:
        """
        Acknowledge a model breach alert.

        Args:
            pbid (int): Policy breach ID of the model breach.
            params: Additional parameters for the API call (future-proofing)
        Returns:
            bool: True if acknowledged successfully, False otherwise.
        """
        endpoint = f'/modelbreaches/{pbid}/acknowledge'
        url = f"{self.client.host}{endpoint}"
        body: Dict[str, bool] = {'acknowledge': True}
        headers, sorted_params = self._get_headers(endpoint, params, body)
        self.client._debug(f"POST {url} params={sorted_params} body={body}")
        
        try:
            # Send JSON as raw data, not as json parameter (as per Darktrace docs)
            # IMPORTANT: Must use same JSON formatting as in signature generation!
            json_data = json.dumps(body, separators=(',', ':'))
            response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
            self.client._debug(f"Response Status: {response.status_code}")
            self.client._debug(f"Response Text: {response.text}")
            
            if response.status_code == 200:
                self.client._debug("Breach acknowledged successfully")
                return True
            else:
                self.client._debug(f"Failed to acknowledge breach. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.client._debug(f"Exception occurred while acknowledging breach: {str(e)}")
            return False

    def unacknowledge(self, pbid: int, **params) -> bool:
        """
        Unacknowledge a model breach alert.

        Args:
            pbid (int): Policy breach ID of the model breach.
            params: Additional parameters for the API call (future-proofing)
        Returns:
            bool: True if unacknowledged successfully, False otherwise.
        """
        endpoint = f'/modelbreaches/{pbid}/unacknowledge'
        url = f"{self.client.host}{endpoint}"
        body: Dict[str, bool] = {'unacknowledge': True}
        headers, sorted_params = self._get_headers(endpoint, params, body)
        self.client._debug(f"POST {url} params={sorted_params} body={body}")
        
        try:
            # Send JSON as raw data, not as json parameter (as per Darktrace docs)
            # IMPORTANT: Must use same JSON formatting as in signature generation!
            json_data = json.dumps(body, separators=(',', ':'))
            response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
            self.client._debug(f"Response Status: {response.status_code}")
            self.client._debug(f"Response Text: {response.text}")
            
            if response.status_code == 200:
                self.client._debug("Breach unacknowledged successfully")
                return True
            else:
                self.client._debug(f"Failed to unacknowledge breach. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.client._debug(f"Exception occurred while unacknowledging breach: {str(e)}")
            return False