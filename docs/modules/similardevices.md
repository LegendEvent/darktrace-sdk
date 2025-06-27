# SimilarDevices Module

The SimilarDevices module provides comprehensive similar device detection and analysis capabilities, helping identify devices with comparable characteristics, behavior patterns, and network usage profiles. This module is essential for device clustering, baseline establishment, and anomaly detection through device similarity analysis.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the similardevices module
similardevices = client.similardevices
```

## Methods Overview

The SimilarDevices module provides the following method:

- **`get()`** - Retrieve similar device information with various filtering and detail options

## Methods

### Get Similar Devices

Retrieve similar device information from the Darktrace platform with flexible filtering and detail options.

```python
# Get all similar device relationships
all_similar = similardevices.get()

# Get similar devices for a specific device
device_similar = similardevices.get(device_id="123")

# Get limited number of similar devices
top_similar = similardevices.get(device_id="123", count=10)

# Get full device details in results
detailed_similar = similardevices.get(
    device_id="123",
    fulldevicedetails=True,
    count=5
)

# Use pagination for large results
paginated_similar = similardevices.get(
    device_id="456",
    count=20,
    token="next_page_token"
)

# Get specific response data only
similarity_scores = similardevices.get(
    device_id="789",
    responsedata="similarity_score,device_info"
)
```

#### Parameters

- `device_id` (str, optional): Device ID to find similar devices for. If not provided, returns all similar device relationships
- `count` (int, optional): Number of similar devices to return
- `fulldevicedetails` (bool, optional): Whether to include full device details in the response
- `token` (str, optional): Pagination token for large result sets
- `responsedata` (str, optional): Restrict returned JSON to only specified field(s)
- `**kwargs`: Additional parameters for future compatibility

#### Response Structure

```python
{
  "similar_devices": [
    {
      "primary_device": {
        "did": 123,
        "hostname": "workstation-01.company.com",
        "ip": "192.168.1.100",
        "mac": "00:11:22:33:44:55",
        "device_type": "workstation",
        "operating_system": "Windows 10",
        "vendor": "Dell Inc.",
        "first_seen": 1640995200,
        "last_seen": 1705324800,
        "tags": ["critical", "finance"],
        "location": "Office Building A"
      },
      "similar_devices": [
        {
          "did": 456,
          "hostname": "workstation-02.company.com",
          "ip": "192.168.1.101",
          "mac": "00:11:22:33:44:66",
          "similarity_score": 0.89,
          "similarity_factors": {
            "network_behavior": 0.92,
            "device_profile": 0.87,
            "traffic_patterns": 0.88,
            "application_usage": 0.91,
            "time_patterns": 0.86
          },
          "shared_characteristics": [
            "same_subnet",
            "similar_traffic_volume",
            "same_os_version",
            "similar_application_profile",
            "comparable_user_behavior"
          ],
          "device_details": {
            "device_type": "workstation",
            "operating_system": "Windows 10",
            "vendor": "Dell Inc.",
            "department": "Finance",
            "user_profile": "office_worker",
            "last_activity": 1705324750
          },
          "behavioral_similarity": {
            "communication_patterns": {
              "internal_external_ratio": 0.75,
              "protocol_distribution": {
                "HTTP/HTTPS": 65.2,
                "SMB": 18.7,
                "DNS": 12.1,
                "Other": 4.0
              },
              "peak_usage_hours": "08:00-18:00",
              "weekend_activity": "minimal"
            },
            "data_transfer_patterns": {
              "average_daily_upload": 524288000,
              "average_daily_download": 2147483648,
              "burst_patterns": "consistent",
              "transfer_timing": "business_hours"
            },
            "connection_patterns": {
              "unique_destinations_per_day": 45,
              "connection_duration_average": 300,
              "retry_patterns": "normal",
              "geographic_distribution": "domestic_focus"
            }
          },
          "risk_correlation": {
            "shared_vulnerabilities": 2,
            "similar_threat_exposure": true,
            "compliance_alignment": "high",
            "security_posture_similarity": 0.84
          }
        },
        {
          "did": 789,
          "hostname": "workstation-03.company.com",
          "ip": "192.168.1.102",
          "similarity_score": 0.76,
          "similarity_factors": {
            "network_behavior": 0.78,
            "device_profile": 0.75,
            "traffic_patterns": 0.74,
            "application_usage": 0.79,
            "time_patterns": 0.72
          },
          "shared_characteristics": [
            "same_department",
            "similar_user_role",
            "comparable_data_usage",
            "similar_security_tools"
          ],
          "divergent_characteristics": [
            "different_hardware_vendor",
            "newer_os_version",
            "additional_software_installed"
          ]
        }
      ],
      "similarity_analysis": {
        "total_similar_devices": 15,
        "high_similarity_devices": 3,
        "medium_similarity_devices": 8,
        "low_similarity_devices": 4,
        "analysis_timestamp": 1705324800,
        "confidence_level": 0.92
      }
    }
  ],
  "clustering_info": {
    "device_clusters": [
      {
        "cluster_id": "finance_workstations",
        "cluster_name": "Finance Department Workstations",
        "member_count": 12,
        "characteristics": [
          "Windows 10 workstations",
          "Finance department users",
          "Similar application usage",
          "Comparable network patterns"
        ],
        "cluster_centroid": {
          "average_similarity": 0.82,
          "typical_behavior": "business_user_profile"
        }
      }
    ],
    "outlier_devices": [
      {
        "did": 999,
        "hostname": "anomaly-device",
        "outlier_score": 0.15,
        "reasons": [
          "unique_traffic_patterns",
          "unusual_application_usage",
          "different_time_patterns"
        ]
      }
    ]
  },
  "pagination": {
    "current_token": "current_page_token",
    "next_token": "next_page_token",
    "has_more": true,
    "total_results": 156
  }
}

