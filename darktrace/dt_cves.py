from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["CVEs"]


class CVEs(BaseEndpoint):
    def get(
        self,
        did: int | None = None,
        fulldevicedetails: bool | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
        """
        Retrieve CVE information for devices from the Darktrace/OT ICS Vulnerability Tracker.

        Parameters:
            did (int, optional): Device ID to filter CVEs for a specific device.
            fulldevicedetails (bool, optional): If True, returns full device detail objects for all referenced devices.
            **params: Additional API parameters.

        Returns:
            dict: JSON response from the /cves endpoint.

        Example usage:
            client.cves.get()
            client.cves.get(did=12, fulldevicedetails=True)
        """
        if did is not None:
            params["did"] = did
        if fulldevicedetails is not None:
            params["fulldevicedetails"] = "true" if fulldevicedetails else "false"
        return self._get("/cves", params=params if params else None, timeout=timeout)
