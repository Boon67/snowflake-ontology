# 📡 API Reference - Snowflake Ontology & Workflow Engine

Complete API documentation for the Snowflake Ontology & Workflow Engine.

---

## Base URL

```
Production: https://your-endpoint.snowflakecomputing.app
Local Dev:  http://localhost:8000
```

## Interactive Documentation

Visit `/docs` for interactive Swagger UI documentation:
```
https://your-endpoint.snowflakecomputing.app/docs
```

---

## Table of Contents

1. [Authentication](#authentication)
2. [Response Format](#response-format)
3. [Error Handling](#error-handling)
4. [Entity Endpoints](#entity-endpoints)
5. [Relationship Endpoints](#relationship-endpoints)
6. [Graph Endpoints](#graph-endpoints)
7. [Workflow Endpoints](#workflow-endpoints)
8. [State Management Endpoints](#state-management-endpoints)
9. [System Endpoints](#system-endpoints)
10. [Code Examples](#code-examples)

---

## Authentication

Currently uses Snowflake OAuth. Future versions will support API keys and JWT tokens.

**Headers:**
```
Content-Type: application/json
```

---

## Response Format

### Success Response

```json
{
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "entity_type": "CUSTOMER",
  "label": "Acme Corporation",
  "properties": {
    "industry": "Technology"
  },
  "tags": ["enterprise"],
  "created_at": "2026-01-30T10:00:00",
  "updated_at": "2026-01-30T10:00:00"
}
```

### Error Response

```json
{
  "detail": "Entity not found"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 204 | No Content | Deletion successful |
| 400 | Bad Request | Invalid input |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "detail": "Validation error message",
  "errors": [
    {
      "loc": ["body", "entity_type"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Entity Endpoints

### Create Entity

Create a new entity in the ontology.

**Endpoint:** `POST /entities`

**Request Body:**
```json
{
  "entity_type": "CUSTOMER",
  "label": "Acme Corporation",
  "properties": {
    "industry": "Technology",
    "size": "Enterprise",
    "revenue": 50000000,
    "employees": 5000,
    "country": "US"
  },
  "tags": ["enterprise", "technology", "active"]
}
```

**Response:** `201 Created`
```json
{
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "entity_type": "CUSTOMER",
  "label": "Acme Corporation",
  "properties": {
    "industry": "Technology",
    "size": "Enterprise",
    "revenue": 50000000,
    "employees": 5000,
    "country": "US"
  },
  "tags": ["enterprise", "technology", "active"],
  "created_at": "2026-01-30T10:00:00",
  "updated_at": "2026-01-30T10:00:00"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/entities" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "CUSTOMER",
    "label": "Acme Corporation",
    "properties": {"industry": "Technology"},
    "tags": ["enterprise"]
  }'
```

---

### List Entities

Get all entities with optional filtering.

**Endpoint:** `GET /entities`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| entity_type | string | No | Filter by entity type |
| tags | string | No | Filter by tags (comma-separated) |
| limit | integer | No | Maximum results (default: 100) |
| offset | integer | No | Pagination offset (default: 0) |

**Response:** `200 OK`
```json
[
  {
    "entity_id": "550e8400-e29b-41d4-a716-446655440000",
    "entity_type": "CUSTOMER",
    "label": "Acme Corporation",
    "properties": {"industry": "Technology"},
    "tags": ["enterprise"],
    "created_at": "2026-01-30T10:00:00",
    "updated_at": "2026-01-30T10:00:00"
  }
]
```

**cURL Examples:**
```bash
# Get all entities
curl "http://localhost:8000/entities"

# Filter by type
curl "http://localhost:8000/entities?entity_type=CUSTOMER"

# Filter by tags
curl "http://localhost:8000/entities?tags=enterprise,active"

# Pagination
curl "http://localhost:8000/entities?limit=50&offset=100"
```

---

### Get Entity

Get a specific entity by ID.

**Endpoint:** `GET /entities/{entity_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| entity_id | string | Yes | Entity UUID |

**Response:** `200 OK`
```json
{
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "entity_type": "CUSTOMER",
  "label": "Acme Corporation",
  "properties": {"industry": "Technology"},
  "tags": ["enterprise"],
  "created_at": "2026-01-30T10:00:00",
  "updated_at": "2026-01-30T10:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Entity not found"
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/entities/550e8400-e29b-41d4-a716-446655440000"
```

---

### Update Entity

Update an existing entity.

**Endpoint:** `PUT /entities/{entity_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| entity_id | string | Yes | Entity UUID |

**Request Body:**
```json
{
  "label": "Acme Corp (Updated)",
  "properties": {
    "industry": "Technology",
    "size": "Large Enterprise",
    "revenue": 75000000
  },
  "tags": ["enterprise", "technology", "platinum"]
}
```

**Response:** `200 OK`
```json
{
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "entity_type": "CUSTOMER",
  "label": "Acme Corp (Updated)",
  "properties": {
    "industry": "Technology",
    "size": "Large Enterprise",
    "revenue": 75000000
  },
  "tags": ["enterprise", "technology", "platinum"],
  "created_at": "2026-01-30T10:00:00",
  "updated_at": "2026-01-30T11:00:00"
}
```

**cURL Example:**
```bash
curl -X PUT "http://localhost:8000/entities/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "label": "Acme Corp (Updated)",
    "properties": {"industry": "Technology", "size": "Large Enterprise"},
    "tags": ["enterprise", "platinum"]
  }'
```

---

### Delete Entity

Delete an entity and its relationships.

**Endpoint:** `DELETE /entities/{entity_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| entity_id | string | Yes | Entity UUID |

**Response:** `204 No Content`

**Error Response:** `404 Not Found`
```json
{
  "detail": "Entity not found"
}
```

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/entities/550e8400-e29b-41d4-a716-446655440000"
```

---

## Relationship Endpoints

### Create Relationship

Create a relationship between two entities.

**Endpoint:** `POST /relationships`

**Request Body:**
```json
{
  "subject_id": "550e8400-e29b-41d4-a716-446655440000",
  "predicate": "OWNS",
  "object_id": "660e8400-e29b-41d4-a716-446655440001",
  "properties": {
    "since": "2024-01-15",
    "type": "primary",
    "strength": 0.95
  }
}
```

**Response:** `201 Created`
```json
{
  "relationship_id": "770e8400-e29b-41d4-a716-446655440002",
  "subject_id": "550e8400-e29b-41d4-a716-446655440000",
  "predicate": "OWNS",
  "object_id": "660e8400-e29b-41d4-a716-446655440001",
  "properties": {
    "since": "2024-01-15",
    "type": "primary",
    "strength": 0.95
  },
  "created_at": "2026-01-30T10:00:00"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/relationships" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id": "550e8400-e29b-41d4-a716-446655440000",
    "predicate": "OWNS",
    "object_id": "660e8400-e29b-41d4-a716-446655440001",
    "properties": {"since": "2024-01-15"}
  }'
```

---

### List Relationships

Get all relationships with optional filtering.

**Endpoint:** `GET /relationships`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| entity_id | string | No | Filter by subject or object entity |
| predicate | string | No | Filter by relationship type |
| subject_id | string | No | Filter by subject entity |
| object_id | string | No | Filter by object entity |
| limit | integer | No | Maximum results (default: 100) |
| offset | integer | No | Pagination offset (default: 0) |

**Response:** `200 OK`
```json
[
  {
    "relationship_id": "770e8400-e29b-41d4-a716-446655440002",
    "subject_id": "550e8400-e29b-41d4-a716-446655440000",
    "predicate": "OWNS",
    "object_id": "660e8400-e29b-41d4-a716-446655440001",
    "properties": {"since": "2024-01-15"},
    "created_at": "2026-01-30T10:00:00"
  }
]
```

**cURL Examples:**
```bash
# Get all relationships
curl "http://localhost:8000/relationships"

# Filter by entity (subject or object)
curl "http://localhost:8000/relationships?entity_id=550e8400-e29b-41d4-a716-446655440000"

# Filter by predicate
curl "http://localhost:8000/relationships?predicate=OWNS"

# Filter by subject
curl "http://localhost:8000/relationships?subject_id=550e8400-e29b-41d4-a716-446655440000"
```

---

### Delete Relationship

Delete a specific relationship.

**Endpoint:** `DELETE /relationships/{relationship_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| relationship_id | string | Yes | Relationship UUID |

**Response:** `204 No Content`

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/relationships/770e8400-e29b-41d4-a716-446655440002"
```

---

## Graph Endpoints

### Query Graph

Perform graph traversal starting from an entity.

**Endpoint:** `POST /graph/query`

**Request Body:**
```json
{
  "start_entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "max_depth": 3,
  "direction": "both",
  "relationship_types": ["OWNS", "HAS", "CONTAINS"],
  "entity_types": ["CUSTOMER", "ACCOUNT", "ORDER"]
}
```

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| start_entity_id | string | Yes | - | Starting entity UUID |
| max_depth | integer | No | 3 | Maximum traversal depth |
| direction | string | No | "both" | "outgoing", "incoming", or "both" |
| relationship_types | array | No | null | Filter by relationship types |
| entity_types | array | No | null | Filter by entity types |

**Response:** `200 OK`
```json
{
  "nodes": [
    {
      "entity_id": "550e8400-e29b-41d4-a716-446655440000",
      "entity_type": "CUSTOMER",
      "label": "Acme Corporation",
      "properties": {"industry": "Technology"},
      "tags": ["enterprise"],
      "depth": 0
    },
    {
      "entity_id": "660e8400-e29b-41d4-a716-446655440001",
      "entity_type": "ACCOUNT",
      "label": "Acme Account",
      "properties": {"status": "Active"},
      "tags": ["active"],
      "depth": 1
    }
  ],
  "edges": [
    {
      "relationship_id": "770e8400-e29b-41d4-a716-446655440002",
      "subject_id": "550e8400-e29b-41d4-a716-446655440000",
      "predicate": "OWNS",
      "object_id": "660e8400-e29b-41d4-a716-446655440001",
      "properties": {"since": "2024-01-15"}
    }
  ],
  "stats": {
    "total_nodes": 2,
    "total_edges": 1,
    "max_depth_reached": 1
  }
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/graph/query" \
  -H "Content-Type: application/json" \
  -d '{
    "start_entity_id": "550e8400-e29b-41d4-a716-446655440000",
    "max_depth": 3,
    "direction": "both"
  }'
```

---

### Get Graph Statistics

Get statistics about the entire graph.

**Endpoint:** `GET /graph/stats`

**Response:** `200 OK`
```json
{
  "total_entities": 1250,
  "total_relationships": 3420,
  "entities_by_type": {
    "CUSTOMER": 150,
    "ACCOUNT": 300,
    "PRODUCT": 500,
    "ORDER": 300
  },
  "relationships_by_predicate": {
    "OWNS": 450,
    "HAS": 620,
    "CONTAINS": 890,
    "PURCHASED": 780,
    "RELATED_TO": 680
  },
  "avg_relationships_per_entity": 2.74,
  "max_relationships_per_entity": 45,
  "isolated_entities": 12
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/graph/stats"
```

---

## Workflow Endpoints

### Create Workflow

Create a new workflow definition.

**Endpoint:** `POST /workflows`

**Request Body:**
```json
{
  "name": "Customer At-Risk Alert",
  "description": "Send alert when customer becomes at-risk",
  "trigger_condition": "entity_type=CUSTOMER AND current_state=AT_RISK",
  "action_type": "EMAIL",
  "action_config": {
    "to": "support@company.com",
    "subject": "Customer At-Risk: {{entity_label}}",
    "body": "Customer {{entity_label}} ({{entity_id}}) needs attention. Health score: {{properties.health_score}}",
    "priority": "high"
  },
  "enabled": true
}
```

**Response:** `201 Created`
```json
{
  "workflow_id": "880e8400-e29b-41d4-a716-446655440003",
  "name": "Customer At-Risk Alert",
  "description": "Send alert when customer becomes at-risk",
  "trigger_condition": "entity_type=CUSTOMER AND current_state=AT_RISK",
  "action_type": "EMAIL",
  "action_config": {
    "to": "support@company.com",
    "subject": "Customer At-Risk: {{entity_label}}",
    "body": "Customer {{entity_label}} ({{entity_id}}) needs attention.",
    "priority": "high"
  },
  "enabled": true,
  "created_at": "2026-01-30T10:00:00"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/workflows" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer At-Risk Alert",
    "description": "Send alert when customer becomes at-risk",
    "trigger_condition": "entity_type=CUSTOMER AND current_state=AT_RISK",
    "action_type": "EMAIL",
    "action_config": {
      "to": "support@company.com",
      "subject": "Customer At-Risk",
      "body": "Customer needs attention"
    },
    "enabled": true
  }'
```

---

### List Workflows

Get all workflow definitions.

**Endpoint:** `GET /workflows`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| enabled | boolean | No | Filter by enabled status |
| action_type | string | No | Filter by action type |

**Response:** `200 OK`
```json
[
  {
    "workflow_id": "880e8400-e29b-41d4-a716-446655440003",
    "name": "Customer At-Risk Alert",
    "description": "Send alert when customer becomes at-risk",
    "trigger_condition": "entity_type=CUSTOMER AND current_state=AT_RISK",
    "action_type": "EMAIL",
    "action_config": {"to": "support@company.com"},
    "enabled": true,
    "created_at": "2026-01-30T10:00:00"
  }
]
```

**cURL Examples:**
```bash
# Get all workflows
curl "http://localhost:8000/workflows"

# Filter by enabled
curl "http://localhost:8000/workflows?enabled=true"

# Filter by action type
curl "http://localhost:8000/workflows?action_type=EMAIL"
```

---

### Get Workflow

Get a specific workflow by ID.

**Endpoint:** `GET /workflows/{workflow_id}`

**Response:** `200 OK`
```json
{
  "workflow_id": "880e8400-e29b-41d4-a716-446655440003",
  "name": "Customer At-Risk Alert",
  "description": "Send alert when customer becomes at-risk",
  "trigger_condition": "entity_type=CUSTOMER AND current_state=AT_RISK",
  "action_type": "EMAIL",
  "action_config": {"to": "support@company.com"},
  "enabled": true,
  "created_at": "2026-01-30T10:00:00"
}
```

---

### Update Workflow

Update an existing workflow.

**Endpoint:** `PUT /workflows/{workflow_id}`

**Request Body:**
```json
{
  "name": "Customer At-Risk Alert (Updated)",
  "description": "Updated description",
  "trigger_condition": "entity_type=CUSTOMER AND current_state=AT_RISK AND previous_state!=AT_RISK",
  "action_type": "EMAIL",
  "action_config": {
    "to": "support@company.com",
    "subject": "Updated subject"
  },
  "enabled": true
}
```

**Response:** `200 OK`

---

### Delete Workflow

Delete a workflow definition.

**Endpoint:** `DELETE /workflows/{workflow_id}`

**Response:** `204 No Content`

---

### Execute Workflow

Manually execute a workflow for a specific entity.

**Endpoint:** `POST /workflows/{workflow_id}/execute`

**Request Body:**
```json
{
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "input_data": {
    "reason": "manual_trigger",
    "triggered_by": "admin"
  }
}
```

**Response:** `200 OK`
```json
{
  "execution_id": "990e8400-e29b-41d4-a716-446655440004",
  "workflow_id": "880e8400-e29b-41d4-a716-446655440003",
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "PENDING",
  "input_data": {"reason": "manual_trigger"},
  "started_at": "2026-01-30T10:00:00"
}
```

---

### List Workflow Executions

Get workflow execution history.

**Endpoint:** `GET /workflows/executions`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workflow_id | string | No | Filter by workflow |
| entity_id | string | No | Filter by entity |
| status | string | No | Filter by status |
| limit | integer | No | Maximum results (default: 100) |
| offset | integer | No | Pagination offset (default: 0) |

**Response:** `200 OK`
```json
[
  {
    "execution_id": "990e8400-e29b-41d4-a716-446655440004",
    "workflow_id": "880e8400-e29b-41d4-a716-446655440003",
    "entity_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "COMPLETED",
    "input_data": {"reason": "state_change"},
    "output_data": {"email_sent": true},
    "error_message": null,
    "started_at": "2026-01-30T10:00:00",
    "completed_at": "2026-01-30T10:00:05"
  }
]
```

---

## State Management Endpoints

### Get Entity State

Get the current state of an entity.

**Endpoint:** `GET /entities/{entity_id}/state`

**Response:** `200 OK`
```json
{
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "current_state": "ACTIVE",
  "previous_state": null,
  "state_data": {
    "health_score": 85,
    "last_contact": "2026-01-15"
  },
  "updated_at": "2026-01-30T10:00:00"
}
```

---

### Update Entity State

Update the state of an entity (triggers workflows).

**Endpoint:** `PUT /entities/{entity_id}/state`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| new_state | string | Yes | New state value |

**Request Body:**
```json
{
  "health_score": 45,
  "last_contact": "2026-01-30",
  "reason": "Low engagement"
}
```

**Response:** `200 OK`
```json
{
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "current_state": "AT_RISK",
  "previous_state": "ACTIVE",
  "state_data": {
    "health_score": 45,
    "last_contact": "2026-01-30",
    "reason": "Low engagement"
  },
  "updated_at": "2026-01-30T11:00:00"
}
```

**cURL Example:**
```bash
curl -X PUT "http://localhost:8000/entities/550e8400-e29b-41d4-a716-446655440000/state?new_state=AT_RISK" \
  -H "Content-Type: application/json" \
  -d '{
    "health_score": 45,
    "reason": "Low engagement"
  }'
```

---

## System Endpoints

### Health Check

Check API health status.

**Endpoint:** `GET /health`

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2026-01-30T10:00:00",
  "version": "1.0.0"
}
```

---

### Root Endpoint

Get API information.

**Endpoint:** `GET /`

**Response:** `200 OK`
```json
{
  "name": "Snowflake Ontology & Workflow Engine API",
  "version": "1.0.0",
  "description": "REST API for ontology and workflow management",
  "docs_url": "/docs",
  "health_url": "/health"
}
```

---

## Code Examples

### Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Create entity
entity_data = {
    "entity_type": "CUSTOMER",
    "label": "Acme Corporation",
    "properties": {
        "industry": "Technology",
        "size": "Enterprise"
    },
    "tags": ["enterprise", "technology"]
}

response = requests.post(f"{BASE_URL}/entities", json=entity_data)
entity = response.json()
print(f"Created entity: {entity['entity_id']}")

# Create relationship
relationship_data = {
    "subject_id": entity['entity_id'],
    "predicate": "OWNS",
    "object_id": "another-entity-id",
    "properties": {"since": "2024-01-15"}
}

response = requests.post(f"{BASE_URL}/relationships", json=relationship_data)
relationship = response.json()
print(f"Created relationship: {relationship['relationship_id']}")

# Query graph
query_data = {
    "start_entity_id": entity['entity_id'],
    "max_depth": 3,
    "direction": "both"
}

response = requests.post(f"{BASE_URL}/graph/query", json=query_data)
graph = response.json()
print(f"Found {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")

# Create workflow
workflow_data = {
    "name": "Customer At-Risk Alert",
    "trigger_condition": "entity_type=CUSTOMER AND current_state=AT_RISK",
    "action_type": "NOTIFICATION",
    "action_config": {"message": "Customer at risk!"},
    "enabled": True
}

response = requests.post(f"{BASE_URL}/workflows", json=workflow_data)
workflow = response.json()
print(f"Created workflow: {workflow['workflow_id']}")

# Update entity state (triggers workflow)
state_data = {"health_score": 45}
response = requests.put(
    f"{BASE_URL}/entities/{entity['entity_id']}/state?new_state=AT_RISK",
    json=state_data
)
print("State updated, workflow triggered")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function main() {
  // Create entity
  const entityData = {
    entity_type: 'CUSTOMER',
    label: 'Acme Corporation',
    properties: {
      industry: 'Technology',
      size: 'Enterprise'
    },
    tags: ['enterprise', 'technology']
  };

  const entityResponse = await axios.post(`${BASE_URL}/entities`, entityData);
  const entity = entityResponse.data;
  console.log(`Created entity: ${entity.entity_id}`);

  // Create relationship
  const relationshipData = {
    subject_id: entity.entity_id,
    predicate: 'OWNS',
    object_id: 'another-entity-id',
    properties: { since: '2024-01-15' }
  };

  const relResponse = await axios.post(`${BASE_URL}/relationships`, relationshipData);
  console.log(`Created relationship: ${relResponse.data.relationship_id}`);

  // Query graph
  const queryData = {
    start_entity_id: entity.entity_id,
    max_depth: 3,
    direction: 'both'
  };

  const graphResponse = await axios.post(`${BASE_URL}/graph/query`, queryData);
  const graph = graphResponse.data;
  console.log(`Found ${graph.nodes.length} nodes and ${graph.edges.length} edges`);

  // Create workflow
  const workflowData = {
    name: 'Customer At-Risk Alert',
    trigger_condition: 'entity_type=CUSTOMER AND current_state=AT_RISK',
    action_type: 'NOTIFICATION',
    action_config: { message: 'Customer at risk!' },
    enabled: true
  };

  const workflowResponse = await axios.post(`${BASE_URL}/workflows`, workflowData);
  console.log(`Created workflow: ${workflowResponse.data.workflow_id}`);
}

main().catch(console.error);
```

### cURL

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

# Create entity
ENTITY_RESPONSE=$(curl -s -X POST "$BASE_URL/entities" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "CUSTOMER",
    "label": "Acme Corporation",
    "properties": {"industry": "Technology"},
    "tags": ["enterprise"]
  }')

ENTITY_ID=$(echo $ENTITY_RESPONSE | jq -r '.entity_id')
echo "Created entity: $ENTITY_ID"

# Create relationship
curl -s -X POST "$BASE_URL/relationships" \
  -H "Content-Type: application/json" \
  -d "{
    \"subject_id\": \"$ENTITY_ID\",
    \"predicate\": \"OWNS\",
    \"object_id\": \"another-entity-id\",
    \"properties\": {\"since\": \"2024-01-15\"}
  }"

# Query graph
curl -s -X POST "$BASE_URL/graph/query" \
  -H "Content-Type: application/json" \
  -d "{
    \"start_entity_id\": \"$ENTITY_ID\",
    \"max_depth\": 3,
    \"direction\": \"both\"
  }" | jq '.'

# Create workflow
curl -s -X POST "$BASE_URL/workflows" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer At-Risk Alert",
    "trigger_condition": "entity_type=CUSTOMER AND current_state=AT_RISK",
    "action_type": "NOTIFICATION",
    "action_config": {"message": "Customer at risk!"},
    "enabled": true
  }'

# Update entity state
curl -s -X PUT "$BASE_URL/entities/$ENTITY_ID/state?new_state=AT_RISK" \
  -H "Content-Type: application/json" \
  -d '{"health_score": 45}'
```

---

## Rate Limiting

Currently no rate limiting is implemented. Future versions will include:
- Per-user rate limits
- Per-endpoint limits
- Burst allowances

---

## Pagination

For list endpoints, use `limit` and `offset` parameters:

```bash
# Page 1 (first 50 results)
curl "http://localhost:8000/entities?limit=50&offset=0"

# Page 2 (next 50 results)
curl "http://localhost:8000/entities?limit=50&offset=50"

# Page 3 (next 50 results)
curl "http://localhost:8000/entities?limit=50&offset=100"
```

---

## Versioning

API version is included in responses but not in URL. Future versions may use:
- URL versioning: `/v1/entities`, `/v2/entities`
- Header versioning: `Accept: application/vnd.ontology.v1+json`

---

## Support

- **Interactive Docs:** Visit `/docs` endpoint
- **GitHub:** https://github.com/Boon67/snowflake-ontology
- **Issues:** Report bugs on GitHub

---

**Version:** 1.0.0  
**Last Updated:** January 30, 2026  
**Built with ❄️ on Snowflake SPCS**
