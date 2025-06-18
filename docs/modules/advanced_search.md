# Advanced Search Module

The Advanced Search module provides access to Darktrace's advanced search functionality for querying logs and events.

## ⚠️ Known Issues

**POST Requests Not Supported**: POST requests to the Advanced Search API are currently not working due to unresolved authentication signature calculation issues. The Darktrace API documentation specifies that POST parameters should be included in the signature calculation, but multiple implementation attempts following the official documentation have resulted in "API SIGNATURE ERROR" responses.

**Workaround**: Use GET requests for Advanced Search queries, which work correctly and support all the same functionality. The SDK automatically defaults to GET requests.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the advanced_search module
advanced_search = client.advanced_search
```

## Methods

### Search

Perform advanced search queries on Darktrace data.

```python
# Basic search query
query = {
    "search": "@type:\"conn\" AND @fields.proto:\"tcp\"",
    "fields": [],
    "offset": 0,
    "timeframe": "3600",  # 1 hour in seconds
    "time": {"user_interval": 0}
}

# Execute search (GET request - recommended)
results = advanced_search.search(query)

# POST request (currently not supported - will raise NotImplementedError)
# results = advanced_search.search(query, post_request=True)
```

#### Parameters

- `query` (dict): Search query dictionary containing:
  - `search` (str): The search query string
  - `fields` (list): Fields to include in response
  - `offset` (int): Starting offset for pagination
  - `timeframe` (str): Time range in seconds
  - `time` (dict): Time configuration
- `post_request` (bool, optional): If True, attempts POST method (currently not supported)

#### Response

```json
{
  "hits": {
    "total": 1234,
    "hits": [
      {
        "_source": {
          "@timestamp": "2023-01-01T12:00:00.000Z",
          "@type": "conn",
          "@fields": {
            "proto": "tcp",
            "dest_port": 443
          }
        }
      }
    ]
  }
}
```

### Analyze

Analyze field data using aggregations.

```python
# Analyze destination ports for DNS traffic
analyze_query = {
    "search": "@type:\"dns\"",
    "fields": [],
    "offset": 0,
    "timeframe": "3600",
    "time": {"user_interval": 0}
}

results = advanced_search.analyze("@fields.dest_port", "terms", analyze_query)
```

### Graph

Generate graph data over time intervals.

```python
# Get connection counts over time with 5-minute intervals
graph_query = {
    "search": "@type:\"conn\"",
    "fields": [],
    "offset": 0,
    "timeframe": "14400",  # 4 hours
    "time": {"user_interval": 0}
}

results = advanced_search.graph("count", 300000, graph_query)  # 5-minute intervals
```

## Examples

### Basic Connection Search

```python
# Search for HTTPS connections in the last hour
query = {
    "search": "@type:\"conn\" AND @fields.dest_port:\"443\"",
    "fields": [],
    "offset": 0,
    "timeframe": "3600",
    "time": {"user_interval": 0}
}

results = client.advanced_search.search(query)
print(f"Found {results['hits']['total']} HTTPS connections")
```

### Field Analysis

```python
# Analyze top destination ports
query = {
    "search": "@type:\"conn\"",
    "fields": [],
    "offset": 0,
    "timeframe": "3600",
    "time": {"user_interval": 0}
}

analysis = client.advanced_search.analyze("@fields.dest_port", "terms", query)
for bucket in analysis['aggregations']['terms']['buckets'][:5]:
    print(f"Port {bucket['key']}: {bucket['doc_count']} connections")
```

## Error Handling

```python
try:
    results = client.advanced_search.search(query)
    # Process the data
except NotImplementedError as e:
    print(f"POST request not supported: {e}")
    # Use GET request instead
    results = client.advanced_search.search(query, post_request=False)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
