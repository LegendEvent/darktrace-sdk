# Authentication Fix: Parameter Order Consistency

## Issue Description

The Darktrace SDK was experiencing API signature errors (400 Bad Request) due to a parameter order mismatch between signature calculation and the actual request URL. This issue specifically affected endpoints with query parameters, such as the Intel Feed endpoint.

### Root Cause

The Darktrace API requires that query parameters be included in the signature calculation in **alphabetical order**. However, the SDK was:

1. Correctly sorting parameters alphabetically for signature calculation:
   ```python
   query_string = '&'.join(f"{k}={v}" for k, v in sorted(params.items()))
   signature_path = f"{request_path}?{query_string}"
   ```

2. But using the original unsorted parameters in the actual request:
   ```python
   response = requests.get(url, headers=headers, params=query_params, verify=False)
   ```

This caused a mismatch between the signature calculation and the actual request, resulting in API signature errors.

### Example

For a request to `/intelfeed` with parameters `source=Threat+Intel` and `fulldetails=true`:

1. **Signature calculation**: Used `/intelfeed?fulldetails=true&source=Threat+Intel` (alphabetically sorted)
2. **Actual request URL**: Used `/intelfeed?source=Threat+Intel&fulldetails=true` (original order)

## Fix Implementation

The fix ensures that the same sorted parameters are used in both the signature calculation and the actual request:

1. **Updated Authentication Class**:
   - Modified `DarktraceAuth.get_headers()` to return both headers and sorted parameters
   - The sorted parameters are then used in the actual request

2. **BaseEndpoint Class**:
   - Created a base class for all endpoint modules
   - Handles parameter sorting consistently across all API calls

3. **Updated All Endpoint Modules**:
   - All modules now inherit from the BaseEndpoint class
   - All API calls use the same sorted parameters for both signature calculation and requests

### Key Code Changes

1. **Authentication Class**:
   ```python
   def get_headers(self, request_path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
       date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
       
       signature_path = request_path
       sorted_params = None
       
       if params and len(params) > 0:
           # Sort parameters alphabetically by key as required by Darktrace API
           sorted_params = dict(sorted(params.items()))
           query_string = '&'.join(f"{k}={v}" for k, v in sorted_params.items())
           signature_path = f"{request_path}?{query_string}"
       
       signature = self.generate_signature(signature_path, date)
       
       return {
           'headers': {
               'DTAPI-Token': self.public_token,
               'DTAPI-Date': date,
               'DTAPI-Signature': signature,
               'Content-Type': 'application/json',
           },
           'params': sorted_params or params
       }
   ```

2. **BaseEndpoint Class**:
   ```python
   def _get_headers(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, str], Optional[Dict[str, Any]]]:
       result = self.client.auth.get_headers(endpoint, params)
       return result['headers'], result['params']
   ```

3. **Endpoint Module Example**:
   ```python
   def get(self, **params):
       endpoint = '/devices'
       url = f"{self.client.host}{endpoint}"
       headers, sorted_params = self._get_headers(endpoint, params)
       response = requests.get(url, headers=headers, params=sorted_params or params, verify=False)
       response.raise_for_status()
       return response.json()
   ```

## Testing

To test the fix:

1. Try using the Intel Feed module with the `sources=true` parameter:
   ```python
   sources = client.intelfeed.get_sources()
   ```

2. Try using the Intel Feed module with the `source` and `fulldetails` parameters:
   ```python
   detailed_domains = client.intelfeed.get_by_source("ThreatIntel", full_details=True)
   ```

The requests should now succeed without any API signature errors.

## Conclusion

This fix ensures that parameter order is consistent between signature calculation and request URLs, resolving the API signature errors while maintaining clean separation of concerns with sorting logic in the authentication module. 