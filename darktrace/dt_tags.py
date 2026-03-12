import requests
from typing import Optional, Union, Tuple
from .dt_utils import debug_print, BaseEndpoint, _UNSET


class Tags(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    # TAGS ENDPOINT
    def get(
        self,
        tag_id: Optional[str] = None,
        tag: Optional[str] = None,
        responsedata: Optional[str] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,  # type: ignore[assignment]
    ):
        """
        Get tag information from Darktrace.

        Args:
            tag_id (str, optional): Tag ID (tid) to retrieve a specific tag by ID (e.g., /tags/5).
            tag (str, optional): Name of an existing tag (e.g., /tags?tag=active threat).
            responsedata (str, optional): Restrict the returned JSON to only the specified field or object.
            timeout (float or tuple, optional): Request timeout in seconds.

        Returns:
            dict or list: Tag information from Darktrace.
        """
        endpoint = f"/tags{f'/{tag_id}' if tag_id else ''}"
        url = f"{self.client.host}{endpoint}"

        params = dict()
        if tag is not None:
            params["tag"] = tag
        if responsedata is not None:
            params["responsedata"] = responsedata

        headers, sorted_params = self._get_headers(endpoint, params)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "GET",
            url,
            headers=headers,
            params=sorted_params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def create(
        self,
        name: str,
        color: Optional[int] = None,
        description: Optional[str] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ):  # type: ignore[assignment]
        """
        Create a new tag in Darktrace.

        Args:
            name (str): Name for the created tag (required).
            color (int, optional): The hue value (in HSL) for the tag in the UI.
            description (str, optional): Optional description for the tag.
            timeout (float or tuple, optional): Request timeout in seconds.

        Returns:
            dict: The created tag information from Darktrace.
        """
        endpoint = "/tags"
        url = f"{self.client.host}{endpoint}"
        body = {"name": name, "data": {}}
        if color is not None:
            body["data"]["color"] = color
        if description is not None:
            body["data"]["description"] = description

        headers, _ = self._get_headers(endpoint)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "POST",
            url,
            headers=headers,
            json=body,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def delete(
        self, tag_id: str, timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET
    ) -> dict:  # type: ignore[assignment]
        """
        Delete a tag by tag ID (tid).

        Args:
            tag_id (str): Tag ID (tid) to delete (e.g., /tags/5).
            timeout (float or tuple, optional): Request timeout in seconds.

        Returns:
            dict: The response from the Darktrace API.
        """
        endpoint = f"/tags/{tag_id}"
        url = f"{self.client.host}{endpoint}"
        headers, _ = self._get_headers(endpoint)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "DELETE",
            url,
            headers=headers,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    # TAGS/ENTITIES ENDPOINT

    def get_entities(
        self,
        did: Optional[int] = None,
        tag: Optional[str] = None,
        responsedata: Optional[str] = None,
        fulldevicedetails: Optional[bool] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ):  # type: ignore[assignment]
        """
        Get tags for a device or devices for a tag via /tags/entities.

        Args:
            did (int, optional): Device ID to list tags for a device.
            tag (str, optional): Name of an existing tag to list devices for a tag.
            responsedata (str, optional): Restrict the returned JSON to only the specified field or object.
            fulldevicedetails (bool, optional): If true and a tag is queried, adds a devices object to the response with more detailed device data.
            timeout (float or tuple, optional): Request timeout in seconds.

        Returns:
            list or dict: Tag or device information from Darktrace.
        """
        endpoint = "/tags/entities"
        url = f"{self.client.host}{endpoint}"
        params = dict()
        if did is not None:
            params["did"] = did
        if tag is not None:
            params["tag"] = tag
        if responsedata is not None:
            params["responsedata"] = responsedata
        if fulldevicedetails is not None:
            params["fulldevicedetails"] = fulldevicedetails
        headers, sorted_params = self._get_headers(endpoint, params)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "GET",
            url,
            headers=headers,
            params=sorted_params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def post_entities(
        self,
        did: int,
        tag: str,
        duration: Optional[int] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ):  # type: ignore[assignment]
        """
        Add a tag to a device via /tags/entities (POST, form-encoded).

        Args:
            did (int): Device ID to tag.
            tag (str): Name of the tag to add.
            duration (int, optional): How long the tag should be set for the device (seconds).
            timeout (float or tuple, optional): Request timeout in seconds.

        Returns:
            dict: API response from Darktrace.
        """
        endpoint = "/tags/entities"
        url = f"{self.client.host}{endpoint}"
        data = {"did": did, "tag": tag}
        if duration is not None:
            data["duration"] = duration
        headers, _ = self._get_headers(endpoint)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "POST",
            url,
            headers=headers,
            data=data,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def delete_entities(
        self,
        did: int,
        tag: str,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> dict:  # type: ignore[assignment]
        """
        Remove a tag from a device via /tags/entities (DELETE).

        Args:
            did (int): Device ID to untag.
            tag (str): Name of the tag to remove.
            timeout (float or tuple, optional): Request timeout in seconds.

        Returns:
            dict: The response from the Darktrace API.
        """
        endpoint = "/tags/entities"
        url = f"{self.client.host}{endpoint}"
        params = {"did": did, "tag": tag}
        headers, sorted_params = self._get_headers(endpoint, params)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "DELETE",
            url,
            headers=headers,
            params=sorted_params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

        # /tags/[tid]/entities ENDPOINT

    def get_tag_entities(
        self,
        tid: int,
        responsedata: Optional[str] = None,
        fulldevicedetails: Optional[bool] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ):  # type: ignore[assignment]
        """
        Get entities (devices or credentials) associated with a specific tag via /tags/[tid]/entities (GET).

        Args:
            tid (int): Tag ID (tid) to query.
            responsedata (str, optional): Restrict the returned JSON to only the specified field or object.
            fulldevicedetails (bool, optional): If true, adds a devices object to the response with more detailed device data.
            timeout (float or tuple, optional): Request timeout in seconds.

        Returns:
            list or dict: Entities associated with the tag from Darktrace.
        """
        endpoint = f"/tags/{tid}/entities"
        url = f"{self.client.host}{endpoint}"
        params = dict()
        if responsedata is not None:
            params["responsedata"] = responsedata
        if fulldevicedetails is not None:
            params["fulldevicedetails"] = fulldevicedetails
        headers, sorted_params = self._get_headers(endpoint, params)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "GET",
            url,
            headers=headers,
            params=sorted_params,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def post_tag_entities(
        self,
        tid: int,
        entityType: str,
        entityValue,
        expiryDuration: Optional[int] = None,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ):  # type: ignore[assignment]
        """
        Add a tag to one or more entities (device or credential) via /tags/[tid]/entities (POST, JSON body).

        Args:
            tid (int): Tag ID (tid) to apply.
            entityType (str): The type of entity to be tagged. Valid values: 'Device', 'Credential'.
            entityValue (str or list): For devices, the did (as string or list of strings). For credentials, the credential value(s).
            expiryDuration (int, optional): Duration in seconds the tag should be applied for.
            timeout (float or tuple, optional): Request timeout in seconds.

        Returns:
            dict: API response from Darktrace.
        """
        endpoint = f"/tags/{tid}/entities"
        url = f"{self.client.host}{endpoint}"
        body = {"entityType": entityType, "entityValue": entityValue}
        if expiryDuration is not None:
            body["expiryDuration"] = expiryDuration
        headers, _ = self._get_headers(endpoint)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "POST",
            url,
            headers=headers,
            json=body,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()

    def delete_tag_entity(
        self,
        tid: int,
        teid: int,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> dict:  # type: ignore[assignment]
        """
        Remove a tag from an entity via /tags/[tid]/entities/[teid] (DELETE).

        Args:
            tid (int): Tag ID (tid).
            teid (int): Tag entity ID (teid) representing the tag-to-entity relationship.
            timeout (float or tuple, optional): Request timeout in seconds.

        Returns:
            dict: The response from the Darktrace API.
        """
        endpoint = f"/tags/{tid}/entities/{teid}"
        url = f"{self.client.host}{endpoint}"
        headers, _ = self._get_headers(endpoint)
        resolved_timeout = self._resolve_timeout(timeout)
        response = self._make_request(
            "DELETE",
            url,
            headers=headers,
            verify=self.client.verify_ssl,
            timeout=resolved_timeout,
        )
        response.raise_for_status()
        return response.json()
