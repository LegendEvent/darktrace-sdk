# SummaryStatistics Module

The SummaryStatistics module provides access to comprehensive system statistics and analytics from your Darktrace deployment. This module offers detailed insights into network activity, security events, bandwidth usage, and MITRE ATT&CK framework mappings.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the summarystatistics module
summarystatistics = client.summarystatistics
```

## Methods

### get()

Retrieve comprehensive summary statistics from the Darktrace platform. This method provides access to various types of system statistics including network bandwidth, security events, and MITRE ATT&CK framework data.

```python
# Get basic summary statistics
basic_stats = summarystatistics.get()

# Get security event statistics for the last 24 hours
security_stats = summarystatistics.get(
    eventtype="security",
    hours=24
)

# Get bandwidth statistics for cSensor agents only
csensor_bandwidth = summarystatistics.get(
    eventtype="bandwidth",
    csensor=True,
    hours=12
)

# Get MITRE ATT&CK framework statistics
mitre_stats = summarystatistics.get(
    eventtype="security",
    mitreTactics=True,
    hours=168  # Last week
)

# Get specific data fields only
filtered_stats = summarystatistics.get(
    responsedata="bandwidth,events",
    hours=6
)
```

#### Parameters

- **responsedata** (str, optional): Restrict the returned JSON to only the specified top-level field(s) or object(s). Use comma-separated values for multiple fields (e.g., "bandwidth,events,alerts").

- **eventtype** (str, optional): Changes the format of data to return numeric event counts. Valid values:
  - `"security"`: Security-related events and alerts
  - `"bandwidth"`: Network bandwidth and traffic statistics  
  - `"connection"`: Network connection statistics
  - `"notice"`: System notices and informational events

- **endtime** (int, optional): End time of data to return in milliseconds since epoch (UTC). Requires `eventtype` parameter. When not specified, uses current time.

- **to** (str, optional): End time of data to return in 'YYYY-MM-DD HH:MM:SS' format. Alternative to `endtime`. Requires `eventtype` parameter.

- **hours** (int, optional): Number of hour intervals from the end time (or current time) to return. Requires `eventtype` parameter. Common values:
  - `1`: Last hour
  - `6`: Last 6 hours
  - `24`: Last day
  - `168`: Last week
  - `720`: Last month

- **csensor** (bool, optional): When `True`, only returns bandwidth statistics for cSensor agents. When `False`, returns statistics for Darktrace/Network bandwidth. Only applicable when `eventtype="bandwidth"`.

- **mitreTactics** (bool, optional): When `True`, alters the returned data to display MITRE ATT&CK Framework breakdown with tactics and techniques mapping. Only applicable with security event types.

#### Response Structure

The response structure varies based on the `eventtype` and parameters used:

##### Basic Statistics Response
```json
{
  "bandwidth": {
    "total_bytes": 1073741824,
    "ingress_bytes": 536870912,
    "egress_bytes": 536870912,
    "peak_throughput": 104857600,
    "average_throughput": 52428800
  },
  "events": {
    "total_events": 15427,
    "security_events": 234,
    "notices": 1245,
    "connections": 13948
  },
  "devices": {
    "total_devices": 156,
    "active_devices": 142,
    "new_devices": 3
  },
  "alerts": {
    "total_alerts": 28,
    "high_priority": 5,
    "medium_priority": 15,
    "low_priority": 8
  },
  "summary_period": {
    "start_time": 1705324800,
    "end_time": 1705328400,
    "duration_hours": 1
  }
}
```

##### Event Type Statistics Response
```json
{
  "eventtype": "security",
  "time_range": {
    "start": "2024-01-15 12:00:00",
    "end": "2024-01-16 12:00:00",
    "hours": 24
  },
  "event_counts": {
    "model_breaches": 45,
    "ai_analyst_incidents": 12,
    "antigena_actions": 8,
    "enhanced_monitoring": 156
  },
  "severity_breakdown": {
    "critical": 3,
    "high": 12,
    "medium": 25,
    "low": 117
  },
  "hourly_distribution": [
    {"hour": "2024-01-15 12:00", "count": 8},
    {"hour": "2024-01-15 13:00", "count": 12},
    // ... more hourly data
  ]
}
```

##### MITRE ATT&CK Framework Response
```json
{
  "mitre_tactics": {
    "initial_access": {
      "count": 5,
      "techniques": [
        {"id": "T1190", "name": "Exploit Public-Facing Application", "count": 3},
        {"id": "T1566", "name": "Phishing", "count": 2}
      ]
    },
    "persistence": {
      "count": 8,
      "techniques": [
        {"id": "T1053", "name": "Scheduled Task/Job", "count": 5},
        {"id": "T1547", "name": "Boot or Logon Autostart Execution", "count": 3}
      ]
    },
    "defense_evasion": {
      "count": 12,
      "techniques": [
        {"id": "T1055", "name": "Process Injection", "count": 7},
        {"id": "T1027", "name": "Obfuscated Files or Information", "count": 5}
      ]
    }
  },
  "total_mapped_events": 67,
  "unmapped_events": 23,
  "coverage_percentage": 74.4
}
```

##### Bandwidth Statistics Response
```json
{
  "bandwidth_stats": {
    "total_bandwidth": {
      "ingress_mb": 15360,
      "egress_mb": 8192,
      "total_mb": 23552
    },
    "peak_usage": {
      "timestamp": "2024-01-15 14:30:00",
      "mbps": 1024
    },
    "average_usage": {
      "ingress_mbps": 256,
      "egress_mbps": 136,
      "total_mbps": 392
    },
    "top_protocols": [
      {"protocol": "HTTPS", "percentage": 45.2, "mb": 10651},
      {"protocol": "HTTP", "percentage": 23.1, "mb": 5441},
      {"protocol": "SSH", "percentage": 12.7, "mb": 2991}
    ],
    "csensor_specific": true
  }
}
```

## Examples

### Get All Summarystatisticss

```python
summarystatistics_data = client.summarystatistics.get()
for item in summarystatistics_data.get("summarystatistics", []):
    print(f"Item: {item}")
