from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["MBComments"]


class MBComments(BaseEndpoint):
    def __init__(self, client) -> None:
        super().__init__(client)

    def get(
        self,
        comment_id: str | None = None,
        starttime: int | None = None,
        endtime: int | None = None,
        responsedata: str | None = None,
        count: int | None = None,
        pbid: int | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
        """
        Get model breach comments or details for a specific comment.

        Args:
            comment_id (str, optional): Specific comment ID to retrieve. If not provided, returns all comments.
            starttime (int, optional): Start time (epoch ms) for comments to return.
            endtime (int, optional): End time (epoch ms) for comments to return.
            responsedata (str, optional): Restrict the returned JSON to only the specified field/object.
            count (int, optional): Number of comments to return (default 100).
            pbid (int, optional): Only return comments for the model breach with this ID.
            timeout (float or tuple, optional): Timeout for the request in seconds.
            **params: Additional query parameters.

        Returns:
            list or dict: Comments or comment details from Darktrace.
        """
        endpoint = f"/mbcomments{f'/{comment_id}' if comment_id else ''}"
        query_params = dict()
        if starttime is not None:
            query_params["starttime"] = starttime
        if endtime is not None:
            query_params["endtime"] = endtime
        if responsedata is not None:
            query_params["responsedata"] = responsedata
        if count is not None:
            query_params["count"] = count
        if pbid is not None:
            query_params["pbid"] = pbid
        query_params.update(params)
        return self._get(endpoint, params=query_params, timeout=timeout)

    def post(
        self,
        breach_id: str,
        comment: str,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict:
        """Add a comment to a model breach.

        Args:
            breach_id (str): Model breach ID.
            comment (str): Comment text to add.
            timeout (float or tuple, optional): Timeout for the request in seconds.
            **params: Additional parameters.
        """
        endpoint = "/mbcomments"
        body: dict[str, str] = {"breachid": breach_id, "comment": comment}
        body.update(params)
        return self._post_json(endpoint, body=body, timeout=timeout)
