from typing import Optional
from urllib.parse import urlparse

import requests

from .auth import DarktraceAuth
from .dt_advanced_search import AdvancedSearch
from .dt_analyst import Analyst
from .dt_antigena import Antigena
from .dt_breaches import ModelBreaches
from .dt_components import Components
from .dt_cves import CVEs
from .dt_details import Details
from .dt_devices import Devices
from .dt_deviceinfo import DeviceInfo
from .dt_devicesearch import DeviceSearch
from .dt_devicesummary import DeviceSummary
from .dt_email import DarktraceEmail
from .dt_endpointdetails import EndpointDetails
from .dt_enums import Enums
from .dt_filtertypes import FilterTypes
from .dt_intelfeed import IntelFeed
from .dt_mbcomments import MBComments
from .dt_metricdata import MetricData
from .dt_metrics import Metrics
from .dt_models import Models
from .dt_network import Network
from .dt_pcaps import PCAPs
from .dt_similardevices import SimilarDevices
from .dt_status import Status
from .dt_subnets import Subnets
from .dt_summarystatistics import SummaryStatistics
from .dt_tags import Tags
from .dt_utils import debug_print, TimeoutType

# Allowed URL schemes - block dangerous ones for SSRF protection
# Note: Private IPs are ALLOWED because Darktrace runs on baremetal in enterprises
_ALLOWED_SCHEMES = frozenset({"http", "https"})


class DarktraceClient:
    host: str
    auth: DarktraceAuth
    debug: bool
    verify_ssl: bool
    timeout: TimeoutType
    advanced_search: "AdvancedSearch"
    antigena: "Antigena"
    analyst: "Analyst"
    breaches: "ModelBreaches"
    components: "Components"
    cves: "CVEs"
    details: "Details"
    deviceinfo: "DeviceInfo"
    devices: "Devices"
    devicesearch: "DeviceSearch"
    devicesummary: "DeviceSummary"
    email: "DarktraceEmail"
    endpointdetails: "EndpointDetails"
    enums: "Enums"
    filtertypes: "FilterTypes"
    intelfeed: "IntelFeed"
    mbcomments: "MBComments"
    metricdata: "MetricData"
    metrics: "Metrics"
    models: "Models"
    network: "Network"
    pcaps: "PCAPs"
    similardevices: "SimilarDevices"
    status: "Status"
    subnets: "Subnets"
    summarystatistics: "SummaryStatistics"
    tags: "Tags"

    def __init__(
        self,
        host: str,
        public_token: str,
        private_token: str,
        debug: bool = False,
        verify_ssl: bool = True,
        timeout: TimeoutType = None,
    ) -> None:
        """
        Initialize the Darktrace API client.

        Args:
            host (str): The Darktrace instance hostname (e.g., 'https://example.darktrace.com')
            public_token (str): Your Darktrace API public token
            private_token (str): Your Darktrace API private token
            debug (bool, optional): Enable debug logging. Defaults to False.
            verify_ssl (bool, optional): Enable SSL certificate verification. Defaults to True.
                Set to False only for development/testing with self-signed certificates.
            timeout (float|tuple, optional): Request timeout in seconds. Can be a single float
                or a tuple of (connect_timeout, read_timeout). None means no timeout (default).

        Example:
            >>> client = DarktraceClient(
            ...     host="https://your-instance.darktrace.com",
            ...     public_token="your_public_token",
            ...     private_token="your_private_token",
            ...     debug=True
            ... )

            >>> # With timeout
            >>> client = DarktraceClient(
            ...     host="https://your-instance.darktrace.com",
            ...     public_token="your_public_token",
            ...     private_token="your_private_token",
            ...     timeout=30  # 30 second timeout for all requests
            ... )
        """

        # Validate and set host URL
        self.host = self._validate_url(host)
        self.auth = DarktraceAuth(public_token, private_token)
        self.debug = debug
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self._session: requests.Session = requests.Session()
        # Endpoint groups
        self.advanced_search = AdvancedSearch(self)
        self.antigena = Antigena(self)
        self.analyst = Analyst(self)
        self.breaches = ModelBreaches(self)
        self.components = Components(self)
        self.cves = CVEs(self)
        self.details = Details(self)
        self.deviceinfo = DeviceInfo(self)
        self.devices = Devices(self)
        self.devicesearch = DeviceSearch(self)
        self.devicesummary = DeviceSummary(self)
        self.email = DarktraceEmail(self)
        self.endpointdetails = EndpointDetails(self)
        self.enums = Enums(self)
        self.filtertypes = FilterTypes(self)
        self.intelfeed = IntelFeed(self)
        self.mbcomments = MBComments(self)
        self.metricdata = MetricData(self)
        self.metrics = Metrics(self)
        self.models = Models(self)
        self.network = Network(self)
        self.pcaps = PCAPs(self)
        self.similardevices = SimilarDevices(self)
        self.status = Status(self)
        self.subnets = Subnets(self)
        self.summarystatistics = SummaryStatistics(self)
        self.tags = Tags(self)

    def _debug(self, message: str):
        debug_print(message, self.debug)

    def _validate_url(self, host: str) -> str:
        """Validate and normalize the host URL.

        Blocks dangerous URL schemes while allowing all HTTP/HTTPS targets
        including private IPs (valid for enterprise baremetal deployments).

        Args:
            host: The host URL to validate

        Returns:
            Normalized host URL with scheme

        Raises:
            ValueError: If URL uses a blocked scheme
        """
        # Parse URL first to check scheme
        parsed = urlparse(host)

        # If no scheme, add https:// and re-parse
        if not parsed.scheme:
            host = f"https://{host}"
            parsed = urlparse(host)

        scheme = parsed.scheme.lower()

        if scheme not in _ALLOWED_SCHEMES:
            allowed = ", ".join(sorted(_ALLOWED_SCHEMES))
            raise ValueError(
                f"Invalid URL scheme '{scheme}'. "
                f"Allowed schemes: {allowed}. "
                f"Host must use HTTP or HTTPS."
            )

        return host.rstrip("/")

    def close(self) -> None:
        """Close the underlying requests session to free resources."""
        self._session.close()

    def __enter__(self) -> "DarktraceClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - closes session."""
        self.close()
