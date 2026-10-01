#!/usr/bin/env python3
"""
READ-ONLY dry run: would any SDK call produce a request whose HMAC signature
the Darktrace server would reject (GitHub issue #59 and relatives)?

Nothing is sent. By default there is no network access at all and no credentials
are needed: every public method of every endpoint class is called against a
stubbed HTTP session. For each request the SDK *would* send we compare

    signed   - the string the SDK fed to the HMAC, with
    expected - the string the server recomputes from what is on the wire:
               path + "?" + query pairs + form pairs  (or  + JSON body)

(per the API guide: "for POST requests add each post parameter into the query
string to generate the signature"). A difference = "API SIGNATURE ERROR" live.

Optional ``--live-get`` additionally sends the GET cases to a real instance with
a hard guard that refuses every non-GET method. Still read-only.

Run from the repo root:
    PYTHONPATH=. python3 tests/real/dryrun_signature_audit.py
    PYTHONPATH=. python3 tests/real/dryrun_signature_audit.py -v          # show passing too
    PYTHONPATH=. python3 tests/real/dryrun_signature_audit.py --live-get \
        --host https://10.0.0.1 --public-token PUB --private-token PRIV --no-verify

Exit code: 0 = no mismatch, 1 = at least one call would fail signature check.
"""

from __future__ import annotations

import argparse
import inspect
import os
import sys
from typing import Any, Callable
from urllib.parse import parse_qsl, urlsplit

import requests
import urllib3

from darktrace import DarktraceClient

# Sample values for required parameters, by name (unknown names fall back to "x").
SAMPLE: dict[str, Any] = {
    "field": "hostname",
    "analysis_type": "terms",
    "query": {"search": "*", "fields": []},
    "graph_type": "line",
    "interval": 3600,
    "codeid": 1,
    "did": 1,
    "action": "gpol",
    "duration": 60,
    "uuids": "u-1",
    "incident_id": "i-1",
    "message": "a b",
    "investigate_time": "1700000000",
    "pbid": 1,
    "hostname": "h",
    "ip": "10.0.0.1",
    "label": "l",
    "mac": "aa:bb:cc:dd:ee:ff",
    "tag": "Active Threat",
    "type": "t",
    "vendor": "v",
    "link": "http://x/y",
    "uuid": "u-1",
    "data": {"a": 1},
    "source": "s",
    "breach_id": "1",
    "comment": "c",
    "ip1": "10.0.0.1",
    "start": 1,
    "end": 2,
    "sid": 1,
    "name": "n",
    "tag_id": "1",
    "tid": 1,
    "teid": 1,
    "entityType": "Device",
    "entityValue": ["1", "2"],
}

# Methods that need more than their required params to be valid calls.
OVERRIDE: dict[str, dict[str, Any]] = {
    "details.get": {"did": 1},
    "intelfeed.update": {"add_entry": "a.com"},
    "tags.get_entities": {"did": 1},
}


def edge_cases(c: DarktraceClient) -> list[tuple]:
    """Optional parameters / unusual values that tend to break signing."""
    return [
        ("analyst.acknowledge([u1,u2])", lambda: c.analyst.acknowledge(["u-1", "u-2"])),
        ("tags.post_entities(tag with space)", lambda: c.tags.post_entities(1, "Active Threat")),
        ("tags.post_entities(special chars)", lambda: c.tags.post_entities(1, "a&b=c,d/ü")),
        ("tags.post_entities(duration=3600)", lambda: c.tags.post_entities(1, "Active Threat", duration=3600)),
        ("breaches.acknowledge([1,2])", lambda: c.breaches.acknowledge([1, 2])),
        ("devices.get(saasfilter=[a,b])", lambda: c.devices.get(saasfilter=["Office365", "Zoom"])),
        ("devices.get(saasfilter='a')", lambda: c.devices.get(saasfilter="Office365")),
        (
            "breaches.get(saasfilter=[a,b])",
            lambda: c.breaches.get(saasfilter=["Office365", "Zoom"]),
            "saasfilter=Office365&saasfilter=Zoom",
        ),
        ("breaches.get(did=None)", lambda: c.breaches.get(did=None, count=1)),
        (
            "breaches.get(from_time/to_time)",
            lambda: c.breaches.get(from_time="2026-01-01 00:00:00", to_time="2026-01-02 00:00:00"),
        ),
        ("breaches.get(unicode value)", lambda: c.breaches.get(device="Müller-PC")),
        ("devices.get(includetags=True, count=5)", lambda: c.devices.get(includetags=True, count=5)),
        ("devicesearch.get(tag with space)", lambda: c.devicesearch.get_tag("Active Threat")),
        ("analyst.add_comment(unicode)", lambda: c.analyst.add_comment("i-1", "Ünï ü")),
        (
            "intelfeed.update(add_list, description)",
            lambda: c.intelfeed.update(add_list=["a.com", "b.com"], description="x y"),
        ),
    ]


