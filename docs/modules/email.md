# Email Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Email module provides access to the Darktrace/Email API (`/agemail/api/ep/api/v1.0/*`): link decoding, dashboard statistics, email lookup, search and download, manual email actions, resource lists and audit events. It is only available on Darktrace/Email deployments.

The official API guide only lists the endpoints and permissions for Darktrace/Email and gives one example response (`user_anomaly`). For all other parameters, request bodies and response schemas it refers to the OpenAPI documentation of your instance at `https://[instance]/agemail/api/api-docs`. This page therefore says "see the API guide" / "see the instance's api-docs" wherever the schema is not defined in the guide.

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

## Methods Overview

- **`decode_link()`** - Decode an encoded link from an email
- **`get_action_summary()`** - Dashboard: action summary
- **`get_dash_stats()`** - Dashboard: statistics
- **`get_data_loss()`** - Dashboard: data loss
- **`get_user_anomaly()`** - Dashboard: user anomaly
- **`email_action()`** - Perform an action on an email
- **`get_email()`** - Retrieve a specific email
- **`download_email()`** - Download raw email content
- **`search_emails()`** - Search emails
- **`get_tags()`** - List email tags
- **`get_actions()`** - List available email actions
- **`get_filters()`** - List available search filters
- **`get_event_types()`** - List audit event types
- **`get_audit_events()`** - Retrieve audit events

All methods return the parsed JSON response (a `dict` or `list`, depending on the endpoint) except `download_email()`, which returns `bytes`. All methods accept an optional `timeout` keyword argument (seconds, or a `(connect, read)` tuple).

## Permissions

Every Darktrace/Email endpoint requires the **Email logs** permission at a minimum. A missing permission results in a `ForbiddenError` (HTTP 403).

| Method | Permissions |
|---|---|
| `decode_link`, `get_action_summary`, `get_dash_stats`, `get_data_loss`, `get_user_anomaly`, `get_email`, `search_emails`, `get_tags`, `get_actions`, `get_filters` | Email logs |
| `email_action` | Email logs, plus **Manual Action** or **Restricted Manual Action** (with Restricted Manual Action, emails can only be released to the original recipient) |
| `download_email` | Email logs, plus **Download Email** |
| `get_event_types`, `get_audit_events` | Email logs, plus **Audit Log (Darktrace/Email)** |

## Methods

### Decode Link

Decode an encoded link from an email (`GET /v1.0/admin/decode_link`).

```python
decoded = email.decode_link(link="https://...encoded...")
print(decoded)
```

#### Parameters

- `link` (str): The encoded link to decode (sent as the `link` query parameter)

#### Response

See the API guide / the instance's api-docs for the response schema.

### Dashboard Methods

`get_action_summary()`, `get_dash_stats()`, `get_data_loss()` and `get_user_anomaly()` share the same signature and call `GET /v1.0/dash/action_summary`, `/dash_stats`, `/data_loss` and `/user_anomaly` respectively.

```python
summary = email.get_action_summary(days=7, limit=10)
stats = email.get_dash_stats(days=28, limit=2)
data_loss = email.get_data_loss(days=7, limit=5)
anomalies = email.get_user_anomaly(days=28, limit=2)
```

#### Parameters

- `days` (int, optional): Number of days to include (sent as `days`)
- `limit` (int, optional): Limit the number of results (sent as `limit`)

Parameters that are not given are not sent. The API guide only demonstrates `days` and `limit` on `user_anomaly`; for the other three dashboard endpoints check the api-docs of your instance for the supported parameters and the default time window.

#### Response

`get_user_anomaly()` returns a dictionary keyed by email address (example from the API guide for `?limit=2&days=28`):

```python
{
  "sofia.martinez@holdingsinc.com": {
    "n_emails": 21,
    "total_emails": 1106,
    "n_last_period": 71,
    "n_last_week": 71,
    "percentage": 29,
    "n_links": 0,
    "n_attachments": 0
  },
  "grayson.stone@holdingsinc.com": {
    "n_emails": 1,
    "total_emails": 32,
    "n_last_period": 0,
    "n_last_week": 0,
    "percentage": 0,
    "n_links": 0,
    "n_attachments": 0
  }
}
```

```python
for address, info in email.get_user_anomaly(days=28, limit=2).items():
    print(address, info["n_emails"], "of", info["total_emails"], f"({info['percentage']}%)")
```

For `get_action_summary()`, `get_dash_stats()` and `get_data_loss()` the API guide gives no response schema; see the instance's api-docs.

