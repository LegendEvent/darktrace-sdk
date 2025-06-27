# CVEs Module

The CVEs module provides access to CVE (Common Vulnerabilities and Exposures) information from the Darktrace/OT ICS Vulnerability Tracker. This module allows you to retrieve vulnerability information related to devices in your network infrastructure.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the CVEs module
cves = client.cves
```

## Methods Overview

The CVEs module provides the following method:

- **`get()`** - Retrieve CVE information with device filtering options

## Methods

### Get CVEs

Retrieve CVE information for devices from the Darktrace/OT ICS Vulnerability Tracker. This provides visibility into known vulnerabilities affecting devices in your network.

```python
# Get all CVEs
all_cves = cves.get()

# Get CVEs for specific device
device_cves = cves.get(did=123)

# Get CVEs with full device details
detailed_cves = cves.get(
    did=123,
    fulldevicedetails=True
)

# Get all CVEs with complete device information
all_detailed_cves = cves.get(fulldevicedetails=True)
```

#### Parameters

- `did` (int, optional): Device ID to filter CVEs for a specific device
- `fulldevicedetails` (bool, optional): Return full device detail objects for all referenced devices. Alters JSON structure to include separate `cves` and `devices` objects

#### Response Structure

```python
# Standard response (fulldevicedetails=False or not specified)
{
  "cves": [
    {
      "cveId": "CVE-2023-12345",
      "description": "Vulnerability description",
      "severity": "HIGH",
      "score": 8.5,
      "published": "2023-06-15T10:00:00Z",
      "modified": "2023-06-15T10:00:00Z",
      "affectedDevices": [
        {
          "did": 123,
          "hostname": "server01",
          "ip": "192.168.1.100",
          "vendor": "Manufacturer Name",
          "product": "Product Name",
          "version": "1.2.3"
        }
      ]
    },
    // ... more CVEs
  ]
}

# With fulldevicedetails=True
{
  "cves": [
    {
      "cveId": "CVE-2023-12345",
      "description": "Vulnerability description",
      "severity": "HIGH",
      "score": 8.5,
      "affectedDeviceIds": [123, 456, 789]
    }
  ],
  "devices": {
    "123": {
      "did": 123,
      "hostname": "server01",
      "ip": "192.168.1.100",
      "vendor": "Manufacturer Name",
      // ... complete device information
    },
    // ... more devices
  }
}
```

## Examples

### Basic CVE Retrieval

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

# Get all CVE information
all_cves = client.cves.get()

print(f"Total CVEs found: {len(all_cves.get('cves', []))}")

for cve in all_cves.get('cves', []):
    cve_id = cve.get('cveId', 'Unknown')
    severity = cve.get('severity', 'Unknown')
    score = cve.get('score', 0)
    affected_count = len(cve.get('affectedDevices', []))
    
    print(f"CVE: {cve_id}")
    print(f"  Severity: {severity} (Score: {score})")
    print(f"  Affected devices: {affected_count}")
    print(f"  Description: {cve.get('description', 'N/A')[:100]}...")
```

### Device-Specific Vulnerability Analysis

```python
# Analyze vulnerabilities for a specific device
device_id = 123
device_cves = client.cves.get(did=device_id)

print(f"CVE Analysis for Device {device_id}:")

if 'cves' in device_cves:
    cves_list = device_cves['cves']
    
    if not cves_list:
        print("  No CVEs found for this device")
    else:
        # Sort by severity/score
        sorted_cves = sorted(cves_list, key=lambda x: x.get('score', 0), reverse=True)
        
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for cve in sorted_cves:
            severity = cve.get('severity', 'UNKNOWN')
            if severity in severity_counts:
                severity_counts[severity] += 1
            
            print(f"  {cve.get('cveId')}: {severity} ({cve.get('score')})")
            
            # Show affected device details if available
            affected_devices = cve.get('affectedDevices', [])
            for device in affected_devices:
                if device.get('did') == device_id:
                    print(f"    Product: {device.get('product', 'Unknown')} v{device.get('version', 'Unknown')}")
                    print(f"    Vendor: {device.get('vendor', 'Unknown')}")
        
        print(f"\nSeverity Summary:")
        for severity, count in severity_counts.items():
            if count > 0:
                print(f"  {severity}: {count}")
```

