# Network Module

The Network module provides access to network information and statistics.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the network module
network = client.network
```

## Methods

### Get Network

Retrieve network information and statistics from the Darktrace platform.

```python
# Get all networks
all_networks = network.get()

# Get a specific number of networks
recent_networks = network.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "networks": [
    {
      // Network data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Networks

```python
networks_data = client.network.get()
for item in networks_data.get("networks", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    networks_data = client.network.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
