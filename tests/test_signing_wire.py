"""Offline guard for issue #59: the HMAC-signed string must match what is sent on the wire."""

import importlib.util
from pathlib import Path

import pytest

from darktrace import DarktraceClient

_spec = importlib.util.spec_from_file_location(
    "dryrun_signature_audit", Path(__file__).parent / "real" / "dryrun_signature_audit.py"
)
audit_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit_mod)

_client = DarktraceClient(host="https://dryrun.invalid", public_token="pub", private_token="priv")
_audit = audit_mod.Audit(_client, live_get=False)
_cases = audit_mod.discover(_client)[0] + audit_mod.edge_cases(_client)


@pytest.mark.parametrize("case", _cases, ids=[c[0] for c in _cases])
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_signature_matches_wire(case):
    label, outcome, detail = _audit.run(*case)
    if outcome == "NOREQ":
        pytest.skip(detail)  # e.g. deprecated no-op methods
    assert outcome == "OK", f"{label}: {detail}"
