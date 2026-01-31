# 📖 Snowflake Ontology & Workflow Engine - User Guide

Complete guide to using the Snowflake Ontology & Workflow Engine.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Core Concepts](#core-concepts)
4. [User Interface Guide](#user-interface-guide)
5. [Working with Entities](#working-with-entities)
6. [Working with Relationships](#working-with-relationships)
7. [Graph Visualization](#graph-visualization)
8. [Workflow Engine](#workflow-engine)
9. [API Usage](#api-usage)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#faq)

---

## Introduction

### What is the Snowflake Ontology & Workflow Engine?

The Snowflake Ontology & Workflow Engine is a sophisticated knowledge management and automation platform built natively on Snowflake. It enables you to:

- **Model complex relationships** between business entities
- **Visualize knowledge graphs** with interactive DAG diagrams
- **Automate workflows** based on entity state changes
- **Track entity lifecycles** with state management
- **Build semantic layers** on top of your data warehouse

### Key Features

✅ **Entity Management** - Create and manage entities with flexible properties  
✅ **Relationship Modeling** - Build knowledge graphs with RDF-style triples  
✅ **Graph Visualization** - Interactive DAG view with hierarchical layout  
✅ **Workflow Automation** - 21 action types for automation  
✅ **State Management** - Track entity states and transitions  
✅ **Real-time Updates** - Live dashboard with statistics  
✅ **Search & Filter** - Tree view with instant search  

### Who Should Use This?

- **Data Engineers** - Building data lineage and metadata management
- **Business Analysts** - Creating customer 360 views
- **Data Scientists** - Modeling entity relationships for ML
- **Solution Architects** - Designing knowledge graphs
- **Operations Teams** - Automating data workflows

---

## Getting Started

### Prerequisites

Before using the application, ensure you have:

- ✅ Snowflake account with appropriate permissions
- ✅ Access to the deployed application URL
- ✅ Basic understanding of entities and relationships
- ✅ (Optional) API access for programmatic usage

### First Login

1. **Access the Application**
   - Open your browser
   - Navigate to the application URL provided by your administrator
   - Example: `https://your-endpoint.snowflakecomputing.app`

2. **Verify Connection**
   - The application should load the Dashboard
   - You should see statistics (may be zero initially)
   - If you see errors, contact your administrator

3. **Explore the Interface**
   - Dashboard - Overview and statistics
   - Entities - Manage entities
   - Relationships - Manage relationships
   - Graph View - Visualize connections
   - Workflows - Configure automation

---

## Core Concepts

### 1. Entities

**What are Entities?**

Entities are the fundamental building blocks of your knowledge graph. They represent real-world objects, concepts, or records.

**Entity Properties:**
- **Entity ID** - Unique identifier (auto-generated)
- **Entity Type** - Category (e.g., CUSTOMER, PRODUCT, ORDER)
- **Label** - Human-readable name
- **Properties** - Flexible JSON attributes
- **Tags** - Classification labels
- **Timestamps** - Created and updated dates

**Common Entity Types:**
```
CUSTOMER        - Business customers or individuals
ACCOUNT         - Customer accounts
PRODUCT         - Products or services
ORDER           - Purchase orders
CAMPAIGN        - Marketing campaigns
CONTACT         - Contact persons
OPPORTUNITY     - Sales opportunities
CASE            - Support cases
ASSET           - Physical or digital assets
LOCATION        - Geographic locations
DEPARTMENT      - Organizational units
PROJECT         - Projects or initiatives
DOCUMENT        - Documents or files
EVENT           - Events or activities
TRANSACTION     - Financial transactions
USER            - System users
ROLE            - User roles
POLICY          - Business policies
```

### 2. Relationships

**What are Relationships?**

Relationships connect entities to form a knowledge graph. They use RDF-style subject-predicate-object triples.

**Relationship Structure:**
- **Subject** - Source entity (e.g., "Customer A")
- **Predicate** - Relationship type (e.g., "OWNS")
- **Object** - Target entity (e.g., "Account B")
- **Properties** - Additional metadata

**Common Relationship Types:**
```
OWNS            - Ownership relationship
HAS             - Possession or containment
BELONGS_TO      - Membership or association
RELATED_TO      - Generic relationship
DEPENDS_ON      - Dependency
CREATED_BY      - Creation attribution
MANAGED_BY      - Management relationship
ASSIGNED_TO     - Assignment
CONTAINS        - Containment
PURCHASED       - Purchase relationship
SUBSCRIBED_TO   - Subscription
INTERACTED_WITH - Interaction
INFLUENCED_BY   - Influence
DERIVED_FROM    - Derivation
PART_OF         - Part-whole relationship
REPORTS_TO      - Reporting structure
```

### 3. Entity States

**What are Entity States?**

States track the lifecycle and current status of entities. State changes can trigger workflows.

**Common States:**
```
ACTIVE          - Entity is active and operational
INACTIVE        - Entity is inactive but not deleted
AT_RISK         - Entity requires attention
PENDING         - Awaiting action or approval
APPROVED        - Approved and ready
REJECTED        - Rejected or declined
IN_PROGRESS     - Work in progress
COMPLETED       - Finished or fulfilled
CANCELLED       - Cancelled or voided
ARCHIVED        - Archived for historical purposes
```

### 4. Workflows

**What are Workflows?**

Workflows are automated actions triggered by entity state changes or conditions.

**Workflow Components:**
- **Trigger Condition** - When to execute (e.g., "entity_type=CUSTOMER AND current_state=AT_RISK")
- **Action Type** - What to do (21 types available)
- **Action Config** - Configuration for the action
- **Enabled/Disabled** - Control execution

**21 Action Types:**
```
1.  NOTIFICATION     - Send in-app notification
2.  EMAIL            - Send email alert
3.  SLACK            - Post to Slack channel
4.  WEBHOOK          - Call external HTTP endpoint
5.  SNOWFLAKE_TASK   - Execute Snowflake task
6.  STORED_PROCEDURE - Call stored procedure
7.  SQL_QUERY        - Execute SQL query
8.  CREATE_ENTITY    - Create new entity
9.  UPDATE_ENTITY    - Update existing entity
10. CREATE_RELATIONSHIP - Create relationship
11. DELETE_RELATIONSHIP - Delete relationship
12. TAG_ENTITY       - Add tags to entity
13. STATE_TRANSITION - Change entity state
14. AGGREGATE        - Aggregate data
15. PROPAGATE        - Propagate changes
16. VALIDATE         - Validate data
17. ENRICH           - Enrich with external data
18. ARCHIVE          - Archive entity
19. ALERT            - Send alert
20. AUDIT_LOG        - Create audit log entry
21. COMPOSITE        - Execute multiple actions
```

---

## User Interface Guide

### Dashboard

**Purpose:** Overview of your ontology with real-time statistics

**Features:**
- **Total Entities** - Count of all entities
- **Total Relationships** - Count of all relationships
- **Active Workflows** - Number of enabled workflows
- **Recent Executions** - Latest workflow runs

**Charts:**
- **Entities by Type** - Bar chart showing distribution
- **Relationships by Type** - Bar chart showing connections

**Use Cases:**
- Monitor system health
- Track growth over time
- Identify imbalances
- Quick status check

### Entities Page

**Purpose:** Manage all entities in your ontology

**Layout:**
- **Tree View** - Entities grouped by type
- **Search Bar** - Filter by label or type
- **Expand/Collapse** - Show/hide entity groups
- **Action Buttons** - Create, edit, delete

**Features:**

1. **Create Entity**
   - Click "+ Add Entity" button
   - Fill in the form:
     - Entity Type (required)
     - Label (required)
     - Properties (JSON format)
     - Tags (comma-separated)
   - Click "Create"

2. **Search & Filter**
   - Type in search bar
   - Filters by label and type
   - Auto-expands matching groups
   - Real-time results

3. **Tree View Navigation**
   - Click type header to expand/collapse
   - Shows entity count per type
   - "Expand All" / "Collapse All" buttons
   - Displays tags as badges

4. **Edit Entity**
   - Click edit icon (✏️) on entity
   - Modify fields in modal
   - Click "Update"

5. **Delete Entity**
   - Click delete icon (🗑️) on entity
   - Confirm deletion
   - Cascades to relationships

**Example Entity Properties:**
```json
{
  "industry": "Technology",
  "size": "Enterprise",
  "annual_revenue": 50000000,
  "employees": 5000,
  "country": "US",
  "health_score": 85
}
```

### Relationships Page

**Purpose:** Create and manage relationships between entities

**Features:**

1. **Create Relationship**
   - Click "+ Add Relationship"
   - Select Subject Entity
   - Select Predicate (relationship type)
   - Select Object Entity
   - Add Properties (optional)
   - Click "Create"

2. **View Relationships**
   - Table view with all relationships
   - Shows: Subject → Predicate → Object
   - Displays properties
   - Creation timestamp

3. **Filter Relationships**
   - Filter by entity (subject or object)
   - Filter by predicate type
   - Search functionality

4. **Delete Relationship**
   - Click delete icon (🗑️)
   - Confirm deletion

**Example Relationships:**
```
Customer A → OWNS → Account B
Account B → HAS → Order C
Order C → CONTAINS → Product D
Product D → BELONGS_TO → Category E
Customer A → INTERACTED_WITH → Campaign F
```

### Graph View

**Purpose:** Visualize entity relationships as an interactive DAG

**Features:**

1. **Interactive Visualization**
   - Drag nodes to reposition
   - Zoom in/out with controls
   - Pan by dragging background
   - Fit view to see all nodes

2. **Node Information**
   - Color-coded by entity type
   - Shows entity label
   - Click for details panel

3. **Edge Information**
   - Arrows show direction
   - Labels show relationship type
   - Hover for details

4. **Graph Controls**
   - Zoom In (+)
   - Zoom Out (-)
   - Fit View
   - Lock/Unlock

5. **Legend**
   - Color key for entity types
   - Relationship type indicators

6. **Details Panel**
   - Entity properties
   - Connected relationships
   - State information
   - Collapse/expand

**Use Cases:**
- Understand entity connections
- Identify relationship patterns
- Discover data lineage
- Visualize customer 360
- Trace dependencies

### Workflows Page

**Purpose:** Configure and manage automated workflows

**Features:**

1. **Create Workflow**
   - Click "+ Create Workflow"
   - Fill in details:
     - Name (required)
     - Description
     - Trigger Condition (use builder)
     - Action Type (dropdown)
     - Action Config (JSON)
     - Enabled (checkbox)
   - Click "Create"

2. **Trigger Condition Builder**
   - Visual builder for conditions
   - Add multiple conditions
   - Combine with AND logic
   - Fields: entity_type, current_state, previous_state, tags
   - Operators: =, !=, >, <, LIKE, IN
   - Auto-generates SQL condition

3. **Edit Workflow**
   - Click edit icon (✏️)
   - Modify fields
   - Trigger condition auto-populates builder
   - Click "Update"

4. **Delete Workflow**
   - Click delete icon (🗑️)
   - Confirm deletion

5. **Enable/Disable**
   - Toggle enabled status
   - Disabled workflows don't execute
   - Useful for testing

6. **View Executions**
   - See execution history
   - Status: PENDING, IN_PROGRESS, COMPLETED, FAILED
   - Timestamps and duration
   - Error messages if failed

**Example Workflow:**
```
Name: Customer At-Risk Alert
Description: Send alert when customer becomes at-risk
Trigger: entity_type=CUSTOMER AND current_state=AT_RISK
Action Type: EMAIL
Action Config:
{
  "to": "support@company.com",
  "subject": "Customer At-Risk",
  "body": "Customer {{entity_label}} needs attention"
}
Enabled: Yes
```

---

## Working with Entities

### Creating Entities

**Step-by-Step:**

1. Navigate to **Entities** page
2. Click **"+ Add Entity"** button
3. Fill in the form:

**Entity Type:**
- Select from dropdown or type custom
- Examples: CUSTOMER, PRODUCT, ORDER
- Case-sensitive

**Label:**
- Human-readable name
- Examples: "Acme Corporation", "iPhone 15", "Order #12345"
- Required field

**Properties (JSON):**
- Flexible key-value pairs
- Must be valid JSON
- Example:
```json
{
  "industry": "Technology",
  "size": "Enterprise",
  "revenue": 50000000,
  "employees": 5000,
  "tier": "Platinum",
  "health_score": 85,
  "last_contact": "2026-01-15",
  "account_manager": "John Smith"
}
```

**Tags:**
- Comma-separated list
- Examples: "enterprise, technology, active, high-value"
- Used for filtering and workflows
- Case-insensitive

4. Click **"Create"**
5. Entity appears in tree view under its type

### Editing Entities

**Step-by-Step:**

1. Find entity in tree view (use search if needed)
2. Click edit icon (✏️) next to entity
3. Modify fields in modal
4. Click **"Update"**
5. Changes are saved immediately

**What You Can Edit:**
- ✅ Label
- ✅ Properties (add, modify, remove)
- ✅ Tags (add, remove)
- ❌ Entity Type (cannot change after creation)
- ❌ Entity ID (system-generated)

### Deleting Entities

**Step-by-Step:**

1. Find entity in tree view
2. Click delete icon (🗑️) next to entity
3. Confirm deletion in dialog
4. Entity is permanently deleted

**⚠️ Warning:**
- Deletion is permanent
- All relationships involving this entity are also deleted
- Workflow executions referencing this entity remain for audit

### Searching Entities

**Search Features:**

1. **Type to Search**
   - Start typing in search bar
   - Searches entity labels and types
   - Results update in real-time

2. **Auto-Expand**
   - Matching entity types auto-expand
   - Non-matching types collapse
   - Shows count of matches

3. **Clear Search**
   - Click X icon in search bar
   - All types collapse to default state

**Search Tips:**
- Search is case-insensitive
- Partial matches work
- Searches both label and type
- Use "Expand All" to see everything

### Entity Best Practices

**Naming Conventions:**
- Use descriptive labels
- Be consistent with entity types
- Use UPPERCASE for types (e.g., CUSTOMER, not customer)
- Use Title Case for labels (e.g., "Acme Corporation")

**Properties:**
- Keep properties flat when possible
- Use consistent property names across same type
- Include timestamps for temporal data
- Add metadata for context

**Tags:**
- Use tags for classification
- Create tag taxonomy
- Use lowercase for consistency
- Examples: "active", "archived", "high-priority"

**Organization:**
- Group related entities by type
- Use meaningful entity types
- Don't create too many types (10-20 is good)
- Consider hierarchy in naming (e.g., CUSTOMER_ENTERPRISE, CUSTOMER_SMB)

---

## Working with Relationships

### Creating Relationships

**Step-by-Step:**

1. Navigate to **Relationships** page
2. Click **"+ Add Relationship"** button
3. Fill in the form:

**Subject Entity:**
- Select from dropdown
- The "from" entity
- Example: "Customer A"

**Predicate:**
- Relationship type
- Select from dropdown or type custom
- Examples: OWNS, HAS, BELONGS_TO
- Use UPPERCASE

**Object Entity:**
- Select from dropdown
- The "to" entity
- Example: "Account B"

**Properties (Optional):**
- Additional metadata about relationship
- JSON format
- Example:
```json
{
  "since": "2024-01-15",
  "strength": 0.95,
  "type": "primary",
  "verified": true
}
```

4. Click **"Create"**
5. Relationship appears in table

### Relationship Patterns

**Common Patterns:**

**1. Ownership:**
```
Customer → OWNS → Account
Account → OWNS → Order
User → OWNS → Document
```

**2. Hierarchy:**
```
Department → CONTAINS → Team
Team → CONTAINS → Employee
Category → CONTAINS → Product
```

**3. Association:**
```
Order → CONTAINS → Product
Campaign → TARGETS → Customer
Project → ASSIGNED_TO → User
```

**4. Temporal:**
```
Customer → INTERACTED_WITH → Campaign
User → CREATED → Document
Order → FULFILLED_BY → Warehouse
```

**5. Dependency:**
```
Service → DEPENDS_ON → Database
Report → DERIVED_FROM → Table
Process → REQUIRES → Resource
```

### Bidirectional Relationships

**Creating Both Directions:**

To create bidirectional relationships, create two separate relationships:

```
Forward:  Customer A → OWNS → Account B
Backward: Account B → BELONGS_TO → Customer A
```

**When to Use:**
- Navigation in both directions needed
- Semantic meaning differs by direction
- Graph queries need efficiency

### Deleting Relationships

**Step-by-Step:**

1. Find relationship in table
2. Click delete icon (🗑️)
3. Confirm deletion
4. Relationship is removed

**⚠️ Note:**
- Only deletes this specific relationship
- Does not delete the entities
- Cannot be undone

### Relationship Best Practices

**Naming:**
- Use UPPERCASE for predicates
- Use verbs or verb phrases
- Be specific (PURCHASED vs HAS)
- Be consistent across similar relationships

**Direction:**
- Subject → Predicate → Object should read naturally
- "Customer OWNS Account" ✅
- "Account OWNED_BY Customer" ✅
- "Customer HAS_OWNER Account" ❌

**Properties:**
- Add temporal information (since, until)
- Add strength or confidence scores
- Add type or category
- Keep properties relevant

**Avoid:**
- Circular dependencies (unless intentional)
- Too many relationship types (consolidate similar ones)
- Relationships between incompatible types
- Redundant relationships

---

## Graph Visualization

### Understanding the DAG View

**What is a DAG?**

DAG = Directed Acyclic Graph
- **Directed:** Arrows show relationship direction
- **Acyclic:** No circular paths (by design)
- **Graph:** Nodes (entities) connected by edges (relationships)

**Layout:**
- Hierarchical top-to-bottom
- Nodes positioned by depth
- Root nodes at top
- Leaf nodes at bottom
- Minimizes edge crossings

### Navigating the Graph

**Mouse Controls:**
- **Click & Drag Node:** Move node
- **Click & Drag Background:** Pan view
- **Scroll Wheel:** Zoom in/out
- **Click Node:** Show details panel

**Toolbar Controls:**
- **+ Button:** Zoom in
- **- Button:** Zoom out
- **⊡ Button:** Fit view to show all nodes
- **🔒 Button:** Lock/unlock node positions

### Node Information

**Node Appearance:**
- **Color:** Indicates entity type (see legend)
- **Label:** Entity label (truncated if long)
- **Size:** All nodes same size
- **Border:** Solid border

**Node Details Panel:**
- Click any node to open
- Shows:
  - Entity ID
  - Entity Type
  - Label
  - Properties (formatted JSON)
  - Tags
  - Connected Relationships
  - Current State
- Click X to close

### Edge Information

**Edge Appearance:**
- **Arrow:** Shows direction (subject → object)
- **Label:** Relationship type (predicate)
- **Color:** Gray by default
- **Style:** Solid line

**Edge Details:**
- Hover over edge to see tooltip
- Shows: Subject → Predicate → Object
- Click edge to highlight path

### Legend

**Color Key:**
- Each entity type has unique color
- Legend shows all types in current graph
- Helps identify entity types quickly

**Example Colors:**
```
CUSTOMER     - Blue
ACCOUNT      - Green
PRODUCT      - Orange
ORDER        - Purple
CAMPAIGN     - Red
CONTACT      - Teal
OPPORTUNITY  - Pink
CASE         - Yellow
```

### Graph Use Cases

**1. Customer 360 View:**
- Start with customer entity
- See all owned accounts
- View all orders
- Trace product purchases
- Identify campaign interactions

**2. Data Lineage:**
- Start with report entity
- Trace back to source tables
- See transformation steps
- Identify dependencies

**3. Supply Chain:**
- Start with product
- See suppliers
- View warehouses
- Trace to orders
- Identify bottlenecks

**4. Organizational Structure:**
- Start with department
- See teams
- View employees
- Trace reporting lines

**5. Dependency Analysis:**
- Start with service
- See all dependencies
- Identify critical paths
- Plan changes safely

---

## Workflow Engine

### Creating Workflows

**Step-by-Step Guide:**

1. Navigate to **Workflows** page
2. Click **"+ Create Workflow"**
3. Fill in the form (see sections below)
4. Click **"Create"**

### Workflow Configuration

**1. Name (Required)**
- Descriptive name for the workflow
- Examples:
  - "Customer At-Risk Alert"
  - "Order Fulfillment Notification"
  - "High-Value Customer Tag"
- Keep it concise but clear

**2. Description (Optional)**
- Detailed explanation of workflow purpose
- Document business logic
- Note any special conditions
- Include contact information

**3. Trigger Condition (Required)**

Use the visual builder to create conditions:

**Adding Conditions:**
- Click **"+ Add Condition"**
- Select Field from dropdown
- Select Operator
- Enter Value
- Repeat for multiple conditions
- All conditions combined with AND

**Available Fields:**
```
entity_type      - Type of entity
current_state    - Current state
previous_state   - Previous state before change
tags             - Entity tags (use IN operator)
```

**Available Operators:**
```
=     - Equals
!=    - Not equals
>     - Greater than
<     - Less than
LIKE  - Pattern match (use % wildcards)
IN    - In list (comma-separated)
```

**Example Conditions:**
```
entity_type = CUSTOMER
current_state = AT_RISK
previous_state != AT_RISK
tags IN (enterprise,high-value)
```

**Generated SQL:**
The builder automatically generates SQL:
```sql
entity_type=CUSTOMER AND current_state=AT_RISK AND previous_state!=ACTIVE
```

**4. Action Type (Required)**

Select from 21 action types:

**Notification Actions:**
- **NOTIFICATION:** In-app notification
- **EMAIL:** Send email
- **SLACK:** Post to Slack
- **ALERT:** Send alert to monitoring system

**Integration Actions:**
- **WEBHOOK:** Call external API
- **SNOWFLAKE_TASK:** Execute Snowflake task
- **STORED_PROCEDURE:** Call stored procedure
- **SQL_QUERY:** Execute SQL query

**Entity Actions:**
- **CREATE_ENTITY:** Create new entity
- **UPDATE_ENTITY:** Update existing entity
- **TAG_ENTITY:** Add tags to entity
- **ARCHIVE:** Archive entity

**Relationship Actions:**
- **CREATE_RELATIONSHIP:** Create relationship
- **DELETE_RELATIONSHIP:** Delete relationship

**State Actions:**
- **STATE_TRANSITION:** Change entity state

**Data Actions:**
- **AGGREGATE:** Aggregate data
- **PROPAGATE:** Propagate changes
- **VALIDATE:** Validate data
- **ENRICH:** Enrich with external data

**Audit Actions:**
- **AUDIT_LOG:** Create audit log entry

**Complex Actions:**
- **COMPOSITE:** Execute multiple actions

**5. Action Config (Required)**

JSON configuration for the selected action type.

**EMAIL Action Config:**
```json
{
  "to": "support@company.com",
  "subject": "Customer At-Risk: {{entity_label}}",
  "body": "Customer {{entity_label}} ({{entity_id}}) has become at-risk. Health score: {{properties.health_score}}",
  "cc": "manager@company.com",
  "priority": "high"
}
```

**SLACK Action Config:**
```json
{
  "channel": "#customer-alerts",
  "message": "🚨 Customer {{entity_label}} is at risk!",
  "username": "Ontology Bot",
  "icon_emoji": ":warning:"
}
```

**WEBHOOK Action Config:**
```json
{
  "url": "https://api.example.com/webhooks/customer-alert",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
  },
  "body": {
    "entity_id": "{{entity_id}}",
    "entity_type": "{{entity_type}}",
    "state": "{{current_state}}",
    "timestamp": "{{timestamp}}"
  }
}
```

**SQL_QUERY Action Config:**
```json
{
  "query": "UPDATE CUSTOMER_METRICS SET at_risk_flag = TRUE WHERE customer_id = '{{entity_id}}'",
  "warehouse": "COMPUTE_WH"
}
```

**CREATE_ENTITY Action Config:**
```json
{
  "entity_type": "CASE",
  "label": "At-Risk Case for {{entity_label}}",
  "properties": {
    "customer_id": "{{entity_id}}",
    "priority": "high",
    "status": "open",
    "created_reason": "automated_at_risk_detection"
  },
  "tags": ["automated", "at-risk", "urgent"]
}
```

**TAG_ENTITY Action Config:**
```json
{
  "tags": ["at-risk", "needs-attention", "automated-flag"],
  "action": "add"
}
```

**STATE_TRANSITION Action Config:**
```json
{
  "new_state": "UNDER_REVIEW",
  "reason": "Automated transition due to at-risk status",
  "notify": true
}
```

**COMPOSITE Action Config:**
```json
{
  "actions": [
    {
      "type": "EMAIL",
      "config": {
        "to": "support@company.com",
        "subject": "Alert",
        "body": "Customer at risk"
      }
    },
    {
      "type": "TAG_ENTITY",
      "config": {
        "tags": ["at-risk"],
        "action": "add"
      }
    },
    {
      "type": "CREATE_ENTITY",
      "config": {
        "entity_type": "CASE",
        "label": "Follow-up case"
      }
    }
  ]
}
```

**Template Variables:**

Use these variables in action configs:
```
{{entity_id}}           - Entity ID
{{entity_type}}         - Entity type
{{entity_label}}        - Entity label
{{current_state}}       - Current state
{{previous_state}}      - Previous state
{{properties.field}}    - Any property field
{{tags}}                - All tags (comma-separated)
{{timestamp}}           - Current timestamp
```

**6. Enabled (Checkbox)**

- ✅ Checked: Workflow will execute when triggered
- ☐ Unchecked: Workflow is disabled (useful for testing)

### Testing Workflows

**Testing Strategy:**

1. **Create Test Entity**
   - Create entity with specific type
   - Set initial state

2. **Create Workflow (Disabled)**
   - Configure workflow
   - Leave disabled initially
   - Verify configuration

3. **Enable Workflow**
   - Check enabled checkbox
   - Update workflow

4. **Trigger Workflow**
   - Change entity state to match trigger
   - Or update entity to match condition

5. **Verify Execution**
   - Check workflow executions table
   - Verify status is COMPLETED
   - Check output data
   - Verify action was performed

6. **Debug if Failed**
   - Check error message
   - Review action config
   - Verify trigger condition
   - Check entity state

### Monitoring Workflows

**Execution History:**

View all workflow executions in the table:
- **Workflow Name:** Which workflow executed
- **Entity:** Which entity triggered it
- **Status:** PENDING, IN_PROGRESS, COMPLETED, FAILED
- **Started At:** When execution began
- **Completed At:** When execution finished
- **Duration:** How long it took
- **Error Message:** If failed, why

**Filtering:**
- Filter by workflow
- Filter by status
- Filter by entity
- Filter by date range

**Troubleshooting Failed Executions:**

1. **Check Error Message**
   - Provides specific failure reason
   - May indicate config issue

2. **Verify Action Config**
   - Ensure JSON is valid
   - Check all required fields
   - Verify template variables exist

3. **Check Trigger Condition**
   - Ensure condition matches entity
   - Verify field names are correct
   - Test condition in SQL

4. **Review Entity State**
   - Verify entity exists
   - Check current state
   - Review properties

### Workflow Best Practices

**Design:**
- Keep workflows simple and focused
- One workflow = one purpose
- Use COMPOSITE for complex scenarios
- Test thoroughly before enabling

**Naming:**
- Use descriptive names
- Include trigger condition in name
- Examples: "Customer At-Risk Email", "Order Complete Notification"

**Trigger Conditions:**
- Be specific to avoid false triggers
- Use multiple conditions to narrow scope
- Consider previous state to avoid re-triggering
- Test conditions with sample data

**Action Configs:**
- Validate JSON before saving
- Use template variables for dynamic content
- Include error handling where possible
- Document complex configurations

**Monitoring:**
- Regularly review execution history
- Set up alerts for failed executions
- Monitor execution duration
- Archive old executions periodically

**Security:**
- Don't hardcode credentials in configs
- Use Snowflake secrets for sensitive data
- Validate webhook URLs
- Limit permissions appropriately

---

## API Usage

### API Documentation

**Interactive API Docs:**
- Navigate to: `https://your-endpoint.snowflakecomputing.app/docs`
- Swagger UI with all endpoints
- Try out API calls directly
- View request/response schemas

### Authentication

Currently, the API uses Snowflake's OAuth authentication. Future versions will support:
- API keys
- JWT tokens
- OAuth2 flows

### Base URL

```
https://your-endpoint.snowflakecomputing.app
```

### Common Endpoints

**Health Check:**
```bash
GET /health
```

**List Entities:**
```bash
GET /entities
GET /entities?entity_type=CUSTOMER
GET /entities?tags=enterprise
```

**Get Entity:**
```bash
GET /entities/{entity_id}
```

**Create Entity:**
```bash
POST /entities
Content-Type: application/json

{
  "entity_type": "CUSTOMER",
  "label": "Acme Corporation",
  "properties": {
    "industry": "Technology",
    "size": "Enterprise"
  },
  "tags": ["enterprise", "technology"]
}
```

**Update Entity:**
```bash
PUT /entities/{entity_id}
Content-Type: application/json

{
  "label": "Acme Corp (Updated)",
  "properties": {
    "industry": "Technology",
    "size": "Large Enterprise"
  }
}
```

**Delete Entity:**
```bash
DELETE /entities/{entity_id}
```

**Create Relationship:**
```bash
POST /relationships
Content-Type: application/json

{
  "subject_id": "customer-001",
  "predicate": "OWNS",
  "object_id": "account-001",
  "properties": {
    "since": "2024-01-15"
  }
}
```

**Query Graph:**
```bash
POST /graph/query
Content-Type: application/json

{
  "start_entity_id": "customer-001",
  "max_depth": 3,
  "direction": "both",
  "relationship_types": ["OWNS", "HAS"]
}
```

**Get Graph Stats:**
```bash
GET /graph/stats
```

**Create Workflow:**
```bash
POST /workflows
Content-Type: application/json

{
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
}
```

**Execute Workflow:**
```bash
POST /workflows/{workflow_id}/execute
Content-Type: application/json

{
  "entity_id": "customer-001",
  "input_data": {
    "reason": "manual_trigger"
  }
}
```

### API Examples

**Python Example:**
```python
import requests

BASE_URL = "https://your-endpoint.snowflakecomputing.app"

# Create entity
response = requests.post(
    f"{BASE_URL}/entities",
    json={
        "entity_type": "CUSTOMER",
        "label": "Acme Corporation",
        "properties": {
            "industry": "Technology",
            "size": "Enterprise"
        },
        "tags": ["enterprise"]
    }
)
entity = response.json()
print(f"Created entity: {entity['entity_id']}")

# Query graph
response = requests.post(
    f"{BASE_URL}/graph/query",
    json={
        "start_entity_id": entity['entity_id'],
        "max_depth": 2,
        "direction": "both"
    }
)
graph = response.json()
print(f"Found {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")
```

**cURL Example:**
```bash
# Create entity
curl -X POST "https://your-endpoint.snowflakecomputing.app/entities" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "CUSTOMER",
    "label": "Acme Corporation",
    "properties": {"industry": "Technology"},
    "tags": ["enterprise"]
  }'

# Get entity
curl "https://your-endpoint.snowflakecomputing.app/entities/customer-001"

# Query graph
curl -X POST "https://your-endpoint.snowflakecomputing.app/graph/query" \
  -H "Content-Type: application/json" \
  -d '{
    "start_entity_id": "customer-001",
    "max_depth": 3,
    "direction": "both"
  }'
```

---

## Best Practices

### Data Modeling

**1. Entity Design**
- Use consistent entity types across your organization
- Define clear entity type taxonomy (10-20 types max)
- Keep properties flat and simple
- Use tags for flexible classification
- Include metadata (created_by, source, etc.)

**2. Relationship Design**
- Use semantic predicates (OWNS, HAS, etc.)
- Be consistent with relationship direction
- Add temporal properties (since, until)
- Consider bidirectional relationships for navigation
- Avoid redundant relationships

**3. State Management**
- Define clear state lifecycle
- Document valid state transitions
- Use meaningful state names
- Track state history
- Add state metadata (reason, changed_by)

### Workflow Design

**1. Trigger Conditions**
- Be specific to avoid false positives
- Use multiple conditions to narrow scope
- Consider previous state to avoid re-triggering
- Test conditions thoroughly
- Document business logic

**2. Action Configuration**
- Keep actions simple and focused
- Use COMPOSITE for complex scenarios
- Validate JSON before saving
- Use template variables for dynamic content
- Include error handling

**3. Monitoring**
- Review execution history regularly
- Set up alerts for failures
- Monitor execution duration
- Archive old executions
- Document common issues

### Performance

**1. Entity Management**
- Batch create entities when possible
- Use bulk operations for large datasets
- Index frequently queried properties
- Archive old entities
- Clean up orphaned relationships

**2. Graph Queries**
- Limit max_depth to reasonable values (3-5)
- Filter by relationship types
- Use direction parameter to reduce scope
- Cache frequently accessed graphs
- Consider materialized views for common queries

**3. Workflow Execution**
- Keep action configs lightweight
- Avoid long-running operations
- Use async processing for heavy tasks
- Monitor execution duration
- Optimize trigger conditions

### Security

**1. Access Control**
- Use Snowflake role-based access control
- Limit permissions to minimum required
- Audit access regularly
- Separate dev/test/prod environments
- Document security policies

**2. Data Protection**
- Encrypt sensitive properties
- Use Snowflake secrets for credentials
- Mask PII in logs
- Implement data retention policies
- Regular security audits

**3. API Security**
- Use HTTPS only
- Implement rate limiting
- Validate all inputs
- Log API access
- Monitor for suspicious activity

### Maintenance

**1. Regular Tasks**
- Review and optimize workflows
- Clean up unused entities
- Archive old executions
- Update documentation
- Monitor system health

**2. Data Quality**
- Validate entity properties
- Check relationship integrity
- Verify state consistency
- Remove duplicates
- Standardize naming

**3. Documentation**
- Document entity types and their purpose
- Maintain relationship type glossary
- Document workflow business logic
- Keep API examples current
- Update user guides

---

## Troubleshooting

### Common Issues

**1. Entity Not Appearing in Tree View**

**Symptoms:**
- Created entity but don't see it
- Search returns no results

**Solutions:**
- Refresh the page (F5)
- Check if entity type is collapsed
- Use "Expand All" button
- Verify entity was created (check API response)
- Check for JavaScript errors in browser console

**2. Relationship Creation Fails**

**Symptoms:**
- Error when creating relationship
- "Entity not found" message

**Solutions:**
- Verify both entities exist
- Check entity IDs are correct
- Ensure entities are not deleted
- Verify predicate is valid
- Check properties JSON is valid

**3. Graph View Not Loading**

**Symptoms:**
- Blank graph view
- Loading spinner forever
- Error message

**Solutions:**
- Check if entities and relationships exist
- Verify backend API is running
- Check browser console for errors
- Try refreshing the page
- Check network connectivity

**4. Workflow Not Triggering**

**Symptoms:**
- Entity state changed but workflow didn't execute
- No execution in history

**Solutions:**
- Verify workflow is enabled
- Check trigger condition matches entity
- Verify entity state actually changed
- Check Snowflake task is running
- Review workflow execution logs

**5. Workflow Execution Failed**

**Symptoms:**
- Execution shows FAILED status
- Error message in execution history

**Solutions:**
- Read error message carefully
- Verify action config JSON is valid
- Check all required fields are present
- Verify template variables exist in entity
- Test action config with sample data
- Check external service availability (for webhooks, email, etc.)

**6. Search Not Working**

**Symptoms:**
- Typing in search bar shows no results
- Search seems frozen

**Solutions:**
- Clear search and try again
- Refresh the page
- Check if entities exist
- Verify entity labels are not empty
- Check browser console for errors

**7. Performance Issues**

**Symptoms:**
- Slow page loads
- Laggy interactions
- Timeouts

**Solutions:**
- Check number of entities (>10,000 may be slow)
- Limit graph depth for large graphs
- Archive old entities
- Optimize Snowflake warehouse size
- Check network latency
- Clear browser cache

### Error Messages

**"Invalid JSON in properties"**
- Properties field must be valid JSON
- Use online JSON validator
- Check for missing quotes, commas, brackets

**"Entity not found"**
- Entity ID doesn't exist
- Entity may have been deleted
- Check entity ID spelling

**"Relationship already exists"**
- Duplicate relationship
- Check existing relationships
- Delete old relationship first

**"Workflow trigger condition invalid"**
- SQL syntax error in condition
- Check field names are correct
- Verify operators are valid
- Test condition in SQL editor

**"Action config validation failed"**
- Required fields missing in action config
- JSON structure doesn't match expected format
- Check action type documentation

**"Database connection failed"**
- Snowflake credentials invalid
- Network connectivity issue
- Warehouse suspended
- Contact administrator

### Getting Help

**1. Check Documentation**
- Review this user guide
- Check README.md
- Review API docs at /docs endpoint

**2. Check Logs**
- Browser console (F12)
- Backend logs (if accessible)
- Snowflake query history

**3. Contact Support**
- Provide error message
- Include steps to reproduce
- Share relevant entity/workflow IDs
- Include browser and OS version

**4. Community Resources**
- GitHub issues (if open source)
- Snowflake community forums
- Internal team chat/wiki

---

## FAQ

**Q: Can I import existing data into the ontology?**

A: Yes, you can use the API to bulk create entities and relationships. Write a script to read your data and call the POST /entities and POST /relationships endpoints.

**Q: How many entities can the system handle?**

A: The system can handle millions of entities. Performance depends on your Snowflake warehouse size. For optimal UI performance, consider pagination or filtering for large datasets.

**Q: Can I export the graph data?**

A: Yes, use the GET /graph/query endpoint to retrieve graph data in JSON format. You can also query the underlying Snowflake tables directly.

**Q: How do I backup my data?**

A: All data is stored in Snowflake tables. Use Snowflake's Time Travel and Fail-safe features for backup and recovery. You can also export data using Snowflake's COPY INTO command.

**Q: Can I customize entity types?**

A: Yes, entity types are flexible. You can create custom types by simply using them when creating entities. Consider maintaining a documented list of types for consistency.

**Q: How do I delete all data and start over?**

A: Run the teardown script or execute:
```sql
DELETE FROM WORKFLOW_EXECUTIONS;
DELETE FROM WORKFLOW_DEFINITIONS;
DELETE FROM ENTITY_STATES;
DELETE FROM RELATIONSHIPS;
DELETE FROM ENTITIES;
```

**Q: Can workflows call external APIs?**

A: Yes, use the WEBHOOK action type to call any HTTP endpoint. Configure the URL, method, headers, and body in the action config.

**Q: How do I monitor workflow execution?**

A: View the workflow executions table on the Workflows page. You can also query the WORKFLOW_EXECUTIONS table directly in Snowflake.

**Q: Can I schedule workflows?**

A: Workflows are event-driven (triggered by state changes). For scheduled execution, use Snowflake tasks to update entity states on a schedule.

**Q: How do I handle errors in workflows?**

A: Failed workflows are logged with error messages. Review the execution history, fix the issue (usually in action config), and manually re-execute if needed.

**Q: Can I version entities?**

A: The system tracks created_at and updated_at timestamps. For full versioning, consider using Snowflake's Time Travel feature or implement a custom versioning strategy.

**Q: How do I model hierarchical relationships?**

A: Use relationships like CONTAINS, PART_OF, or BELONGS_TO. Create relationships from parent to child entities. The graph view will show the hierarchy.

**Q: Can I integrate with other Snowflake features?**

A: Yes, workflows can execute SQL queries, call stored procedures, and trigger Snowflake tasks. You can integrate with Streams, Tasks, and other Snowflake features.

**Q: How do I optimize graph queries?**

A: Limit max_depth, filter by relationship types, use direction parameter, and consider creating materialized views for frequently accessed subgraphs.

**Q: Can I use this for data lineage?**

A: Yes, create entities for tables, views, and reports. Use relationships like DERIVED_FROM, DEPENDS_ON, and TRANSFORMS to model lineage.

**Q: How do I handle many-to-many relationships?**

A: Create relationships in both directions or use an intermediate entity. For example: Student ← ENROLLED_IN → Course.

**Q: Can I add custom fields to entities?**

A: Yes, use the properties field (JSON) to add any custom fields. Properties are flexible and don't require schema changes.

**Q: How do I search across all properties?**

A: The UI search currently searches labels and types. For property search, use the API or query Snowflake tables directly with JSON functions.

**Q: Can I import from other graph databases?**

A: Yes, export your graph data to JSON or CSV, then use the API to import. You may need to write a custom migration script.

**Q: How do I handle large graphs in the visualization?**

A: The graph view works best with <500 nodes. For larger graphs, filter by entity type or relationship type, or query specific subgraphs.

**Q: Can I customize the UI?**

A: The frontend is React-based. You can modify the source code to customize appearance, add features, or change behavior.

**Q: How do I set up multiple environments (dev/test/prod)?**

A: Deploy separate instances with different Snowflake databases. Use environment variables to configure each instance.

---

## Appendix

### Keyboard Shortcuts

**Global:**
- `Ctrl/Cmd + K` - Focus search bar (if available)
- `F5` - Refresh page
- `Esc` - Close modal/dialog

**Graph View:**
- `+` - Zoom in
- `-` - Zoom out
- `0` - Fit view
- `Arrow keys` - Pan view

### Glossary

**Entity:** A node in the knowledge graph representing a real-world object or concept

**Relationship:** A directed edge connecting two entities with a semantic predicate

**Ontology:** The formal structure defining entity types, relationships, and rules

**Workflow:** An automated action triggered by entity state changes or conditions

**Predicate:** The relationship type in a subject-predicate-object triple

**DAG:** Directed Acyclic Graph - a graph with directed edges and no cycles

**State:** The current status or lifecycle stage of an entity

**Tag:** A label used for classification and filtering of entities

**Property:** A key-value attribute of an entity or relationship

**Trigger Condition:** The SQL condition that determines when a workflow executes

**Action Type:** The type of automated action a workflow performs

**Action Config:** The JSON configuration for a workflow action

**Graph Traversal:** The process of exploring entity connections in the graph

**Depth:** The number of relationship hops from a starting entity

**SPCS:** Snowflake Snowpark Container Services - the deployment platform

---

## Support

For additional help:

- **Documentation:** Review README.md and API docs
- **GitHub:** https://github.com/Boon67/snowflake-ontology
- **Issues:** Report bugs and request features on GitHub
- **Snowflake Community:** https://community.snowflake.com

---

**Version:** 1.0.0  
**Last Updated:** January 30, 2026  
**Built with ❄️ on Snowflake SPCS**