```

### Comprehensive Security Operations Dashboard

```python
from darktrace import DarktraceClient
from datetime import datetime, timedelta
import json

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def create_security_operations_dashboard(time_periods=[1, 6, 24, 168]):
    """Create a comprehensive security operations dashboard with multiple time periods"""
    
    print("Darktrace Security Operations Dashboard")
    print("=" * 60)
    
    dashboard_data = {
        'generated_at': datetime.now().isoformat(),
        'time_periods': {},
        'summary': {},
        'trends': {},
        'recommendations': []
    }
    
    try:
        # Collect statistics for different time periods
        for hours in time_periods:
            period_name = f"{hours}h"
            if hours == 168:
                period_name = "7d"
            elif hours == 720:
                period_name = "30d"
            
            print(f"\nCollecting statistics for {period_name}...")
            
            # Get comprehensive security statistics
            security_stats = client.summarystatistics.get(
                eventtype="security",
                hours=hours
            )
            
            # Get bandwidth statistics
            bandwidth_stats = client.summarystatistics.get(
                eventtype="bandwidth",
                hours=hours
            )
            
            # Get MITRE ATT&CK statistics
            mitre_stats = client.summarystatistics.get(
                eventtype="security",
                hours=hours,
                mitreTactics=True
            )
            
            dashboard_data['time_periods'][period_name] = {
                'hours': hours,
                'security': security_stats,
                'bandwidth': bandwidth_stats,
                'mitre': mitre_stats
            }
            
            print(f"   ✅ {period_name} statistics collected")
        
        # Generate summary analysis
        print(f"\nGenerating dashboard summary...")
        
        # Get latest period data for summary
        latest_period = dashboard_data['time_periods']['24h'] if '24h' in dashboard_data['time_periods'] else list(dashboard_data['time_periods'].values())[0]
        
        latest_security = latest_period['security']
        latest_bandwidth = latest_period['bandwidth']
        latest_mitre = latest_period['mitre']
        
        # Security summary
        security_events = latest_security.get('event_counts', {})
        severity_breakdown = latest_security.get('severity_breakdown', {})
        
        dashboard_data['summary']['security'] = {
            'total_security_events': sum(security_events.values()) if security_events else 0,
            'critical_alerts': severity_breakdown.get('critical', 0),
            'high_alerts': severity_breakdown.get('high', 0),
            'model_breaches': security_events.get('model_breaches', 0),
            'ai_analyst_incidents': security_events.get('ai_analyst_incidents', 0),
            'antigena_actions': security_events.get('antigena_actions', 0)
        }
        
        # Bandwidth summary
        bandwidth_data = latest_bandwidth.get('bandwidth_stats', {})
        total_bw = bandwidth_data.get('total_bandwidth', {});
        
        dashboard_data['summary']['bandwidth'] = {
            'total_gb': (total_bw.get('total_mb', 0)) / 1024,
            'ingress_gb': (total_bw.get('ingress_mb', 0)) / 1024,
            'egress_gb': (total_bw.get('egress_mb', 0)) / 1024,
            'peak_mbps': bandwidth_data.get('peak_usage', {}).get('mbps', 0),
            'average_mbps': bandwidth_data.get('average_usage', {}).get('total_mbps', 0)
        }
        
        # MITRE ATT&CK summary
        mitre_tactics = latest_mitre.get('mitre_tactics', {})
        
        dashboard_data['summary']['mitre'] = {
            'total_tactics': len(mitre_tactics),
            'total_mapped_events': latest_mitre.get('total_mapped_events', 0),
            'coverage_percentage': latest_mitre.get('coverage_percentage', 0),
            'top_tactics': sorted(
                [(tactic, data.get('count', 0)) for tactic, data in mitre_tactics.items()],
                key=lambda x: x[1], reverse=True
            )[:5]
        }
        
        # Calculate trends
        print(f"Analyzing trends...")
        
        if len(time_periods) >= 2:
            # Compare shortest and longest periods for trend analysis
            short_period = dashboard_data['time_periods'][f"{time_periods[0]}h"]
            long_period = dashboard_data['time_periods'][f"{time_periods[-1]}h"]
            
            # Security trends
            short_events = short_period['security'].get('event_counts', {})
            long_events = long_period['security'].get('event_counts', {})
            
            # Calculate hourly rates
            short_hours = time_periods[0]
            long_hours = time_periods[-1]
            
            short_hourly_rate = sum(short_events.values()) / short_hours if short_events and short_hours > 0 else 0
            long_hourly_rate = sum(long_events.values()) / long_hours if long_events and long_hours > 0 else 0
            
            trend_percentage = ((short_hourly_rate - long_hourly_rate) / long_hourly_rate * 100) if long_hourly_rate > 0 else 0;
            
            dashboard_data['trends']['security_events'] = {
                'short_period_hourly_rate': short_hourly_rate,
                'long_period_hourly_rate': long_hourly_rate,
                'trend_percentage': trend_percentage,
                'trend_direction': 'increasing' if trend_percentage > 5 else 'decreasing' if trend_percentage < -5 else 'stable'
            }
        }
        
        # Generate recommendations
        print(f"Generating recommendations...")
        
        recommendations = []
        
        # Security recommendations
        critical_count = dashboard_data['summary']['security']['critical_alerts']
        high_count = dashboard_data['summary']['security']['high_alerts']
        
        if critical_count > 0:
            recommendations.append({
                'type': 'security',
                'priority': 'critical',
                'message': f'{critical_count} critical security alerts require immediate attention',
                'action': 'Review and respond to critical alerts in AI Analyst'
            })
        
        if high_count > 5:
            recommendations.append({
                'type': 'security',
                'priority': 'high',
                'message': f'{high_count} high-priority alerts detected',
                'action': 'Investigate high-priority alerts for potential threats'
            })
        
        # Bandwidth recommendations
        peak_mbps = dashboard_data['summary']['bandwidth']['peak_mbps']
        avg_mbps = dashboard_data['summary']['bandwidth']['average_mbps']
        
        if peak_mbps > avg_mbps * 3:
            recommendations.append({
                'type': 'bandwidth',
                'priority': 'medium',
                'message': f'High bandwidth spikes detected (peak: {peak_mbps:.0f} Mbps vs avg: {avg_mbps:.0f} Mbps)',
                'action': 'Investigate bandwidth usage patterns and potential data exfiltration'
            })
        
        # MITRE coverage recommendations
        coverage_pct = dashboard_data['summary']['mitre']['coverage_percentage']
        
        if coverage_pct < 70:
            recommendations.append({
                'type': 'mitre',
                'priority': 'medium',
                'message': f'MITRE ATT&CK coverage is {coverage_pct:.1f}% - below recommended 70%',
                'action': 'Review detection coverage and enhance monitoring for unmapped techniques'
            })
        
        # Trend-based recommendations
        if 'security_events' in dashboard_data['trends']:
            trend = dashboard_data['trends']['security_events']
            if trend['trend_direction'] == 'increasing' and trend['trend_percentage'] > 20:
                recommendations.append({
                    'type': 'trend',
                    'priority': 'high',
                    'message': f'Security events increasing by {trend["trend_percentage"]:.1f}%',
                    'action': 'Investigate cause of increasing security events - potential ongoing campaign'
                })
        
        dashboard_data['recommendations'] = recommendations
        
        # Display dashboard
        print(f"\n" + "=" * 60)
        print(f"SECURITY OPERATIONS DASHBOARD")
        print(f"Generated: {dashboard_data['generated_at']}")
        print(f"=" * 60)
        
        # Security summary
        sec_summary = dashboard_data['summary']['security']
        print(f"\n🛡️  SECURITY OVERVIEW (Last 24h):")
        print(f"   Total Security Events: {sec_summary['total_security_events']:,}")
        print(f"   Critical Alerts: {sec_summary['critical_alerts']}")
        print(f"   High Priority Alerts: {sec_summary['high_alerts']}")
        print(f"   Model Breaches: {sec_summary['model_breaches']}")
        print(f"   AI Analyst Incidents: {sec_summary['ai_analyst_incidents']}")
        print(f"   Antigena Actions: {sec_summary['antigena_actions']}")
        
        # Bandwidth summary
        bw_summary = dashboard_data['summary']['bandwidth']
        print(f"\n📊 BANDWIDTH OVERVIEW (Last 24h):")
        print(f"   Total Traffic: {bw_summary['total_gb']:.1f} GB")
        print(f"   Ingress: {bw_summary['ingress_gb']:.1f} GB")
        print(f"   Egress: {bw_summary['egress_gb']:.1f} GB")
        print(f"   Peak Usage: {bw_summary['peak_mbps']:.0f} Mbps")
        print(f"   Average Usage: {bw_summary['average_mbps']:.0f} Mbps")
        
        # MITRE summary
        mitre_summary = dashboard_data['summary']['mitre']
        print(f"\n🎯 MITRE ATT&CK OVERVIEW:")
        print(f"   Coverage: {mitre_summary['coverage_percentage']:.1f}%")
        print(f"   Mapped Events: {mitre_summary['total_mapped_events']:,}")
        print(f"   Active Tactics: {mitre_summary['total_tactics']}")
        print(f"   Top Tactics:")
        for tactic, count in mitre_summary['top_tactics']:
            print(f"     • {tactic.replace('_', ' ').title()}: {count} events")
        
        # Trends
        if 'security_events' in dashboard_data['trends']:
            trend = dashboard_data['trends']['security_events']
            trend_icon = "📈" if trend['trend_direction'] == 'increasing' else "📉" if trend['trend_direction'] == 'decreasing' else "➡️"
            print(f"\n{trend_icon} SECURITY TRENDS:")
            print(f"   Event Rate Trend: {trend['trend_direction'].title()} ({trend['trend_percentage']:+.1f}%)")
            print(f"   Current Rate: {trend['short_period_hourly_rate']:.1f} events/hour")
            print(f"   Historical Rate: {trend['long_period_hourly_rate']:.1f} events/hour")
        
        # Recommendations
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                priority_icon = "🔴" if rec['priority'] == 'critical' else "🟡" if rec['priority'] == 'high' else "🟢"
                print(f"   {i}. {priority_icon} {rec['message']}")
                print(f"      Action: {rec['action']}")
        
        print(f"\n" + "=" * 60)
        
        return dashboard_data
        
    except Exception as e:
        print(f"Error creating security operations dashboard: {e}")
        return None

