# Analyst Module

The Analyst module provides access to AI Analyst incidents and investigations.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the analyst module
analyst = client.analyst
```

## Methods

### Get Analyst

Retrieve aI Analyst incidents and investigations from the Darktrace platform.

```python
# Get all analysts
all_analysts = analyst.get()

# Get a specific number of analysts
recent_analysts = analyst.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "analysts": [
    {
      // Analyst data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Analysts

```python
analysts_data = client.analyst.get()
for item in analysts_data.get("analysts", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    analysts_data = client.analyst.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
