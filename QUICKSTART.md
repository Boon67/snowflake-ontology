# ⚡ Quick Start Guide - Snowflake Ontology & Workflow Engine

Get up and running in 10 minutes!

---

## 🎯 Goal

Deploy the Snowflake Ontology & Workflow Engine and create your first entity, relationship, and workflow.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ Snowflake account (with SPCS enabled)
- ✅ ACCOUNTADMIN role or equivalent
- ✅ Docker installed and running
- ✅ 10 minutes of time

---

## 🚀 5-Step Deployment

### Step 1: Install Snow CLI (2 minutes)

```bash
# Install Snow CLI
pip install snowflake-cli-labs

# Verify installation
snow --version
```

### Step 2: Configure Snowflake Connection (2 minutes)

```bash
# Add connection
snow connection add

# Follow prompts:
# - Connection name: default
# - Account: your_account.region (e.g., abc12345.us-east-1)
# - User: your_username
# - Password: your_password
# - Role: ACCOUNTADMIN
# - Warehouse: COMPUTE_WH
# - Database: (leave blank)
# - Schema: (leave blank)

# Test connection
snow connection test
```

**Finding Your Account Identifier:**
- Log into Snowflake web UI
- Look at URL: `https://app.snowflake.com/REGION/ACCOUNT/`
- Or run: `SELECT CURRENT_ACCOUNT();` in a worksheet

### Step 3: Clone Repository (1 minute)

```bash
# Clone from GitHub
git clone https://github.com/Boon67/snowflake-ontology.git
cd snowflake-ontology

# Or if you already have it
cd /path/to/snowflake-ontology
```

### Step 4: Configure Environment (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor

# Required variables:
# SNOWFLAKE_ACCOUNT=your_account.region
# SNOWFLAKE_USER=your_username
# SNOWFLAKE_PASSWORD=your_password
# SNOWFLAKE_WAREHOUSE=COMPUTE_WH
# SNOWFLAKE_DATABASE=ONTOLOGY_DB
# SNOWFLAKE_SCHEMA=PUBLIC
# SNOWFLAKE_ROLE=ACCOUNTADMIN
```

### Step 5: Deploy! (4 minutes)

```bash
# Make script executable
chmod +x scripts/deploy.sh

# Run deployment
./scripts/deploy.sh

# Wait for deployment to complete...
# This will:
# ✓ Create database schema
# ✓ Setup SPCS infrastructure
# ✓ Build Docker images
# ✓ Deploy services
# ✓ Display endpoints
```

**Expected Output:**
```
======================================
Snowflake Ontology Engine - Deployment
======================================
Step 1: Setting up database schema...
Step 2: Setting up SPCS infrastructure...
Step 3: Getting image repository URL...
Step 4: Logging into Snowflake container registry...
Step 5: Building and pushing backend image...
Step 6: Building and pushing frontend image...
Step 7: Creating single service...
Step 8: Waiting for service to be ready...
Step 9: Getting service endpoints...
======================================
Deployment completed successfully!
======================================