# Example usage
# dashboard = create_security_operations_dashboard([1, 6, 24, 168])
```

### MITRE ATT&CK Analysis and Reporting

```python
def comprehensive_mitre_analysis(time_range_hours=168):
    """Comprehensive MITRE ATT&CK framework analysis and reporting"""
    
    print(f"MITRE ATT&CK Analysis Report")
    print("=" * 50)
    print(f"Time Range: {time_range_hours} hours ({time_range_hours/24:.1f} days)")
    
    try:
        # Get MITRE ATT&CK statistics
        mitre_stats = client.summarystatistics.get(
            eventtype="security",
            hours=time_range_hours,
            mitreTactics=True
        )
        
        # Get general security statistics for context
        security_stats = client.summarystatistics.get(
            eventtype="security",
            hours=time_range_hours
        )
        
        analysis_report = {
            'time_range': time_range_hours,
            'generated_at': datetime.now().isoformat(),
            'mitre_statistics': mitre_stats,
            'security_context': security_stats,
            'analysis': {},
            'recommendations': []
        }
        
        print(f"\nProcessing MITRE ATT&CK data...")
        
        # Extract MITRE data
        mitre_tactics = mitre_stats.get('mitre_tactics', {})
        total_mapped = mitre_stats.get('total_mapped_events', 0)
        total_unmapped = mitre_stats.get('unmapped_events', 0)
        coverage_pct = mitre_stats.get('coverage_percentage', 0)
        
        # Analyze tactics distribution
        tactics_analysis = {}
        total_tactic_events = 0
        
        for tactic, data in mitre_tactics.items():
            count = data.get('count', 0)
            techniques = data.get('techniques', [])
            
            total_tactic_events += count;
            
            tactics_analysis[tactic] = {
                'event_count': count,
                'technique_count': len(techniques),
                'percentage_of_mapped': (count / total_mapped * 100) if total_mapped > 0 else 0,
                'techniques': techniques,
                'top_technique': max(techniques, key=lambda x: x.get('count', 0)) if techniques else None
            }
        }
        
        # Sort tactics by event count
        tactics_by_frequency = sorted(tactics_analysis.items(), key=lambda x: x[1]['event_count'], reverse=True)
        
        # Identify coverage gaps and strengths
        print(f"\nAnalyzing MITRE ATT&CK coverage...")
        
        # Standard MITRE ATT&CK tactics for comparison
        standard_tactics = [
            'initial_access', 'execution', 'persistence', 'privilege_escalation',
            'defense_evasion', 'credential_access', 'discovery', 'lateral_movement',
            'collection', 'command_and_control', 'exfiltration', 'impact'
        ]
        
        covered_tactics = set(mitre_tactics.keys())
        missing_tactics = set(standard_tactics) - covered_tactics;
        
        analysis_report['analysis'] = {
            'coverage_summary': {
                'total_events': total_mapped + total_unmapped,
                'mapped_events': total_mapped,
                'unmapped_events': total_unmapped,
                'coverage_percentage': coverage_pct,
                'tactics_covered': len(covered_tactics),
                'tactics_missing': len(missing_tactics)
            },
            'tactics_distribution': tactics_analysis,
            'top_tactics': tactics_by_frequency[:5],
            'coverage_gaps': list(missing_tactics),
            'risk_assessment': {}
        }
        
        # Risk assessment based on tactics
        high_risk_tactics = ['initial_access', 'persistence', 'credential_access', 'lateral_movement', 'exfiltration']
        detected_high_risk = [tactic for tactic in high_risk_tactics if tactic in covered_tactics]
        
        analysis_report['analysis']['risk_assessment'] = {
            'high_risk_tactics_detected': detected_high_risk,
            'high_risk_coverage': len(detected_high_risk) / len(high_risk_tactics) * 100,
            'attack_progression_indicators': []
        }
        
        # Look for attack progression patterns
        progression_patterns = {
            'full_kill_chain': ['initial_access', 'execution', 'persistence', 'lateral_movement', 'exfiltration'],
            'credential_attack': ['initial_access', 'credential_access', 'lateral_movement'],
            'data_theft': ['discovery', 'collection', 'exfiltration'],
            'persistence_focused': ['execution', 'persistence', 'defense_evasion']
        }
        
        for pattern_name, required_tactics in progression_patterns.items():
            detected_tactics = [tactic for tactic in required_tactics if tactic in covered_tactics]
            completion_rate = len(detected_tactics) / len(required_tactics) * 100;
            
            if completion_rate >= 75:  # 75% or more tactics detected
                analysis_report['analysis']['risk_assessment']['attack_progression_indicators'].append({
                    'pattern': pattern_name,
                    'completion_rate': completion_rate,
                    'detected_tactics': detected_tactics,
                    'missing_tactics': [t for t in required_tactics if t not in covered_tactics]
                })
        }
        
        # Generate recommendations
        print(f"Generating security recommendations...")
        
        recommendations = []
        
        # Coverage recommendations
        if coverage_pct < 60:
            recommendations.append({
                'type': 'coverage',
                'priority': 'high',
                'title': 'Low MITRE ATT&CK Coverage',
                'description': f'Only {coverage_pct:.1f}% of security events mapped to MITRE framework',
                'action': 'Review detection rules and enhance coverage for unmapped events'
            })
        
        # Missing tactics recommendations
        if missing_tactics:
            critical_missing = set(missing_tactics) & set(high_risk_tactics)
            if critical_missing:
                recommendations.append({
                    'type': 'gaps',
                    'priority': 'high',
                    'title': 'Critical Tactic Coverage Gaps',
                    'description': f'Missing coverage for high-risk tactics: {", ".join(critical_missing)}',
                    'action': 'Implement detection rules for missing high-risk tactics'
                })
        }
        
        # High-frequency tactic recommendations
        top_tactic, top_data = tactics_by_frequency[0] if tactics_by_frequency else (None, None)
        if top_tactic and top_data['event_count'] > total_mapped * 0.3:  # More than 30% of events
            recommendations.append({
                'type': 'investigation',
                'priority': 'medium',
                'title': f'High Activity in {top_tactic.replace("_", " ").title()}',
                'description': f'{top_data["event_count"]} events ({top_data["percentage_of_mapped"]:.1f}% of mapped events)',
                'action': f'Investigate unusual activity patterns in {top_tactic.replace("_", " ")} techniques'
            })
        }
        
        # Attack progression recommendations
        progression_indicators = analysis_report['analysis']['risk_assessment']['attack_progression_indicators']
        if progression_indicators:
            for indicator in progression_indicators:
                if indicator['completion_rate'] >= 90:
                    recommendations.append({
                        'type': 'threat',
                        'priority': 'critical',
                        'title': f'Potential {indicator["pattern"].replace("_", " ").title()} Attack',
                        'description': f'{indicator["completion_rate"]:.0f}% of attack pattern detected',
                        'action': 'Immediate investigation required - potential active attack campaign'
                    })
        }
        
        analysis_report['recommendations'] = recommendations
        
        # Display comprehensive report
        print(f"\n" + "=" * 50)
        print(f"MITRE ATT&CK ANALYSIS REPORT")
        print(f"Time Range: {time_range_hours} hours")
        print(f"Generated: {analysis_report['generated_at']}")
        print(f"=" * 50)
        
        # Coverage overview
        coverage = analysis_report['analysis']['coverage_summary']
        print(f"\n📊 COVERAGE OVERVIEW:")
        print(f"   Total Security Events: {coverage['total_events']:,}")
        print(f"   Mapped to MITRE: {coverage['mapped_events']:,} ({coverage['coverage_percentage']:.1f}%)")
        print(f"   Unmapped Events: {coverage['unmapped_events']:,}")
        print(f"   Tactics Covered: {coverage['tactics_covered']}/12")
        
        if coverage['tactics_missing'] > 0:
            print(f"   Missing Tactics: {coverage['tactics_missing']}")
        
        # Top tactics
        print(f"\n🎯 TOP ACTIVE TACTICS:")
        for i, (tactic, data) in enumerate(tactics_by_frequency[:5], 1):
            tactic_name = tactic.replace('_', ' ').title()
            print(f"   {i}. {tactic_name}: {data['event_count']} events ({data['percentage_of_mapped']:.1f}%)")
            print(f"      Techniques: {data['technique_count']}")
            
            if data['top_technique']:
                top_tech = data['top_technique']
                print(f"      Top Technique: {top_tech['name']} ({top_tech['count']} events)")
        
        # Coverage gaps
        if analysis_report['analysis']['coverage_gaps']:
            print(f"\n⚠️  COVERAGE GAPS:")
            for gap in analysis_report['analysis']['coverage_gaps']:
                gap_name = gap.replace('_', ' ').title()
                priority = "🔴 HIGH" if gap in high_risk_tactics else "🟡 MEDIUM"
                print(f"   • {gap_name} ({priority})")
        
        # Risk assessment
        risk_assessment = analysis_report['analysis']['risk_assessment']
        print(f"\n🚨 RISK ASSESSMENT:")
        print(f"   High-Risk Tactics Detected: {len(risk_assessment['high_risk_tactics_detected'])}/5")
        print(f"   High-Risk Coverage: {risk_assessment['high_risk_coverage']:.1f}%")
        
        # Attack progression indicators
        if risk_assessment['attack_progression_indicators']:
            print(f"\n🎭 ATTACK PROGRESSION INDICATORS:")
            for indicator in risk_assessment['attack_progression_indicators']:
                pattern_name = indicator['pattern'].replace('_', ' ').title()
                completion = indicator['completion_rate']
                priority = "🔴 CRITICAL" if completion >= 90 else "🟡 HIGH" if completion >= 75 else "🟢 MEDIUM"
                
                print(f"   • {pattern_name}: {completion:.0f}% complete ({priority})")
                print(f"     Detected: {', '.join(indicator['detected_tactics'])}")
                if indicator['missing_tactics']:
                    print(f"     Missing: {', '.join(indicator['missing_tactics'])}")
        
        # Recommendations
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                priority_icon = "🔴" if rec['priority'] == 'critical' else "🟡" if rec['priority'] == 'high' else "🟢"
                print(f"   {i}. {priority_icon} {rec['title']}")
                print(f"      {rec['description']}")
                print(f"      Action: {rec['action']}")
        
        # Detailed technique analysis
        print(f"\n🔍 DETAILED TECHNIQUE ANALYSIS:")
        for tactic, data in tactics_by_frequency[:3]:  # Top 3 tactics
            tactic_name = tactic.replace('_', ' ').title()
            print(f"\n   {tactic_name} ({data['event_count']} events):")
            
            techniques = sorted(data['techniques'], key=lambda x: x.get('count', 0), reverse=True)
            for tech in techniques[:5]:  # Top 5 techniques per tactic
                print(f"     • {tech['id']}: {tech['name']} ({tech['count']} events)")
        
        print(f"\n" + "=" * 50)
        
        return analysis_report
        
    except Exception as e:
        print(f"Error in MITRE ATT&CK analysis: {e}")
        return None