## Examples

### Device Similarity Analysis

```python
from darktrace import DarktraceClient
from datetime import datetime

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def analyze_device_similarity(target_device_id, similarity_threshold=0.7):
    """Analyze device similarity and clustering"""
    
    print(f"Device Similarity Analysis")
    print("=" * 50)
    print(f"Target Device ID: {target_device_id}")
    print(f"Similarity Threshold: {similarity_threshold}")
    
    try:
        # Get similar devices for target device
        similar_data = client.similardevices.get(
            device_id=target_device_id,
            fulldevicedetails=True,
            count=20
        )
        
        if not similar_data.get('similar_devices'):
            print(f"No similar devices found for device {target_device_id}")
            return None
        
        device_group = similar_data['similar_devices'][0]
        primary_device = device_group.get('primary_device', {})
        similar_devices = device_group.get('similar_devices', [])
        
        print(f"\nPRIMARY DEVICE:")
        print(f"  Hostname: {primary_device.get('hostname', 'Unknown')}")
        print(f"  IP: {primary_device.get('ip', 'Unknown')}")
        print(f"  Type: {primary_device.get('device_type', 'Unknown')}")
        print(f"  OS: {primary_device.get('operating_system', 'Unknown')}")
        print(f"  Location: {primary_device.get('location', 'Unknown')}")
        
        # Filter by similarity threshold
        high_similarity_devices = [
            d for d in similar_devices 
            if d.get('similarity_score', 0) >= similarity_threshold
        ]
        
        print(f"\nSIMILAR DEVICES (≥{similarity_threshold} similarity):")
        print(f"Found {len(high_similarity_devices)} highly similar devices")
        
        similarity_analysis = {
            'target_device': primary_device,
            'similar_devices': [],
            'similarity_patterns': {},
            'clustering_insights': {},
            'security_implications': []
        }
        
        for device in high_similarity_devices:
            hostname = device.get('hostname', 'Unknown')
            similarity_score = device.get('similarity_score', 0)
            
            print(f"\n📊 {hostname} (Similarity: {similarity_score:.3f})")
            
            # Similarity factors breakdown
            factors = device.get('similarity_factors', {})
            if factors:
                print(f"   Similarity Breakdown:")
                for factor, score in factors.items():
                    print(f"     {factor.replace('_', ' ').title()}: {score:.3f}")
            
            # Shared characteristics
            shared_chars = device.get('shared_characteristics', [])
            if shared_chars:
                print(f"   Shared Characteristics:")
                for char in shared_chars:
                    print(f"     • {char.replace('_', ' ').title()}")
            
            # Behavioral similarity
            behavioral = device.get('behavioral_similarity', {})
            if behavioral:
                comm_patterns = behavioral.get('communication_patterns', {})
                if comm_patterns:
                    ratio = comm_patterns.get('internal_external_ratio', 0)
                    peak_hours = comm_patterns.get('peak_usage_hours', 'Unknown')
                    print(f"   Behavioral Patterns:")
                    print(f"     Internal/External Ratio: {ratio:.2f}")
                    print(f"     Peak Hours: {peak_hours}")
            
            # Risk correlation
            risk_corr = device.get('risk_correlation', {})
            if risk_corr:
                shared_vulns = risk_corr.get('shared_vulnerabilities', 0)
                security_similarity = risk_corr.get('security_posture_similarity', 0)
                print(f"   Security Correlation:")
                print(f"     Shared Vulnerabilities: {shared_vulns}")
                print(f"     Security Posture Similarity: {security_similarity:.3f}")
            
            # Store for analysis
            similarity_analysis['similar_devices'].append({
                'device': device,
                'similarity_score': similarity_score,
                'factors': factors
            })
        
        # Pattern analysis
        print(f"\n" + "="*50)
        print(f"SIMILARITY PATTERN ANALYSIS:")
        
        if similarity_analysis['similar_devices']:
            # Calculate average similarity factors
            all_factors = {}
            for device_data in similarity_analysis['similar_devices']:
                factors = device_data.get('factors', {})
                for factor, score in factors.items():
                    if factor not in all_factors:
                        all_factors[factor] = []
                    all_factors[factor].append(score)
            
            print(f"  Average Similarity Factors:")
            for factor, scores in all_factors.items():
                avg_score = sum(scores) / len(scores)
                print(f"    {factor.replace('_', ' ').title()}: {avg_score:.3f}")
                similarity_analysis['similarity_patterns'][factor] = avg_score
        
        # Clustering analysis
        clustering_info = similar_data.get('clustering_info', {})
        if clustering_info:
            clusters = clustering_info.get('device_clusters', [])
            outliers = clustering_info.get('outlier_devices', [])
            
            print(f"\nCLUSTERING ANALYSIS:")
            print(f"  Device Clusters: {len(clusters)}")
            
            for cluster in clusters:
                cluster_name = cluster.get('cluster_name', 'Unknown')
                member_count = cluster.get('member_count', 0)
                characteristics = cluster.get('characteristics', [])
                
                print(f"    • {cluster_name}: {member_count} devices")
                for char in characteristics[:3]:  # Show top 3 characteristics
                    print(f"      - {char}")
            
            if outliers:
                print(f"  Outlier Devices: {len(outliers)}")
                for outlier in outliers:
                    hostname = outlier.get('hostname', 'Unknown')
                    outlier_score = outlier.get('outlier_score', 0)
                    print(f"    • {hostname} (outlier score: {outlier_score:.3f})")
        
        # Security implications
        print(f"\nSECURITY IMPLICATIONS:")
        
        security_implications = []
        
        # High similarity group analysis
        if len(high_similarity_devices) >= 5:
            security_implications.append("Large similar device group - consider group-based security policies")
            
        # Shared vulnerability analysis
        total_shared_vulns = sum(
            d.get('risk_correlation', {}).get('shared_vulnerabilities', 0)
            for d in high_similarity_devices
        )
        if total_shared_vulns > 0:
            avg_shared_vulns = total_shared_vulns / len(high_similarity_devices)
            security_implications.append(f"Average {avg_shared_vulns:.1f} shared vulnerabilities per device")
        
        # Behavioral consistency
        behavioral_scores = [
            d.get('similarity_factors', {}).get('network_behavior', 0)
            for d in high_similarity_devices
        ]
        if behavioral_scores:
            avg_behavioral = sum(behavioral_scores) / len(behavioral_scores)
            if avg_behavioral > 0.8:
                security_implications.append("High behavioral consistency - good for baseline establishment")
            elif avg_behavioral < 0.5:
                security_implications.append("Low behavioral consistency - investigate anomalies")
        
        # Display implications
        if security_implications:
            for implication in security_implications:
                print(f"  • {implication}")
            similarity_analysis['security_implications'] = security_implications
        else:
            print(f"  • No specific security implications identified")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        recommendations = []
        
        if len(high_similarity_devices) >= 3:
            recommendations.append("Consider creating device group policies for similar devices")
            recommendations.append("Use similar devices as baselines for anomaly detection")
        
        if similarity_analysis['similarity_patterns'].get('security_posture_similarity', 0) > 0.8:
            recommendations.append("Apply consistent security configurations across similar devices")
        
        if clustering_info.get('outlier_devices'):
            recommendations.append("Investigate outlier devices for potential security risks")
        
        recommendations.append("Monitor similar devices for coordinated threats")
        recommendations.append("Use similarity data for incident response prioritization")
        
        for rec in recommendations:
            print(f"  • {rec}")
        
        return similarity_analysis
        
    except Exception as e:
        print(f"Error analyzing device similarity: {e}")
        return None

# Example usage
# similarity_report = analyze_device_similarity("123", similarity_threshold=0.7)
```

