import requests
import json
from typing import Dict, Any, Union, Optional, List
from .dt_utils import debug_print, BaseEndpoint

class Antigena(BaseEndpoint):
    """
    Darktrace RESPOND/Network (formerly Antigena Network) endpoint handler.
    
    The /antigena endpoint returns information about current and past Darktrace RESPOND/Network actions.
    It can be used to retrieve a list of currently quarantined devices or Darktrace RESPOND Actions 
    requiring approval. Information from active integrations such as firewalls is not included in this data.
    
    If a time window is not specified, the request will return all current actions with a future expiry 
    date and all historic actions with an expiry date in the last 14 days. Actions which were not 
    activated will still be returned.
    """
    
    def __init__(self, client):
        super().__init__(client)

    def get_actions(self, **params):
        """
        Get information about current and past Darktrace RESPOND actions.
        
        If a time window is not specified, returns all current actions with a future expiry date 
        and all historic actions with an expiry date in the last 14 days.
        
        Args:
            fulldevicedetails (bool): Returns the full device detail objects for all devices 
                referenced by data in an API response. Use of this parameter will alter the 
                JSON structure of the API response for certain calls.
            includecleared (bool): Returns all Darktrace RESPOND actions including those 
                already cleared. Defaults to false.
            includehistory (bool): Include additional history information about the action 
                state, such as when it was created or extended.
            needconfirming (bool): Filters returned Darktrace RESPOND actions by those that 
                need human confirmation or do not need human confirmation.
            endtime (int): End time of data to return in millisecond format, relative to 
                midnight January 1st 1970 UTC.
            from_time (str): Start time of data to return in YYYY-MM-DD HH:MM:SS format.
            starttime (int): Start time of data to return in millisecond format, relative to 
                midnight January 1st 1970 UTC.
            to_time (str): End time of data to return in YYYY-MM-DD HH:MM:SS format.
            includeconnections (bool): Adds a connections object which returns connections 
                blocked by a Darktrace RESPOND action.
            responsedata (str): When given the name of a top-level field or object, restricts 
                the returned JSON to only that field or object.
            pbid (int): Only return the Darktrace RESPOND actions created as a result of the 
                model breach with the specified ID.
            did (int): Device ID to filter actions for a specific device.
                
        Returns:
            dict or list: API response containing action data
            
        Notes:
            - Time parameters must always be specified in pairs
            - When fulldevicedetails=true, actions will be contained in an actions: object 
              and devices in a devices: object
            - active=true means the action has been activated, either by human confirmation 
              or automatically in fully autonomous mode
            - Actions manually cleared by a user will have the value cleared=true, expired 
              actions will have cleared=false
            - Manual Darktrace RESPOND/Network actions can be identified by "manual": true 
              in the response
        """
        endpoint = '/antigena'
          # Handle special parameter names for backwards compatibility
        if 'from_time' in params:
            params['from'] = params.pop('from_time')
        if 'to_time' in params:
            params['to'] = params.pop('to_time')
            
        # Get headers and sorted parameters for authentication
        headers, sorted_params = self._get_headers(endpoint, params)
        url = f"{self.client.host}{endpoint}"
        self.client._debug(f"GET {url} params={sorted_params}")
        
        response = requests.get(
            url,
            headers=headers,
            params=sorted_params,
            verify=False        )
        response.raise_for_status()
        return response.json()

    def activate_action(self, codeid: int, reason: str = "", duration: Optional[int] = None) -> dict:
        """
        Activate a pending Darktrace RESPOND action.
        
        This method changes the state of a RESPOND action from pending to active. Actions created 
        by models will have a default duration, defined by the "Darktrace RESPOND Action Duration" 
        setting on the model. If no duration value is provided, the action is activated for the 
        default time period.
        
        Args:
            codeid (int): Unique numeric identifier of a RESPOND action.
            reason (str, optional): Free text field to specify the action purpose. Required if 
                "Audit Antigena" setting is enabled on the Darktrace System Config page.
            duration (int, optional): Specify how long the action should be active for in seconds.
                
        Returns:
            bool: True if activation was successful, False otherwise.
            
        Example:
            # Activate action with default duration
            success = client.antigena.activate_action(123, reason="Suspicious activity detected")
            
            # Activate action with custom duration (10 minutes)
            success = client.antigena.activate_action(123, duration=600, reason="Extended monitoring")
        """
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        
        body: Dict[str, Any] = {
            "codeid": codeid, 
            "activate": True
        }
        
        if reason:
            body["reason"] = reason
        if duration is not None:
            body["duration"] = duration
            
        headers, sorted_params = self._get_headers(endpoint, json_body=body)
        self.client._debug(f"POST {url} body={body}")
        
        # Send JSON as raw data with consistent formatting (same as signature generation)
        json_data = json.dumps(body, separators=(',', ':'))
        response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()

    def extend_action(self, codeid: int, duration: int, reason: str = "") -> dict:
        """
        Extend an active Darktrace RESPOND action.
        
        The duration value defines the length the action should cover; a POST including this value 
        will cause the action duration to be changed. For example, if an action has 100 seconds 
        remaining, a POST request with "duration": 110 will extend the length of the action by 
        10 seconds. Conversely, a POST request with "duration": 10 will reduce the remaining time 
        to 10 seconds, causing the action to expire 90 seconds early.
        
        Args:
            codeid (int): Unique numeric identifier of a RESPOND action.
            duration (int): New total duration for the action in seconds. This should be the 
                current duration plus the amount the action should be extended for.
            reason (str, optional): Free text field to specify the extension purpose.
                
        Returns:
            bool: True if extension was successful, False otherwise.
            
        Warning:
            The duration parameter should be used carefully as it defines the total length 
            the action should cover, not the additional time to add.
            
        Example:
            # Extend action to run for total of 300 seconds
            success = client.antigena.extend_action(123, duration=300, reason="Extended monitoring")
        """
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        
        body: Dict[str, Any] = {
            "codeid": codeid, 
            "duration": duration
        }
        
        if reason:
            body["reason"] = reason
            
        headers, sorted_params = self._get_headers(endpoint, json_body=body)
        self.client._debug(f"POST {url} body={body}")
        
        # Send JSON as raw data with consistent formatting (same as signature generation)
        json_data = json.dumps(body, separators=(',', ':'))
        response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()

    def clear_action(self, codeid: int, reason: str = "") -> dict:
        """
        Clear an active, pending or expired Darktrace RESPOND action.
        
        Clearing an active action will also suppress the combination of Darktrace RESPOND action 
        and model breach conditions for the remainder of the time the action was active for. 
        The duration parameter does not impact the length that an action/condition combination 
        is cleared for.
        
        It is also possible to clear an expired action. Doing so will remove it from the returned 
        results unless includecleared is used.
        
        Args:
            codeid (int): Unique numeric identifier of a RESPOND action.
            reason (str, optional): Free text field to specify the clearing purpose.
                
        Returns:
            bool: True if clearing was successful, False otherwise.
            
        Example:
            # Clear an active action
            success = client.antigena.clear_action(123, reason="False positive confirmed")
        """
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        
        body: Dict[str, Any] = {
            "codeid": codeid, 
            "clear": True
        }
        
        if reason:
            body["reason"] = reason
            
        headers, sorted_params = self._get_headers(endpoint, json_body=body)
        self.client._debug(f"POST {url} body={body}")
        
        # Send JSON as raw data with consistent formatting (same as signature generation)
        json_data = json.dumps(body, separators=(',', ':'))
        response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()

    def reactivate_action(self, codeid: int, duration: int, reason: str = "") -> dict:
        """
        Reactivate a cleared or expired Darktrace RESPOND action.
        
        To reactivate a cleared or expired action, a duration must be supplied.
        
        Args:
            codeid (int): Unique numeric identifier of a RESPOND action.
            duration (int): Duration for the reactivated action in seconds. Required.
            reason (str, optional): Free text field to specify the reactivation purpose.
                
        Returns:
            bool: True if reactivation was successful, False otherwise.
            
        Example:
            # Reactivate a cleared action for 10 minutes
            success = client.antigena.reactivate_action(123, duration=600, reason="New evidence found")
        """
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"
        
        body: Dict[str, Any] = {
            "codeid": codeid, 
            "activate": True, 
            "duration": duration
        }
        
        if reason:
            body["reason"] = reason
            
        headers, sorted_params = self._get_headers(endpoint, json_body=body)
        self.client._debug(f"POST {url} body={body}")
        
        # Send JSON as raw data with consistent formatting (same as signature generation)
        json_data = json.dumps(body, separators=(',', ':'))
        response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()

    def create_manual_action(self, did: int, action: str, duration: int, reason: str = "", 
                           connections: Optional[List[Dict[str, Union[str, int]]]] = None) -> dict:
        """
        Create a manual Darktrace RESPOND/Network action.
        
        The /antigena/manual endpoint can be used to create manual Darktrace RESPOND/Network 
        actions from Darktrace Threat Visualizer 6+.
        
        Args:
            did (int): Identification number of a device modelled in the Darktrace system.
            action (str): The type of action to be created. Supported types:
                - 'connection': Block Matching Connections
                - 'pol': Enforce pattern of life
                - 'gpol': Enforce group pattern of life
                - 'quarantine': Quarantine device
                - 'quarantineOutgoing': Block all outgoing traffic
                - 'quarantineIncoming': Block all incoming traffic
            duration (int): The duration of the action in seconds.
            reason (str, optional): Free text field to specify the action purpose.
            connections (list, optional): An array of connection pairs to block against. 
                Only valid for the 'connection' action type. Each connection should be a dict with:
                - 'src' (str): IP or hostname of source endpoint
                - 'dst' (str): IP or hostname of destination endpoint  
                - 'port' (int, optional): Port for destination value
                
        Returns:
            int: The codeid (unique numeric ID) for the created action, or 0 if creation failed.
            
        Notes:
            - The action reason and the username associated with the API token will appear 
              in the action history in the Threat Visualizer
            - These values are also returned from /antigena as triggerer.username and 
              triggerer.reason
              
        Examples:
            # Create a quarantine action for 10 minutes
            codeid = client.antigena.create_manual_action(
                did=12, 
                action="quarantine", 
                duration=600, 
                reason="Suspicious activity detected"
            )
            
            # Create a connection blocking action
            codeid = client.antigena.create_manual_action(
                did=12, 
                action="connection", 
                duration=600,
                reason="Block malicious connections",
                connections=[
                    {"src": "10.10.10.10", "dst": "8.8.8.8"},
                    {"src": "10.10.10.10", "dst": "example.com", "port": 443}
                ]
            )
        """
        endpoint = '/antigena/manual'
        url = f"{self.client.host}{endpoint}"
        
        body: Dict[str, Any] = {
            "did": did, 
            "action": action, 
            "duration": duration,
            "reason": reason
        }
        
        if action == 'connection' and connections:
            body["connections"] = connections
            
        headers, sorted_params = self._get_headers(endpoint, json_body=body)
        self.client._debug(f"POST {url} body={body}")
        
        # Send JSON as raw data with consistent formatting (same as signature generation)
        json_data = json.dumps(body, separators=(',', ':'))
        response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        
        response.raise_for_status()
        return response.json()

    def get_summary(self, **params):
        """
        Get a summary of active and pending Darktrace RESPOND actions.
        
        The /summary extension of the /antigena endpoint is a simple summary of active and 
        pending Darktrace RESPOND actions. If a time window is not specified, the request 
        will return the state of actions now. If queried with a time window, the endpoint 
        will return information about active actions during that time window.
        
        Args:
            endtime (int): End time of data to return in millisecond format, relative to 
                midnight January 1st 1970 UTC.
            starttime (int): Start time of data to return in millisecond format, relative to 
                midnight January 1st 1970 UTC.
            responsedata (str): When given the name of a top-level field or object, restricts 
                the returned JSON to only that field or object.
                
        Returns:
            dict: Summary containing:
                - pendingCount (int): Number of pending actions
                - activeCount (int): Number of active actions  
                - pendingActionDevices (list): Device IDs with pending actions
                - activeActionDevices (list): Device IDs with active actions
                
        Notes:
            - This endpoint only identifies devices by their system id (did). This value can 
              be used to query /devices for more information
            - Historic information about which actions were pending at a given point in time 
              is not available from this endpoint
            - Pending action information is only returned if starttime/endtime parameters are 
              not specified, and is only valid for the time of query
            - Time parameters must always be specified in pairs
            - The endpoint will return information about all devices with active actions during 
              the timeframe - information about when those specific actions were active, and for 
              how long, is not included
            - A device may have more than one active or pending action against it - the number 
              of actions may therefore not match the total number of impacted devices
              
        Example:
            # Get current summary
            summary = client.antigena.get_summary()
            print(f"Active actions: {summary['activeCount']}")
            print(f"Pending actions: {summary['pendingCount']}")
            
            # Get summary for specific time window
            summary = client.antigena.get_summary(
                starttime=1667260800000,
                endtime=1667260860000
            )
        """
        endpoint = '/antigena/summary'
        
        # Get headers and sorted parameters for authentication
        headers, sorted_params = self._get_headers(endpoint, params)
        
        url = f"{self.client.host}{endpoint}"
        self.client._debug(f"GET {url} params={sorted_params}")
        
        response = requests.get(
            url, 
            headers=headers, 
            params=sorted_params, 
            verify=False
        )
        response.raise_for_status()
        return response.json()

    # Backwards compatibility methods (deprecated)
    def approve_action(self, code_id: int, reason: str = "", duration: int = 0) -> dict:
        """
        Deprecated: Use activate_action() instead.
        Approve/activate a pending Antigena action.
        """
        endpoint = '/antigena'
        url = f"{self.client.host}{endpoint}"

        body: Dict[str, Any] = {
            "codeid": code_id,
            "activate": True
        }

        if reason:
            body["reason"] = reason
        if duration > 0:
            body["duration"] = duration

        headers, sorted_params = self._get_headers(endpoint, json_body=body)
        self.client._debug(f"POST {url} body={body}")

        json_data = json.dumps(body, separators=(',', ':'))
        response = requests.post(url, headers=headers, params=sorted_params, data=json_data, verify=False)
        self.client._debug(f"Response Status: {response.status_code}")
        self.client._debug(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()