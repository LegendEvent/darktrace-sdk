# Enums Module

The Enums module provides access to enumeration mappings that translate numeric codes to human-readable string values used throughout the Darktrace API. This is essential for interpreting API responses that contain enumerated values such as device types, connection states, threat levels, and other categorical data.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the enums module
enums = client.enums
```

## Methods Overview

The Enums module provides the following method:

- **`get()`** - Retrieve enumeration mappings for all types or specific categories

## Methods

### Get Enumeration Values

Retrieve string values for numeric codes (enumerated types) used throughout the Darktrace API. This endpoint provides translations for all categorical data in API responses.

```python
# Get all enumeration mappings
all_enums = enums.get()

# Get specific enumeration category
countries = enums.get(responsedata="countries")
protocols = enums.get(responsedata="protocols")
device_types = enums.get(responsedata="devicetypes")

# Get multiple categories
threat_data = enums.get(responsedata="threattypes,severities")
```

#### Parameters

- `responsedata` (str, optional): Restrict returned JSON to specific field/object (comma-separated for multiple fields)
- `**params`: Additional query parameters for forward compatibility

#### Response Structure

```python
{
  "countries": {
    "0": "Unknown",
    "1": "Afghanistan",
    "2": "Albania", 
    "3": "Algeria",
    "4": "Andorra",
    "5": "Angola",
    // ... more country mappings
    "840": "United States",
    "826": "United Kingdom"
  },
  "protocols": {
    "0": "Unknown",
    "1": "ICMP",
    "6": "TCP",
    "17": "UDP",
    "47": "GRE",
    "50": "ESP",
    "51": "AH",
    // ... more protocol mappings
  },
  "devicetypes": {
    "0": "Unknown",
    "1": "Server",
    "2": "Desktop",
    "3": "Laptop",
    "4": "Mobile",
    "5": "Printer",
    "6": "Network Device",
    "7": "IoT Device",
    "8": "Virtual Machine",
    // ... more device type mappings
  },
  "threattypes": {
    "0": "Unknown",
    "1": "Malware",
    "2": "Data Exfiltration",
    "3": "Lateral Movement",
    "4": "Command & Control",
    "5": "Reconnaissance",
    "6": "Privilege Escalation",
    // ... more threat type mappings
  },
  "severities": {
    "0": "Informational",
    "1": "Low",
    "2": "Medium", 
    "3": "High",
    "4": "Critical"
  },
  "connectionstates": {
    "0": "Unknown",
    "1": "Established",
    "2": "Failed",
    "3": "Rejected",
    "4": "Timeout",
    "5": "Reset"
  },
  "operatingsystems": {
    "0": "Unknown",
    "1": "Windows",
    "2": "Linux",
    "3": "macOS",
    "4": "iOS",
    "5": "Android",
    "6": "FreeBSD",
    "7": "Solaris"
  },
  "services": {
    "20": "FTP Data",
    "21": "FTP Control",
    "22": "SSH",
    "23": "Telnet",
    "25": "SMTP",
    "53": "DNS",
    "80": "HTTP",
    "110": "POP3",
    "143": "IMAP",
    "443": "HTTPS",
    "993": "IMAPS",
    "995": "POP3S"
  }
}

# With responsedata="countries"
{
  "countries": {
    "0": "Unknown",
    "1": "Afghanistan",
    "2": "Albania",
    // ... only country mappings
  }
}

