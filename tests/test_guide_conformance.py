"""Offline checks that requests match the official API guide (no network)."""

import json
from urllib.parse import parse_qsl, urlsplit

import pytest
import requests

from darktrace import DarktraceClient


@pytest.fixture
def sent():
    c = DarktraceClient(host="https://x.invalid", public_token="pub", private_token="priv")
    log = []

    def fake(method, url, **kw):
        log.append((method, url, kw))
        r = requests.Response()
        r.status_code, r._content = 200, b"{}"
        return r

    c._session.request = fake
    return c, log


def _prep(log):
    method, url, kw = log[-1]
    p = requests.Request(method, url, params=kw.get("params"), data=kw.get("data"), headers=kw.get("headers")).prepare()
    return method, urlsplit(p.url).path, parse_qsl(urlsplit(p.url).query), p.body


def test_bool_params_are_lowercase(sent):
    c, log = sent
    c.status.get(includechildren=True, fast=False)
    q = dict(_prep(log)[2])
    assert q == {"includechildren": "true", "fast": "false"}


def test_metricdata_multiple_metrics_use_numbered_keys(sent):
    c, log = sent
    c.metricdata.get(metrics=["connections", "externalconnections"], did=1, interval=3600)
    q = _prep(log)[2]
    assert ("metric1", "connections") in q and ("metric2", "externalconnections") in q
    assert not any(k == "metric" for k, _ in q)


def test_metricdata_time_pairs_required(sent):
    c, _ = sent
    with pytest.raises(ValueError):
        c.metricdata.get(metric="connections", starttime=1)
    with pytest.raises(ValueError):
        c.metricdata.get(metric="connections", from_="2020-03-20 00:00:00")


def test_similardevices_uses_did_query(sent):
    c, log = sent
    c.similardevices.get(device_id=123, count=3)
    _, path, q, _ = _prep(log)
    assert path == "/similardevices" and ("did", "123") in q


def test_mbcomments_post_uses_modelbreaches_path(sent):
    c, log = sent
    c.mbcomments.post("55", "hello")
    method, path, _, body = _prep(log)
    assert (method, path) == ("POST", "/modelbreaches/55/comments")
    assert json.loads(body) == {"message": "hello"}


def test_antigena_activate_accepts_duration(sent):
    c, log = sent
    c.antigena.activate_action(5, reason="r", duration=600)
    assert json.loads(_prep(log)[3]) == {"codeid": 5, "activate": True, "reason": "r", "duration": 600}


def test_details_accepts_did_zero(sent):
    c, log = sent
    c.details.get(did=0)
    assert ("did", "0") in _prep(log)[2]


def test_tags_get_entities_needs_did_or_tag(sent):
    c, _ = sent
    with pytest.raises(ValueError):
        c.tags.get_entities()


def test_tags_post_tag_entities_coerces_ids_to_strings(sent):
    c, log = sent
    c.tags.post_tag_entities(7, "Device", [1, 2])
    assert json.loads(_prep(log)[3])["entityValue"] == ["1", "2"]


def test_intelfeed_addlist_accepts_string(sent):
    c, log = sent
    c.intelfeed.update(add_list="a.com,b.com")
    assert json.loads(_prep(log)[3])["addlist"] == "a.com,b.com"


def test_subnets_id_sent_as_sid_query(sent):
    c, log = sent
    c.subnets.get(subnet_id=7)
    _, path, q, _ = _prep(log)
    assert path == "/subnets" and ("sid", "7") in q


def test_mbcomments_get_rejects_path_form(sent):
    c, _ = sent
    with pytest.raises(ValueError):
        c.mbcomments.get(comment_id="1")


def test_pcaps_get_strips_tm_prefix(sent):
    c, log = sent
    c.pcaps.get(pcap_id="/tm/abc.pcap")
    assert _prep(log)[1] == "/pcaps/abc.pcap"


def test_endpointdetails_bools_lowercase(sent):
    c, log = sent
    c.endpointdetails.get(ip="1.2.3.4", additionalinfo=True, devices=False)
    q = dict(_prep(log)[2])
    assert q["additionalinfo"] == "true" and q["devices"] == "false"


def test_summarystatistics_only_one_selector(sent):
    ss = sent[0].summarystatistics
    for kw in (
        {"eventtype": "saas", "csensor": True},
        {"eventtype": "saas", "mitreTactics": True},
        {"csensor": True, "mitreTactics": True},
    ):
        with pytest.raises(ValueError, match="Only one of"):
            ss.get(**kw)


def test_summarystatistics_time_params_require_eventtype(sent):
    ss = sent[0].summarystatistics
    for kw in ({"endtime": 1}, {"to": "2021-02-12 12:00:00"}, {"hours": 3}, {"csensor": True, "hours": 3}):
        with pytest.raises(ValueError, match="require eventtype"):
            ss.get(**kw)


def test_summarystatistics_guide_example_is_allowed(sent):
    client, log = sent
    client.summarystatistics.get(eventtype="networkdevicedetails", to="2021-02-12 12:00:00", hours=24)
    q = dict(_prep(log)[2])
    assert q["eventtype"] == "networkdevicedetails" and q["hours"] == "24"
