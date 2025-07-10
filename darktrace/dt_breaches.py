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

    def get_comments(self, pbid: Union[int, list], **params):
        """
        Get comments for a specific model breach alert.

        Args:
            pbid (int or list of int): Policy breach ID(s) of the model breach(es).
            responsedata (str, optional): Restrict response to specific fields.
        Returns:
            list or dict: List of comment objects (see API docs for schema), or dict mapping pbid to comments if pbid is a list.
        """
        if isinstance(pbid, (list, tuple)):
            # Build dict with string keys for valid JSON
            return {str(single_pbid): self.get_comments(single_pbid, **params) for single_pbid in pbid}
        endpoint = f'/modelbreaches/{pbid}/comments'
        url = f"{self.client.host}{endpoint}"
        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def add_comment(self, pbid: int, message: str, **params) -> dict:
        """
        Add a comment to a model breach alert.

        Args:
            pbid (int): Policy breach ID of the model breach.
            message (str): The comment text to add.
            params: Additional parameters for the API call (future-proofing, e.g., responsedata)
        Returns:
            dict: The full JSON response from Darktrace (or error info as dict)
        """
        debug_print(f"BREACHES: add_comment called with:", self.client.debug)
        debug_print(f"  - pbid: {pbid}", self.client.debug)
        debug_print(f"  - message: '{message}'", self.client.debug)
        debug_print(f"  - params: {params}", self.client.debug)
        
        endpoint = f'/modelbreaches/{pbid}/comments'
        url = f"{self.client.host}{endpoint}"
        body: Dict[str, Any] = {'message': message}
        
        debug_print(f"BREACHES: Calling _get_headers with:", self.client.debug)
        debug_print(f"  - endpoint: '{endpoint}'", self.client.debug)
        debug_print(f"  - params: {params}", self.client.debug)
        debug_print(f"  - body: {body}", self.client.debug)
        
        headers, sorted_params = self._get_headers(endpoint, params, body)
        
        debug_print(f"BREACHES: Received from _get_headers:", self.client.debug)
        debug_print(f"  - headers: {headers}", self.client.debug)
        debug_print(f"  - sorted_params: {sorted_params}", self.client.debug)
        
        self.client._debug(f"POST {url} params={sorted_params} body={body}")
        
        try:
            # Send JSON as raw data, not as json parameter (as per Darktrace docs)
            # IMPORTANT: Must use same JSON formatting as in signature generation!
            json_data = json.dumps(body, separators=(',', ':'))
            debug_print(f"BREACHES: JSON data to send: '{json_data}'", self.client.debug)
            debug_print(f"BREACHES: Making POST request to: {url}", self.client.debug)
            debug_print(f"BREACHES: With headers: {headers}", self.client.debug)
            debug_print(f"BREACHES: With params: {sorted_params}", self.client.debug)
            debug_print(f"BREACHES: With data: '{json_data}'", self.client.debug)
            
            response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
            self.client._debug(f"Response Status: {response.status_code}")
            self.client._debug(f"Response Text: {response.text}")
            debug_print(f"BREACHES: Response status: {response.status_code}", self.client.debug)
            debug_print(f"BREACHES: Response headers: {dict(response.headers)}", self.client.debug)
            debug_print(f"BREACHES: Response text: '{response.text}'", self.client.debug)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.client._debug(f"Exception occurred while adding comment: {str(e)}")
            debug_print(f"BREACHES: Exception: {str(e)}", self.client.debug)
            return {"error": str(e)}

    def acknowledge(self, pbid: Union[int, list], **params) -> dict:
        """
        Acknowledge a model breach alert.

        Args:
            pbid (int or list of int): Policy breach ID(s) of the model breach(es).
            params: Additional parameters for the API call (future-proofing)
        Returns:
            dict: The full JSON response from Darktrace (or error info as dict), or a dict mapping pbid to response if pbid is a list.
        """
        if isinstance(pbid, (list, tuple)):
            return {single_pbid: self.acknowledge(single_pbid, **params) for single_pbid in pbid}
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
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.client._debug(f"Exception occurred while acknowledging breach: {str(e)}")
            return {"error": str(e)}

    def unacknowledge(self, pbid: Union[int, list], **params) -> dict:
        """
        Unacknowledge a model breach alert.

        Args:
            pbid (int or list of int): Policy breach ID(s) of the model breach(es).
            params: Additional parameters for the API call (future-proofing)
        Returns:
            dict: The full JSON response from Darktrace (or error info as dict), or a dict mapping pbid to response if pbid is a list.
        """
        if isinstance(pbid, (list, tuple)):
            return {single_pbid: self.unacknowledge(single_pbid, **params) for single_pbid in pbid}
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
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.client._debug(f"Exception occurred while unacknowledging breach: {str(e)}")
            return {"error": str(e)}
        
    def acknowledge_with_comment(self, pbid: int, message: str, **params) -> dict:
        """
        Acknowledge a model breach and add a comment in one call.

        Args:
            pbid (int): Policy breach ID of the model breach.
            message (str): The comment text to add.
            params: Additional parameters for the API call.

        Returns:
            dict: Contains the responses from both acknowledge and add_comment.
        """
        ack_response = self.acknowledge(pbid, **params)
        comment_response = self.add_comment(pbid, message, **params)
        return {
            "acknowledge": ack_response,
            "add_comment": comment_response
        }
    
    def unacknowledge_with_comment(self, pbid: int, message: str, **params) -> dict:
        """
        Unacknowledge a model breach and add a comment in one call.

        Args:
            pbid (int): Policy breach ID of the model breach.
            message (str): The comment text to add.
            params: Additional parameters for the API call.

        Returns:
            dict: Contains the responses from both unacknowledge and add_comment.
        """
        unack_response = self.unacknowledge(pbid, **params)
        comment_response = self.add_comment(pbid, message, **params)
        return {
            "unacknowledge": unack_response,
            "add_comment": comment_response
        }