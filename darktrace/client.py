from .auth import DarktraceAuth
from .dt_antigena import Antigena
from .dt_analyst import Analyst
from .dt_breaches import ModelBreaches
from .dt_devices import Devices
from .dt_email import DarktraceEmail
from .dt_utils import debug_print

class DarktraceClient:
    def __init__(self, host: str, public_token: str, private_token: str, debug: bool = False):
        self.host = host.rstrip('/')
        self.auth = DarktraceAuth(public_token, private_token)
        self.debug = debug
        # Endpoint groups
        self.antigena = Antigena(self)
        self.analyst = Analyst(self)
        self.breaches = ModelBreaches(self)
        self.devices = Devices(self)
        self.email = DarktraceEmail(self)
        # Add more endpoint groups as needed

    def _debug(self, message: str):
        debug_print(message, self.debug) 