# With responsedata="protocols,severities"
{
  "protocols": {
    "0": "Unknown",
    "1": "ICMP",
    "6": "TCP",
    "17": "UDP"
    // ... protocol mappings
  },
  "severities": {
    "0": "Informational",
    "1": "Low",
    "2": "Medium",
    "3": "High",
    "4": "Critical"
  }
}
```

## Examples

### Comprehensive Enumeration Mapping

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get all enumeration mappings
all_enums = client.enums.get()

print("Darktrace Enumeration Mappings")
print("=" * 50)

# Display overview of available enum categories
enum_categories = list(all_enums.keys())
print(f"Available enumeration categories: {len(enum_categories)}")

for category in sorted(enum_categories):
    enum_values = all_enums[category]
    print(f"\n{category.upper()}:")
    print(f"  Total values: {len(enum_values)}")
    
    # Show sample values
    sample_items = list(enum_values.items())[:5]
    for code, description in sample_items:
        print(f"  {code}: {description}")
    
    if len(enum_values) > 5:
        print(f"  ... and {len(enum_values) - 5} more values")

# Create enumeration lookup functions
def create_enum_lookup(enum_data):
    """Create lookup functions for each enumeration category"""
    lookups = {}
    
    for category, mappings in enum_data.items():
        # Create forward lookup (code -> string)
        forward_lookup = {int(k): v for k, v in mappings.items()}
        
        # Create reverse lookup (string -> code)
        reverse_lookup = {v: int(k) for k, v in mappings.items()}
        
        lookups[category] = {
            'to_string': forward_lookup,
            'to_code': reverse_lookup,
            'mappings': mappings
        }
    
    return lookups

# Create lookup functions
enum_lookups = create_enum_lookup(all_enums)

# Example usage of lookup functions
def demonstrate_lookups():
    print("\nEnumeration Lookup Examples")
    print("=" * 40)
    
    # Protocol lookup
    if 'protocols' in enum_lookups:
        protocol_lookup = enum_lookups['protocols']
        
        # Code to string
        tcp_name = protocol_lookup['to_string'].get(6, "Unknown")
        udp_name = protocol_lookup['to_string'].get(17, "Unknown")
        print(f"Protocol 6: {tcp_name}")
        print(f"Protocol 17: {udp_name}")
        
        # String to code
        http_code = protocol_lookup['to_code'].get("TCP", "Unknown")
        print(f"TCP protocol code: {http_code}")
    
    # Country lookup
    if 'countries' in enum_lookups:
        country_lookup = enum_lookups['countries']
        
        us_name = country_lookup['to_string'].get(840, "Unknown")
        uk_name = country_lookup['to_string'].get(826, "Unknown")
        print(f"Country 840: {us_name}")
        print(f"Country 826: {uk_name}")
    
    # Severity lookup
    if 'severities' in enum_lookups:
        severity_lookup = enum_lookups['severities']
        
        for code in range(0, 5):
            severity_name = severity_lookup['to_string'].get(code, "Unknown")
            print(f"Severity {code}: {severity_name}")

demonstrate_lookups()
```

### API Response Enhancement

```python
# Enhance API responses by translating enumerated values
def enhance_api_response(api_response, enum_data):
    """
    Enhance API response by adding human-readable strings for enumerated values
    """
    enhanced_response = api_response.copy()
    
    # Common enum field mappings
    enum_field_mappings = {
        'protocol': 'protocols',
        'country': 'countries',
        'devicetype': 'devicetypes',
        'severity': 'severities',
        'os': 'operatingsystems',
        'service': 'services',
        'threattype': 'threattypes',
        'connectionstate': 'connectionstates'
    }
    
    def enhance_object(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = f"{path}.{key}" if path else key
                
                # Check if this field should be enhanced
                enum_category = enum_field_mappings.get(key.lower())
                if enum_category and enum_category in enum_data:
                    # Add human-readable version
                    if isinstance(value, (int, str)):
                        try:
                            enum_value = enum_data[enum_category].get(str(value), "Unknown")
                            obj[f"{key}_name"] = enum_value
                        except (ValueError, KeyError):
                            pass
                
                # Recursively enhance nested objects
                if isinstance(value, (dict, list)):
                    enhance_object(value, current_path)
                    
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    enhance_object(item, path)
    
    enhance_object(enhanced_response)
    return enhanced_response

# Example: Enhance device information
sample_device_response = {
    "devices": [
        {
            "id": 1,
            "ip": "192.168.1.100",
            "hostname": "workstation-01",
            "devicetype": 2,
            "os": 1,
            "country": 840,
            "connections": [
                {
                    "protocol": 6,
                    "port": 443,
                    "service": 443,
                    "connectionstate": 1
                }
            ]
        },
        {
            "id": 2,
            "ip": "192.168.1.200", 
            "hostname": "server-01",
            "devicetype": 1,
            "os": 2,
            "country": 826
        }
    ]
}

# Enhance the response
enhanced_devices = enhance_api_response(sample_device_response, all_enums)

print("Enhanced Device Response:")
print("=" * 40)

for device in enhanced_devices.get('devices', []):
    print(f"\nDevice: {device.get('hostname', 'Unknown')}")
    print(f"  IP: {device.get('ip')}")
    print(f"  Type: {device.get('devicetype')} ({device.get('devicetype_name', 'Unknown')})")
    print(f"  OS: {device.get('os')} ({device.get('os_name', 'Unknown')})")
    print(f"  Country: {device.get('country')} ({device.get('country_name', 'Unknown')})")
    
    if 'connections' in device:
        print("  Connections:")
        for conn in device['connections']:
            protocol_name = conn.get('protocol_name', 'Unknown')
            service_name = conn.get('service_name', 'Unknown')
            state_name = conn.get('connectionstate_name', 'Unknown')
            print(f"    {protocol_name}:{conn.get('port')} ({service_name}) - {state_name}")
```

