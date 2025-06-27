# Tags Module

The Tags module provides comprehensive tag management functionality for devices, credentials, and other entities within your Darktrace deployment. Tags enable you to organize, categorize, and manage your assets for better security operations and incident response.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the tags module
tags = client.tags
```

## Methods

### Tag Management

#### get()

Retrieve tag information from the Darktrace platform. Can fetch all tags or specific tags by ID or name.

```python
# Get all tags
all_tags = tags.get()

# Get specific tag by ID
specific_tag = tags.get(tag_id="5")

# Get tag by name
tag_by_name = tags.get(tag="critical_assets")

# Get only specific response data
filtered_response = tags.get(responsedata="name,color,description")
```

**Parameters:**
- **tag_id** (str, optional): Tag ID (tid) to retrieve a specific tag by ID
- **tag** (str, optional): Name of an existing tag to retrieve by name
- **responsedata** (str, optional): Restrict returned JSON to specific fields or objects

#### create()

Create a new tag in the Darktrace system with optional color and description.

```python
# Create basic tag
new_tag = tags.create(name="high_priority_assets")

# Create tag with color (HSL hue value)
colored_tag = tags.create(
    name="critical_servers",
    color=0,  # Red hue
    description="Mission-critical server infrastructure"
)

# Create tag with full details
detailed_tag = tags.create(
    name="iot_devices",
    color=240,  # Blue hue
    description="Internet of Things devices requiring special monitoring"
)
```

**Parameters:**
- **name** (str, required): Name for the created tag
- **color** (int, optional): HSL hue value (0-360) for the tag color in the UI
- **description** (str, optional): Description for the tag

#### delete()

Delete a tag by its tag ID. This removes the tag and all its associations.

```python
# Delete tag by ID
success = tags.delete(tag_id="5")
if success:
    print("Tag deleted successfully")
else:
    print("Failed to delete tag")
```

**Parameters:**
- **tag_id** (str, required): Tag ID (tid) to delete

**Returns:** Boolean indicating success/failure

### Entity Tag Management

#### get_entities()

Retrieve tag-entity relationships. Can get tags for a specific device or devices for a specific tag.

```python
# Get all tags for a specific device
device_tags = tags.get_entities(did=123)

# Get all devices with a specific tag
tagged_devices = tags.get_entities(tag="critical_assets")

# Get devices with full details
detailed_devices = tags.get_entities(
    tag="high_priority",
    fulldevicedetails=True
)

# Get specific response data only
filtered_entities = tags.get_entities(
    tag="servers",
    responsedata="devices"
)
```

**Parameters:**
- **did** (int, optional): Device ID to list tags for a device
- **tag** (str, optional): Tag name to list devices for a tag
- **responsedata** (str, optional): Restrict returned JSON to specific fields
- **fulldevicedetails** (bool, optional): Include detailed device information when querying by tag

#### post_entities()

Add a tag to a device with optional duration for temporary tagging.

```python
# Add permanent tag to device
tags.post_entities(did=123, tag="under_investigation")

# Add temporary tag (expires after 1 hour)
tags.post_entities(
    did=456,
    tag="temporary_quarantine",
    duration=3600  # 1 hour in seconds
)

# Add tag for 24 hours
tags.post_entities(
    did=789,
    tag="incident_response",
    duration=86400  # 24 hours
)
```

**Parameters:**
- **did** (int, required): Device ID to tag
- **tag** (str, required): Name of the tag to add
- **duration** (int, optional): Duration in seconds for temporary tags

#### delete_entities()

Remove a tag from a device.

```python
# Remove tag from device
success = tags.delete_entities(did=123, tag="under_investigation")
if success:
    print("Tag removed successfully")
```

**Parameters:**
- **did** (int, required): Device ID to untag
- **tag** (str, required): Name of the tag to remove

**Returns:** Boolean indicating success/failure

### Advanced Entity Management

#### get_tag_entities()

Get entities associated with a specific tag using the tag ID.

```python
# Get entities for tag ID 5
entities = tags.get_tag_entities(tid=5)

# Get entities with full device details
detailed_entities = tags.get_tag_entities(
    tid=5,
    fulldevicedetails=True
)

# Get only device information
devices_only = tags.get_tag_entities(
    tid=5,
    responsedata="devices"
)
```

**Parameters:**
- **tid** (int, required): Tag ID to query
- **responsedata** (str, optional): Restrict returned JSON to specific fields
- **fulldevicedetails** (bool, optional): Include detailed device information

#### post_tag_entities()

Add a tag to one or more entities (devices or credentials) using tag ID.

```python
# Tag single device
tags.post_tag_entities(
    tid=5,
    entityType="Device",
    entityValue="123"
)

# Tag multiple devices
tags.post_tag_entities(
    tid=5,
    entityType="Device",
    entityValue=["123", "456", "789"]
)

# Tag credential
tags.post_tag_entities(
    tid=5,
    entityType="Credential",
    entityValue="admin@company.com"
)

