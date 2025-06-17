# Authentication Module

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

To use the Darktrace API, you need to generate API tokens from your Darktrace instance:

1. Log in to your Darktrace instance with an administrator account
2. Navigate to System Config > API Keys
3. Click "Generate New API Key"
4. Save both the public and private tokens securely

## Authentication Process

The authentication process is handled automatically by the SDK, but here's how it works:

1. For each API request, the SDK generates a timestamp in UTC format
2. It creates a signature using:
   - The request path (e.g., `/devices`)
   - Any query parameters, sorted alphabetically by key (e.g., `?fulldetails=true&source=ThreatIntel`)
   - Your public token
   - The current timestamp
   - Your private token as the HMAC key
3. The signature is generated using HMAC-SHA1 and converted to a hexadecimal string
4. The headers are added to the request:
   - `DTAPI-Token`: Your public token
   - `DTAPI-Date`: The current timestamp
   - `DTAPI-Signature`: The generated signature
   - `Content-Type`: `application/json`
5. The same sorted query parameters are used in the actual request to ensure consistency

## Parameter Ordering

The Darktrace API requires that query parameters be included in the signature calculation in **alphabetical order**. The SDK ensures that:

1. Parameters are sorted alphabetically for signature calculation
2. The same sorted parameters are used in the actual request

This prevents API signature errors that can occur if the parameter order differs between signature calculation and the actual request.

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
- **403 Forbidden**: Valid tokens but insufficient permissions
- **429 Too Many Requests**: Rate limiting applied

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