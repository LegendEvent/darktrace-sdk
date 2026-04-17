from __future__ import annotations

from typing import Any

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["DeviceSummary"]


class DeviceSummary(BaseEndpoint):
    """
    Interface for the /devicesummary endpoint.
    Returns contextual information for a device, aggregated from /devices, /similardevices, /modelbreaches, /deviceinfo und /details.

    Parameters:
        did (int): Identification number of a device modelled in the Darktrace system. Required.
        device_name (str, optional): Device name.
        ip_address (str, optional): IP address.
        end_timestamp (int, optional): Epoch time for end of time range.
        start_timestamp (int, optional): Epoch time for start of time range.
        devicesummary_by (str, optional): Field to group summary by.
        devicesummary_by_value (str, optional): Value for grouping.
        device_type (str, optional): Device type filter.
        network_location (str, optional): Network location filter.
        network_location_id (str, optional): Network location ID filter.
        peer_id (str, optional): Peer device filter.
        source (str, optional): Source filter.
        status (str, optional): Device status filter.
        responsedata (str, optional): Restrict returned JSON to only this field/object.
        **kwargs: Additional API parameters (not in official docs).
    """

    def get(
        self,
        did: int,
        device_name: str | None = None,
        ip_address: str | None = None,
        end_timestamp: int | None = None,
        start_timestamp: int | None = None,
        devicesummary_by: str | None = None,
        devicesummary_by_value: str | None = None,
        device_type: str | None = None,
        network_location: str | None = None,
        network_location_id: str | None = None,
        peer_id: str | None = None,
        source: str | None = None,
        status: str | None = None,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **kwargs,
    ) -> dict | list:
        """
        Get device summary information for a specific device.

        Args:
            did (int): Device ID (required)
            device_name (str, optional): Device name
            ip_address (str, optional): IP address
            end_timestamp (int, optional): Epoch time for end of time range
            start_timestamp (int, optional): Epoch time for start of time range
            devicesummary_by (str, optional): Field to group summary by
            devicesummary_by_value (str, optional): Value for grouping
            device_type (str, optional): Device type filter
            network_location (str, optional): Network location filter
            network_location_id (str, optional): Network location ID filter
            peer_id (str, optional): Peer device filter
            source (str, optional): Source filter
            status (str, optional): Device status filter
            responsedata (str, optional): Restrict returned JSON to only this field/object
            **kwargs: Any additional parameters (not in official docs)

        Returns:
            dict: API response
        """
        endpoint = "/devicesummary"
        params: dict[str, Any] = {"did": did}
        if device_name is not None:
            params["device_name"] = device_name
        if ip_address is not None:
            params["ip_address"] = ip_address
        if end_timestamp is not None:
            params["end_timestamp"] = end_timestamp
        if start_timestamp is not None:
            params["start_timestamp"] = start_timestamp
        if devicesummary_by is not None:
            params["devicesummary_by"] = devicesummary_by
        if devicesummary_by_value is not None:
            params["devicesummary_by_value"] = devicesummary_by_value
        if device_type is not None:
            params["device_type"] = device_type
        if network_location is not None:
            params["network_location"] = network_location
        if network_location_id is not None:
            params["network_location_id"] = network_location_id
        if peer_id is not None:
            params["peer_id"] = peer_id
        if source is not None:
            params["source"] = source
        if status is not None:
            params["status"] = status
        if responsedata is not None:
            params["responsedata"] = responsedata
        params.update(kwargs)
        return self._get(endpoint, params=params, timeout=timeout)