# --------------------------------------------------------------------------- #
class Audit:
    def __init__(self, client: DarktraceClient, live_get: bool) -> None:
        self.c = client
        self.live_get = live_get
        self.signed: list[str] = []
        self.captured: list[requests.PreparedRequest] = []
        self.real_request = client._session.request
        real_sign = client.auth.generate_signature

        def spy_sign(path: str, date: str) -> str:
            self.signed.append(path)
            return real_sign(path, date)

        client.auth.generate_signature = spy_sign  # type: ignore[method-assign]
        client._session.request = self._intercept  # type: ignore[method-assign]

    def _intercept(self, method: str, url: str, **kw: Any) -> requests.Response:
        prep = self.c._session.prepare_request(
            requests.Request(method, url, headers=kw.get("headers"), params=kw.get("params"), data=kw.get("data"))
        )
        self.captured.append(prep)
        if self.live_get:
            if method.upper() != "GET":  # hard read-only guard
                raise RuntimeError(f"BLOCKED non-GET {method} {url}")
            return self.real_request(method, url, **kw)
        resp = requests.Response()
        resp.status_code, resp._content = 200, b"{}"
        return resp

    @staticmethod
    def expected(prep: requests.PreparedRequest) -> set[str]:
        """What the server derives from the wire; both sent order and sorted order are legal."""
        parts = urlsplit(prep.url)
        pairs = parse_qsl(parts.query, keep_blank_values=True)  # query: signed decoded (verified live)
        body = prep.body.decode() if isinstance(prep.body, bytes) else prep.body
        ctype = prep.headers.get("Content-Type", "")
        json_tail = ""
        if body and "x-www-form-urlencoded" in ctype:
            # form body: signed exactly as sent, still url-encoded (verified live: "a b" -> "a+b")
            pairs += [tuple(kv.split("=", 1)) for kv in body.split("&")]
        elif body:
            json_tail = body
        out = set()
        for seq in (pairs, sorted(pairs)):
            s = parts.path + ("?" + "&".join(f"{k}={v}" for k, v in seq) if seq else "")
            if json_tail:
                s += ("&" if "?" in s else "?") + json_tail
            out.add(s)
        return out

    def run(self, label: str, call: Callable[[], Any], must_send: str = "") -> tuple[str, str, str]:
        self.signed.clear()
        self.captured.clear()
        try:
            call()
        except Exception as exc:  # noqa: BLE001
            return label, "CRASH", f"{type(exc).__name__}: {exc}"
        if not self.captured:
            return label, "NOREQ", "no request issued"
        verdicts, detail = [], ""
        if must_send and not any(must_send in p.url for p in self.captured):
            return label, "BAD", f"data loss: {must_send!r} not on the wire, sent {self.captured[0].url!r}"
        for prep, signed in zip(self.captured, self.signed):
            exp = self.expected(prep)
            if signed in exp:
                verdicts.append("OK")
            else:
                verdicts.append("BAD")
                detail = f"{prep.method} signed={signed!r} server-expects={sorted(exp)[0]!r}"
        return label, ("BAD" if "BAD" in verdicts else "OK"), detail or f"{prep.method} {signed}"


def discover(c: DarktraceClient) -> tuple[list[tuple[str, Callable[[], Any]]], list[str]]:
    cases, skipped = [], []  # noqa: F841
    for attr, ep in vars(c).items():
        if attr.startswith("_") or not hasattr(ep, "client"):
            continue
        for name, fn in inspect.getmembers(ep, inspect.ismethod):
            if name.startswith("_"):
                continue
            sig = inspect.signature(fn)
            kwargs = {
                k: SAMPLE.get(k, "x")
                for k, p in sig.parameters.items()
                if p.default is p.empty and p.kind not in (p.VAR_KEYWORD, p.VAR_POSITIONAL)
            }
            kwargs.update(OVERRIDE.get(f"{attr}.{name}", {}))
            cases.append((f"{attr}.{name}", lambda fn=fn, kwargs=kwargs: fn(**kwargs)))
    return cases, skipped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--live-get", action="store_true", help="also send GET cases to a real instance (non-GET blocked)")
    ap.add_argument("--host", default=os.getenv("DARKTRACE_HOST", "https://dryrun.invalid"))
    ap.add_argument("--public-token", default=os.getenv("DARKTRACE_PUBLIC_TOKEN", "pub"))
    ap.add_argument("--private-token", default=os.getenv("DARKTRACE_PRIVATE_TOKEN", "priv"))
    ap.add_argument("--no-verify", action="store_true")
    a = ap.parse_args()
    if a.no_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    client = DarktraceClient(
        host=a.host, public_token=a.public_token, private_token=a.private_token, verify_ssl=not a.no_verify, timeout=30
    )
    audit = Audit(client, a.live_get)
    cases, _ = discover(client)
    cases += edge_cases(client)

    results = [audit.run(*case) for case in cases]
    if a.live_get:  # re-run: results above for GETs were real sends; non-GET were blocked -> report as BLOCKED
        results = [(lb, "SAFE-BLOCKED" if "BLOCKED" in d else o, d) for lb, o, d in results]

    bad = [r for r in results if r[1] in ("BAD", "CRASH")]
    for label, outcome, detail in results:
        if outcome in ("BAD", "CRASH") or a.verbose:
            print(f"{outcome:6} {label:48} {detail if outcome != 'OK' else ''}")
    print(
        f"\n{len(results)} calls checked, {len(results) - len(bad)} would pass, {len(bad)} would FAIL the signature check"
    )
    print("Mode: " + ("LIVE GET only (non-GET blocked)" if a.live_get else "pure dry run, no network"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