### Device Clustering and Fleet Analysis

```python
def analyze_device_fleet_clustering():
    """Analyze device clustering across the entire fleet"""
    
    print(f"Device Fleet Clustering Analysis")
    print("=" * 60)
    
    try:
        # Get all similar device relationships
        all_similar = client.similardevices.get(count=100)
        
        if not all_similar.get('similar_devices'):
            print("No similar device data available")
            return None
        
        fleet_analysis = {
            'total_devices': 0,
            'device_clusters': {},
            'similarity_distribution': {},
            'outlier_analysis': {},
            'behavioral_patterns': {},
            'security_clustering': {}
        }
        
        print(f"Processing {len(all_similar['similar_devices'])} device groups...")
        
        all_similarity_scores = []
        device_count = 0
        
        # Process each device group
        for group in all_similar['similar_devices']:
            primary_device = group.get('primary_device', {})
            similar_devices = group.get('similar_devices', [])
            
            device_count += 1 + len(similar_devices)  # Primary + similar devices
            
            # Collect similarity scores
            for device in similar_devices:
                score = device.get('similarity_score', 0)
                all_similarity_scores.append(score)
                
                # Categorize by similarity level
                if score >= 0.8:
                    level = 'high'
                elif score >= 0.6:
                    level = 'medium'
                else:
                    level = 'low'
                
                fleet_analysis['similarity_distribution'][level] = \
                    fleet_analysis['similarity_distribution'].get(level, 0) + 1
        
        fleet_analysis['total_devices'] = device_count
        
        # Similarity statistics
        if all_similarity_scores:
            avg_similarity = sum(all_similarity_scores) / len(all_similarity_scores)
            max_similarity = max(all_similarity_scores)
            min_similarity = min(all_similarity_scores)
            
            print(f"\nSIMILARITY STATISTICS:")
            print(f"  Total Device Relationships: {len(all_similarity_scores):,}")
            print(f"  Average Similarity: {avg_similarity:.3f}")
            print(f"  Maximum Similarity: {max_similarity:.3f}")
            print(f"  Minimum Similarity: {min_similarity:.3f}")
            
            # Distribution breakdown
            total_relationships = len(all_similarity_scores)
            print(f"\nSIMILARITY DISTRIBUTION:")
            for level, count in fleet_analysis['similarity_distribution'].items():
                percentage = (count / total_relationships) * 100
                print(f"  {level.title()} Similarity (≥{0.8 if level=='high' else 0.6 if level=='medium' else 0.0}): {count:,} ({percentage:.1f}%)")
        
        # Clustering analysis from API data
        clustering_info = all_similar.get('clustering_info', {})
        if clustering_info:
            clusters = clustering_info.get('device_clusters', [])
            outliers = clustering_info.get('outlier_devices', [])
            
            print(f"\nDEVICE CLUSTERING:")
            print(f"  Identified Clusters: {len(clusters)}")
            
            cluster_analysis = {}
            total_clustered_devices = 0
            
            for cluster in clusters:
                cluster_id = cluster.get('cluster_id', 'unknown')
                cluster_name = cluster.get('cluster_name', 'Unknown Cluster')
                member_count = cluster.get('member_count', 0)
                characteristics = cluster.get('characteristics', [])
                
                total_clustered_devices += member_count
                cluster_analysis[cluster_id] = {
                    'name': cluster_name,
                    'size': member_count,
                    'characteristics': characteristics
                }
                
                print(f"\n  📊 {cluster_name}:")
                print(f"     Devices: {member_count}")
                print(f"     Characteristics:")
                for char in characteristics:
                    print(f"       • {char}")
            
            fleet_analysis['device_clusters'] = cluster_analysis
            
            # Clustering coverage
            clustering_coverage = (total_clustered_devices / device_count) * 100 if device_count > 0 else 0
            print(f"\n  Clustering Coverage: {total_clustered_devices:,}/{device_count:,} devices ({clustering_coverage:.1f}%)")
            
            # Outlier analysis
            if outliers:
                print(f"\n  OUTLIER DEVICES:")
                print(f"  Count: {len(outliers)}")
                
                outlier_analysis = {}
                for outlier in outliers:
                    hostname = outlier.get('hostname', 'Unknown')
                    outlier_score = outlier.get('outlier_score', 0)
                    reasons = outlier.get('reasons', [])
                    
                    outlier_analysis[hostname] = {
                        'score': outlier_score,
                        'reasons': reasons
                    }
                    
                    print(f"    • {hostname} (score: {outlier_score:.3f})")
                    for reason in reasons:
                        print(f"      - {reason.replace('_', ' ').title()}")
                
                fleet_analysis['outlier_analysis'] = outlier_analysis
        
        # Behavioral pattern analysis
        print(f"\nBEHAVIORAL PATTERN ANALYSIS:")
        
        behavioral_patterns = {
            'communication_patterns': {},
            'traffic_patterns': {},
            'time_patterns': {},
            'application_patterns': {}
        }
        
        pattern_counts = {}
        
        # Extract behavioral patterns from device groups
        for group in all_similar['similar_devices']:
            similar_devices = group.get('similar_devices', [])
            
            for device in similar_devices:
                behavioral = device.get('behavioral_similarity', {})
                
                # Communication patterns
                comm_patterns = behavioral.get('communication_patterns', {})
                if comm_patterns:
                    peak_hours = comm_patterns.get('peak_usage_hours', 'unknown')
                    weekend_activity = comm_patterns.get('weekend_activity', 'unknown')
                    
                    pattern_counts[f"peak_{peak_hours}"] = pattern_counts.get(f"peak_{peak_hours}", 0) + 1
                    pattern_counts[f"weekend_{weekend_activity}"] = pattern_counts.get(f"weekend_{weekend_activity}", 0) + 1
        
        # Display top patterns
        if pattern_counts:
            sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
            print(f"  Top Behavioral Patterns:")
            for pattern, count in sorted_patterns[:5]:
                print(f"    • {pattern.replace('_', ' ').title()}: {count} devices")
        
        # Security clustering analysis
        print(f"\nSECURITY CLUSTERING ANALYSIS:")
        
        security_groups = {
            'high_risk_clusters': [],
            'vulnerable_clusters': [],
            'secure_clusters': []
        }
        
        for group in all_similar['similar_devices']:
            similar_devices = group.get('similar_devices', [])
            
            # Analyze risk correlation within clusters
            shared_vulns = []
            security_scores = []
            
            for device in similar_devices:
                risk_corr = device.get('risk_correlation', {})
                shared_vulns.append(risk_corr.get('shared_vulnerabilities', 0))
                security_scores.append(risk_corr.get('security_posture_similarity', 0))
            
            if shared_vulns and security_scores:
                avg_vulns = sum(shared_vulns) / len(shared_vulns)
                avg_security = sum(security_scores) / len(security_scores)
                
                # Categorize security clusters
                if avg_vulns > 3 or avg_security < 0.5:
                    security_groups['high_risk_clusters'].append({
                        'primary_device': group.get('primary_device', {}),
                        'avg_vulnerabilities': avg_vulns,
                        'avg_security_score': avg_security,
                        'cluster_size': len(similar_devices)
                    })
                elif avg_vulns == 0 and avg_security > 0.8:
                    security_groups['secure_clusters'].append({
                        'primary_device': group.get('primary_device', {}),
                        'cluster_size': len(similar_devices)
                    })
        
        fleet_analysis['security_clustering'] = security_groups
        
        # Display security clustering results
        print(f"  High Risk Clusters: {len(security_groups['high_risk_clusters'])}")
        print(f"  Secure Clusters: {len(security_groups['secure_clusters'])}")
        
        if security_groups['high_risk_clusters']:
            print(f"  High Risk Cluster Details:")
            for cluster in security_groups['high_risk_clusters'][:3]:  # Show top 3
                primary = cluster['primary_device']
                hostname = primary.get('hostname', 'Unknown')
                avg_vulns = cluster['avg_vulnerabilities']
                print(f"    • {hostname}: {avg_vulns:.1f} avg vulnerabilities, {cluster['cluster_size']} devices")
        
        # Fleet recommendations
        print(f"\n" + "="*60)
        print(f"FLEET RECOMMENDATIONS:")
        
        recommendations = []
        
        if clustering_coverage < 70:
            recommendations.append("• Improve device clustering - low clustering coverage detected")
        
        if len(security_groups['high_risk_clusters']) > 0:
            recommendations.append(f"• Address {len(security_groups['high_risk_clusters'])} high-risk device clusters")
        
        if fleet_analysis['similarity_distribution'].get('high', 0) / total_relationships > 0.7:
            recommendations.append("• Leverage high device similarity for group-based policies")
        
        if len(outliers) > device_count * 0.1:  # More than 10% outliers
            recommendations.append("• Investigate high number of outlier devices")
        
        recommendations.extend([
            "• Use clustering data for security policy optimization",
            "• Implement cluster-based monitoring and alerting",
            "• Regular clustering analysis for fleet management"
        ])
        
        for rec in recommendations:
            print(f"  {rec}")
        
        return fleet_analysis
        
    except Exception as e:
        print(f"Error analyzing device fleet clustering: {e}")
        return None

# Example usage
# fleet_clustering = analyze_device_fleet_clustering()
```

