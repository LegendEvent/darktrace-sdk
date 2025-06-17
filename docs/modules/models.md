# Models Module

The Models module provides access to Darktrace models and their configurations.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the models module
models = client.models
```

## Methods

### Get Models

Retrieve darktrace models and their configurations from the Darktrace platform.

```python
# Get all models
all_models = models.get()

# Get a specific number of models
recent_models = models.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "models": [
    {
      // Models data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Modelss

```python
models_data = client.models.get()
for item in models_data.get("models", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    models_data = client.models.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
