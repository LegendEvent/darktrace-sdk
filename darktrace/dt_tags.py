import requests
from typing import Optional
from .dt_utils import debug_print, BaseEndpoint

class Tags(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self,
            tag_id: Optional[str] = None,
            tag: Optional[str] = None,
            responsedata: Optional[str] = None
        ):
        """
        Get tag information from Darktrace.

        Args:
            tag_id (str, optional): Tag ID (tid) to retrieve a specific tag by ID (e.g., /tags/5).
            tag (str, optional): Name of an existing tag (e.g., /tags?tag=active threat).
            responsedata (str, optional): Restrict the returned JSON to only the specified field or object.

        Returns:
            dict or list: Tag information from Darktrace.
        """
        endpoint = f'/tags{f"/{tag_id}" if tag_id else ""}'
        url = f"{self.client.host}{endpoint}"

        params = dict()
        if tag is not None:
            params['tag'] = tag
        if responsedata is not None:
            params['responsedata'] = responsedata

        headers, sorted_params = self._get_headers(endpoint, params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def create(self, name: str, color: Optional[int] = None, description: Optional[str] = None):
        """
        Create a new tag in Darktrace.

        Args:
            name (str): Name for the created tag (required).
            color (int, optional): The hue value (in HSL) for the tag in the UI.
            description (str, optional): Optional description for the tag.

        Returns:
            dict: The created tag information from Darktrace.
        """
        endpoint = '/tags'
        url = f"{self.client.host}{endpoint}"
        body = {"name": name, "data": {}}
        if color is not None:
            body["data"]["color"] = color
        if description is not None:
            body["data"]["description"] = description

        headers, _ = self._get_headers(endpoint)
        self.client._debug(f"POST {url} body={body}")
        response = requests.post(url, headers=headers, json=body, verify=False)
        response.raise_for_status()
        return response.json()

    def delete(self, tag_id: str):
        """
        Delete a tag by tag ID (tid).

        Args:
            tag_id (str): Tag ID (tid) to delete (e.g., /tags/5).

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        endpoint = f'/tags/{tag_id}'
        url = f"{self.client.host}{endpoint}"
        headers, _ = self._get_headers(endpoint)
        self.client._debug(f"DELETE {url}")
        response = requests.delete(url, headers=headers, verify=False)
        if response.status_code == 200:
            return True
        response.raise_for_status()
        return False