# Authentication Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The Authentication module handles the HMAC-SHA1 signature generation required for authenticating with the Darktrace API.

## Overview

Darktrace API uses a token-based authentication system with HMAC-SHA1 signatures. Each request requires:

1. A public token (provided in the `DTAPI-Token` header)
2. The current date/time (provided in the `DTAPI-Date` header)
3. A signature generated using the private token (provided in the `DTAPI-Signature` header)

The SDK handles all of this automatically when you initialize the client with your tokens.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)
```

## Getting API Tokens

Each Darktrace master instance needs an API token pair (public and private). The private token is shown only once, so store it securely.

**Per-user token** (Threat Visualizer 5.1 and later):

1. The user must first be granted API access. Only local users (created within the Threat Visualizer) can have tokens, not LDAP or SAML SSO users.
2. In the Permissions Admin page (Main Menu > Admin, "Created Accounts" tab), edit the user and turn on "API Access" in the Flags step.
3. As that user, open Account Settings from the main menu, click "API Access" and then "New".

A user token can only reach the endpoints that user can access in the Threat Visualizer interface (see "Minimum Required Permissions for API Endpoints" in the API guide).

**Global token** (generated before 5.1 or from System Config):

1. Open System Config > Settings on the Threat Visualizer.
2. In the "API Token" subsection, click "New".

Actions made with a global token are attributed to the `DTAPI_[token]` user, where `[token]` is the public token.

## Authentication Process

The authentication process is handled automatically by the SDK, but here's how it works:

1. For each API request, the SDK generates a timestamp in UTC format
2. It creates a signature using:
   - The request path (e.g., `/devices`), without the host
   - Any query parameters, sorted alphabetically by key (e.g., `?fulldetails=true&source=ThreatIntel`)
   - Your public token
   - The current timestamp (`YYYY-MM-DD HH:MM:SS`, UTC)
   - Your private token as the HMAC key

   The signed string is `<path and parameters>\n<public token>\n<date>`.
3. The signature is generated using HMAC-SHA1 and converted to a hexadecimal string
4. The headers are added to the request:
   - `DTAPI-Token`: Your public token
   - `DTAPI-Date`: The current timestamp
   - `DTAPI-Signature`: The generated signature
   - `Content-Type`: `application/json` by default (form POSTs override it with `application/x-www-form-urlencoded`)
5. The same sorted query parameters are used in the actual request to ensure consistency

## Parameter Ordering and Request Bodies

The Darktrace API recomputes the signature from what it receives, so the SDK signs exactly what it sends:

1. **GET query parameters** are sorted alphabetically. List/tuple values are signed as repeated keys (`a=1&a=2`, the way `requests` sends them), `None` values are dropped and booleans are sent lowercase (`true`/`false`). Values are signed as plain `key=value` text, without extra encoding.
2. **Form POSTs** (`analyst.acknowledge/unacknowledge/pin/unpin`, `tags.post_entities`) send one sorted, url-encoded body, and the same string is signed (the API guide: "add each POST parameter into the query string"). Before 0.10.1 these calls failed with `API SIGNATURE ERROR` (#59).
3. **JSON POSTs** are signed with the compact JSON body appended after the path, e.g. `/modelbreaches/101/comments?{"message":"x"}`, as in the API guide. If a JSON POST also has query parameters, the SDK signs `path?a=1&{json}`; the guide does not define this combined case.

This prevents API signature errors that occur when the signed string differs from the request on the wire.

## Security Best Practices

1. **Store tokens securely**: Never hardcode tokens in your application code
2. **Use environment variables**: Store tokens in environment variables or a secure vault
3. **Limit token permissions**: Generate tokens with the minimum required permissions
4. **Rotate tokens regularly**: Create new tokens and retire old ones periodically

## Example: Using Environment Variables

```python
import os
from darktrace import DarktraceClient

# Load tokens from environment variables
public_token = os.environ.get("DARKTRACE_PUBLIC_TOKEN")
private_token = os.environ.get("DARKTRACE_PRIVATE_TOKEN")
host = os.environ.get("DARKTRACE_HOST")

# Initialize client with tokens
client = DarktraceClient(
    host=host,
    public_token=public_token,
    private_token=private_token
)
```

## Error Handling

Common authentication errors include:

- **401 Unauthorized**: Invalid tokens or signature
- **403 Forbidden**: Valid tokens but insufficient permissions (the token's user cannot access the endpoint)

The `DTAPI-Date` must be within 30 minutes of the Darktrace system time (UTC), so a badly skewed local clock causes authentication failures. The SDK's exceptions (`AuthenticationError`, `ForbiddenError`, ...) subclass `requests.HTTPError`.

```python
import requests
from darktrace import DarktraceClient

try:
    client = DarktraceClient(
        host="https://your-darktrace-instance",
        public_token="YOUR_PUBLIC_TOKEN",
        private_token="YOUR_PRIVATE_TOKEN"
    )
    
    # Test authentication with a simple API call
    status = client.status.get()
    print("Authentication successful!")

except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Authentication failed: Invalid tokens or signature")
    elif e.response.status_code == 403:
        print("Authentication failed: Insufficient permissions")
    else:
        print(f"HTTP error: {e}")
except Exception as e:
    print(f"Error: {e}")