### Similarity-Based Threat Hunting

```python
def hunt_threats_using_similarity(target_device_id, threat_indicators):
    """Hunt for threats using device similarity patterns"""
    
    print(f"Similarity-Based Threat Hunting")
    print("=" * 50)
    print(f"Target Device: {target_device_id}")
    print(f"Threat Indicators: {len(threat_indicators)}")
    
    try:
        # Get similar devices for threat correlation
        similar_data = client.similardevices.get(
            device_id=target_device_id,
            fulldevicedetails=True,
            count=50
        )
        
        if not similar_data.get('similar_devices'):
            print("No similar devices found for threat hunting")
            return None
        
        threat_hunt_results = {
            'target_device': target_device_id,
            'similar_devices_analyzed': 0,
            'potential_threats': [],
            'threat_patterns': {},
            'similarity_risk_correlation': {},
            'investigation_priorities': []
        }
        
        device_group = similar_data['similar_devices'][0]
        primary_device = device_group.get('primary_device', {})
        similar_devices = device_group.get('similar_devices', [])
        
        print(f"\nTARGET DEVICE ANALYSIS:")
        print(f"  Hostname: {primary_device.get('hostname', 'Unknown')}")
        print(f"  IP: {primary_device.get('ip', 'Unknown')}")
        print(f"  Type: {primary_device.get('device_type', 'Unknown')}")
        
        print(f"\nANALYZING {len(similar_devices)} SIMILAR DEVICES:")
        
        threat_hunt_results['similar_devices_analyzed'] = len(similar_devices)
        
        # Analyze each similar device for threat indicators
        for device in similar_devices:
            hostname = device.get('hostname', 'Unknown')
            similarity_score = device.get('similarity_score', 0)
            
            print(f"\n🔍 Analyzing {hostname} (similarity: {similarity_score:.3f})")
            
            device_threats = []
            
            # Check behavioral anomalies
            behavioral = device.get('behavioral_similarity', {})
            if behavioral:
                comm_patterns = behavioral.get('communication_patterns', {})
                
                # Check for suspicious communication patterns
                for indicator in threat_indicators:
                    if indicator['type'] == 'network_behavior':
                        # Example: Check for unusual external communication
                        ext_ratio = comm_patterns.get('internal_external_ratio', 0)
                        if indicator['pattern'] == 'high_external_traffic' and ext_ratio < 0.3:
                            device_threats.append({
                                'indicator': indicator,
                                'matched_pattern': 'high_external_traffic',
                                'severity': 'medium',
                                'details': f"External traffic ratio: {ext_ratio:.2f}"
                            })
                
                # Check protocol distribution anomalies
                protocol_dist = comm_patterns.get('protocol_distribution', {})
                for indicator in threat_indicators:
                    if indicator['type'] == 'protocol_anomaly':
                        suspicious_protocol = indicator.get('protocol', '')
                        usage_pct = protocol_dist.get(suspicious_protocol, 0)
                        threshold = indicator.get('threshold', 50)
                        
                        if usage_pct > threshold:
                            device_threats.append({
                                'indicator': indicator,
                                'matched_pattern': 'suspicious_protocol_usage',
                                'severity': 'high',
                                'details': f"{suspicious_protocol} usage: {usage_pct:.1f}%"
                            })
            
            # Check risk correlation patterns
            risk_corr = device.get('risk_correlation', {})
            if risk_corr:
                shared_vulns = risk_corr.get('shared_vulnerabilities', 0)
                threat_exposure = risk_corr.get('similar_threat_exposure', False)
                
                for indicator in threat_indicators:
                    if indicator['type'] == 'vulnerability_correlation':
                        if shared_vulns >= indicator.get('min_vulnerabilities', 3):
                            device_threats.append({
                                'indicator': indicator,
                                'matched_pattern': 'vulnerability_clustering',
                                'severity': 'high',
                                'details': f"Shared vulnerabilities: {shared_vulns}"
                            })
                    
                    if indicator['type'] == 'threat_exposure' and threat_exposure:
                        device_threats.append({
                            'indicator': indicator,
                            'matched_pattern': 'similar_threat_exposure',
                            'severity': 'medium',
                            'details': "Similar threat exposure profile"
                        })
            
            # Check for timing pattern anomalies
            for indicator in threat_indicators:
                if indicator['type'] == 'timing_anomaly':
                    # Extract timing information from behavioral data
                    data_patterns = behavioral.get('data_transfer_patterns', {})
                    timing = data_patterns.get('transfer_timing', 'unknown')
                    
                    if timing != 'business_hours' and indicator['pattern'] == 'off_hours_activity':
                        device_threats.append({
                            'indicator': indicator,
                            'matched_pattern': 'off_hours_data_transfer',
                            'severity': 'medium',
                            'details': f"Transfer timing: {timing}"
                        })
            
            # Store threat findings
            if device_threats:
                threat_device = {
                    'device': device,
                    'hostname': hostname,
                    'similarity_score': similarity_score,
                    'threats_detected': device_threats,
                    'threat_count': len(device_threats),
                    'max_severity': max([t['severity'] for t in device_threats], default='low')
                }
                
                threat_hunt_results['potential_threats'].append(threat_device)
                
                print(f"   🚨 {len(device_threats)} threat indicators detected")
                for threat in device_threats:
                    severity_icon = "🔴" if threat['severity'] == 'high' else "🟡" if threat['severity'] == 'medium' else "🔵"
                    print(f"     {severity_icon} {threat['matched_pattern']}: {threat['details']}")
            else:
                print(f"   ✅ No threat indicators detected")
        
        # Threat pattern analysis
        print(f"\n" + "="*50)
        print(f"THREAT PATTERN ANALYSIS:")
        
        if threat_hunt_results['potential_threats']:
            # Count threat patterns
            pattern_counts = {}
            severity_counts = {'high': 0, 'medium': 0, 'low': 0}
            
            for threat_device in threat_hunt_results['potential_threats']:
                for threat in threat_device['threats_detected']:
                    pattern = threat['matched_pattern']
                    severity = threat['severity']
                    
                    pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
                    severity_counts[severity] += 1
            
            threat_hunt_results['threat_patterns'] = pattern_counts
            
            print(f"  Devices with Threats: {len(threat_hunt_results['potential_threats'])}")
            print(f"  Total Threat Instances: {sum(severity_counts.values())}")
            
            print(f"\n  Severity Breakdown:")
            for severity, count in severity_counts.items():
                print(f"    {severity.title()}: {count}")
            
            print(f"\n  Most Common Threat Patterns:")
            sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
            for pattern, count in sorted_patterns:
                print(f"    • {pattern.replace('_', ' ').title()}: {count} devices")
            
            # Similarity-risk correlation
            print(f"\n  Similarity-Risk Correlation:")
            
            high_similarity_threats = [
                t for t in threat_hunt_results['potential_threats']
                if t['similarity_score'] > 0.8
            ]
            
            if high_similarity_threats:
                print(f"    High-similarity devices with threats: {len(high_similarity_threats)}")
                print(f"    Risk correlation: High similarity may indicate coordinated threat")
                
                threat_hunt_results['similarity_risk_correlation']['high_similarity_threat_cluster'] = True
            
            # Investigation priorities
            print(f"\nINVESTIGATION PRIORITIES:")
            
            # Sort by threat severity and similarity
            prioritized_threats = sorted(
                threat_hunt_results['potential_threats'],
                key=lambda x: (
                    {'high': 3, 'medium': 2, 'low': 1}[x['max_severity']],
                    x['similarity_score'],
                    x['threat_count']
                ),
                reverse=True
            )
            
            for i, threat_device in enumerate(prioritized_threats[:5], 1):
                hostname = threat_device['hostname']
                similarity = threat_device['similarity_score']
                threat_count = threat_device['threat_count']
                max_severity = threat_device['max_severity']
                
                print(f"  {i}. {hostname}")
                print(f"     Similarity: {similarity:.3f}, Threats: {threat_count}, Max Severity: {max_severity}")
                
                threat_hunt_results['investigation_priorities'].append({
                    'rank': i,
                    'hostname': hostname,
                    'priority_score': similarity * threat_count,
                    'details': threat_device
                })
        
        else:
            print(f"  No threats detected in similar devices")
        
        # Recommendations
        print(f"\nTHREAT HUNTING RECOMMENDATIONS:")
        
        recommendations = []
        
        if threat_hunt_results['potential_threats']:
            recommendations.append("• Investigate high-priority devices immediately")
            recommendations.append("• Correlate findings with security logs and events")
            recommendations.append("• Consider isolating devices with high-severity threats")
            
            if threat_hunt_results['similarity_risk_correlation'].get('high_similarity_threat_cluster'):
                recommendations.append("• Investigate potential coordinated attack across similar devices")
            
            recommendations.append("• Update threat indicators based on findings")
            recommendations.append("• Expand hunting to devices similar to those with threats")
        else:
            recommendations.append("• No immediate threats found in similar devices")
            recommendations.append("• Consider expanding threat indicators or similarity scope")
            recommendations.append("• Continue regular threat hunting activities")
        
        recommendations.extend([
            "• Use similarity data to predict threat spread patterns",
            "• Develop similarity-based threat detection rules",
            "• Regular threat hunting using device clustering"
        ])
        
        for rec in recommendations:
            print(f"  {rec}")
        
        return threat_hunt_results
        
    except Exception as e:
        print(f"Error in similarity-based threat hunting: {e}")
        return None

# Example threat indicators
example_threat_indicators = [
    {
        'type': 'network_behavior',
        'pattern': 'high_external_traffic',
        'description': 'Unusually high external network traffic'
    },
    {
        'type': 'protocol_anomaly',
        'protocol': 'DNS',
        'threshold': 30,
        'description': 'Excessive DNS usage'
    },
    {
        'type': 'vulnerability_correlation',
        'min_vulnerabilities': 3,
        'description': 'High number of shared vulnerabilities'
    },
    {
        'type': 'timing_anomaly',
        'pattern': 'off_hours_activity',
        'description': 'Unusual off-hours network activity'
    },
    {
        'type': 'threat_exposure',
        'description': 'Similar threat exposure profiles'
    }
]

# Example usage
# threat_hunt_results = hunt_threats_using_similarity("123", example_threat_indicators)
```

