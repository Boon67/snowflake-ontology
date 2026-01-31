# 🚀 Deployment Guide - Snowflake Ontology & Workflow Engine

Complete guide for deploying the Snowflake Ontology & Workflow Engine to production.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Deployment Options](#deployment-options)
4. [Production Deployment (SPCS)](#production-deployment-spcs)
5. [Local Development](#local-development)
6. [Configuration](#configuration)
7. [Post-Deployment](#post-deployment)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Troubleshooting](#troubleshooting)
10. [Scaling & Performance](#scaling--performance)
11. [Security Hardening](#security-hardening)
12. [Backup & Recovery](#backup--recovery)

---

## Prerequisites

### Required Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| **Snowflake Account** | Any | Data platform | https://signup.snowflake.com |
| **Snow CLI** | Latest | Deployment tool | `pip install snowflake-cli-labs` |
| **Docker** | 20.10+ | Container runtime | https://www.docker.com/get-started |
| **Git** | 2.0+ | Version control | https://git-scm.com/downloads |
| **jq** | 1.6+ | JSON processing | `brew install jq` or `apt install jq` |

### Optional Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| **Node.js** | 20+ | Frontend development | https://nodejs.org |
| **Python** | 3.11+ | Backend development | https://python.org |
| **GitHub CLI** | Latest | Repository management | `brew install gh` |

### Snowflake Requirements

**Account Requirements:**
- ✅ Snowflake account with SPCS enabled
- ✅ ACCOUNTADMIN role or equivalent permissions
- ✅ Compute pool quota available
- ✅ Image repository storage available

**Permissions Required:**
```sql
-- User must have these permissions
GRANT CREATE DATABASE ON ACCOUNT TO ROLE your_role;
GRANT CREATE COMPUTE POOL ON ACCOUNT TO ROLE your_role;
GRANT CREATE IMAGE REPOSITORY ON ACCOUNT TO ROLE your_role;
GRANT CREATE SERVICE ON ACCOUNT TO ROLE your_role;
GRANT CREATE STAGE ON ACCOUNT TO ROLE your_role;
GRANT CREATE NETWORK RULE ON ACCOUNT TO ROLE your_role;
GRANT CREATE EXTERNAL ACCESS INTEGRATION ON ACCOUNT TO ROLE your_role;
```

**Resource Quotas:**
- Compute Pool: At least 1 node (CPU_X64_S or higher)
- Image Repository: ~2GB storage for Docker images
- Database: Standard warehouse for queries

### System Requirements

**Development Machine:**
- OS: macOS, Linux, or Windows (with WSL2)
- RAM: 8GB minimum, 16GB recommended
- Disk: 10GB free space
- Network: Stable internet connection

**Snowflake Compute:**
- Compute Pool: CPU_X64_S (1-3 nodes)
- Warehouse: SMALL or larger
- Auto-suspend: 1 hour recommended

---

## Pre-Deployment Checklist

### Step 1: Verify Prerequisites

Run the validation script:

```bash
cd /path/to/snowflake-ontology
./scripts/validate.sh
```

This checks:
- ✅ Snow CLI installed and configured
- ✅ Docker installed and running
- ✅ Required files present
- ✅ Configuration files valid
- ✅ Snowflake connection working
- ✅ Dependencies installed

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

**Required Variables:**
```bash
SNOWFLAKE_ACCOUNT=your_account.region
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ONTOLOGY_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

### Step 3: Configure Snow CLI

```bash
# Add Snowflake connection
snow connection add

# Follow prompts:
# - Connection name: default
# - Account: your_account.region
# - User: your_username
# - Password: your_password
# - Role: ACCOUNTADMIN
# - Warehouse: COMPUTE_WH
# - Database: (leave blank)
# - Schema: (leave blank)

# Test connection
snow connection test
```

### Step 4: Review Configuration Files

**Backend Configuration:**
```bash
# Check backend/.env.example
cat backend/.env.example

# Verify Docker configuration
cat backend/Dockerfile
cat backend/requirements.txt
```

**Frontend Configuration:**
```bash
# Check frontend configuration
cat frontend/package.json
cat frontend/Dockerfile
cat frontend/nginx.conf
```

**SPCS Configuration:**
```bash
# Check service specifications
cat spcs/service_spec_single.yaml
cat spcs/service_spec_backend.yaml
cat spcs/service_spec_frontend.yaml
```

### Step 5: Verify Docker

```bash
# Check Docker is running
docker ps

# Test Docker build (optional)
cd backend
docker build -t test-backend .
cd ../frontend
docker build -t test-frontend .
cd ..

# Clean up test images
docker rmi test-backend test-frontend
```

---

## Deployment Options

### Option 1: Production Deployment (SPCS)

**Best for:**
- Production environments
- Scalable deployments
- High availability
- Native Snowflake integration

**Pros:**
- Auto-scaling
- High availability
- Managed infrastructure
- Native Snowflake security
- No external infrastructure needed

**Cons:**
- Requires SPCS-enabled account
- Higher cost than local dev
- Longer deployment time

**Deploy Command:**
```bash
./scripts/deploy.sh
```

### Option 2: Local Development

**Best for:**
- Development and testing
- Quick iterations
- Learning and experimentation
- Offline development

**Pros:**
- Fast startup
- Easy debugging
- No cloud costs
- Full control

**Cons:**
- Not scalable
- No high availability
- Requires local resources
- Manual management

**Deploy Command:**
```bash
./scripts/local_dev.sh
```

### Option 3: Hybrid Approach

**Best for:**
- Teams with mixed needs
- Development → Testing → Production pipeline

**Strategy:**
- Develop locally
- Test in SPCS dev environment
- Deploy to SPCS production

---

## Production Deployment (SPCS)

### Step-by-Step Deployment

**1. Prepare Environment**

```bash
# Navigate to project directory
cd /path/to/snowflake-ontology

# Ensure .env is configured
cat .env

# Run validation
./scripts/validate.sh
```

**2. Execute Deployment**

```bash
# Run deployment script
./scripts/deploy.sh

# This will:
# - Setup database schema
# - Create SPCS infrastructure
# - Build Docker images
# - Push images to Snowflake registry
# - Create services
# - Display endpoints
```

**3. Monitor Deployment**

```bash
# Watch deployment progress
# The script will show progress for each step

# Expected output:
# ======================================
# Snowflake Ontology Engine - Deployment
# ======================================
# Step 1: Setting up database schema...
# Step 2: Setting up SPCS infrastructure...
# Step 3: Getting image repository URL...
# Step 4: Logging into Snowflake container registry...
# Step 5: Building and pushing backend image...
# Step 6: Building and pushing frontend image...
# Step 7: Creating single service...
# Step 8: Waiting for service to be ready...
# Step 9: Getting service endpoints...
# ======================================
# Deployment completed successfully!
# ======================================
```

**4. Verify Deployment**

```bash
# Check service status
snow sql -q "SHOW SERVICES IN DATABASE ONTOLOGY_DB;"

# Check service details
snow sql -q "DESCRIBE SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;"

# Get service status
snow sql -q "SELECT SYSTEM\$GET_SERVICE_STATUS('ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE');"

# View endpoints
snow sql -q "SHOW ENDPOINTS IN SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;"
```

**5. Access Application**

```bash
# Get endpoint URL from deployment output
# Example: https://abc123-ontology-service.snowflakecomputing.app

# Open in browser
# Frontend: Port 80 endpoint
# API Docs: Port 8000 endpoint + /docs
```

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Snowflake Account                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  ONTOLOGY_DB Database                   │ │
│  │                                                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │ │
│  │  │   Tables     │  │   Streams    │  │    Tasks     │ │ │
│  │  │  - ENTITIES  │  │  - CDC       │  │  - Workflow  │ │ │
│  │  │  - RELATIONS │  │  - Changes   │  │  - Triggers  │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │ │
│  │                                                          │ │
│  │  ┌──────────────┐  ┌──────────────┐                   │ │
│  │  │ Image Repo   │  │    Stage     │                   │ │
│  │  │  - Backend   │  │  - Specs     │                   │ │
│  │  │  - Frontend  │  │  - Files     │                   │ │
│  │  └──────────────┘  └──────────────┘                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              ONTOLOGY_COMPUTE_POOL                      │ │
│  │                                                          │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │           ONTOLOGY_SERVICE                       │  │ │
│  │  │                                                   │  │ │
│  │  │  ┌──────────────┐      ┌──────────────┐        │  │ │
│  │  │  │   Backend    │◄────►│   Frontend   │        │  │ │
│  │  │  │   FastAPI    │      │   React      │        │  │ │
│  │  │  │   Port 8000  │      │   Port 80    │        │  │ │
│  │  │  └──────────────┘      └──────────────┘        │  │ │
│  │  │         │                      │                 │  │ │
│  │  │         └──────────┬───────────┘                │  │ │
│  │  │                    │                             │  │ │
│  │  │              ┌─────▼─────┐                      │  │ │
│  │  │              │ Database  │                      │  │ │
│  │  │              │ Connection│                      │  │ │
│  │  │              └───────────┘                      │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           │                                  │
│                    ┌──────▼──────┐                          │
│                    │  Endpoints  │                          │
│                    │  - Web (80) │                          │
│                    │  - API(8000)│                          │
│                    └──────┬──────┘                          │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            │ HTTPS
                            │
                    ┌───────▼────────┐
                    │   End Users    │
                    │   Browsers     │
                    │   API Clients  │
                    └────────────────┘
```

### Resource Configuration

**Compute Pool:**
```yaml
Name: ONTOLOGY_COMPUTE_POOL
Instance Family: CPU_X64_S
Min Instances: 1
Max Instances: 3
Auto Resume: true
Auto Suspend: 1 hour
```

**Service Resources:**
```yaml
Backend:
  Memory: 2Gi (request) / 4Gi (limit)
  CPU: 1 (request) / 2 (limit)
  
Frontend:
  Memory: 1Gi (request) / 2Gi (limit)
  CPU: 0.5 (request) / 1 (limit)
```

**Estimated Costs:**
- Compute Pool: ~$2-6/hour when running (depends on region)
- Storage: ~$23/TB/month for data
- Image Repository: ~$23/TB/month
- Auto-suspend reduces costs significantly

---

## Local Development

### Step-by-Step Setup

**1. Prepare Environment**

```bash
# Navigate to project directory
cd /path/to/snowflake-ontology

# Copy environment file
cp backend/.env.example .env

# Edit with your credentials
nano .env
```

**2. Setup Database**

```bash
# Create database schema
snow sql -f sql/setup_database.sql

# Verify tables created
snow sql -q "USE DATABASE ONTOLOGY_DB; SHOW TABLES;"
```

**3. Start Services**

```bash
# Start with docker-compose
./scripts/local_dev.sh

# Or manually:
docker-compose up --build -d

# View logs
docker-compose logs -f
```

**4. Access Application**

```
Frontend:  http://localhost
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/docs
```

**5. Stop Services**

```bash
# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Local Development Architecture

```
┌─────────────────────────────────────────────────────┐
│              Local Machine                           │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │         Docker Compose                          │ │
│  │                                                  │ │
│  │  ┌──────────────┐      ┌──────────────┐       │ │
│  │  │   Backend    │      │   Frontend   │       │ │
│  │  │   Container  │◄────►│   Container  │       │ │
│  │  │              │      │              │       │ │
│  │  │   FastAPI    │      │   Nginx      │       │ │
│  │  │   Port 8000  │      │   Port 80    │       │ │
│  │  └──────┬───────┘      └──────────────┘       │ │
│  │         │                                       │ │
│  └─────────┼───────────────────────────────────────┘ │
│            │                                          │
└────────────┼──────────────────────────────────────────┘
             │
             │ Network
             │
┌────────────▼──────────────────────────────────────────┐
│                 Snowflake Cloud                        │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │           ONTOLOGY_DB Database                    │ │
│  │                                                    │ │
│  │  - ENTITIES                                       │ │
│  │  - RELATIONSHIPS                                  │ │
│  │  - ENTITY_STATES                                  │ │
│  │  - WORKFLOW_DEFINITIONS                           │ │
│  │  - WORKFLOW_EXECUTIONS                            │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

### Development Workflow

**1. Make Code Changes**

```bash
# Edit backend code
nano backend/main.py

# Edit frontend code
nano frontend/src/pages/Dashboard.tsx
```

**2. Rebuild and Restart**

```bash
# Rebuild specific service
docker-compose up --build -d backend

# Or rebuild all
docker-compose up --build -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

**3. Test Changes**

```bash
# Test backend
curl http://localhost:8000/health

# Test frontend
open http://localhost

# Run backend tests (if available)
docker-compose exec backend pytest

# Run frontend tests (if available)
docker-compose exec frontend npm test
```

**4. Debug Issues**

```bash
# View logs
docker-compose logs -f

# Execute commands in container
docker-compose exec backend bash
docker-compose exec frontend sh

# Check container status
docker-compose ps

# Restart service
docker-compose restart backend
```

---

## Configuration

### Environment Variables

**Backend (.env):**
```bash
# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account.region
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ONTOLOGY_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
MAX_CONNECTIONS=10
QUERY_TIMEOUT=300

# CORS Settings (for local dev)
CORS_ORIGINS=http://localhost,http://localhost:80
```

**Frontend (build-time):**
```bash
# API URL (set during Docker build)
VITE_API_URL=http://localhost:8000  # Local
VITE_API_URL=https://api-endpoint   # Production
```

### Service Specifications

**Single Service (spcs/service_spec_single.yaml):**
```yaml
spec:
  containers:
    - name: backend
      image: /ontology_db/public/ontology_backend_image:latest
      env:
        SNOWFLAKE_ACCOUNT:
          value: "{{ SNOWFLAKE_ACCOUNT }}"
        # ... other env vars
      resources:
        requests:
          memory: 2Gi
          cpu: "1"
        limits:
          memory: 4Gi
          cpu: "2"
    - name: frontend
      image: /ontology_db/public/ontology_frontend_image:latest
      resources:
        requests:
          memory: 1Gi
          cpu: "0.5"
        limits:
          memory: 2Gi
          cpu: "1"
  endpoints:
    - name: web
      port: 80
      public: true
    - name: api
      port: 8000
      public: true
```

### Database Configuration

**Warehouse Settings:**
```sql
-- Create or modify warehouse
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
  WAREHOUSE_SIZE = 'SMALL'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

-- For production, consider larger size
ALTER WAREHOUSE COMPUTE_WH SET WAREHOUSE_SIZE = 'MEDIUM';
```

**Database Settings:**
```sql
-- Set retention period
ALTER DATABASE ONTOLOGY_DB SET DATA_RETENTION_TIME_IN_DAYS = 7;

-- Enable change tracking
ALTER TABLE ENTITIES SET CHANGE_TRACKING = TRUE;
ALTER TABLE ENTITY_STATES SET CHANGE_TRACKING = TRUE;
```

---

## Post-Deployment

### Verification Steps

**1. Check Service Status**

```bash
# List services
snow sql -q "SHOW SERVICES IN DATABASE ONTOLOGY_DB;"

# Get service status
snow sql -q "SELECT SYSTEM\$GET_SERVICE_STATUS('ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE');"

# Expected output: {"status":"READY","message":"Running"}
```

**2. Test Endpoints**

```bash
# Get endpoints
snow sql -q "SHOW ENDPOINTS IN SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;"

# Test health endpoint
curl https://your-api-endpoint/health

# Expected: {"status":"healthy"}
```

**3. Test Frontend**

```bash
# Open frontend URL in browser
open https://your-frontend-endpoint

# Should see:
# - Dashboard loads
# - No errors in browser console
# - Statistics display (may be 0)
```

**4. Test API**

```bash
# Test API docs
open https://your-api-endpoint/docs

# Create test entity
curl -X POST https://your-api-endpoint/entities \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "TEST",
    "label": "Test Entity",
    "properties": {},
    "tags": ["test"]
  }'

# List entities
curl https://your-api-endpoint/entities

# Delete test entity
curl -X DELETE https://your-api-endpoint/entities/{entity_id}
```

**5. Verify Database**

```sql
-- Check tables exist
USE DATABASE ONTOLOGY_DB;
SHOW TABLES;

-- Check streams
SHOW STREAMS;

-- Check tasks
SHOW TASKS;

-- Check dynamic tables
SHOW DYNAMIC TABLES;

-- Verify data
SELECT COUNT(*) FROM ENTITIES;
SELECT COUNT(*) FROM RELATIONSHIPS;
```

### Initial Data Population

**Option 1: Use Sample Data Script**

```bash
# If you have a sample data script
snow sql -f sql/populate_sample_data.sql
```

**Option 2: Use API**

```python
import requests

BASE_URL = "https://your-api-endpoint"

# Create entities
entities = [
    {"entity_type": "CUSTOMER", "label": "Acme Corp", "tags": ["enterprise"]},
    {"entity_type": "ACCOUNT", "label": "Acme Account", "tags": ["active"]},
    {"entity_type": "PRODUCT", "label": "Widget Pro", "tags": ["premium"]},
]

for entity in entities:
    response = requests.post(f"{BASE_URL}/entities", json=entity)
    print(f"Created: {response.json()['entity_id']}")

# Create relationships
relationships = [
    {"subject_id": "customer-id", "predicate": "OWNS", "object_id": "account-id"},
    {"subject_id": "account-id", "predicate": "PURCHASED", "object_id": "product-id"},
]

for rel in relationships:
    response = requests.post(f"{BASE_URL}/relationships", json=rel)
    print(f"Created relationship: {response.json()['relationship_id']}")
```

**Option 3: Manual Entry**

Use the UI to manually create entities and relationships.

### Save Deployment Information

```bash
# Save endpoint URLs
snow sql -q "SHOW ENDPOINTS IN SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;" > CURRENT_ENDPOINTS.txt

# Save service details
snow sql -q "DESCRIBE SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;" > SERVICE_DETAILS.txt

# Document in version control
echo "Frontend: https://your-frontend-endpoint" > DEPLOYMENT_INFO.md
echo "API: https://your-api-endpoint" >> DEPLOYMENT_INFO.md
echo "API Docs: https://your-api-endpoint/docs" >> DEPLOYMENT_INFO.md
echo "Deployed: $(date)" >> DEPLOYMENT_INFO.md
```

---

## Monitoring & Maintenance

### Service Monitoring

**Check Service Health:**

```bash
# Service status
snow sql -q "SELECT SYSTEM\$GET_SERVICE_STATUS('ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE');"

# Service logs (last 100 lines)
snow sql -q "CALL SYSTEM\$GET_SERVICE_LOGS('ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE', 0, 'backend', 100);"
snow sql -q "CALL SYSTEM\$GET_SERVICE_LOGS('ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE', 0, 'frontend', 100);"

# Compute pool status
snow sql -q "DESCRIBE COMPUTE POOL ONTOLOGY_COMPUTE_POOL;"
```

**Monitor Resource Usage:**

```sql
-- Compute pool history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.COMPUTE_POOL_HISTORY(
  COMPUTE_POOL_NAME => 'ONTOLOGY_COMPUTE_POOL'
))
ORDER BY START_TIME DESC
LIMIT 100;

-- Service history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.SERVICE_HISTORY(
  SERVICE_NAME => 'ONTOLOGY_SERVICE'
))
ORDER BY START_TIME DESC
LIMIT 100;

-- Query history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE DATABASE_NAME = 'ONTOLOGY_DB'
ORDER BY START_TIME DESC
LIMIT 100;
```

### Application Monitoring

**Database Metrics:**

```sql
-- Entity counts by type
SELECT entity_type, COUNT(*) as count
FROM ENTITIES
GROUP BY entity_type
ORDER BY count DESC;

-- Relationship counts by predicate
SELECT predicate, COUNT(*) as count
FROM RELATIONSHIPS
GROUP BY predicate
ORDER BY count DESC;

-- Workflow execution stats
SELECT 
  status,
  COUNT(*) as count,
  AVG(DATEDIFF('second', started_at, completed_at)) as avg_duration_sec
FROM WORKFLOW_EXECUTIONS
WHERE started_at > DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY status;

-- Failed workflows
SELECT *
FROM WORKFLOW_EXECUTIONS
WHERE status = 'FAILED'
ORDER BY started_at DESC
LIMIT 20;
```

**Health Checks:**

```bash
# Automated health check script
cat > check_health.sh <<'EOF'
#!/bin/bash

API_URL="https://your-api-endpoint"

# Check health endpoint
if curl -sf "$API_URL/health" > /dev/null; then
  echo "✓ API is healthy"
else
  echo "✗ API is down"
  exit 1
fi

# Check entity count
ENTITY_COUNT=$(curl -s "$API_URL/entities" | jq 'length')
echo "✓ Entity count: $ENTITY_COUNT"

# Check workflow count
WORKFLOW_COUNT=$(curl -s "$API_URL/workflows" | jq 'length')
echo "✓ Workflow count: $WORKFLOW_COUNT"

echo "✓ All checks passed"
EOF

chmod +x check_health.sh
./check_health.sh
```

### Maintenance Tasks

**Daily:**
- Check service status
- Review error logs
- Monitor resource usage

**Weekly:**
- Review workflow execution history
- Check for failed workflows
- Analyze query performance
- Review entity/relationship growth

**Monthly:**
- Archive old workflow executions
- Optimize database tables
- Review and update workflows
- Check for security updates
- Review access logs

**Quarterly:**
- Review resource allocation
- Optimize compute pool size
- Review and update documentation
- Security audit
- Disaster recovery test

---

## Troubleshooting

### Service Won't Start

**Symptoms:**
- Service status shows "FAILED" or "PENDING"
- Endpoints not available

**Solutions:**

```bash
# Check service logs
snow sql -q "CALL SYSTEM\$GET_SERVICE_LOGS('ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE', 0, 'backend', 100);"

# Check compute pool
snow sql -q "DESCRIBE COMPUTE POOL ONTOLOGY_COMPUTE_POOL;"

# Verify images exist
snow sql -q "SHOW IMAGES IN IMAGE REPOSITORY ONTOLOGY_DB.PUBLIC.ONTOLOGY_IMAGES;"

# Restart service
snow sql -q "ALTER SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE SUSPEND;"
snow sql -q "ALTER SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE RESUME;"
```

### Image Push Fails

**Symptoms:**
- Docker push fails
- Authentication errors

**Solutions:**

```bash
# Re-authenticate
REPO_URL=$(snow sql -q "SHOW IMAGE REPOSITORIES LIKE 'ONTOLOGY_IMAGES'" --format json | jq -r '.[0].repository_url')
echo "$SNOWFLAKE_PASSWORD" | docker login $REPO_URL -u $SNOWFLAKE_USER --password-stdin

# Verify credentials
docker login $REPO_URL -u $SNOWFLAKE_USER

# Retry push
docker push $REPO_URL/ontology_backend_image:latest
```

### Database Connection Fails

**Symptoms:**
- Backend logs show connection errors
- API returns 500 errors

**Solutions:**

```bash
# Test connection from local machine
snow sql -q "SELECT CURRENT_USER();"

# Check warehouse is running
snow sql -q "SHOW WAREHOUSES LIKE 'COMPUTE_WH';"

# Resume warehouse if suspended
snow sql -q "ALTER WAREHOUSE COMPUTE_WH RESUME;"

# Verify credentials in service spec
cat spcs/service_spec_single.yaml
```

### Performance Issues

**Symptoms:**
- Slow API responses
- Timeouts
- High resource usage

**Solutions:**

```sql
-- Check query performance
SELECT *
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE DATABASE_NAME = 'ONTOLOGY_DB'
  AND EXECUTION_TIME > 10000  -- 10 seconds
ORDER BY EXECUTION_TIME DESC
LIMIT 20;

-- Optimize warehouse size
ALTER WAREHOUSE COMPUTE_WH SET WAREHOUSE_SIZE = 'MEDIUM';

-- Scale compute pool
ALTER COMPUTE POOL ONTOLOGY_COMPUTE_POOL SET MAX_INSTANCES = 5;

-- Add indexes (if not present)
-- Note: Snowflake auto-optimizes, but you can cluster tables
ALTER TABLE ENTITIES CLUSTER BY (entity_type, created_at);
```

---

## Scaling & Performance

### Horizontal Scaling

**Increase Service Instances:**

```sql
-- Scale up
ALTER SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE
  SET MIN_INSTANCES = 2
  MAX_INSTANCES = 5;

-- Scale down
ALTER SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE
  SET MIN_INSTANCES = 1
  MAX_INSTANCES = 2;
```

### Vertical Scaling

**Increase Compute Pool Size:**

```sql
-- Larger instance family
ALTER COMPUTE POOL ONTOLOGY_COMPUTE_POOL
  SET INSTANCE_FAMILY = 'CPU_X64_M';  -- Medium instances

-- More nodes
ALTER COMPUTE POOL ONTOLOGY_COMPUTE_POOL
  SET MAX_NODES = 5;
```

**Increase Container Resources:**

Edit `spcs/service_spec_single.yaml`:

```yaml
resources:
  requests:
    memory: 4Gi  # Increased from 2Gi
    cpu: "2"     # Increased from 1
  limits:
    memory: 8Gi  # Increased from 4Gi
    cpu: "4"     # Increased from 2
```

Then redeploy:

```bash
./scripts/deploy.sh
```

### Database Optimization

**Clustering:**

```sql
-- Cluster frequently queried tables
ALTER TABLE ENTITIES CLUSTER BY (entity_type, created_at);
ALTER TABLE RELATIONSHIPS CLUSTER BY (subject_id, predicate);
ALTER TABLE ENTITY_STATES CLUSTER BY (entity_id, updated_at);
```

**Materialized Views:**

```sql
-- Create materialized views for common queries
CREATE OR REPLACE DYNAMIC TABLE ENTITY_SUMMARY
  TARGET_LAG = '1 minute'
  WAREHOUSE = COMPUTE_WH
AS
SELECT 
  entity_type,
  COUNT(*) as entity_count,
  COUNT(DISTINCT tags) as unique_tags,
  MAX(updated_at) as last_updated
FROM ENTITIES
GROUP BY entity_type;
```

**Query Optimization:**

```sql
-- Use result caching
ALTER SESSION SET USE_CACHED_RESULT = TRUE;

-- Optimize warehouse
ALTER WAREHOUSE COMPUTE_WH SET
  WAREHOUSE_SIZE = 'MEDIUM'
  MAX_CONCURRENCY_LEVEL = 8
  STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = 300
  STATEMENT_TIMEOUT_IN_SECONDS = 3600;
```

---

## Security Hardening

### Network Security

**Restrict Access:**

```sql
-- Create network rule for specific IPs
CREATE OR REPLACE NETWORK RULE ontology_api_rule
  MODE = INGRESS
  TYPE = IPV4
  VALUE_LIST = ('203.0.113.0/24', '198.51.100.0/24');

-- Apply to service
ALTER SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE
  SET NETWORK_RULES = (ontology_api_rule);
```

### Authentication

**Use Snowflake Secrets:**

```sql
-- Create secret for database password
CREATE OR REPLACE SECRET ontology_db_password
  TYPE = PASSWORD
  USERNAME = 'ontology_user'
  PASSWORD = 'your_secure_password';

-- Grant usage
GRANT USAGE ON SECRET ontology_db_password TO ROLE your_role;
```

Update service spec to use secret:

```yaml
env:
  SNOWFLAKE_PASSWORD:
    secretKeyRef:
      name: ontology_db_password
      key: password
```

### Role-Based Access Control

```sql
-- Create roles
CREATE ROLE IF NOT EXISTS ontology_admin;
CREATE ROLE IF NOT EXISTS ontology_user;
CREATE ROLE IF NOT EXISTS ontology_readonly;

-- Grant permissions
GRANT ALL ON DATABASE ONTOLOGY_DB TO ROLE ontology_admin;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA ONTOLOGY_DB.PUBLIC TO ROLE ontology_user;
GRANT SELECT ON ALL TABLES IN SCHEMA ONTOLOGY_DB.PUBLIC TO ROLE ontology_readonly;

-- Grant service usage
GRANT USAGE ON SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE TO ROLE ontology_user;
```

### Audit Logging

```sql
-- Enable query logging
ALTER ACCOUNT SET QUERY_TAG = 'ontology_app';

-- Create audit table
CREATE TABLE IF NOT EXISTS AUDIT_LOG (
  log_id VARCHAR PRIMARY KEY DEFAULT UUID_STRING(),
  user_name VARCHAR,
  action VARCHAR,
  entity_id VARCHAR,
  timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  details VARIANT
);

-- Query audit logs
SELECT *
FROM AUDIT_LOG
WHERE timestamp > DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY timestamp DESC;
```

---

## Backup & Recovery

### Database Backup

**Time Travel:**

```sql
-- Query historical data (within retention period)
SELECT * FROM ENTITIES AT(OFFSET => -3600);  -- 1 hour ago
SELECT * FROM ENTITIES BEFORE(TIMESTAMP => '2026-01-30 10:00:00');

-- Restore deleted data
CREATE TABLE ENTITIES_RESTORED AS
SELECT * FROM ENTITIES AT(OFFSET => -3600);

-- Restore entire table
CREATE OR REPLACE TABLE ENTITIES AS
SELECT * FROM ENTITIES AT(OFFSET => -3600);
```

**Cloning:**

```sql
-- Clone database
CREATE DATABASE ONTOLOGY_DB_BACKUP
  CLONE ONTOLOGY_DB;

-- Clone specific table
CREATE TABLE ENTITIES_BACKUP
  CLONE ENTITIES;

-- Clone at specific time
CREATE TABLE ENTITIES_BACKUP
  CLONE ENTITIES AT(TIMESTAMP => '2026-01-30 10:00:00');
```

**Export Data:**

```sql
-- Export to stage
COPY INTO @ONTOLOGY_STAGE/backups/entities/
FROM ENTITIES
FILE_FORMAT = (TYPE = 'JSON')
OVERWRITE = TRUE;

-- Export to external stage (S3, Azure, GCS)
COPY INTO @my_external_stage/backups/entities/
FROM ENTITIES
FILE_FORMAT = (TYPE = 'JSON');
```

### Service Backup

**Export Service Configuration:**

```bash
# Export service spec
snow sql -q "DESCRIBE SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;" > service_backup.txt

# Export compute pool config
snow sql -q "DESCRIBE COMPUTE POOL ONTOLOGY_COMPUTE_POOL;" > compute_pool_backup.txt

# Backup service specs
cp spcs/service_spec_single.yaml backups/service_spec_$(date +%Y%m%d).yaml
```

**Backup Docker Images:**

```bash
# Pull images from Snowflake
docker pull $REPO_URL/ontology_backend_image:latest
docker pull $REPO_URL/ontology_frontend_image:latest

# Tag for backup
docker tag $REPO_URL/ontology_backend_image:latest ontology_backend_backup:$(date +%Y%m%d)
docker tag $REPO_URL/ontology_frontend_image:latest ontology_frontend_backup:$(date +%Y%m%d)

# Save to tar
docker save ontology_backend_backup:$(date +%Y%m%d) | gzip > backend_backup_$(date +%Y%m%d).tar.gz
docker save ontology_frontend_backup:$(date +%Y%m%d) | gzip > frontend_backup_$(date +%Y%m%d).tar.gz
```

### Disaster Recovery

**Recovery Plan:**

1. **Assess Damage**
   - Identify what was lost
   - Determine recovery point objective (RPO)
   - Determine recovery time objective (RTO)

2. **Restore Database**
   ```sql
   -- Restore from Time Travel
   CREATE OR REPLACE DATABASE ONTOLOGY_DB AS
   SELECT * FROM ONTOLOGY_DB_BACKUP;
   
   -- Or restore from clone
   CREATE DATABASE ONTOLOGY_DB
   CLONE ONTOLOGY_DB_BACKUP;
   ```

3. **Redeploy Services**
   ```bash
   # Redeploy from backup
   ./scripts/deploy.sh
   ```

4. **Verify Recovery**
   ```bash
   # Check data
   snow sql -q "SELECT COUNT(*) FROM ONTOLOGY_DB.PUBLIC.ENTITIES;"
   
   # Check services
   snow sql -q "SHOW SERVICES IN DATABASE ONTOLOGY_DB;"
   
   # Test application
   curl https://your-api-endpoint/health
   ```

5. **Post-Recovery**
   - Document incident
   - Update recovery procedures
   - Review backup strategy
   - Implement preventive measures

---

## Appendix

### Useful Commands

**Service Management:**
```bash
# List services
snow sql -q "SHOW SERVICES;"

# Suspend service
snow sql -q "ALTER SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE SUSPEND;"

# Resume service
snow sql -q "ALTER SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE RESUME;"

# Drop service
snow sql -q "DROP SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;"
```

**Compute Pool Management:**
```bash
# List compute pools
snow sql -q "SHOW COMPUTE POOLS;"

# Suspend compute pool
snow sql -q "ALTER COMPUTE POOL ONTOLOGY_COMPUTE_POOL SUSPEND;"

# Resume compute pool
snow sql -q "ALTER COMPUTE POOL ONTOLOGY_COMPUTE_POOL RESUME;"

# Drop compute pool
snow sql -q "DROP COMPUTE POOL ONTOLOGY_COMPUTE_POOL;"
```

**Image Management:**
```bash
# List images
snow sql -q "SHOW IMAGES IN IMAGE REPOSITORY ONTOLOGY_DB.PUBLIC.ONTOLOGY_IMAGES;"

# Remove old images
snow sql -q "DROP IMAGE ONTOLOGY_DB.PUBLIC.ONTOLOGY_IMAGES/ontology_backend_image:old_tag;"
```

### Cost Optimization

**Tips:**
- Use auto-suspend for compute pools (1 hour)
- Use smaller warehouse for development
- Monitor and optimize query performance
- Archive old data
- Use result caching
- Scale down during off-hours
- Use spot instances (if available)

**Estimated Monthly Costs:**
```
Compute Pool (CPU_X64_S):
  - Running 24/7: ~$1,440/month
  - With auto-suspend (8h/day): ~$480/month
  - Development (4h/day): ~$240/month

Storage:
  - 100GB data: ~$2.30/month
  - 10GB images: ~$0.23/month

Total Estimate:
  - Production: $482-1,442/month
  - Development: $242-482/month
```

---

**Version:** 1.0.0  
**Last Updated:** January 30, 2026  
**Built with ❄️ on Snowflake SPCS**