# Tag with expiry duration
tags.post_tag_entities(
    tid=5,
    entityType="Device",
    entityValue="123",
    expiryDuration=7200  # 2 hours
)
```

**Parameters:**
- **tid** (int, required): Tag ID to apply
- **entityType** (str, required): Type of entity - "Device" or "Credential"
- **entityValue** (str or list, required): Entity identifier(s) - device ID(s) or credential value(s)
- **expiryDuration** (int, optional): Duration in seconds for temporary tags

#### delete_tag_entity()

Remove a tag from a specific entity using tag-entity relationship ID.

```python
# Remove tag-entity relationship
success = tags.delete_tag_entity(tid=5, teid=123)
if success:
    print("Tag-entity relationship removed")
```

**Parameters:**
- **tid** (int, required): Tag ID
- **teid** (int, required): Tag-entity relationship ID

**Returns:** Boolean indicating success/failure

## Response Structures

### Tag Information Response
```json
{
  "tid": 5,
  "name": "critical_assets",
  "color": 0,
  "description": "Mission-critical infrastructure components",
  "created_at": "2024-01-15T10:30:00Z",
  "created_by": "admin@company.com",
  "entity_count": 25
}
```

### Tag List Response
```json
{
  "tags": [
    {
      "tid": 1,
      "name": "servers",
      "color": 120,
      "description": "Server infrastructure",
      "entity_count": 50
    },
    {
      "tid": 2,
      "name": "workstations",
      "color": 240,
      "description": "User workstations",
      "entity_count": 200
    }
  ]
}
```

### Entity Tags Response
```json
{
  "device_id": 123,
  "tags": [
    {
      "tid": 1,
      "name": "critical_assets",
      "color": 0,
      "expires_at": null
    },
    {
      "tid": 2,
      "name": "temporary_quarantine",
      "color": 30,
      "expires_at": "2024-01-15T14:30:00Z"
    }
  ]
}
```

### Tagged Devices Response
```json
{
  "tag": "critical_assets",
  "devices": [
    {
      "did": 123,
      "hostname": "web-server-01",
      "ip": "192.168.1.10",
      "mac": "00:1B:44:11:3A:B7",
      "tag_applied_at": "2024-01-15T10:30:00Z",
      "tag_expires_at": null
    }
  ],
  "credentials": [
    {
      "credential": "admin@company.com",
      "tag_applied_at": "2024-01-15T11:00:00Z",
      "tag_expires_at": "2024-01-16T11:00:00Z"
    }
  ]
}
```

## Examples

### Incident Response Tagging Workflow

```python
from darktrace import DarktraceClient
from datetime import datetime, timedelta
import time

client = DarktraceClient(
    host="https://your-darktrace-instance.com",
    public_token="your_public_token",
    private_token="your_private_token"
)

