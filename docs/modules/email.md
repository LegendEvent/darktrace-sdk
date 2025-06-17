# Email Module

The Email module provides access to Darktrace Email security features.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the email module
email = client.email
```

## Methods

### Get Email

Retrieve darktrace Email security features from the Darktrace platform.

```python
# Get all emails
all_emails = email.get()

# Get a specific number of emails
recent_emails = email.get(count=10)
```

#### Parameters

- `count` (int, optional): Number of items to return
- `offset` (int, optional): Starting offset for pagination

#### Response

```json
{
  "emails": [
    {
      // Email data
    },
    // ... more items
  ]
}
```

## Examples

### Get All Emails

```python
emails_data = client.email.get()
for item in emails_data.get("emails", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    emails_data = client.email.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
