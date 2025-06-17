from .auth import DarktraceAuth
from .dt_antigena import Antigena
from .dt_analyst import Analyst
from .dt_breaches import ModelBreaches
from .dt_devices import Devices
from .dt_email import DarktraceEmail
from .dt_utils import debug_print
from .dt_advanced_search import AdvancedSearch
from .dt_components import Components
from .dt_cves import CVEs
from .dt_details import Details
from .dt_deviceinfo import DeviceInfo
from .dt_devicesearch import DeviceSearch
from .dt_devicesummary import DeviceSummary
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

class DarktraceClient:
    def __init__(self, host: str, public_token: str, private_token: str, debug: bool = False):
        self.host = host.rstrip('/')
        self.auth = DarktraceAuth(public_token, private_token)
        self.debug = debug
        
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