### Enumeration Analysis and Statistics

```python
# Analyze enumeration data for insights
def analyze_enumerations():
    all_enums = client.enums.get()
    
    print("Enumeration Analysis")
    print("=" * 50)
    
    analysis = {
        'categories': len(all_enums),
        'total_values': 0,
        'category_sizes': {},
        'largest_categories': [],
        'smallest_categories': []
    }
    
    # Analyze each category
    for category, mappings in all_enums.items():
        category_size = len(mappings)
        analysis['total_values'] += category_size
        analysis['category_sizes'][category] = category_size
    
    # Sort categories by size
    sorted_categories = sorted(
        analysis['category_sizes'].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    analysis['largest_categories'] = sorted_categories[:5]
    analysis['smallest_categories'] = sorted_categories[-5:]
    
    # Display analysis
    print(f"Total enumeration categories: {analysis['categories']}")
    print(f"Total enumeration values: {analysis['total_values']}")
    print(f"Average values per category: {analysis['total_values'] / analysis['categories']:.1f}")
    
    print(f"\nLargest categories:")
    for category, size in analysis['largest_categories']:
        print(f"  {category}: {size} values")
    
    print(f"\nSmallest categories:")
    for category, size in analysis['smallest_categories']:
        print(f"  {category}: {size} values")
    
    # Look for patterns in enumeration values
    print(f"\nEnumeration Patterns:")
    
    # Check for standard severity scales
    if 'severities' in all_enums:
        severities = all_enums['severities']
        print(f"  Severity scale: {len(severities)} levels")
        for code, level in sorted(severities.items(), key=lambda x: int(x[0])):
            print(f"    {code}: {level}")
    
    # Check for protocol coverage
    if 'protocols' in all_enums:
        protocols = all_enums['protocols']
        common_protocols = ['6', '17', '1']  # TCP, UDP, ICMP
        print(f"  Protocol coverage: {len(protocols)} protocols")
        print(f"  Common protocols:")
        for proto_code in common_protocols:
            if proto_code in protocols:
                print(f"    {proto_code}: {protocols[proto_code]}")
    
    # Check geographic coverage
    if 'countries' in all_enums:
        countries = all_enums['countries']
        print(f"  Geographic coverage: {len(countries)} countries/regions")
        
        # Look for major countries
        major_country_codes = ['840', '826', '276', '250', '392', '156']  # US, UK, DE, FR, JP, CN
        print(f"  Major countries:")
        for country_code in major_country_codes:
            if country_code in countries:
                print(f"    {country_code}: {countries[country_code]}")
    
    return analysis

# Run enumeration analysis
enum_analysis = analyze_enumerations()
```

### Specific Enumeration Retrieval

```python
# Retrieve specific enumeration categories
def get_specific_enums():
    print("Specific Enumeration Retrieval")
    print("=" * 50)
    
    # Get only country information
    countries = client.enums.get(responsedata="countries")
    if 'countries' in countries:
        country_data = countries['countries']
        print(f"Countries: {len(country_data)} entries")
        
        # Find specific countries
        target_countries = ['United States', 'United Kingdom', 'Germany', 'France', 'Japan']
        found_countries = {}
        
        for code, name in country_data.items():
            if name in target_countries:
                found_countries[name] = code
        
        print(f"Target countries found:")
        for country, code in found_countries.items():
            print(f"  {country}: {code}")
    
    # Get protocol information
    protocols = client.enums.get(responsedata="protocols")
    if 'protocols' in protocols:
        protocol_data = protocols['protocols']
        print(f"\nProtocols: {len(protocol_data)} entries")
        
        # Common network protocols
        common_protocols = ['1', '6', '17', '47', '50']  # ICMP, TCP, UDP, GRE, ESP
        print(f"Common protocols:")
        for proto_code in common_protocols:
            if proto_code in protocol_data:
                print(f"  {proto_code}: {protocol_data[proto_code]}")
    
    # Get severity levels
    severities = client.enums.get(responsedata="severities")
    if 'severities' in severities:
        severity_data = severities['severities']
        print(f"\nSeverity levels: {len(severity_data)} levels")
        
        for code in sorted(severity_data.keys(), key=int):
            print(f"  Level {code}: {severity_data[code]}")
    
    # Get multiple categories at once
    multiple_enums = client.enums.get(responsedata="devicetypes,operatingsystems,services")
    
    print(f"\nMultiple categories retrieved:")
    for category in multiple_enums.keys():
        category_size = len(multiple_enums[category])
        print(f"  {category}: {category_size} entries")

get_specific_enums()
```

