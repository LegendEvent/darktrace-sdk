#!/usr/bin/env python3
"""
Live signature probe against a REAL Darktrace - designed to change nothing.

Default (no flag): GET requests only (connectivity / signing controls).

--allow-sentinel-post: additionally fires the five form POSTs from issue #59
(analyst ack/unack/pin/unpin, tags.post_entities) but ONLY with sentinel IDs that
cannot exist (fresh uuid4s / a did verified absent, a tag name that does not exist). Darktrace
verifies the signature BEFORE it looks up the object, so:
    "API SIGNATURE ERROR"        -> signature rejected  (the bug)
    anything else (404/400/ok)   -> signature accepted  (the fix works)
Nothing real is addressed, so nothing is acknowledged, pinned or tagged.
(If an instance unexpectedly returned success for the sentinel, there is still
no object to change.)

Run the SAME script against old and new SDK code and compare:
    git worktree add /tmp/dt-old HEAD
    PYTHONPATH=/tmp/dt-old python3 tests/real/live_signature_probe.py  [flags]   # OLD
    PYTHONPATH=.           python3 tests/real/live_signature_probe.py  [flags]   # NEW

Flags: --host --public-token --private-token --no-verify (or DARKTRACE_* env vars)
"""

from __future__ import annotations

import argparse
import os
import sys
import uuid
from typing import Any, Callable

import urllib3

import darktrace
from darktrace import DarktraceClient

SENTINEL_TAG = "sdk probe,tag&x=ü (does not exist)"  # space/comma/&/=/non-ASCII on purpose


def classify(call: Callable[[], Any]) -> tuple[str, str]:
    try:
        out = call()
        text = str(out)
    except Exception as exc:  # noqa: BLE001 - HTTP errors carry the server message
        resp = getattr(exc, "response", None)
        text = f"{type(exc).__name__}: {exc} {getattr(resp, 'text', '') or ''}"
    if "SIGNATURE" in text.upper():
        return "SIGNATURE-REJECTED", text[:140]
    if text.startswith(("UnicodeEncodeError", "ConnectionError", "DarktraceConnectionError")):
        return "CLIENT-ERROR", text[:140]
    return "SIGNATURE-ACCEPTED", text[:140]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default=os.getenv("DARKTRACE_HOST"))
    ap.add_argument("--public-token", default=os.getenv("DARKTRACE_PUBLIC_TOKEN"))
    ap.add_argument("--private-token", default=os.getenv("DARKTRACE_PRIVATE_TOKEN"))
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--allow-sentinel-post", action="store_true")
    a = ap.parse_args()
    if not (a.host and a.public_token and a.private_token):
        ap.error("host and both tokens required")
    if a.no_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    c = DarktraceClient(
        host=a.host, public_token=a.public_token, private_token=a.private_token, verify_ssl=not a.no_verify, timeout=30
    )
    print(f"SDK under test: {darktrace.__file__}\n")

    cases: list[tuple[str, Callable[[], Any]]] = [
        ("GET control: status.get", lambda: c.status.get()),
        ("GET control: devices.get(count=1)", lambda: c.devices.get(count=1)),
    ]
    if a.allow_sentinel_post:
        # ids that look real but are verified absent: fresh uuid4s, and max(did)+100000
        devs = c.devices.get(responsedata="did", count=100000)
        dids = {d["did"] for d in (devs if isinstance(devs, list) else devs.get("devices", []))}
        SENTINEL_DID = max(dids, default=0) + 100000
        SENTINEL_UUID, SENTINEL_UUID2 = str(uuid.uuid4()), str(uuid.uuid4())
        print(f"sentinels: did={SENTINEL_DID} (not among {len(dids)} devices), fresh uuid4s\n")
        cases += [
            ("POST analyst.acknowledge(sentinel)", lambda: c.analyst.acknowledge(SENTINEL_UUID)),
            ("POST analyst.unacknowledge(sentinel)", lambda: c.analyst.unacknowledge(SENTINEL_UUID)),
            ("POST analyst.pin(sentinel)", lambda: c.analyst.pin(SENTINEL_UUID)),
            ("POST analyst.unpin(sentinel)", lambda: c.analyst.unpin(SENTINEL_UUID)),
            ("POST analyst.acknowledge([s,s])", lambda: c.analyst.acknowledge([SENTINEL_UUID, SENTINEL_UUID2])),
            (
                "POST tags.post_entities(absent did, tag w/ specials)",
                lambda: c.tags.post_entities(SENTINEL_DID, SENTINEL_TAG, duration=60),
            ),
        ]
    else:
        print("(read-only: GET only; add --allow-sentinel-post to also test the form POSTs with fake IDs)\n")

    rejected = 0
    for label, call in cases:
        verdict, detail = classify(call)
        rejected += verdict in ("SIGNATURE-REJECTED", "CLIENT-ERROR")
        print(f"{verdict:20} {label:42} {detail if verdict != 'SIGNATURE-ACCEPTED' else ''}")
    print(f"\n{len(cases) - rejected}/{len(cases)} accepted by the server's signature check")
    return 1 if rejected else 0


if __name__ == "__main__":
    sys.exit(main())
