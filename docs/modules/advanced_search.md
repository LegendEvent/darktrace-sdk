# Advanced Search Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.

The Advanced Search module queries Darktrace Advanced Search data (logs and events) in JSON format via `/advancedsearch/api/search`, `/advancedsearch/api/analyze` and `/advancedsearch/api/graph`.

Advanced Search queries are JSON objects that the SDK encodes as a Base64 string. For `search`, `analyze` and `graph` the string is placed in the URL path (GET). For `search` it can instead be sent in a POST body `{"hash": "<base64>"}` (Darktrace 6.1+), which the guide describes as the way to make more complex queries.

**Permissions:** the guide lists "Unrestricted Devices and Advanced Search" as the minimum permission for all three endpoints.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

advanced_search = client.advanced_search
```

## Query structure

A query is a dictionary with these keys (as in the guide's Base64-decoded examples):

```python
query = {
    "search": '@type:"ssl" AND @fields.dest_port:"443"',  # double quotes inside the string must be escaped/embedded as shown
    "fields": [],          # required by the API; its contents do not change the response (all fields are returned)
    "offset": 0,
    "timeframe": "3600",   # seconds back from now, or "custom"
    "time": {"user_interval": 0},
}
```

Rules from the API guide:

- The timeframe is either a `timeframe` interval in seconds relative to the current time (the `time` object may then be omitted; results differ between calls because the interval is relative), or `timeframe: "custom"` together with a `time` object containing `from` and `to`. Time values must always be given in pairs.
- Time formats: the guide's parameter tables describe `from`/`to` as `YYYY-MM-DD HH:MM:SS`, while its examples use `"2020-02-01T08:00:00Z"`. `starttime`/`endtime` are epoch milliseconds.
- `search` is optional. Double quotes in the search string must be escaped before encoding (the SDK's JSON encoding does this for you).
- The empty `fields` array is required. `graphmode` and `mode` (seen in Threat Visualizer URLs) are not needed.
- `size` (search and graph): default 50 results, maximum 10,000. For pagination keep `size` fixed and increase `offset` by `size` each request.

## Methods

### search

```python
search(query: dict, post_request: bool = False, timeout=...) -> dict | list
```

Returns the parsed JSON response. `post_request=False` sends a GET with the encoded query in the path; `post_request=True` POSTs `{"hash": "<base64>"}` to `/advancedsearch/api/search` (Darktrace 6.1+).

The SDK builds the encoded query from these keys of `query` only: `search` (default `""`), `fields` (default `[]`), `offset` (default `0`), `timeframe` (default `"3600"`), `time`, plus these time helpers:

- `from` and `to`: sets `timeframe` to `"custom"` and `time` to `{"from": ..., "to": ..., "user_interval": "0"}`.
- `starttime` and `endtime` (POST only; ignored on GET): same, using the millisecond values.
- `interval`: sets `timeframe` to `str(interval)` (seconds).

Any other key (including `size`) is not forwarded by `search()`.

```python
# Last 12 hours (43200 s), GET
results = advanced_search.search({
    "search": '@type:conn AND @fields.proto:tcp AND @fields.dest_port:"443"',
    "fields": [],
    "offset": 0,
    "timeframe": "43200",
})

# Custom time range, POST (Darktrace 6.1+)
results = advanced_search.search({
    "search": '@type:files_identified AND _exists_:"@fields.sha1"',
    "fields": [],
    "offset": 0,
    "from": "2020-02-01T08:00:00Z",
    "to": "2020-02-01T10:00:00Z",
}, post_request=True)

# Hits are in hits.hits[]._source
print(results["hits"]["total"])
for hit in results["hits"]["hits"]:
    src = hit["_source"]
    print(src["@timestamp"], src["@type"], src["@fields"])