# Example usage
# mitre_analysis = comprehensive_mitre_analysis(168)  # Last week
```

### Bandwidth Usage Analysis and Optimization

```python
def bandwidth_analysis_and_optimization(hours_list=[1, 6, 24, 168]):
    """Comprehensive bandwidth usage analysis and optimization recommendations"""
    
    print(f"Bandwidth Usage Analysis and Optimization")
    print("=" * 60)
    
    try:
        bandwidth_data = {}
        
        # Collect bandwidth data for different time periods
        for hours in hours_list:
            period_name = f"{hours}h"
            if hours == 168:
                period_name = "7d"
            elif hours == 720:
                period_name = "30d"
            
            print(f"Collecting bandwidth data for {period_name}...")
            
            # Get general bandwidth statistics
            general_bw = client.summarystatistics.get(
                eventtype="bandwidth",
                hours=hours
            )
            
            # Get cSensor-specific bandwidth if available
            try:
                csensor_bw = client.summarystatistics.get(
                    eventtype="bandwidth",
                    hours=hours,
                    csensor=True
                )
            except:
                csensor_bw = None
            
            # Get network-only bandwidth
            try:
                network_bw = client.summarystatistics.get(
                    eventtype="bandwidth",
                    hours=hours,
                    csensor=False
                )
            except:
                network_bw = None
            
            bandwidth_data[period_name] = {
                'hours': hours,
                'general': general_bw,
                'csensor': csensor_bw,
                'network': network_bw
            }
            
            print(f"   ✅ {period_name} data collected")
        
        # Analysis and reporting
        analysis_report = {
            'generated_at': datetime.now().isoformat(),
            'time_periods': hours_list,
            'bandwidth_data': bandwidth_data,
            'analysis': {},
            'optimization_recommendations': []
        }
        
        print(f"\nAnalyzing bandwidth patterns...")
        
        # Analyze latest period (typically 24h)
        latest_period = "24h" if "24h" in bandwidth_data else list(bandwidth_data.keys())[-1]
        latest_data = bandwidth_data[latest_period]['general']
        
        bw_stats = latest_data.get('bandwidth_stats', {})
        total_bw = bw_stats.get('total_bandwidth', {});
        peak_usage = bw_stats.get('peak_usage', {});
        avg_usage = bw_stats.get('average_usage', {});
        protocol_breakdown = bw_stats.get('top_protocols', []);
        
        # Calculate key metrics
        total_gb = total_bw.get('total_mb', 0) / 1024
        ingress_gb = total_bw.get('ingress_mb', 0) / 1024
        egress_gb = total_bw.get('egress_mb', 0) / 1024
        peak_mbps = peak_usage.get('mbps', 0)
        avg_total_mbps = avg_usage.get('total_mbps', 0)
        avg_ingress_mbps = avg_usage.get('ingress_mbps', 0)
        avg_egress_mbps = avg_usage.get('egress_mbps', 0)
        
        # Traffic direction analysis
        if ingress_gb > 0 and egress_gb > 0:
            ingress_ratio = ingress_gb / (ingress_gb + egress_gb) * 100
            egress_ratio = egress_gb / (ingress_gb + egress_gb) * 100
        else:
            ingress_ratio = egress_ratio = 0
        
        # Peak to average ratio analysis
        peak_to_avg_ratio = peak_mbps / avg_total_mbps if avg_total_mbps > 0 else 0
        
        analysis_report['analysis']['current_usage'] = {
            'total_gb': total_gb,
            'ingress_gb': ingress_gb,
            'egress_gb': egress_gb,
            'ingress_ratio': ingress_ratio,
            'egress_ratio': egress_ratio,
            'peak_mbps': peak_mbps,
            'average_mbps': avg_total_mbps,
            'peak_to_avg_ratio': peak_to_avg_ratio,
            'protocol_breakdown': protocol_breakdown
        }
        
        # Trend analysis across time periods
        if len(bandwidth_data) >= 2:
            print(f"Analyzing bandwidth trends...")
            
            # Compare different time periods
            periods = sorted(bandwidth_data.keys(), key=lambda x: bandwidth_data[x]['hours'])
            trends = {}
            
            for i in range(1, len(periods)):
                current_period = periods[i]
                previous_period = periods[i-1]
                
                current_data = bandwidth_data[current_period]['general']
                previous_data = bandwidth_data[previous_period]['general']
                
                # Calculate hourly rates for comparison
                current_total = current_data.get('bandwidth_stats', {}).get('total_bandwidth', {}).get('total_mb', 0)
                previous_total = previous_data.get('bandwidth_stats', {}).get('total_bandwidth', {}).get('total_mb', 0)
                
                current_hours = bandwidth_data[current_period]['hours']
                previous_hours = bandwidth_data[previous_period]['hours']
                
                current_rate = current_total / current_hours if current_hours > 0 else 0
                previous_rate = previous_total / previous_hours if previous_hours > 0 else 0
                
                trend_pct = ((current_rate - previous_rate) / previous_rate * 100) if previous_rate > 0 else 0;
                
                trends[f"{previous_period}_to_{current_period}"] = {
                    'current_rate_mb_per_hour': current_rate,
                    'previous_rate_mb_per_hour': previous_rate,
                    'trend_percentage': trend_pct,
                    'trend_direction': 'increasing' if trend_pct > 5 else 'decreasing' if trend_pct < -5 else 'stable'
                }
            }
            
            analysis_report['analysis']['trends'] = trends
        }
        
        # cSensor vs Network analysis
        if bandwidth_data[latest_period]['csensor'] and bandwidth_data[latest_period]['network']:
            print(f"Analyzing cSensor vs Network bandwidth...")
            
            csensor_data = bandwidth_data[latest_period]['csensor']
            network_data = bandwidth_data[latest_period]['network']
            
            csensor_total = csensor_data.get('bandwidth_stats', {}).get('total_bandwidth', {}).get('total_mb', 0)
            network_total = network_data.get('bandwidth_stats', {}).get('total_bandwidth', {}).get('total_mb', 0)
            
            total_monitored = csensor_total + network_total;
            
            if total_monitored > 0:
                csensor_percentage = csensor_total / total_monitored * 100
                network_percentage = network_total / total_monitored * 100
                
                analysis_report['analysis']['deployment_breakdown'] = {
                    'csensor_gb': csensor_total / 1024,
                    'network_gb': network_total / 1024,
                    'csensor_percentage': csensor_percentage,
                    'network_percentage': network_percentage,
                    'total_monitored_gb': total_monitored / 1024
                }
        }
        
        # Generate optimization recommendations
        print(f"Generating optimization recommendations...")
        
        recommendations = []
        
        # High bandwidth usage recommendations
        if total_gb > 1000:  # More than 1TB per day
            recommendations.append({
                'type': 'usage',
                'priority': 'medium',
                'title': 'High Bandwidth Usage Detected',
                'description': f'{total_gb:.1f} GB used in {latest_period}',
                'action': 'Review traffic patterns and consider bandwidth optimization strategies'
            })
        
        # Peak usage recommendations
        if peak_to_avg_ratio > 5:
            recommendations.append({
                'type': 'performance',
                'priority': 'medium',
                'title': 'High Peak-to-Average Bandwidth Ratio',
                'description': f'Peak usage ({peak_mbps:.0f} Mbps) is {peak_to_avg_ratio:.1f}x average ({avg_total_mbps:.0f} Mbps)',
                'action': 'Investigate bandwidth spikes and consider traffic shaping or load balancing'
            })
        
        # Traffic direction imbalance
        if abs(ingress_ratio - egress_ratio) > 30:  # More than 30% difference
            direction = "ingress" if ingress_ratio > egress_ratio else "egress"
            percentage = max(ingress_ratio, egress_ratio)
            recommendations.append({
                'type': 'balance',
                'priority': 'low',
                'title': f'Traffic Direction Imbalance',
                'description': f'{direction.title()} traffic dominates at {percentage:.1f}%',
                'action': f'Monitor {direction} traffic patterns for potential data exfiltration or unusual activity'
            })
        }
        
        # Protocol-based recommendations
        if protocol_breakdown:
            # Check for unusual protocol distributions
            total_protocol_traffic = sum(p.get('mb', 0) for p in protocol_breakdown)
            
            for protocol in protocol_breakdown:
                protocol_name = protocol.get('protocol', 'Unknown')
                protocol_mb = protocol.get('mb', 0)
                protocol_pct = protocol.get('percentage', 0)
                
                # Flag unusual protocol usage
                if protocol_name.lower() in ['p2p', 'bittorrent', 'torrent'] and protocol_pct > 5:
                    recommendations.append({
                        'type': 'protocol',
                        'priority': 'high',
                        'title': f'P2P Traffic Detected',
                        'description': f'{protocol_name}: {protocol_pct:.1f}% of traffic ({protocol_mb/1024:.1f} GB)',
                        'action': 'Investigate P2P traffic for policy violations or potential security risks'
                    })
                
                elif protocol_name.lower() in ['dns', 'ntp'] and protocol_pct > 15:
                    recommendations.append({
                        'type': 'protocol',
                        'priority': 'medium',
                        'title': f'Unusual {protocol_name} Traffic Volume',
                        'description': f'{protocol_name}: {protocol_pct:.1f}% of traffic - higher than typical',
                        'action': f'Investigate {protocol_name} traffic patterns for potential DNS tunneling or amplification attacks'
                    })
        }
        
        # Trend-based recommendations
        if 'trends' in analysis_report['analysis']:
            for trend_period, trend_data in analysis_report['analysis']['trends'].items():
                if trend_data['trend_direction'] == 'increasing' and trend_data['trend_percentage'] > 50:
                    recommendations.append({
                        'type': 'trend',
                        'priority': 'high',
                        'title': f'Rapid Bandwidth Increase',
                        'description': f'Bandwidth usage increased {trend_data["trend_percentage"]:.1f}% ({trend_period})',
                        'action': 'Investigate sudden bandwidth increase - potential data exfiltration or system compromise'
                    })
        }
        
        # Monitoring recommendations
        recommendations.extend([
            {
                'type': 'monitoring',
                'priority': 'low',
                'title': 'Enhanced Bandwidth Monitoring',
                'description': 'Implement real-time bandwidth monitoring and alerting',
                'action': 'Set up automated alerts for bandwidth thresholds and unusual patterns'
            },
            {
                'type': 'optimization',
                'priority': 'low',
                'title': 'Traffic Optimization',
                'description': 'Consider implementing traffic optimization techniques',
                'action': 'Evaluate QoS policies, traffic shaping, and bandwidth allocation strategies'
            }
        ])
        
        analysis_report['optimization_recommendations'] = recommendations
        
        # Display comprehensive report
        print(f"\n" + "=" * 60)
        print(f"BANDWIDTH ANALYSIS REPORT")
        print(f"Generated: {analysis_report['generated_at']}")
        print(f"=" * 60)
        
        # Current usage overview
        current = analysis_report['analysis']['current_usage']
        print(f"\n📊 CURRENT USAGE OVERVIEW ({latest_period}):")
        print(f"   Total Bandwidth: {current['total_gb']:.1f} GB")
        print(f"   Ingress: {current['ingress_gb']:.1f} GB ({current['ingress_ratio']:.1f}%)")
        print(f"   Egress: {current['egress_gb']:.1f} GB ({current['egress_ratio']:.1f}%)")
        print(f"   Peak Usage: {current['peak_mbps']:.0f} Mbps")
        print(f"   Average Usage: {current['average_mbps']:.0f} Mbps")
        print(f"   Peak/Avg Ratio: {current['peak_to_avg_ratio']:.1f}x")
        
        # Protocol breakdown
        if current['protocol_breakdown']:
            print(f"\n🌐 PROTOCOL BREAKDOWN:")
            for protocol in current['protocol_breakdown'][:5]:  # Top 5 protocols
                print(f"   • {protocol['protocol']}: {protocol['percentage']:.1f}% ({protocol['mb']/1024:.1f} GB)")
        
        # Deployment breakdown
        if 'deployment_breakdown' in analysis_report['analysis']:
            deploy = analysis_report['analysis']['deployment_breakdown']
            print(f"\n🏗️  DEPLOYMENT BREAKDOWN:")
            print(f"   Total Monitored: {deploy['total_monitored_gb']:.1f} GB")
            print(f"   cSensor Agents: {deploy['csensor_gb']:.1f} GB ({deploy['csensor_percentage']:.1f}%)")
            print(f"   Network Appliances: {deploy['network_gb']:.1f} GB ({deploy['network_percentage']:.1f}%)")
        
        # Trends
        if 'trends' in analysis_report['analysis']:
            print(f"\n📈 BANDWIDTH TRENDS:")
            for trend_period, trend_data in analysis_report['analysis']['trends'].items():
                periods = trend_period.replace('_to_', ' → ')
                direction = trend_data['trend_direction']
                percentage = trend_data['trend_percentage']
                
                trend_icon = "📈" if direction == 'increasing' else "📉" if direction == 'decreasing' else "➡️"
                print(f"   {trend_icon} {periods}: {direction.title()} ({percentage:+.1f}%)")
        
        # Recommendations
        if recommendations:
            print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                priority_icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                print(f"   {i}. {priority_icon} {rec['title']}")
                print(f"      {rec['description']}")
                print(f"      Action: {rec['action']}")
        
        print(f"\n" + "=" * 60)
        
        return analysis_report
        
    except Exception as e:
        print(f"Error in bandwidth analysis: {e}")
        return None

