from typing import Any, Dict, Optional, Tuple, Union

from .dt_utils import _UNSET, BaseEndpoint, encode_query

__all__ = ["AdvancedSearch"]


class AdvancedSearch(BaseEndpoint):
    def __init__(self, client):
        super().__init__(client)

    def search(
        self,
        query: Dict[str, Any],
        post_request: bool = False,
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
        """Perform Advanced Search query.

        Parameters:
            query: Dictionary containing the search query parameters
            post_request: If True, use POST method (6.1+), otherwise GET method

        Returns:
            dict: Search results from Darktrace Advanced Search API
        """
        endpoint = "/advancedsearch/api/search"

        if post_request:
            # For POST requests (6.1+), we need to create the full Advanced Search structure
            # and encode it as base64, then send it as {"hash": "encoded_string"}

            # Build the complete Advanced Search query structure
            full_query = {
                "search": query.get("search", ""),
                "fields": query.get("fields", []),
                "offset": query.get("offset", 0),
                "timeframe": query.get("timeframe", "3600"),  # Default 1 hour
                "time": query.get("time", {"user_interval": 0}),
            }

            # If custom timeframe is used, ensure proper time structure
            if "from" in query and "to" in query:
                full_query["timeframe"] = "custom"
                full_query["time"] = {
                    "from": query["from"],
                    "to": query["to"],
                    "user_interval": "0",
                }
            elif "starttime" in query and "endtime" in query:
                full_query["timeframe"] = "custom"
                full_query["time"] = {
                    "from": query["starttime"],
                    "to": query["endtime"],
                    "user_interval": "0",
                }
            elif "interval" in query:
                full_query["timeframe"] = str(query["interval"])

            # Encode the complete query structure
            encoded_query = encode_query(full_query)

            # Use POST request with JSON body containing the hash
            body = {"hash": encoded_query}
            return self._post_json(endpoint, body=body, timeout=timeout)
        else:
            # Use GET request (traditional method) - encode the full query structure
            full_query = {
                "search": query.get("search", ""),
                "fields": query.get("fields", []),
                "offset": query.get("offset", 0),
                "timeframe": query.get("timeframe", "3600"),
            }

            # Handle custom timeframes for GET as well
            if "from" in query and "to" in query:
                full_query["timeframe"] = "custom"
                full_query["time"] = {
                    "from": query["from"],
                    "to": query["to"],
                    "user_interval": "0",
                }
            elif "interval" in query:
                full_query["timeframe"] = str(query["interval"])
            else:
                # Use default time structure if no custom timeframe specified
                full_query["time"] = query.get("time", {"user_interval": 0})

            encoded_query = encode_query(full_query)
            return self._get(f"{endpoint}/{encoded_query}", timeout=timeout)

    def analyze(
        self,
        field: str,
        analysis_type: str,
        query: Dict[str, Any],
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
        """Analyze field data."""
        encoded_query = encode_query(query)
        endpoint = f"/advancedsearch/api/analyze/{field}/{analysis_type}/{encoded_query}"
        return self._get(endpoint, timeout=timeout)

    def graph(
        self,
        graph_type: str,
        interval: int,
        query: Dict[str, Any],
        timeout: Optional[Union[float, Tuple[float, float]]] = _UNSET,
    ) -> Any:
        """Get graph data."""
        encoded_query = encode_query(query)
        endpoint = f"/advancedsearch/api/graph/{graph_type}/{interval}/{encoded_query}"
        return self._get(endpoint, timeout=timeout)
