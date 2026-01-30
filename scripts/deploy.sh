#!/bin/bash

# Deployment script for Snowflake SPCS
# This script builds, tags, and pushes Docker images, then creates services
# Usage:
#   ./deploy.sh           - Deploy the application
#   ./deploy.sh --undeploy - Remove the deployment

set -e

# Function to perform teardown
undeploy() {
    echo "======================================"
    echo "Snowflake Ontology Engine - Teardown"
    echo "======================================"
    
    # Confirm teardown
    read -p "Are you sure you want to teardown the deployment? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Teardown cancelled"
        exit 0
    fi
    
    echo ""
    echo "Step 1: Dropping services..."
    snow sql -q "DROP SERVICE IF EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_FRONTEND_SERVICE;" || true
    snow sql -q "DROP SERVICE IF EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_BACKEND_SERVICE;" || true
    
    echo ""
    echo "Step 2: Dropping compute pool..."
    snow sql -q "DROP COMPUTE POOL IF EXISTS ONTOLOGY_COMPUTE_POOL;" || true
    
    echo ""
    read -p "Do you want to drop the database and all data? (yes/no): " drop_db
    if [ "$drop_db" = "yes" ]; then
        echo "Dropping database..."
        snow sql -q "DROP DATABASE IF EXISTS ONTOLOGY_DB;" || true
        echo "Database dropped"
    else
        echo "Database preserved"
    fi
    
    echo ""
    echo "======================================"
    echo "Teardown completed!"
    echo "======================================"
    exit 0
}

# Check for undeploy flag
if [ "$1" = "--undeploy" ] || [ "$1" = "-u" ]; then
    undeploy
fi

echo "======================================"
echo "Snowflake Ontology Engine - Deployment"
echo "======================================"

# Load environment variables
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "Loaded environment variables from .env"
fi

# Check required environment variables
if [ -z "$SNOWFLAKE_ACCOUNT" ]; then
    echo "Error: SNOWFLAKE_ACCOUNT not set"
    exit 1
fi

# Get Snowflake connection details
echo ""
echo "Using Snowflake account: $SNOWFLAKE_ACCOUNT"

# Step 1: Setup database schema
echo ""
echo "Step 1: Setting up database schema..."
snow sql -f sql/setup_database.sql

# Step 2: Setup SPCS infrastructure
echo ""
echo "Step 2: Setting up SPCS infrastructure..."
snow sql -f scripts/setup_spcs.sql

# Step 3: Get image repository URL
echo ""
echo "Step 3: Getting image repository URL..."
REPO_URL=$(snow sql -q "SHOW IMAGE REPOSITORIES LIKE 'ONTOLOGY_IMAGES' IN SCHEMA ONTOLOGY_DB.PUBLIC" --format json | jq -r '.[0].repository_url')

if [ -z "$REPO_URL" ]; then
    echo "Error: Could not get repository URL"
    exit 1
fi

echo "Repository URL: $REPO_URL"

# Step 4: Docker login to Snowflake registry
echo ""
echo "Step 4: Logging into Snowflake container registry..."

# Get credentials from Snowflake CLI connection
if [ -z "$SNOWFLAKE_USER" ] || [ -z "$SNOWFLAKE_PASSWORD" ]; then
    echo "Getting credentials from Snowflake CLI connection..."
    SNOWFLAKE_USER=$(snow connection list --format json | jq -r '.[] | select(.is_default == true) | .parameters.user' 2>/dev/null)
    
    # Try to get password from connections.toml
    if [ -f "$HOME/.snowflake/connections.toml" ]; then
        # Get the default connection name
        DEFAULT_CONN=$(snow connection list --format json | jq -r '.[] | select(.is_default == true) | .connection_name' 2>/dev/null)
        if [ -n "$DEFAULT_CONN" ]; then
            SNOWFLAKE_PASSWORD=$(grep -A 5 "\[$DEFAULT_CONN\]" "$HOME/.snowflake/connections.toml" | grep "password" | cut -d'"' -f2)
        fi
    fi
fi

if [ -z "$SNOWFLAKE_USER" ]; then
    echo "Error: SNOWFLAKE_USER not found. Please configure Snowflake CLI connection."
    exit 1
fi

if [ -z "$SNOWFLAKE_PASSWORD" ]; then
    echo "Error: SNOWFLAKE_PASSWORD not found. Please set it in .env file or Snowflake CLI connection."
    exit 1
fi

echo "Authenticating as user: $SNOWFLAKE_USER"
echo "$SNOWFLAKE_PASSWORD" | docker login $REPO_URL -u $SNOWFLAKE_USER --password-stdin

# Step 5: Build and push backend image
echo ""
echo "Step 5: Building and pushing backend image..."
cd backend
docker build --platform linux/amd64 -t ontology-backend:latest .
docker tag ontology-backend:latest $REPO_URL/ontology_backend_image:latest
docker push $REPO_URL/ontology_backend_image:latest
cd ..

# Step 6: Build and push frontend image
echo ""
echo "Step 6: Building and pushing frontend image..."
cd frontend
docker build --platform linux/amd64 -t ontology-frontend:latest .
docker tag ontology-frontend:latest $REPO_URL/ontology_frontend_image:latest
docker push $REPO_URL/ontology_frontend_image:latest
cd ..

# Step 7: Create single service with frontend and backend
echo ""
echo "Step 7: Creating single service with frontend (nginx proxy) and backend..."

# Copy service spec to stage
snow sql -q "PUT file://$(pwd)/spcs/service_spec_single.yaml @ONTOLOGY_DB.PUBLIC.ONTOLOGY_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;"

# Drop existing services if they exist
snow sql -q "DROP SERVICE IF EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;" || true
snow sql -q "DROP SERVICE IF EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_BACKEND_SERVICE;" || true
snow sql -q "DROP SERVICE IF EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_FRONTEND_SERVICE;" || true

# Create single service
snow sql -q "
CREATE SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE
  IN COMPUTE POOL ONTOLOGY_COMPUTE_POOL
  FROM @ONTOLOGY_DB.PUBLIC.ONTOLOGY_STAGE
  SPECIFICATION_FILE = 'service_spec_single.yaml'
  MIN_INSTANCES = 1
  MAX_INSTANCES = 2
  COMMENT = 'Ontology Engine - Single Service with Frontend (Nginx) and Backend (FastAPI)';
"

# Step 8: Wait for service to be ready
echo ""
echo "Step 8: Waiting for service to be ready..."
sleep 30

# Step 9: Get service endpoints
echo ""
echo "Step 9: Getting service endpoints..."
echo ""
snow sql -q "SHOW ENDPOINTS IN SERVICE ONTOLOGY_DB.PUBLIC.ONTOLOGY_SERVICE;"

echo ""
echo "======================================"
echo "Deployment completed successfully!"
echo "======================================"
echo ""
echo "Access your application:"
echo "1. Get the frontend endpoint URL from above"
echo "2. Open it in your browser"
echo ""
echo "To check service status:"
echo "  snow sql -q 'SHOW SERVICES IN DATABASE ONTOLOGY_DB;'"
echo ""
echo "To view service logs:"
echo "  snow object stage list @ONTOLOGY_DB.PUBLIC.ONTOLOGY_STAGE"
echo ""