def incident_response_tagging_workflow(incident_id, affected_device_ids, incident_severity="medium"):
    """Complete incident response workflow using tags for organization and tracking"""
    
    print(f"Incident Response Tagging Workflow")
    print("=" * 50)
    print(f"Incident ID: {incident_id}")
    print(f"Severity: {incident_severity}")
    print(f"Affected Devices: {len(affected_device_ids)}")
    
    workflow_results = {
        'incident_id': incident_id,
        'severity': incident_severity,
        'affected_devices': affected_device_ids,
        'tags_created': [],
        'devices_tagged': [],
        'workflow_status': 'initiated'
    }
    
    try:
        # Step 1: Create incident-specific tags
        print(f"\n1. CREATING INCIDENT TAGS...")
        
        # Determine tag colors based on severity
        severity_colors = {
            'critical': 0,    # Red
            'high': 30,       # Orange
            'medium': 60,     # Yellow
            'low': 120        # Green
        }
        
        base_color = severity_colors.get(incident_severity, 60)
        
        # Create main incident tag
        incident_tag_name = f"incident_{incident_id}"
        incident_tag = client.tags.create(
            name=incident_tag_name,
            color=base_color,
            description=f"Incident {incident_id} - {incident_severity.title()} severity security incident"
        )
        
        workflow_results['tags_created'].append({
            'name': incident_tag_name,
            'tid': incident_tag.get('tid'),
            'purpose': 'main_incident_tracker'
        })
        
        print(f"   ✅ Created main incident tag: {incident_tag_name} (ID: {incident_tag.get('tid')})")
        
        # Create investigation status tag
        investigation_tag_name = f"under_investigation_{incident_id}"
        investigation_tag = client.tags.create(
            name=investigation_tag_name,
            color=240,  # Blue
            description=f"Devices currently under investigation for incident {incident_id}"
        )
        
        workflow_results['tags_created'].append({
            'name': investigation_tag_name,
            'tid': investigation_tag.get('tid'),
            'purpose': 'investigation_status'
        })
        
        print(f"   ✅ Created investigation tag: {investigation_tag_name} (ID: {investigation_tag.get('tid')})")
        
        # Create quarantine tag if high/critical severity
        quarantine_tag = None
        if incident_severity in ['high', 'critical']:
            quarantine_tag_name = f"quarantine_{incident_id}"
            quarantine_tag = client.tags.create(
                name=quarantine_tag_name,
                color=300,  # Purple
                description=f"Devices quarantined due to incident {incident_id}"
            )
            
            workflow_results['tags_created'].append({
                'name': quarantine_tag_name,
                'tid': quarantine_tag.get('tid'),
                'purpose': 'quarantine_status'
            })
            
            print(f"   ✅ Created quarantine tag: {quarantine_tag_name} (ID: {quarantine_tag.get('tid')})")
        
        # Step 2: Tag affected devices
        print(f"\n2. TAGGING AFFECTED DEVICES...")
        
        # Calculate tag duration based on severity (temporary tags)
        duration_mapping = {
            'critical': 48 * 3600,  # 48 hours
            'high': 24 * 3600,      # 24 hours
            'medium': 12 * 3600,    # 12 hours
            'low': 6 * 3600         # 6 hours
        }
        
        tag_duration = duration_mapping.get(incident_severity, 12 * 3600)
        
        for device_id in affected_device_ids:
            try:
                # Apply main incident tag (permanent)
                client.tags.post_entities(
                    did=device_id,
                    tag=incident_tag_name
                )
                
                # Apply investigation tag (temporary)
                client.tags.post_entities(
                    did=device_id,
                    tag=investigation_tag_name,
                    duration=tag_duration
                )
                
                device_result = {
                    'device_id': device_id,
                    'tags_applied': [incident_tag_name, investigation_tag_name],
                    'quarantined': False
                }
                
                # Apply quarantine tag for high/critical incidents
                if quarantine_tag and incident_severity in ['high', 'critical']:
                    client.tags.post_entities(
                        did=device_id,
                        tag=quarantine_tag['name'],
                        duration=tag_duration
                    )
                    device_result['tags_applied'].append(quarantine_tag['name'])
                    device_result['quarantined'] = True
                
                workflow_results['devices_tagged'].append(device_result)
                
                quarantine_status = " (QUARANTINED)" if device_result['quarantined'] else ""
                print(f"   ✅ Tagged device {device_id}{quarantine_status}")
                
            except Exception as e:
                print(f"   ❌ Failed to tag device {device_id}: {e}")
                workflow_results['devices_tagged'].append({
                    'device_id': device_id,
                    'tags_applied': [],
                    'error': str(e)
                })
        
        # Step 3: Generate incident tracking report
        print(f"\n3. INCIDENT TRACKING SUMMARY...")
        
        successfully_tagged = len([d for d in workflow_results['devices_tagged'] if not d.get('error')])
        failed_tags = len([d for d in workflow_results['devices_tagged'] if d.get('error')])
        quarantined_devices = len([d for d in workflow_results['devices_tagged'] if d.get('quarantined')])
        
        print(f"   Incident ID: {incident_id}")
        print(f"   Severity: {incident_severity.title()}")
        print(f"   Tags Created: {len(workflow_results['tags_created'])}")
        print(f"   Devices Successfully Tagged: {successfully_tagged}/{len(affected_device_ids)}")
        print(f"   Devices Quarantined: {quarantined_devices}")
        
        if failed_tags > 0:
            print(f"   Failed Tagging Operations: {failed_tags}")
        
        # Step 4: Set up monitoring and alerts
        print(f"\n4. MONITORING SETUP...")
        
        monitoring_recommendations = [
            f"• Monitor devices with tag '{incident_tag_name}' for additional suspicious activity",
            f"• Review investigation progress for devices with tag '{investigation_tag_name}'",
            f"• Track tag expiration times for temporary incident tags",
            f"• Correlate future alerts with incident-tagged devices"
        ]
        
        if quarantine_tag:
            monitoring_recommendations.append(
                f"• Ensure quarantined devices with tag '{quarantine_tag['name']}' remain isolated"
            )
        
        for rec in monitoring_recommendations:
            print(f"   {rec}")
        
        workflow_results['workflow_status'] = 'completed'
        
        # Step 5: Cleanup scheduling
        print(f"\n5. CLEANUP SCHEDULING...")
        
        cleanup_time = datetime.now() + timedelta(seconds=tag_duration)
        print(f"   Temporary tags will expire: {cleanup_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Manual cleanup recommended after incident resolution")
        
        # Return comprehensive workflow results
        return workflow_results
        
    except Exception as e:
        print(f"Error in incident response tagging workflow: {e}")
        workflow_results['workflow_status'] = 'failed'
        workflow_results['error'] = str(e)
        return workflow_results

