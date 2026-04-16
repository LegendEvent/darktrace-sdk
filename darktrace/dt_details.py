from __future__ import annotations

from .dt_utils import _UNSET, BaseEndpoint

__all__ = ["Details"]


class Details(BaseEndpoint):
    def get(
        self,
        did: int | None = None,
        pbid: int | None = None,
        msg: str | None = None,
        blockedconnections: str | None = None,
        eventtype: str = "connection",
        count: int | None = None,
        starttime: int | None = None,
        endtime: int | None = None,
        from_: str | None = None,
        to: str | None = None,
        applicationprotocol: str | None = None,
        destinationport: int | None = None,
        sourceport: int | None = None,
        port: int | None = None,
        protocol: str | None = None,
        ddid: int | None = None,
        odid: int | None = None,
        externalhostname: str | None = None,
        intext: str | None = None,
        uid: str | None = None,
        deduplicate: bool = False,
        fulldevicedetails: bool = False,
        responsedata: str | None = None,
        timeout: float | tuple[float, float] | None = _UNSET,
        **params,
    ) -> dict | list:
        """
        Get detailed connection and event information for a device or entity.

        Parameters:
            did (int, optional): Device ID to filter data for.
            pbid (int, optional): Model breach ID to filter data for.
            msg (str, optional): Message field value for notice events.
            blockedconnections (str, optional): Filter for RESPOND/Network attempted actions. Valid: 'all', 'failed', 'true'.
            eventtype (str, optional): Event type to return. One of: 'connection', 'unusualconnection', 'newconnection', 'notice', 'devicehistory', 'modelbreach'. Default: 'connection'.
            count (int, optional): Maximum number of items to return. Cannot be used with from_ or starttime.
            starttime (int, optional): Start time in ms since epoch. Must be paired with endtime.
            endtime (int, optional): End time in ms since epoch. Must be paired with starttime.
            from_ (str, optional): Start time in 'YYYY-MM-DD HH:MM:SS' format. Must be paired with to.
            to (str, optional): End time in 'YYYY-MM-DD HH:MM:SS' format. Must be paired with from_.
            applicationprotocol (str, optional): Filter by application protocol (see /enums).
            destinationport (int, optional): Filter by destination port.
            sourceport (int, optional): Filter by source port.
            port (int, optional): Filter by source or destination port.
            protocol (str, optional): Filter by IP protocol (see /enums).
            ddid (int, optional): Destination device ID.
            odid (int, optional): Other device ID.
            externalhostname (str, optional): Filter by external hostname.
            intext (str, optional): Filter for internal/external ('internal' or 'external').
            uid (str, optional): Connection UID to return.
            deduplicate (bool, optional): Only one equivalent connection per hour.
            fulldevicedetails (bool, optional): Return full device detail objects.
            responsedata (str, optional): Restrict returned JSON to only this field/object.
            **params: Any additional query parameters.

        Notes:
            - At least one of did, pbid, msg, or blockedconnections is required.
            - Time parameters must always be specified in pairs.
            - If from_ or starttime is used, count must not be used.
        """
        endpoint = "/details"
        # --- Parameter validation logic ---
        # At least one of did, pbid, msg, or blockedconnections is required
        if not any([did, pbid, msg, blockedconnections]):
            raise ValueError("At least one of did, pbid, msg, or blockedconnections must be specified.")

        # Time parameter validation
        # starttime/endtime must be both present or both absent
        if (starttime is not None) ^ (endtime is not None):
            raise ValueError("Both starttime and endtime must be specified together.")
        # from_/to must be both present or both absent
        if (from_ is not None) ^ (to is not None):
            raise ValueError("Both from_ and to must be specified together.")
        # count cannot be used with from_/to or starttime/endtime
        if count is not None and (from_ is not None or starttime is not None):
            raise ValueError("count cannot be used with from_/to or starttime/endtime.")

        # Map all parameters to API names
        if did is not None:
            params["did"] = did
        if pbid is not None:
            params["pbid"] = pbid
        if msg is not None:
            params["msg"] = msg
        if blockedconnections is not None:
            params["blockedconnections"] = blockedconnections
        if eventtype is not None:
            params["eventtype"] = eventtype
        if count is not None:
            params["count"] = count
        if starttime is not None:
            params["starttime"] = starttime
        if endtime is not None:
            params["endtime"] = endtime
        if from_ is not None:
            params["from"] = from_
        if to is not None:
            params["to"] = to
        if applicationprotocol is not None:
            params["applicationprotocol"] = applicationprotocol
        if destinationport is not None:
            params["destinationport"] = destinationport
        if sourceport is not None:
            params["sourceport"] = sourceport
        if port is not None:
            params["port"] = port
        if protocol is not None:
            params["protocol"] = protocol
        if ddid is not None:
            params["ddid"] = ddid
        if odid is not None:
            params["odid"] = odid
        if externalhostname is not None:
            params["externalhostname"] = externalhostname
        if intext is not None:
            params["intext"] = intext
        if uid is not None:
            params["uid"] = uid
        if deduplicate:
            params["deduplicate"] = str(deduplicate).lower()
        if fulldevicedetails:
            params["fulldevicedetails"] = str(fulldevicedetails).lower()
        if responsedata is not None:
            params["responsedata"] = responsedata

        return self._get(endpoint, params=params, timeout=timeout)
