from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["MBComments"]


class MBComments(BaseEndpoint):
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
            comment_id (str, optional): Not supported by the API; raises ValueError. Use pbid/starttime/endtime/count.
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
        if comment_id:
            raise ValueError(
                "/mbcomments has no per-comment path in the API guide (the server returns a non-JSON error); "
                "filter with pbid=, starttime=/endtime= or count= instead."
            )
        endpoint = "/mbcomments"
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

        The API guide documents /mbcomments as GET only; comments are added with
        POST /modelbreaches/[pbid]/comments and a JSON body {"message": ...}
        (identical to ``client.breaches.add_comment``).

        Args:
            breach_id (str): Model breach ID (pbid).
            comment (str): Comment text to add.
            timeout (float or tuple, optional): Timeout for the request in seconds.
            **params: Ignored; the guide states this call takes no parameters.
        """
        endpoint = f"/modelbreaches/{breach_id}/comments"
        return self._post_json(endpoint, body={"message": comment}, timeout=timeout)