# Example usage
# incident_workflow = incident_response_tagging_workflow(
#     incident_id="INC-2024-001",
#     affected_device_ids=[123, 456, 789, 101, 102],
#     incident_severity="high"
# )
```

### Asset Management and Classification System

```python
def implement_asset_classification_system():
    """Implement a comprehensive asset classification system using tags"""
    
    print(f"Asset Classification System Implementation")
    print("=" * 60)
    
    try:
        classification_system = {
            'asset_categories': {},
            'risk_levels': {},
            'operational_status': {},
            'compliance_tags': {},
            'implementation_results': {}
        }
        
        # Step 1: Create Asset Category Tags
        print(f"\n1. CREATING ASSET CATEGORY TAGS...")
        
        asset_categories = [
            {
                'name': 'servers',
                'color': 200,  # Cyan
                'description': 'Server infrastructure including web, database, and application servers'
            },
            {
                'name': 'workstations',
                'color': 240,  # Blue
                'description': 'End-user workstations and laptops'
            },
            {
                'name': 'network_infrastructure',
                'color': 120,  # Green
                'description': 'Network equipment including routers, switches, and firewalls'
            },
            {
                'name': 'iot_devices',
                'color': 300,  # Purple
                'description': 'Internet of Things devices and embedded systems'
            },
            {
                'name': 'mobile_devices',
                'color': 180,  # Light blue
                'description': 'Mobile phones, tablets, and portable devices'
            },
            {
                'name': 'security_appliances',
                'color': 0,    # Red
                'description': 'Security-specific devices and appliances'
            }
        ]
        
        for category in asset_categories:
            try:
                tag = client.tags.create(
                    name=category['name'],
                    color=category['color'],
                    description=category['description']
                )
                
                classification_system['asset_categories'][category['name']] = {
                    'tid': tag.get('tid'),
                    'color': category['color'],
                    'description': category['description']
                }
                
                print(f"   ✅ Created category tag: {category['name']} (ID: {tag.get('tid')})")
                
            except Exception as e:
                print(f"   ❌ Failed to create category tag {category['name']}: {e}")
        
        # Step 2: Create Risk Level Tags
        print(f"\n2. CREATING RISK LEVEL TAGS...")
        
        risk_levels = [
            {
                'name': 'critical_assets',
                'color': 0,    # Red
                'description': 'Mission-critical assets requiring highest protection'
            },
            {
                'name': 'high_value_assets',
                'color': 30,   # Orange
                'description': 'High-value assets with significant business impact'
            },
            {
                'name': 'standard_assets',
                'color': 60,   # Yellow
                'description': 'Standard business assets with normal protection requirements'
            },
            {
                'name': 'low_risk_assets',
                'color': 120,  # Green
                'description': 'Low-risk assets with minimal business impact'
            }
        ]
        
        for risk_level in risk_levels:
            try:
                tag = client.tags.create(
                    name=risk_level['name'],
                    color=risk_level['color'],
                    description=risk_level['description']
                )
                
                classification_system['risk_levels'][risk_level['name']] = {
                    'tid': tag.get('tid'),
                    'color': risk_level['color'],
                    'description': risk_level['description']
                }
                
                print(f"   ✅ Created risk level tag: {risk_level['name']} (ID: {tag.get('tid')})")
                
            except Exception as e:
                print(f"   ❌ Failed to create risk level tag {risk_level['name']}: {e}")
        
        # Step 3: Create Operational Status Tags
        print(f"\n3. CREATING OPERATIONAL STATUS TAGS...")
        
        operational_statuses = [
            {
                'name': 'production',
                'color': 120,  # Green
                'description': 'Production systems in active use'
            },
            {
                'name': 'staging',
                'color': 60,   # Yellow
                'description': 'Staging and testing environments'
            },
            {
                'name': 'development',
                'color': 240,  # Blue
                'description': 'Development and experimental systems'
            },
            {
                'name': 'maintenance',
                'color': 30,   # Orange
                'description': 'Systems currently under maintenance'
            },
            {
                'name': 'decommissioned',
                'color': 0,    # Red
                'description': 'Systems scheduled for or undergoing decommissioning'
            }
        ]
        
        for status in operational_statuses:
            try:
                tag = client.tags.create(
                    name=status['name'],
                    color=status['color'],
                    description=status['description']
                )
                
                classification_system['operational_status'][status['name']] = {
                    'tid': tag.get('tid'),
                    'color': status['color'],
                    'description': status['description']
                }
                
                print(f"   ✅ Created operational status tag: {status['name']} (ID: {tag.get('tid')})")
                
            except Exception as e:
                print(f"   ❌ Failed to create operational status tag {status['name']}: {e}")
        
        # Step 4: Create Compliance Tags
        print(f"\n4. CREATING COMPLIANCE TAGS...")
        
        compliance_tags = [
            {
                'name': 'pci_dss_scope',
                'color': 270,  # Purple
                'description': 'Systems within PCI DSS compliance scope'
            },
            {
                'name': 'hipaa_covered',
                'color': 200,  # Cyan
                'description': 'Systems handling HIPAA-covered health information'
            },
            {
                'name': 'gdpr_personal_data',
                'color': 150,  # Light green
                'description': 'Systems processing GDPR-covered personal data'
            },
            {
                'name': 'sox_financial',
                'color': 330,  # Pink
                'description': 'Systems involved in SOX financial reporting'
            },
            {
                'name': 'export_controlled',
                'color': 90,   # Yellow-green
                'description': 'Systems with export-controlled technology or data'
            }
        ]
        
        for compliance in compliance_tags:
            try:
                tag = client.tags.create(
                    name=compliance['name'],
                    color=compliance['color'],
                    description=compliance['description']
                )
                
                classification_system['compliance_tags'][compliance['name']] = {
                    'tid': tag.get('tid'),
                    'color': compliance['color'],
                    'description': compliance['description']
                }
                
                print(f"   ✅ Created compliance tag: {compliance['name']} (ID: {tag.get('tid')})")
                
            except Exception as e:
                print(f"   ❌ Failed to create compliance tag {compliance['name']}: {e}")
        
        # Step 5: Implementation Summary
        print(f"\n5. IMPLEMENTATION SUMMARY...")
        
        total_categories = len(classification_system['asset_categories'])
        total_risk_levels = len(classification_system['risk_levels'])
        total_operational = len(classification_system['operational_status'])
        total_compliance = len(classification_system['compliance_tags'])
        total_tags = total_categories + total_risk_levels + total_operational + total_compliance
        
        classification_system['implementation_results'] = {
            'asset_categories_created': total_categories,
            'risk_levels_created': total_risk_levels,
            'operational_statuses_created': total_operational,
            'compliance_tags_created': total_compliance,
            'total_tags_created': total_tags
        }
        
        print(f"   Asset Categories: {total_categories}")
        print(f"   Risk Levels: {total_risk_levels}")
        print(f"   Operational Statuses: {total_operational}")
        print(f"   Compliance Tags: {total_compliance}")
        print(f"   Total Tags Created: {total_tags}")
        
        # Step 6: Usage Guidelines
        print(f"\n6. USAGE GUIDELINES...")
        
        guidelines = [
            "• Assign exactly one category tag per device (servers, workstations, etc.)",
            "• Assign exactly one risk level tag per device (critical, high, standard, low)",
            "• Assign exactly one operational status tag per device (production, staging, etc.)",
            "• Assign relevant compliance tags as needed (multiple allowed per device)",
            "• Review and update tags regularly as asset profiles change",
            "• Use tag combinations for advanced security policy automation",
            "• Implement tag-based monitoring and alerting rules"
        ]
        
        for guideline in guidelines:
            print(f"   {guideline}")
        
        # Step 7: Example Device Classification
        print(f"\n7. EXAMPLE DEVICE CLASSIFICATION WORKFLOW...")
        
        example_classifications = [
            {
                'device_type': 'Production Web Server',
                'suggested_tags': ['servers', 'critical_assets', 'production', 'pci_dss_scope']
            },
            {
                'device_type': 'Developer Workstation',
                'suggested_tags': ['workstations', 'standard_assets', 'development']
            },
            {
                'device_type': 'Network Firewall',
                'suggested_tags': ['network_infrastructure', 'critical_assets', 'production']
            },
            {
                'device_type': 'IoT Sensor',
                'suggested_tags': ['iot_devices', 'low_risk_assets', 'production']
            }
        ]
        
        for example in example_classifications:
            print(f"   {example['device_type']}:")
            print(f"     Recommended tags: {', '.join(example['suggested_tags'])}")
        
        return classification_system
        
    except Exception as e:
        print(f"Error implementing asset classification system: {e}")
        return None

