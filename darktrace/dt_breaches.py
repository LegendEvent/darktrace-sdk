from __future__ import annotations

from typing import Any

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["ModelBreaches"]


class ModelBreaches(BaseEndpoint):
    """Model breach alerts endpoint (/modelbreaches).

    Retrieve, acknowledge, unacknowledge, and comment on Darktrace model breach alerts.
    """

    def get(
        self,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
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
        endpoint = "/modelbreaches"

        if "from_time" in params:
            params["from"] = params.pop("from_time")
        if "to_time" in params:
            params["to"] = params.pop("to_time")

        # Support multiple saasfilter values
        if "saasfilter" in params and isinstance(params["saasfilter"], list):
            saasfilters = params.pop("saasfilter")
            params_list = list(params.items()) + [("saasfilter", v) for v in saasfilters]
        else:
            params_list = list(params.items())

        return self._get(endpoint, params=dict(params_list), timeout=timeout)

    def get_comments(
        self,
        pbid: int | list,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
        """
        Get comments for a specific model breach alert.

        Args:
            pbid (int or list of int): Policy breach ID(s) of the model breach(es).
            responsedata (str, optional): Restrict response to specific fields.
        Returns:
            list or dict: List of comment objects (see API docs for schema), or dict mapping pbid to comments if pbid is a list.
        """
        if isinstance(pbid, (list, tuple)):
            return {str(single_pbid): self.get_comments(single_pbid, timeout=timeout, **params) for single_pbid in pbid}
        endpoint = f"/modelbreaches/{pbid}/comments"
        return self._get(endpoint, params=params, timeout=timeout)

    def add_comment(
        self,
        pbid: int,
        message: str,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict:
        """
        Add a comment to a model breach alert.

        Args:
            pbid (int): Policy breach ID of the model breach.
            message (str): The comment text to add.
            params: Additional API parameters (e.g., responsedata).
        Returns:
            dict: The full JSON response from Darktrace
        """
        endpoint = f"/modelbreaches/{pbid}/comments"
        body: dict[str, Any] = {"message": message}
        return self._post_json(endpoint, body, params=params, timeout=timeout)

    def acknowledge(
        self,
        pbid: int | list,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict:
        """
        Acknowledge a model breach alert.

        Args:
            pbid (int or list of int): Policy breach ID(s) of the model breach(es).
            params: Additional API parameters.
        Returns:
            dict: The full JSON response from Darktrace, or a dict mapping pbid to response if pbid is a list.
        """
        if isinstance(pbid, (list, tuple)):
            return {single_pbid: self.acknowledge(single_pbid, timeout=timeout, **params) for single_pbid in pbid}
        endpoint = f"/modelbreaches/{pbid}/acknowledge"
        body: dict[str, bool] = {"acknowledge": True}
        return self._post_json(endpoint, body, params=params, timeout=timeout)

    def unacknowledge(
        self,
        pbid: int | list,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict:
        """
        Unacknowledge a model breach alert.

        Args:
            pbid (int or list of int): Policy breach ID(s) of the model breach(es).
            params: Additional API parameters.
        Returns:
            dict: The full JSON response from Darktrace, or a dict mapping pbid to response if pbid is a list.
        """
        if isinstance(pbid, (list, tuple)):
            return {single_pbid: self.unacknowledge(single_pbid, timeout=timeout, **params) for single_pbid in pbid}
        endpoint = f"/modelbreaches/{pbid}/unacknowledge"
        body: dict[str, bool] = {"unacknowledge": True}
        return self._post_json(endpoint, body, params=params, timeout=timeout)

    def acknowledge_with_comment(
        self,
        pbid: int,
        message: str,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict:
        """
        Acknowledge a model breach and add a comment in one call.

        Args:
            pbid (int): Policy breach ID of the model breach.
            message (str): The comment text to add.
            params: Additional parameters for the API call.

        Returns:
            dict: Contains the responses from both acknowledge and add_comment.
        """
        ack_response = self.acknowledge(pbid, timeout=timeout, **params)
        comment_response = self.add_comment(pbid, message, timeout=timeout, **params)
        return {"acknowledge": ack_response, "add_comment": comment_response}

    def unacknowledge_with_comment(
        self,
        pbid: int,
        message: str,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict:
        """
        Unacknowledge a model breach and add a comment in one call.

        Args:
            pbid (int): Policy breach ID of the model breach.
            message (str): The comment text to add.
            params: Additional parameters for the API call.

        Returns:
            dict: Contains the responses from both unacknowledge and add_comment.
        """
        unack_response = self.unacknowledge(pbid, timeout=timeout, **params)
        comment_response = self.add_comment(pbid, message, timeout=timeout, **params)
        return {"unacknowledge": unack_response, "add_comment": comment_response}