## Error Handling

```python
try:
    # Get all similar devices
    all_similar = client.similardevices.get()
    print("Similar devices retrieved successfully")
    
    # Get similar devices for specific device
    device_similar = client.similardevices.get(device_id="123")
    print("Device similarity analysis completed")
    
    # Get detailed similar devices
    detailed_similar = client.similardevices.get(
        device_id="456",
        fulldevicedetails=True,
        count=10
    )
    print("Detailed similarity data retrieved")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check device ID parameter")
        elif e.response.status_code == 401:
            print("Authentication failed - check tokens")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions")
        elif e.response.status_code == 404:
            print("Device not found - check device ID")
        elif e.response.status_code == 429:
            print("Rate limit exceeded - reduce request frequency")
        else:
            print(f"Response: {e.response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
    print("Check network connectivity and host URL")

except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
    print("The response might not be valid JSON")
    # Handle non-JSON response (e.g., HTML login page)
    print("This might indicate an authentication or connectivity issue")

except ValueError as e:
    print(f"Value error: {e}")
    print("Check that device_id parameter is valid")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Device Similarity Analysis
- **Behavioral correlation**: Analyze devices with similar network behavior patterns
- **Profile matching**: Identify devices with comparable characteristics and usage
- **Clustering algorithms**: Group devices based on multiple similarity factors
- **Baseline establishment**: Use similar devices to establish behavioral baselines

### Similarity Factors
- **Network behavior**: Communication patterns, protocol usage, traffic volume
- **Device profile**: Hardware, software, operating system characteristics
- **Traffic patterns**: Data transfer patterns, timing, geographic distribution
- **Application usage**: Software usage patterns and application profiles
- **Time patterns**: Usage timing, peak hours, weekend activity patterns

### Clustering Applications
- **Security policy management**: Apply consistent policies to similar device groups
- **Anomaly detection**: Identify devices that deviate from their cluster behavior
- **Threat hunting**: Use similarity to predict threat spread patterns
- **Asset management**: Organize and manage devices based on similarity clusters

### Risk Correlation
- **Vulnerability clustering**: Identify devices with similar vulnerability profiles
- **Threat exposure**: Analyze shared threat exposure across similar devices
- **Security posture**: Compare security configurations and postures
- **Compliance alignment**: Ensure similar devices meet similar compliance requirements

### Outlier Detection
- **Anomaly identification**: Identify devices that don't fit established patterns
- **Security investigation**: Focus on outlier devices for potential threats
- **Configuration drift**: Detect devices that have drifted from standard configurations
- **New device detection**: Identify newly added devices that haven't been clustered

### Behavioral Baseline
- **Normal behavior**: Establish what constitutes normal behavior for device groups
- **Deviation detection**: Identify when devices deviate from group norms
- **Pattern recognition**: Recognize recurring behavioral patterns
- **Predictive analysis**: Predict future behavior based on similarity patterns

### Threat Intelligence
- **Coordinated attacks**: Identify potential coordinated attacks across similar devices
- **Lateral movement**: Track potential lateral movement between similar devices
- **Attack pattern recognition**: Recognize attack patterns using similarity data
- **Incident response**: Use similarity for incident scope determination

### Performance Optimization
- **Pagination support**: Handle large similarity datasets with pagination tokens
- **Detail control**: Use fulldevicedetails parameter to control response size
- **Response filtering**: Use responsedata parameter to limit returned fields
- **Batch processing**: Process multiple device similarity analyses efficiently

### Use Cases
- **Security operations**: Enhance security monitoring and threat detection
- **Asset management**: Organize and manage device inventory by similarity
- **Compliance monitoring**: Ensure similar devices meet similar requirements
- **Incident response**: Use similarity for scope determination and investigation
- **Policy management**: Apply group-based policies to similar devices
- **Capacity planning**: Plan resources based on device clustering patterns
- **Threat hunting**: Proactive threat hunting using device similarity patterns