# Example usage
# classification_system = implement_asset_classification_system()
```

### Automated Tag Lifecycle Management

```python
def automated_tag_lifecycle_management():
    """Comprehensive tag lifecycle management with automated cleanup and optimization"""
    
    print(f"Automated Tag Lifecycle Management")
    print("=" * 50)
    
    try:
        # Get all current tags
        all_tags = client.tags.get()
        
        if not all_tags or 'tags' not in all_tags:
            print("No tags found in the system")
            return None
        
        tags_list = all_tags['tags']
        
        lifecycle_analysis = {
            'total_tags': len(tags_list),
            'tag_categories': {},
            'usage_analysis': {},
            'cleanup_recommendations': [],
            'optimization_suggestions': []
        }
        
        print(f"Analyzing {len(tags_list)} tags...")
        
        # Step 1: Categorize tags by naming patterns
        print(f"\n1. TAG CATEGORIZATION ANALYSIS...")
        
        tag_patterns = {
            'incident_tags': [],
            'asset_category_tags': [],
            'risk_level_tags': [],
            'operational_tags': [],
            'compliance_tags': [],
            'temporary_tags': [],
            'custom_tags': []
        }
        
        # Categorize tags based on naming patterns
        for tag in tags_list:
            tag_name = tag.get('name', '').lower()
            
            if tag_name.startswith('incident_'):
                tag_patterns['incident_tags'].append(tag)
            elif tag_name in ['servers', 'workstations', 'network_infrastructure', 'iot_devices', 'mobile_devices']:
                tag_patterns['asset_category_tags'].append(tag)
            elif 'critical' in tag_name or 'high_value' in tag_name or 'low_risk' in tag_name:
                tag_patterns['risk_level_tags'].append(tag)
            elif tag_name in ['production', 'staging', 'development', 'maintenance', 'decommissioned']:
                tag_patterns['operational_tags'].append(tag)
            elif any(compliance in tag_name for compliance in ['pci', 'hipaa', 'gdpr', 'sox']):
                tag_patterns['compliance_tags'].append(tag)
            elif 'temporary' in tag_name or 'quarantine' in tag_name or 'investigation' in tag_name:
                tag_patterns['temporary_tags'].append(tag)
            else:
                tag_patterns['custom_tags'].append(tag)
        
        lifecycle_analysis['tag_categories'] = {
            category: len(tags) for category, tags in tag_patterns.items()
        }
        
        for category, count in lifecycle_analysis['tag_categories'].items():
            category_name = category.replace('_', ' ').title()
            print(f"   {category_name}: {count} tags")
        
        # Step 2: Analyze tag usage and entity associations
        print(f"\n2. TAG USAGE ANALYSIS...")
        
        usage_stats = {
            'active_tags': 0,
            'unused_tags': 0,
            'high_usage_tags': [],
            'low_usage_tags': [],
            'orphaned_tags': []
        }
        
        for tag in tags_list:
            tag_id = tag.get('tid')
            tag_name = tag.get('name')
            
            try:
                # Check tag entity associations
                entities = client.tags.get_tag_entities(tid=tag_id)
                
                entity_count = 0
                if isinstance(entities, dict):
                    entity_count += len(entities.get('devices', []))
                    entity_count += len(entities.get('credentials', []))
                elif isinstance(entities, list):
                    entity_count = len(entities)
                
                tag_usage = {
                    'tag_id': tag_id,
                    'tag_name': tag_name,
                    'entity_count': entity_count,
                    'usage_level': 'high' if entity_count > 10 else 'medium' if entity_count > 0 else 'unused'
                }
                
                if entity_count > 10:
                    usage_stats['high_usage_tags'].append(tag_usage)
                elif entity_count == 0:
                    usage_stats['unused_tags'] += 1
                    usage_stats['orphaned_tags'].append(tag_usage)
                else:
                    usage_stats['low_usage_tags'].append(tag_usage)
                    usage_stats['active_tags'] += 1
                
            except Exception as e:
                print(f"   Warning: Could not analyze usage for tag {tag_name}: {e}")
                usage_stats['orphaned_tags'].append({
                    'tag_id': tag_id,
                    'tag_name': tag_name,
                    'entity_count': 0,
                    'usage_level': 'error',
                    'error': str(e)
                })
        
        lifecycle_analysis['usage_analysis'] = usage_stats
        
        print(f"   Active Tags: {usage_stats['active_tags']}")
        print(f"   Unused Tags: {usage_stats['unused_tags']}")
        print(f"   High Usage Tags: {len(usage_stats['high_usage_tags'])}")
        print(f"   Low Usage Tags: {len(usage_stats['low_usage_tags'])}")
        print(f"   Orphaned/Error Tags: {len(usage_stats['orphaned_tags'])}")
        
        # Step 3: Generate cleanup recommendations
        print(f"\n3. CLEANUP RECOMMENDATIONS...")
        
        cleanup_recommendations = []
        
        # Recommend cleanup of unused tags
        if usage_stats['unused_tags'] > 0:
            cleanup_recommendations.append({
                'type': 'unused_cleanup',
                'priority': 'medium',
                'description': f'{usage_stats["unused_tags"]} unused tags found',
                'action': 'Consider removing tags with no entity associations',
                'affected_tags': [tag['tag_name'] for tag in usage_stats['orphaned_tags'] if tag.get('entity_count', 0) == 0]
            })
        
        # Recommend incident tag cleanup
        old_incident_tags = []
        for tag in tag_patterns['incident_tags']:
            tag_name = tag.get('name', '')
            # Look for incident tags that might be old (simple heuristic)
            if 'incident_' in tag_name:
                old_incident_tags.append(tag_name)
        
        if old_incident_tags:
            cleanup_recommendations.append({
                'type': 'incident_cleanup',
                'priority': 'low',
                'description': f'{len(old_incident_tags)} incident tags found',
                'action': 'Review incident tags and remove those from resolved incidents',
                'affected_tags': old_incident_tags[:10]  # Show first 10
            })
        
        # Recommend temporary tag review
        if tag_patterns['temporary_tags']:
            temp_tag_names = [tag.get('name') for tag in tag_patterns['temporary_tags']]
            cleanup_recommendations.append({
                'type': 'temporary_review',
                'priority': 'high',
                'description': f'{len(temp_tag_names)} temporary tags found',
                'action': 'Review temporary tags for expiration and cleanup',
                'affected_tags': temp_tag_names
            })
        
        lifecycle_analysis['cleanup_recommendations'] = cleanup_recommendations
        
        for i, rec in enumerate(cleanup_recommendations, 1):
            priority_icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            print(f"   {i}. {priority_icon} {rec['description']}")
            print(f"      Action: {rec['action']}")
            if rec['affected_tags']:
                sample_tags = rec['affected_tags'][:3]
                more_count = len(rec['affected_tags']) - 3
                tags_display = ', '.join(sample_tags)
                if more_count > 0:
                    tags_display += f" (and {more_count} more)"
                print(f"      Examples: {tags_display}")
        
        # Step 4: Generate optimization suggestions
        print(f"\n4. OPTIMIZATION SUGGESTIONS...")
        
        optimization_suggestions = []
        
        # Suggest tag standardization
        if len(tag_patterns['custom_tags']) > len(tag_patterns['asset_category_tags']):
            optimization_suggestions.append({
                'type': 'standardization',
                'description': 'High number of custom tags compared to standard categories',
                'suggestion': 'Consider implementing standardized tag naming conventions'
            })
        
        # Suggest consolidation for high usage tags
        high_usage_count = len(usage_stats['high_usage_tags'])
        if high_usage_count > 10:
            optimization_suggestions.append({
                'type': 'consolidation',
                'description': f'{high_usage_count} tags have high usage (>10 entities)',
                'suggestion': 'Review high-usage tags for potential consolidation opportunities'
            })
        
        # Suggest automation opportunities
        if tag_patterns['incident_tags'] or tag_patterns['temporary_tags']:
            optimization_suggestions.append({
                'type': 'automation',
                'description': 'Manual incident and temporary tag management detected',
                'suggestion': 'Implement automated tag lifecycle management for incidents and temporary tags'
            })
        
        # Suggest missing categories
        expected_categories = ['servers', 'workstations', 'network_infrastructure']
        missing_categories = [cat for cat in expected_categories 
                            if not any(tag.get('name') == cat for tag in tag_patterns['asset_category_tags'])]
        
        if missing_categories:
            optimization_suggestions.append({
                'type': 'missing_categories',
                'description': f'Missing standard asset categories: {", ".join(missing_categories)}',
                'suggestion': 'Consider creating missing standard asset category tags'
            })
        
        lifecycle_analysis['optimization_suggestions'] = optimization_suggestions
        
        for i, suggestion in enumerate(optimization_suggestions, 1):
            print(f"   {i}. {suggestion['description']}")
            print(f"      Suggestion: {suggestion['suggestion']}")
        
        # Step 5: Tag health score calculation
        print(f"\n5. TAG SYSTEM HEALTH SCORE...")
        
        # Calculate health score based on various factors
        health_factors = {
            'standardization': min(100, (len(tag_patterns['asset_category_tags']) + 
                                       len(tag_patterns['risk_level_tags']) + 
                                       len(tag_patterns['operational_tags'])) / len(tags_list) * 100),
            'usage_efficiency': (usage_stats['active_tags'] + len(usage_stats['high_usage_tags'])) / len(tags_list) * 100,
            'cleanup_needed': max(0, 100 - (usage_stats['unused_tags'] / len(tags_list) * 100)),
            'organization': min(100, len(lifecycle_analysis['tag_categories']) * 15)
        }
        
        overall_health = sum(health_factors.values()) / len(health_factors)
        
        print(f"   Standardization Score: {health_factors['standardization']:.1f}/100")
        print(f"   Usage Efficiency Score: {health_factors['usage_efficiency']:.1f}/100")
        print(f"   Cleanup Score: {health_factors['cleanup_needed']:.1f}/100")
        print(f"   Organization Score: {health_factors['organization']:.1f}/100")
        print(f"   Overall Health Score: {overall_health:.1f}/100")
        
        health_rating = "Excellent" if overall_health >= 90 else "Good" if overall_health >= 75 else "Fair" if overall_health >= 60 else "Poor"
        print(f"   Health Rating: {health_rating}")
        
        lifecycle_analysis['health_score'] = {
            'factors': health_factors,
            'overall_score': overall_health,
            'rating': health_rating
        }
        
        # Step 6: Automated cleanup execution (with user confirmation)
        print(f"\n6. AUTOMATED CLEANUP OPTIONS...")
        
        print(f"   The following automated cleanup actions are available:")
        print(f"   • Remove unused tags (0 entity associations)")
        print(f"   • Archive old incident tags (create backup before deletion)")
        print(f"   • Standardize tag naming conventions")
        print(f"   • Consolidate duplicate or similar tags")
        print(f"   Note: Automated cleanup requires manual confirmation for safety")
        
        return lifecycle_analysis
        
    except Exception as e:
        print(f"Error in tag lifecycle management: {e}")
        return None