Access your application:
Frontend: https://abc123-ontology-service.snowflakecomputing.app
API: https://abc123-ontology-service-api.snowflakecomputing.app
API Docs: https://abc123-ontology-service-api.snowflakecomputing.app/docs
```

---

## 🎉 You're Live!

### Access Your Application

1. **Open Frontend**
   - Copy the frontend URL from deployment output
   - Open in your browser
   - You should see the Dashboard

2. **Check API Docs**
   - Copy the API URL from deployment output
   - Add `/docs` to the end
   - Open in your browser
   - You should see interactive API documentation

3. **Verify Everything Works**
   - Dashboard should show 0 entities, 0 relationships
   - All menu items should be accessible
   - No errors in browser console (F12)

---

## 🏃 First Steps - Create Your First Data

### Create Your First Entity (1 minute)

1. **Navigate to Entities Page**
   - Click "Entities" in the navigation menu

2. **Click "+ Add Entity"**

3. **Fill in the Form:**
   ```
   Entity Type: CUSTOMER
   Label: Acme Corporation
   Properties (JSON):
   {
     "industry": "Technology",
     "size": "Enterprise",
     "revenue": 50000000,
     "employees": 5000
   }
   Tags: enterprise, technology, active
   ```

4. **Click "Create"**

5. **Success!** Your first entity appears in the tree view under "CUSTOMER"

### Create Your Second Entity (1 minute)

1. **Click "+ Add Entity" again**

2. **Fill in the Form:**
   ```
   Entity Type: ACCOUNT
   Label: Acme Enterprise Account
   Properties (JSON):
   {
     "account_type": "Enterprise",
     "status": "Active",
     "created_date": "2024-01-15"
   }
   Tags: active, enterprise
   ```

3. **Click "Create"**

### Create Your First Relationship (1 minute)

1. **Navigate to Relationships Page**
   - Click "Relationships" in the navigation menu

2. **Click "+ Add Relationship"**

3. **Fill in the Form:**
   ```
   Subject Entity: Acme Corporation (CUSTOMER)
   Predicate: OWNS
   Object Entity: Acme Enterprise Account (ACCOUNT)
   Properties (JSON):
   {
     "since": "2024-01-15",
     "type": "primary"
   }
   ```

4. **Click "Create"**

5. **Success!** Your relationship appears in the table

### View Your Graph (1 minute)

1. **Navigate to Graph View**
   - Click "Graph View" in the navigation menu

2. **See Your Data Visualized**
   - You should see 2 nodes (Customer and Account)
   - Connected by an arrow labeled "OWNS"
   - Color-coded by entity type

3. **Interact with the Graph**
   - Click and drag nodes to move them
   - Zoom in/out with mouse wheel
   - Click a node to see details panel

### Create Your First Workflow (2 minutes)

1. **Navigate to Workflows Page**
   - Click "Workflows" in the navigation menu

2. **Click "+ Create Workflow"**

3. **Fill in the Form:**
   ```
   Name: Customer At-Risk Alert
   Description: Send notification when customer becomes at-risk
   ```

4. **Build Trigger Condition:**
   - Click "+ Add Condition"
   - Field: entity_type
   - Operator: =
   - Value: CUSTOMER
   - Click "+ Add Condition" again
   - Field: current_state
   - Operator: =
   - Value: AT_RISK

5. **Configure Action:**
   ```
   Action Type: NOTIFICATION
   Action Config (JSON):
   {
     "message": "Customer {{entity_label}} is at risk!",
     "severity": "HIGH"
   }
   Enabled: ✓ (checked)
   ```

6. **Click "Create"**

7. **Success!** Your workflow is created and enabled

---

## 🎓 Next Steps

### Learn More

1. **Explore the UI**
   - Try the search feature on Entities page
   - Expand/collapse entity types in tree view
   - Edit and delete entities
   - Create more relationships
   - View the interactive graph

2. **Read the Documentation**
   - **USER_GUIDE.md** - Complete user guide with all features
   - **DEPLOYMENT_GUIDE.md** - Detailed deployment and operations
   - **README.md** - Architecture and technical details
   - **API Docs** - Interactive API documentation at `/docs`

3. **Try the API**
   - Open API docs at your-api-endpoint/docs
   - Try out the endpoints directly
   - See request/response examples
   - Test with curl or Postman

4. **Populate Sample Data**
   - Create more entities of different types
   - Build a knowledge graph
   - Create workflows for automation
   - Test state transitions

### Common Use Cases

**Customer 360 View:**
```
1. Create CUSTOMER entity
2. Create ACCOUNT entities
3. Create ORDER entities
4. Create PRODUCT entities
5. Link with relationships:
   - Customer OWNS Account
   - Account HAS Order
   - Order CONTAINS Product
6. View in Graph View
```

**Data Lineage:**
```
1. Create TABLE entities (source tables)
2. Create VIEW entities (transformations)
3. Create REPORT entities (outputs)
4. Link with relationships:
   - View DERIVED_FROM Table
   - Report DEPENDS_ON View
5. View lineage in Graph View
```

**Workflow Automation:**
```
1. Create entities with states
2. Create workflows with triggers
3. Update entity state
4. Watch workflow execute automatically
5. Check execution history
```

---

## 🐛 Troubleshooting

### Deployment Failed?

**Check Prerequisites:**
```bash
# Verify Snow CLI
snow --version

# Verify Docker
docker ps