```

#### Response

The response has the structure shown in the guide (Elasticsearch-style):

```json
{
  "took": 22,
  "timed_out": false,
  "_shards": {"total": 2, "successful": 2, "skipped": 0, "failed": 0},
  "hits": {
    "total": 13123,
    "max_score": null,
    "hits": [
      {
        "_index": "logstash-dt-01-2020.03.23",
        "_type": "doc",
        "_id": "K18S2Iqiu7Wz1jaN",
        "_score": null,
        "_source": {
          "@fields": {},
          "@type": "conn",
          "@timestamp": "2020-03-23T11:59:09",
          "@message": "..."
        },
        "sort": [1586937600000]
      }
    ]
  },
  "darktraceChildError": "",
  "kibana": {"index": [], "per_page": 50}
}
```

`hits.hits._source.@fields` holds the protocol-specific fields (see the API guide for the fields per protocol). `darktraceChildError` names a probe that did not respond. `kibana` contains system details about the advanced search logs (`index`, `per_page`, and `time.from`/`time.to` for custom ranges). The `hits` list is paginated via `size`/`offset` as described above.

### analyze

```python
analyze(field: str, analysis_type: str, query: dict, timeout=...) -> dict | list
```

GET only. Performs an analysis on one field of the data matched by the query. `analysis_type` is one of `trend`, `score`, `terms` or `mean`. The `query` dictionary is Base64-encoded verbatim (no key translation like in `search()`), so write it in the guide's structure, including the `time` object for custom ranges.

```python
analysis = advanced_search.analyze(
    field="@fields.dest_port",
    analysis_type="terms",
    query={
        "search": '@type:"dns" AND @fields.proto:"udp"',
        "fields": [],
        "offset": 0,
        "timeframe": "custom",
        "time": {
            "from": "2020-02-20T17:00:00Z",
            "to": "2020-02-20T17:15:00Z",
            "user_interval": "0",
        },
    },
)

for bucket in analysis["aggregations"]["terms"]["buckets"]:
    print(bucket["key"], bucket["doc_count"])
```

`terms` returns `aggregations.terms` with `doc_count_error_upper_bound`, `sum_other_doc_count` and `buckets` (`key`, `doc_count`). `mean` returns `aggregations.stats` with `count`, `min`, `max`, `avg`, `sum`. For `trend` and `score`, see the API guide. The response also contains `took`, `timed_out`, `hits` (with an empty `hits` array), `darktraceChildError` and `kibana`.

### graph

```python
graph(graph_type: str, interval: int, query: dict, timeout=...) -> dict | list
```

GET only. Returns data for a time series graph. `graph_type` is `count` or `mean`.

- `interval` is the graph interval in **milliseconds** (seconds * 1000): the time window each bucket groups. The SDK inserts the value unchanged into the path (`/graph/<graph_type>/<interval>/<query>`).
- The guide's recommended minimum intervals: 15m -> 10000 (10s), 60m -> 30000 (30s), 4h -> 60000 (1m), 12h and 24h -> 300000 (10m), 48h -> 1800000 (30m), 7d -> 3600000 (1h). Large timeframes with small intervals use significant resources and are strongly discouraged.
- `graph_type="mean"` requires `analyze_field` (the field to aggregate) inside the query dictionary. `graph()` has no separate argument for it.
- The API returns data in 24-hour blocks split at 00:00. Further blocks are requested with an incrementing numeric path extension (`/1`, each step goes 24 hours further back), and `kibana.next` in the response signals further pages. The SDK's `graph()` does not append this extension, so only the first block is returned.

```python
# Count graph in 30-minute buckets over the last 48 hours
counts = advanced_search.graph(
    graph_type="count",
    interval=1800000,
    query={
        "search": '@type:ssh AND @fields.dest_ip:"10.0.56.12"',
        "fields": [],
        "offset": 0,
        "timeframe": "172800",
        "time": {"user_interval": 0},
    },
)
for bucket in counts["aggregations"]["count"]["buckets"]:
    print(bucket["key"], bucket["doc_count"])

# Mean graph: analyze_field is required in the query
means = advanced_search.graph(
    graph_type="mean",
    interval=30000,
    query={
        "search": '@fields.dest_ip:"10.0.56.12" AND @type:"conn"',
        "fields": [],
        "offset": 0,
        "timeframe": "custom",
        "time": {
            "from": "2020-02-02T00:00:00Z",
            "to": "2020-02-02T23:59:59Z",
            "user_interval": 0,
        },
        "analyze_field": "@fields.orig_ip_bytes",
    },
)
for bucket in means["aggregations"]["mean"]["buckets"]:
    print(bucket["key_as_string"], bucket["mean_stats"]["avg"])
```

For `count`, `aggregations.count.buckets` has `key` (epoch ms) and `doc_count`. For `mean`, `aggregations.mean.buckets` has `key_as_string`, `key`, `doc_count` and `mean_stats` (`count`, `min`, `max`, `avg`, ...). The response also contains `took`, `timed_out`, `hits`, `darktraceChildError` and `kibana` (`index`, `per_page`, `next`).

## Error Handling

```python
import requests

try:
    results = client.advanced_search.search(query, post_request=True)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