# Example usage
# lifecycle_results = automated_tag_lifecycle_management()
```

## Error Handling

```python
try:
    # Get all tags
    all_tags = client.tags.get()
    print("Tags retrieved successfully")
    
    # Create new tag
    new_tag = client.tags.create(
        name="test_tag",
        color=120,
        description="Test tag for documentation"
    )
    print("Tag created successfully")
    
    # Tag a device
    client.tags.post_entities(
        did=123,
        tag="test_tag",
        duration=3600
    )
    print("Device tagged successfully")
    
    # Get device tags
    device_tags = client.tags.get_entities(did=123)
    print("Device tags retrieved successfully")
    
    # Remove tag from device
    success = client.tags.delete_entities(did=123, tag="test_tag")
    if success:
        print("Tag removed from device successfully")
    
    # Delete tag
    success = client.tags.delete(tag_id=str(new_tag.get('tid')))
    if success:
        print("Tag deleted successfully")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        if e.response.status_code == 400:
            print("Bad request - check parameters (tag name, device ID, duration)")
        elif e.response.status_code == 401:
            print("Authentication failed - check tokens")
        elif e.response.status_code == 403:
            print("Access denied - check API permissions for tag operations")
        elif e.response.status_code == 404:
            print("Tag or device not found - check IDs")
        elif e.response.status_code == 409:
            print("Conflict - tag name may already exist or device already tagged")
        elif e.response.status_code == 422:
            print("Invalid parameters - check tag name format, color range (0-360), device ID")
        elif e.response.status_code == 429:
            print("Rate limit exceeded - too many tag operations")
        else:
            print(f"Response: {e.response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
    print("Check network connectivity and host URL")

except requests.exceptions.Timeout as e:
    print(f"Request timeout: {e}")
    print("Tag operations should be fast - check network conditions")

except ValueError as e:
    print(f"Value error: {e}")
    print("Check parameter types - IDs (int/str), duration (int), color (int 0-360)")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

### Tag Management
- **Tag Creation**: Create tags with names, colors (HSL hue 0-360), and descriptions
- **Tag Organization**: Use consistent naming conventions for better organization
- **Tag Lifecycle**: Manage tag creation, assignment, and cleanup processes
- **Tag Categories**: Organize tags by purpose (asset types, risk levels, status, compliance)

### Entity Association
- **Device Tagging**: Associate tags with devices using device IDs
- **Credential Tagging**: Associate tags with credentials and user accounts
- **Bulk Operations**: Tag multiple entities simultaneously with single operations
- **Temporary Tags**: Set expiration durations for temporary tag assignments

### Tag Colors and Visualization
- **Color Coding**: Use HSL hue values (0-360) for visual organization in the UI
- **Consistent Schemes**: Implement consistent color schemes for tag categories
- **Visual Hierarchy**: Use colors to indicate priority, risk level, or category
- **UI Integration**: Tags appear in the Darktrace UI with assigned colors

### Duration and Expiration
- **Permanent Tags**: Tags without duration remain until manually removed
- **Temporary Tags**: Tags with duration expire automatically after specified time
- **Incident Response**: Use temporary tags for incident response workflows
- **Maintenance Windows**: Tag devices during maintenance with automatic expiration

### Automation and Integration
- **Incident Response**: Automate tagging during security incident workflows
- **Asset Management**: Integrate with asset management systems for automatic classification
- **Compliance**: Use tags to track compliance requirements and scope
- **Monitoring**: Create monitoring rules based on tag assignments

### Best Practices
- **Naming Conventions**: Use consistent, descriptive tag names with clear purposes
- **Tag Hierarchy**: Implement hierarchical tagging strategies for complex environments
- **Regular Cleanup**: Periodically review and clean up unused or outdated tags
- **Documentation**: Maintain documentation of tag meanings and usage guidelines

### Performance Considerations
- **Bulk Operations**: Use bulk tagging operations for large numbers of entities
- **Tag Limits**: Be aware of practical limits on number of tags per entity
- **Query Optimization**: Structure tag queries efficiently for large deployments
- **Cache Efficiency**: Consider tag query patterns for optimal performance

### Security and Access Control
- **Tag Permissions**: Ensure appropriate access controls for tag management operations
- **Audit Trails**: Track tag creation, modification, and deletion for security audit purposes
- **Sensitive Data**: Avoid including sensitive information in tag names or descriptions
- **Compliance Tags**: Use tags to track compliance scope and requirements

### Use Cases
- **Asset Classification**: Categorize devices by type, risk level, and operational status
- **Incident Response**: Track devices involved in security incidents and investigations
- **Compliance Management**: Mark devices subject to regulatory compliance requirements
- **Maintenance Tracking**: Tag devices during maintenance windows and system updates
- **Risk Management**: Identify and track high-risk or critical assets
- **Network Segmentation**: Support network segmentation strategies with device categorization
- **Automated Response**: Enable automated response actions based on device tags