# Example usage
# bandwidth_analysis = bandwidth_analysis_and_optimization([1, 6, 24, 168])
```

## Error Handling

```python
try:
    # Get basic summary statistics
    basic_stats = client.summarystatistics.get()
    print("Basic statistics retrieved successfully")
    
    # Get security event statistics
    security_stats = client.summarystatistics.get(
        eventtype="security",
        hours=24
    )
    print("Security statistics retrieved successfully")
    
    # Get MITRE ATT&CK statistics
    mitre_stats = client.summarystatistics.get(
        eventtype="security",
        hours=168,
        mitreTactics=True
    )
    print("MITRE ATT&CK statistics retrieved successfully")
    
    # Get bandwidth statistics
    bandwidth_stats = client.summarystatistics.get(
        eventtype="bandwidth",
        hours=6,
        csensor=True
    )
    print("Bandwidth statistics retrieved successfully")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check parameters (eventtype, time format, boolean values)")
        elif e.response.status_code == 401:
            print("Authentication failed - check tokens")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for summary statistics")
        elif e.response.status_code == 404:
            print("Endpoint not found - check API endpoint availability")
        elif e.response.status_code == 422:
            print("Invalid parameters - check eventtype values and time parameters")
        elif e.response.status_code == 429:
            print("Rate limit exceeded - too many requests")
        elif e.response.status_code == 500:
            print("Internal server error - statistics service may be unavailable")
        else:
            print(f"Response: {e.response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
    print("Check network connectivity and host URL")

except requests.exceptions.Timeout as e:
    print(f"Request timeout: {e}")
    print("Statistics queries may take time - consider increasing timeout")

except ValueError as e:
    print(f"Value error: {e}")
    print("Check parameter types - hours (int), times (int), booleans (bool)")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Statistics Categories
- **Security Statistics**: Model breaches, AI Analyst incidents, Antigena actions, and security events
- **Bandwidth Statistics**: Network traffic analysis, protocol breakdown, and usage patterns  
- **Event Statistics**: System notices, connections, and operational events
- **MITRE ATT&CK Statistics**: Tactics and techniques mapping with coverage analysis

### Time Range Specifications
- **Relative Time**: Use `hours` parameter for time ranges relative to current time
- **Absolute Time**: Use `endtime` (Unix timestamp) or `to` (formatted string) for specific end times
- **Common Ranges**: 1h, 6h, 24h (1 day), 168h (1 week), 720h (30 days)

### MITRE ATT&CK Integration
- **Tactics Mapping**: Events mapped to MITRE ATT&CK tactics and techniques
- **Coverage Analysis**: Percentage of events successfully mapped to the framework
- **Technique Breakdown**: Detailed analysis of specific techniques detected
- **Attack Progression**: Identification of potential attack campaign patterns

### Bandwidth Analysis
- **Traffic Direction**: Separate analysis of ingress and egress traffic
- **Protocol Breakdown**: Distribution of traffic across different network protocols
- **Peak Analysis**: Peak usage identification and capacity planning
- **Deployment Types**: Separate statistics for cSensor agents vs network appliances

### Performance Considerations
- **Time Range Impact**: Longer time ranges require more processing time
- **Data Volume**: Large deployments may have significant data volumes
- **Caching**: Statistics may be cached for performance optimization
- **Real-time vs Historical**: Recent data may be more accurate than historical

### Integration Workflows
- **Dashboard Creation**: Build comprehensive security operations dashboards
- **Trend Analysis**: Identify patterns and trends across different time periods
- **Capacity Planning**: Use bandwidth statistics for network capacity planning
- **Threat Hunting**: Correlate statistics with threat hunting activities

### Reporting and Analytics
- **Executive Reporting**: High-level summaries for management reporting
- **Operational Metrics**: Detailed metrics for security operations teams
- **Compliance Reporting**: Statistics for regulatory compliance requirements
- **Performance Monitoring**: System performance and health metrics

### Filtering and Customization
- **Response Filtering**: Use `responsedata` to limit returned data fields
- **Event Type Filtering**: Focus on specific types of events or statistics
- **Deployment Filtering**: Separate analysis for different monitoring technologies
- **Custom Time Ranges**: Flexible time range specification for specific analysis needs

### Use Cases
- **Security Operations Centers**: Real-time and historical security metrics
- **Network Operations**: Bandwidth usage monitoring and optimization
- **Compliance Auditing**: Statistical reporting for compliance requirements
- **Capacity Planning**: Network and system capacity planning based on usage trends
- **Threat Intelligence**: Statistical analysis to support threat intelligence activities
- **Executive Reporting**: High-level security and operational metrics for leadership
