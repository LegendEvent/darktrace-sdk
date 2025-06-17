# Endpointdetails Module

The Endpointdetails module provides access to endpoint-specific information.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the endpointdetails module
endpointdetails = client.endpointdetails
```

## Methods

### Get Endpointdetails

Retrieve endpoint-specific information from the Darktrace platform.

```python
# Get all endpointdetails
all_endpointdetails = endpointdetails.get()

# Get a specific number of endpointdetails
recent_endpointdetails = endpointdetails.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "endpointdetails": [
    {
      // Endpointdetails data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Endpointdetailss

```python
endpointdetails_data = client.endpointdetails.get()
for item in endpointdetails_data.get("endpointdetails", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    endpointdetails_data = client.endpointdetails.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
