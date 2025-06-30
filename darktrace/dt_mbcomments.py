import requests
import json
from typing import Optional, Dict, Any
from .dt_utils import debug_print, BaseEndpoint

class MBComments(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def get(self,
            comment_id: Optional[str] = None,
            starttime: Optional[int] = None,
            endtime: Optional[int] = None,
            responsedata: Optional[str] = None,
            count: Optional[int] = None,
            pbid: Optional[int] = None,
            **params
    ):
        """
        Get model breach comments or details for a specific comment.

        Args:
            comment_id (str, optional): Specific comment ID to retrieve. If not provided, returns all comments.
            starttime (int, optional): Start time (epoch ms) for comments to return.
            endtime (int, optional): End time (epoch ms) for comments to return.
            responsedata (str, optional): Restrict the returned JSON to only the specified field/object.
            count (int, optional): Number of comments to return (default 100).
            pbid (int, optional): Only return comments for the model breach with this ID.
            **params: Additional query parameters.

        Returns:
            list or dict: Comments or comment details from Darktrace.
        """
        endpoint = f'/mbcomments{f"/{comment_id}" if comment_id else ""}'
        url = f"{self.client.host}{endpoint}"
        query_params = dict()
        if starttime is not None:
            query_params['starttime'] = starttime
        if endtime is not None:
            query_params['endtime'] = endtime
        if responsedata is not None:
            query_params['responsedata'] = responsedata
        if count is not None:
            query_params['count'] = count
        if pbid is not None:
            query_params['pbid'] = pbid
        query_params.update(params)
        headers, sorted_params = self._get_headers(endpoint, query_params)
        self.client._debug(f"GET {url} params={sorted_params}")
        response = requests.get(url, headers=headers, params=sorted_params, verify=False)
        response.raise_for_status()
        return response.json()

    def post(self, breach_id: str, comment: str, **params):
        """Add a comment to a model breach."""
        endpoint = '/mbcomments'
        url = f"{self.client.host}{endpoint}"
        data: Dict[str, Any] = {'breachid': breach_id, 'comment': comment}
        data.update(params)
        headers, sorted_params = self._get_headers(endpoint, json_body=data)
        headers['Content-Type'] = 'application/json'
        self.client._debug(f"POST {url} data={data}")
        response = requests.post(url, headers=headers, data=json.dumps(data, separators=(',', ':')), verify=False)
        self.client._debug(f"Response status: {response.status_code}")
        self.client._debug(f"Response text: {response.text}")
        response.raise_for_status()
        return response.json() 