### Enumeration Caching and Optimization

```python
# Implement caching for enumeration data
import time
import json
from datetime import datetime, timedelta

class EnumCache:
    def __init__(self, client, cache_duration_hours=24):
        self.client = client
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache = {}
        self.last_updated = {}
    
    def get_enums(self, responsedata=None, force_refresh=False):
        """Get enumeration data with caching"""
        cache_key = responsedata or "all"
        
        # Check if cache is valid
        if not force_refresh and cache_key in self.cache:
            if datetime.now() - self.last_updated[cache_key] < self.cache_duration:
                print(f"Returning cached enumeration data for: {cache_key}")
                return self.cache[cache_key]
        
        # Fetch fresh data
        print(f"Fetching fresh enumeration data for: {cache_key}")
        if responsedata:
            enum_data = self.client.enums.get(responsedata=responsedata)
        else:
            enum_data = self.client.enums.get()
        
        # Update cache
        self.cache[cache_key] = enum_data
        self.last_updated[cache_key] = datetime.now()
        
        return enum_data
    
    def get_enum_value(self, category, code):
        """Get specific enumeration value with caching"""
        all_enums = self.get_enums()
        
        if category in all_enums:
            return all_enums[category].get(str(code), "Unknown")
        return "Unknown"
    
    def save_cache(self, filepath):
        """Save cache to file"""
        cache_data = {
            'cache': self.cache,
            'last_updated': {k: v.isoformat() for k, v in self.last_updated.items()},
            'cache_duration_hours': self.cache_duration.total_seconds() / 3600
        }
        
        with open(filepath, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"Enumeration cache saved to: {filepath}")
    
    def load_cache(self, filepath):
        """Load cache from file"""
        try:
            with open(filepath, 'r') as f:
                cache_data = json.load(f)
            
            self.cache = cache_data.get('cache', {})
            self.last_updated = {
                k: datetime.fromisoformat(v) 
                for k, v in cache_data.get('last_updated', {}).items()
            }
            
            # Update cache duration if specified
            if 'cache_duration_hours' in cache_data:
                self.cache_duration = timedelta(hours=cache_data['cache_duration_hours'])
            
            print(f"Enumeration cache loaded from: {filepath}")
            return True
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Could not load cache: {e}")
            return False

# Example usage of enumeration caching
enum_cache = EnumCache(client, cache_duration_hours=12)

# Load existing cache if available
enum_cache.load_cache('darktrace_enum_cache.json')

# Use cached enumeration data
countries = enum_cache.get_enums(responsedata="countries")
protocols = enum_cache.get_enums(responsedata="protocols")

# Get specific values
us_country = enum_cache.get_enum_value("countries", 840)
tcp_protocol = enum_cache.get_enum_value("protocols", 6)

print(f"Country 840: {us_country}")
print(f"Protocol 6: {tcp_protocol}")

# Save cache for future use
enum_cache.save_cache('darktrace_enum_cache.json')
```

### Integration with Other Modules

```python
# Demonstrate integration with other Darktrace modules
def enhance_device_data_with_enums():
    """Enhance device data with enumeration translations"""
    
    # Get enumeration mappings
    enums = client.enums.get()
    
    # Get device data (assuming devices module exists)
    try:
        devices = client.devices.get(count=5)  # Get first 5 devices
        
        print("Enhanced Device Information")
        print("=" * 50)
        
        for device in devices.get('devices', []):
            print(f"\nDevice: {device.get('hostname', 'Unknown')}")
            print(f"  IP: {device.get('ip', 'Unknown')}")
            
            # Enhance device type
            device_type_code = device.get('devicetype')
            if device_type_code is not None and 'devicetypes' in enums:
                device_type_name = enums['devicetypes'].get(str(device_type_code), 'Unknown')
                print(f"  Type: {device_type_name} (code: {device_type_code})")
            
            # Enhance operating system
            os_code = device.get('os')
            if os_code is not None and 'operatingsystems' in enums:
                os_name = enums['operatingsystems'].get(str(os_code), 'Unknown')
                print(f"  OS: {os_name} (code: {os_code})")
            
            # Enhance country
            country_code = device.get('country')
            if country_code is not None and 'countries' in enums:
                country_name = enums['countries'].get(str(country_code), 'Unknown')
                print(f"  Country: {country_name} (code: {country_code})")
    
    except AttributeError:
        print("Devices module not available for integration example")
    except Exception as e:
        print(f"Error enhancing device data: {e}")

# Run integration example
enhance_device_data_with_enums()
```