### Comprehensive Vulnerability Assessment

```python
# Get complete CVE data with full device details
comprehensive_data = client.cves.get(fulldevicedetails=True)

cves = comprehensive_data.get('cves', [])
devices = comprehensive_data.get('devices', {})

print(f"Comprehensive Vulnerability Assessment:")
print(f"Total CVEs: {len(cves)}")
print(f"Total affected devices: {len(devices)}")

# Analyze critical vulnerabilities
critical_cves = [cve for cve in cves if cve.get('severity') == 'CRITICAL']
high_cves = [cve for cve in cves if cve.get('severity') == 'HIGH']

print(f"\nCritical Vulnerabilities: {len(critical_cves)}")
for cve in critical_cves[:5]:  # Top 5 critical
    affected_device_ids = cve.get('affectedDeviceIds', [])
    print(f"  {cve.get('cveId')}: Score {cve.get('score')} - {len(affected_device_ids)} devices affected")

# Device risk analysis
device_risk_scores = {}
for cve in cves:
    score = cve.get('score', 0)
    affected_device_ids = cve.get('affectedDeviceIds', [])
    
    for device_id in affected_device_ids:
        if device_id not in device_risk_scores:
            device_risk_scores[device_id] = {'total_score': 0, 'cve_count': 0, 'critical_count': 0}
        
        device_risk_scores[device_id]['total_score'] += score
        device_risk_scores[device_id]['cve_count'] += 1
        
        if cve.get('severity') == 'CRITICAL':
            device_risk_scores[device_id]['critical_count'] += 1

# Top 10 highest risk devices
top_risk_devices = sorted(
    device_risk_scores.items(),
    key=lambda x: (x[1]['critical_count'], x[1]['total_score']),
    reverse=True
)[:10]

print(f"\nTop 10 Highest Risk Devices:")
for device_id, risk_data in top_risk_devices:
    device_info = devices.get(str(device_id), {})
    hostname = device_info.get('hostname', 'Unknown')
    
    print(f"  Device {device_id} ({hostname}):")
    print(f"    Total CVEs: {risk_data['cve_count']}")
    print(f"    Critical CVEs: {risk_data['critical_count']}")
    print(f"    Total Risk Score: {risk_data['total_score']:.1f}")
```

### CVE Tracking and Reporting

```python
# Generate vulnerability report
def generate_cve_report():
    all_cves = client.cves.get(fulldevicedetails=True)
    
    cves = all_cves.get('cves', [])
    devices = all_cves.get('devices', {})
    
    # Statistics
    severity_stats = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    vendor_stats = {}
    product_stats = {}
    
    for cve in cves:
        severity = cve.get('severity', 'UNKNOWN')
        if severity in severity_stats:
            severity_stats[severity] += 1
        
        # Analyze affected products/vendors
        affected_device_ids = cve.get('affectedDeviceIds', [])
        for device_id in affected_device_ids:
            device_info = devices.get(str(device_id), {})
            vendor = device_info.get('vendor', 'Unknown')
            product = device_info.get('product', 'Unknown')
            
            vendor_stats[vendor] = vendor_stats.get(vendor, 0) + 1
            product_stats[product] = product_stats.get(product, 0) + 1
    
    # Generate report
    report = f"""
CVE Vulnerability Report
========================
Total CVEs: {len(cves)}
Total Affected Devices: {len(devices)}

Severity Distribution:
{chr(10).join([f"  {sev}: {count}" for sev, count in severity_stats.items() if count > 0])}

Top 5 Most Affected Vendors:
{chr(10).join([f"  {vendor}: {count} vulnerabilities" for vendor, count in sorted(vendor_stats.items(), key=lambda x: x[1], reverse=True)[:5]])}

Top 5 Most Affected Products:
{chr(10).join([f"  {product}: {count} vulnerabilities" for product, count in sorted(product_stats.items(), key=lambda x: x[1], reverse=True)[:5]])}
"""
    
    return report

# Generate and print report
report = generate_cve_report()
print(report)
```