# Test Snowflake connection
snow connection test
```

**Common Issues:**

1. **"Snow CLI not found"**
   ```bash
   pip install snowflake-cli-labs
   ```

2. **"Docker not running"**
   - Start Docker Desktop
   - Or run: `sudo systemctl start docker` (Linux)

3. **"Connection failed"**
   - Verify credentials in .env file
   - Check account identifier format
   - Ensure warehouse exists and is running

4. **"Permission denied"**
   ```bash
   chmod +x scripts/deploy.sh
   ```

### Service Not Starting?

```bash
# Check service status
snow sql -q "SELECT SYSTEM\$GET_SERVICE_STATUS('ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE');"

# View logs
snow sql -q "CALL SYSTEM\$GET_SERVICE_LOGS('ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE', 0, 'backend', 100);"

# Restart service
snow sql -q "ALTER SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE SUSPEND;"
snow sql -q "ALTER SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE RESUME;"
```

### Frontend Not Loading?

1. **Check URL**
   - Ensure you're using the correct endpoint URL
   - Try both HTTP and HTTPS

2. **Check Browser Console**
   - Press F12 to open developer tools
   - Look for errors in Console tab
   - Check Network tab for failed requests

3. **Verify Service**
   ```bash
   snow sql -q "SHOW ENDPOINTS IN SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;"
   ```

### Need Help?

- **Documentation:** Check USER_GUIDE.md and DEPLOYMENT_GUIDE.md
- **GitHub Issues:** https://github.com/Boon67/snowflake-ontology/issues
- **Snowflake Community:** https://community.snowflake.com

---

## 🧹 Clean Up (Optional)

### Remove Everything

If you want to remove the deployment:

```bash
# Run teardown script
./scripts/teardown.sh

# Confirm when prompted
# This will:
# - Drop services
# - Drop compute pool
# - Optionally drop database
```

### Keep Database, Remove Services

```bash
# Drop services only
snow sql -q "DROP SERVICE IF EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;"

# Drop compute pool
snow sql -q "DROP COMPUTE POOL IF EXISTS ONTOLOGY_COMPUTE_POOL;"

# Database remains for later use
```

---

## 📚 Additional Resources

### Documentation

- **README.md** - Project overview and architecture
- **USER_GUIDE.md** - Complete user manual (100+ pages)
- **DEPLOYMENT_GUIDE.md** - Deployment and operations guide
- **API Documentation** - Available at `/docs` endpoint

### Links

- **GitHub Repository:** https://github.com/Boon67/snowflake-ontology
- **Snowflake Docs:** https://docs.snowflake.com
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **React Docs:** https://react.dev

### Support

- **Issues:** Report bugs on GitHub
- **Discussions:** Ask questions on GitHub Discussions
- **Community:** Join Snowflake Community forums

---

## ✅ Checklist

Use this checklist to track your progress:

**Setup:**
- [ ] Snow CLI installed
- [ ] Snowflake connection configured
- [ ] Repository cloned
- [ ] .env file configured
- [ ] Docker running

**Deployment:**
- [ ] Validation script passed
- [ ] Deployment completed successfully
- [ ] Frontend accessible
- [ ] API accessible
- [ ] API docs accessible

**First Data:**
- [ ] First entity created
- [ ] Second entity created
- [ ] First relationship created
- [ ] Graph view working
- [ ] First workflow created

**Learning:**
- [ ] Explored all UI pages
- [ ] Read USER_GUIDE.md
- [ ] Tried API endpoints
- [ ] Created sample data

---

## 🎉 Congratulations!

You've successfully deployed the Snowflake Ontology & Workflow Engine and created your first entities, relationships, and workflows!

**What's Next?**

1. **Build Your Knowledge Graph**
   - Add more entities
   - Create complex relationships
   - Visualize connections

2. **Automate with Workflows**
   - Create workflows for your use cases
   - Test state transitions
   - Monitor executions

3. **Integrate with Your Systems**
   - Use the API to import data
   - Connect to external services
   - Build custom integrations

4. **Share with Your Team**
   - Invite team members
   - Document your ontology
   - Establish governance

---

**Happy Building! 🚀**

Built with ❄️ on Snowflake SPCS

---

**Version:** 1.0.0  
**Last Updated:** January 30, 2026