### Email Actions

Perform an action on a specific email identified by UUID (`POST /v1.0/emails/{uuid}/action`). Requires Email logs plus Manual Action or Restricted Manual Action.

```python
# Discover the actions your instance supports first
available = email.get_actions()

# The body is passed through unchanged as JSON - build it according to the api-docs
result = email.email_action(uuid="email-uuid-here", data={...})
```

#### Parameters

- `uuid` (str): Email UUID
- `data` (dict): JSON request body. The request body schema (action names and fields) is not defined in the API guide; see `https://[instance]/agemail/api/api-docs` and `get_actions()`.

#### Response

Returns the parsed JSON response. See the instance's api-docs for its schema.

### Get Email Details

Retrieve a specific email by UUID (`GET /v1.0/emails/{uuid}`).

```python
email_info = email.get_email(uuid="email-uuid-here")

# Include email headers
email_with_headers = email.get_email(uuid="email-uuid-here", include_headers=True)
```

#### Parameters

- `uuid` (str): Email UUID
- `include_headers` (bool, optional): Sent as `include_headers=true` / `false` (lowercase)

#### Response

Returns the parsed JSON. The API guide gives no schema; see the instance's api-docs.

### Download Email

Download the raw email content (`GET /v1.0/emails/{uuid}/download`). Requires Email logs plus Download Email.

```python
email_content = email.download_email(uuid="email-uuid-here")

with open("suspicious_email.eml", "wb") as f:
    f.write(email_content)
```

#### Parameters

- `uuid` (str): Email UUID

#### Response

Returns the raw response body as `bytes` (not parsed JSON).

### Search Emails

Search emails (`POST /v1.0/emails/search`).

```python
# The body is passed through unchanged as JSON - build it according to the api-docs
results = email.search_emails(data={...})
```

#### Parameters

- `data` (dict): JSON search body. The body schema and the available filters are not defined in the API guide; see `https://[instance]/agemail/api/api-docs` and use `get_filters()` to list the filters your instance supports.

#### Response

Returns the parsed JSON. See the instance's api-docs for its schema.

### Resource Methods

These take no parameters other than `timeout` and return the parsed JSON. The API guide gives no response schema for them; see the instance's api-docs.

```python
tags = email.get_tags()        # GET /v1.0/resources/tags
actions = email.get_actions()  # GET /v1.0/resources/actions
filters = email.get_filters()  # GET /v1.0/resources/filters
```

### Audit Methods

Both audit endpoints require Email logs plus Audit Log (Darktrace/Email).

```python
event_types = email.get_event_types()   # GET /v1.0/system/audit/eventTypes

events = email.get_audit_events(event_type="login", limit=10, offset=0)   # GET /v1.0/system/audit/events
```

#### `get_audit_events()` Parameters

- `event_type` (str, optional): Filter by event type (sent as `eventType`). Valid values come from `get_event_types()`.
- `limit` (int, optional): Limit the number of results (sent as `limit`)
- `offset` (int, optional): Offset for pagination (sent as `offset`)

The API guide does not describe these parameters or the response; see the instance's api-docs.

## Example

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Users with the most anomalous email activity (dict keyed by email address)
anomalies = client.email.get_user_anomaly(days=28, limit=10)
for address, info in anomalies.items():
    print(f"{address}: {info['n_emails']}/{info['total_emails']} emails ({info['percentage']}%)")

# Fetch one email and save its raw MIME content
details = client.email.get_email(uuid="email-uuid-here", include_headers=True)
raw = client.email.download_email(uuid="email-uuid-here")
with open("email.eml", "wb") as f:
    f.write(raw)
```

## Error Handling

The SDK raises its own exceptions, which subclass `requests.HTTPError`.

```python
from darktrace import DarktraceClient, DarktraceError, ForbiddenError

try:
    stats = client.email.get_dash_stats(days=7)
except ForbiddenError:
    print("Access denied - check the Darktrace/Email permissions of the API token")
except DarktraceError as e:
    print(f"API error: {e} (status {e.status_code})")
```

## Notes

- All endpoints live under `/agemail/api/ep/api/v1.0/` and use the standard Darktrace API token workflow with the relevant Darktrace/Email permissions.
- The endpoint list in the API guide is "subject to change"; the instance's api-docs at `/agemail/api/api-docs` are authoritative for parameters, bodies and schemas.
- Use `get_actions()`, `get_filters()` and `get_event_types()` to discover the values your instance accepts before building action bodies, search bodies or audit filters.