### Monitoring Specific Device Vulnerabilities

```python
# Monitor critical devices for new vulnerabilities
critical_device_ids = [123, 456, 789]  # Your critical devices

for device_id in critical_device_ids:
    print(f"\nVulnerability Status for Device {device_id}:")
    
    device_cves = client.cves.get(did=device_id)
    cves_list = device_cves.get('cves', [])
    
    if not cves_list:
        print("  ✅ No known vulnerabilities")
        continue
    
    critical_cves = [cve for cve in cves_list if cve.get('severity') == 'CRITICAL']
    high_cves = [cve for cve in cves_list if cve.get('severity') == 'HIGH']
    
    if critical_cves:
        print(f"  🚨 {len(critical_cves)} CRITICAL vulnerabilities:")
        for cve in critical_cves:
            print(f"    - {cve.get('cveId')}: Score {cve.get('score')}")
    
    if high_cves:
        print(f"  ⚠️  {len(high_cves)} HIGH vulnerabilities:")
        for cve in high_cves[:3]:  # Show top 3
            print(f"    - {cve.get('cveId')}: Score {cve.get('score')}")
        
        if len(high_cves) > 3:
            print(f"    ... and {len(high_cves) - 3} more")
    
    # Calculate risk score
    total_score = sum(cve.get('score', 0) for cve in cves_list)
    print(f"  📊 Total Risk Score: {total_score:.1f}")
```

## Error Handling

```python
try:
    # Attempt to get CVE data
    cves_data = client.cves.get()
    
    # Process CVE information
    for cve in cves_data.get('cves', []):
        cve_id = cve.get('cveId')
        print(f"Processing CVE: {cve_id}")
        
        # Attempt to get device-specific CVEs
        if 'affectedDevices' in cve:
            for device in cve['affectedDevices']:
                device_id = device.get('did')
                
                try:
                    device_cves = client.cves.get(did=device_id)
                    print(f"  Device {device_id}: {len(device_cves.get('cves', []))} CVEs")
                    
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 404:
                        print(f"  Device {device_id}: No CVE data available")
                    else:
                        print(f"  Error retrieving CVEs for device {device_id}: {e}")
                        
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
        
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Data Source
- CVE information comes from the Darktrace/OT ICS Vulnerability Tracker
- Provides vulnerability data specifically for industrial control systems and OT devices
- CVE data is continuously updated from official CVE databases

### Response Structure
- Standard response includes CVE details with embedded affected device information
- `fulldevicedetails=True` separates CVEs and devices into distinct objects for better data normalization
- Use full device details for large datasets to avoid data duplication

### CVE Severity Levels
- **CRITICAL**: Extremely severe vulnerabilities requiring immediate attention
- **HIGH**: Serious vulnerabilities that should be addressed quickly
- **MEDIUM**: Moderate vulnerabilities requiring assessment
- **LOW**: Minor vulnerabilities for awareness

### Filtering Capabilities
- **Device-specific filtering**: Use `did` parameter to focus on specific devices
- **No time-based filtering**: CVEs represent current vulnerability state
- **Severity filtering**: Must be done client-side after retrieval

### Best Practices
- Use `fulldevicedetails=True` for comprehensive analysis across multiple devices
- Filter by device ID when focusing on specific assets
- Implement regular CVE monitoring for critical infrastructure
- Prioritize remediation based on severity scores and device criticality
- Combine CVE data with device metadata for risk assessment

### Performance Considerations
- CVE endpoint may return large datasets for environments with many vulnerable devices
- Use device-specific queries to reduce response size when possible
- Consider caching CVE data for reporting and analysis workflows
- Full device details may significantly increase response size but reduce subsequent API calls

## Examples

### Get All Cvess

```python
cves_data = client.cves.get()
for item in cves_data.get("cves", []):
    print(f"Item: {item}")
```

## Error Handling

```python
try:
    cves_data = client.cves.get()
    # Process the data
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
