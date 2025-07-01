# Advanced Search Module

The Advanced Search module provides access to Darktrace's advanced search functionality for querying logs and events.

## ✅ POST Request Support (v0.8.3+)

**RESOLVED**: POST requests to the Advanced Search API now work correctly! This was resolved in v0.8.3 by fixing JSON formatting inconsistencies in the authentication system.

- **Darktrace 6.1+**: POST requests are recommended for advanced queries
- **Earlier versions**: GET requests continue to work as before
- **Both methods supported**: You can choose between GET and POST based on your needs

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

Perform advanced search queries on Darktrace logs and events.

```python
# Basic search query structure
query = {
    "search": "@type:\"ssl\" AND @fields.dest_port:\"443\"",
    "fields": [],
    "offset": 0,
    "timeframe": "3600"  # 1 hour in seconds
}

# GET request (traditional method, works with all Darktrace versions)
results = advanced_search.search(query)
# or explicitly
results = advanced_search.search(query, post_request=False)

# POST request (recommended for Darktrace 6.1+)
results = advanced_search.search(query, post_request=True)
```

#### Advanced Query Examples

```python
# Search for SSL connections with custom timeframe
ssl_query = {
    "search": "@type:\"ssl\" AND @fields.dest_port:\"443\"",
    "fields": ["@fields.source_ip", "@fields.dest_ip", "@fields.cipher"],
    "offset": 0,
    "timeframe": "7200"  # 2 hours
}
results = advanced_search.search(ssl_query, post_request=True)

# Search with custom time range
custom_time_query = {
    "search": "@type:\"conn\" AND @fields.proto:\"tcp\"",
    "fields": [],
    "offset": 0,
    "timeframe": "custom",
    "from": "2025-07-01T09:00:00",
    "to": "2025-07-01T10:00:00"
}
results = advanced_search.search(custom_time_query, post_request=True)
```

#### Parameters

- `query` (Dict[str, Any]): Dictionary containing the search query parameters
- `post_request` (bool, optional): If True, attempts to use POST method. Defaults to False (GET method)

#### Query Parameters

The query dictionary can include:
- `offset` (int): Starting offset for results
- `count` (int): Number of results to return
- `query` (str): Search query string
- `timeframe` (str): Time frame for the search (e.g., "1 hour", "24 hours")

### Analyze

Analyze field data from search results.

```python
# Analyze a specific field
query = {
    "query": "*",
    "timeframe": "1 hour"
}
analysis = advanced_search.analyze(
    field="source_ip",
    analysis_type="count",
    query=query
)
```

#### Parameters

- `field` (str): The field to analyze
- `analysis_type` (str): Type of analysis to perform (e.g., "count", "unique")
- `query` (Dict[str, Any]): Search query parameters

### Graph

Get graph data for visualization.

```python
# Get graph data
query = {
    "query": "*",
    "timeframe": "1 hour"
}
graph_data = advanced_search.graph(
    graph_type="timeseries",
    interval=300,  # 5 minutes in seconds
    query=query
)
```

#### Parameters

- `graph_type` (str): Type of graph to generate (e.g., "timeseries")
- `interval` (int): Time interval in seconds for graph data points
- `query` (Dict[str, Any]): Search query parameters

## Examples

### Basic Search

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Perform a basic search
query = {
    "offset": 0,
    "count": 50,
    "query": "source_ip:192.168.1.100",
    "timeframe": "2 hours"
}

try:
    results = client.advanced_search.search(query)
    print(f"Found {len(results.get('events', []))} events")
    for event in results.get('events', [])[:5]:
        print(f"Event: {event}")
except Exception as e:
    print(f"Search failed: {e}")
```

### Field Analysis

```python
# Analyze source IPs
query = {
    "query": "*",
    "timeframe": "24 hours"
}

analysis = client.advanced_search.analyze(
    field="source_ip",
    analysis_type="count",
    query=query
)
print(f"Top source IPs: {analysis}")
```

### Time Series Graph

```python
# Generate time series graph data
graph_data = client.advanced_search.graph(
    graph_type="timeseries",
    interval=600,  # 10-minute intervals
    query=query
)
print(f"Graph data points: {len(graph_data.get('data', []))}")
```

## Error Handling

```python
try:
    results = client.advanced_search.search(query, post_request=True)
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Notes

- All queries are automatically base64-encoded before being sent to the API
- **POST requests now supported** (v0.8.3+) for Darktrace 6.1+ installations
- **GET requests continue to work** for all Darktrace versions
- Time intervals for graphs are specified in seconds
- Query syntax follows Darktrace's advanced search format

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

# Execute search (GET request - traditional method)
results = advanced_search.search(query)

# Execute search (POST request - recommended for Darktrace 6.1+)
results = advanced_search.search(query, post_request=True)
```

#### Parameters

- `query` (dict): Search query dictionary containing:
  - `search` (str): The search query string
  - `fields` (list): Fields to include in response
  - `offset` (int): Starting offset for pagination
  - `timeframe` (str): Time range in seconds
  - `time` (dict): Time configuration
- `post_request` (bool, optional): If True, uses POST method (supported in v0.8.3+)

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
    results = client.advanced_search.search(query, post_request=True)
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