## Error Handling

```python
try:
    # Attempt to get enumeration data
    all_enums = client.enums.get()
    
    print(f"Retrieved {len(all_enums)} enumeration categories")
    
    # Process enumeration data
    for category, mappings in all_enums.items():
        print(f"Category: {category}")
        print(f"  Values: {len(mappings)}")
        
        # Display first few values
        for i, (code, description) in enumerate(mappings.items()):
            if i >= 3:  # Show only first 3
                break
            print(f"    {code}: {description}")
        
        if len(mappings) > 3:
            print(f"    ... and {len(mappings) - 3} more values")
        
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 403:
            print("Access denied - check API permissions for enums endpoint")
        elif e.response.status_code == 404:
            print("Enums endpoint not found - check Darktrace version compatibility")
        else:
            print(f"Response: {e.response.text}")
            
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
    print("The response might not be valid JSON")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Enumeration Categories
Common enumeration categories include:
- **countries**: ISO country codes and names
- **protocols**: Network protocol numbers and names
- **devicetypes**: Device classification types
- **operatingsystems**: Operating system identifiers
- **severities**: Alert/threat severity levels
- **services**: Common network services by port
- **threattypes**: Threat classification categories
- **connectionstates**: Network connection status values

### Value Type Patterns
- **Numeric codes**: Most enumerations use integer codes starting from 0
- **String descriptions**: Human-readable names for each code
- **Hierarchical**: Some categories may have hierarchical relationships
- **Standards-based**: Many follow international standards (ISO, RFC, etc.)

### Response Data Filtering
Use `responsedata` parameter to optimize API calls:
- `"countries"`: Get only country mappings
- `"protocols"`: Get only protocol mappings
- `"severities"`: Get only severity level mappings
- `"countries,protocols"`: Get multiple specific categories
- No parameter: Get all enumeration categories

### Performance Considerations
- **Caching recommended**: Enumeration data changes infrequently
- **Selective retrieval**: Use `responsedata` for specific categories only
- **Memory usage**: Full enumeration data can be substantial
- **Network efficiency**: Cache to minimize repeated API calls

### Integration Patterns
- **API response enhancement**: Translate codes to readable strings
- **User interface**: Display meaningful names instead of codes
- **Data validation**: Validate input values against known enumerations
- **Reporting**: Generate human-readable reports with proper names
- **Configuration**: Use enumeration data for dropdown menus and selection

### Common Use Cases
- **Data interpretation**: Translate numeric codes in API responses
- **User interfaces**: Populate dropdown menus and selection lists
- **Report generation**: Create readable reports with proper descriptions
- **Data validation**: Validate user input against known enumeration values
- **Integration**: Map between Darktrace and external system nomenclature

### Caching Strategies
- **Local storage**: Cache enumeration data in application memory
- **File-based**: Save enumeration mappings to local files
- **Database**: Store in application database for shared access
- **TTL management**: Implement time-to-live for cache invalidation
- **Partial updates**: Refresh specific categories when needed

### Error Scenarios
- **Network connectivity**: Handle API communication failures
- **Authentication**: Manage token expiration and refresh
- **Data format**: Handle unexpected response formats
- **Missing categories**: Gracefully handle missing enumeration categories
- **Invalid codes**: Provide fallback values for unknown codes

### Best Practices
- **Implement caching**: Enumeration data changes rarely
- **Graceful degradation**: Show codes if descriptions unavailable
- **Regular updates**: Periodically refresh cached enumeration data
- **Error handling**: Handle missing or invalid enumeration categories
- **Documentation**: Maintain local documentation of enumeration meanings

### Version Compatibility
- **API evolution**: New enumeration categories may be added
- **Backward compatibility**: Existing codes typically remain stable
- **Version checking**: Verify enumeration availability for your API version
- **Feature detection**: Check for enumeration category existence before use
- **Migration planning**: Plan for enumeration changes in upgrades
