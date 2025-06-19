def pytest_addoption(parser):
    parser.addoption('--host', action='store', help='Darktrace instance URL')
    parser.addoption('--public-token', action='store', help='Public API token')
    parser.addoption('--private-token', action='store', help='Private API token')
    parser.addoption('--no-verify', action='store_true', help='Disable SSL verification')


# Suppress InsecureRequestWarning globally for all tests
import warnings
from urllib3.exceptions import InsecureRequestWarning

def pytest_configure(config):
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)