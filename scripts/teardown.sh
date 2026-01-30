#!/bin/bash

# Teardown script for Snowflake SPCS deployment
# This script removes all services and optionally the database

set -e

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
snow sql -q "DROP SERVICE IF EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_FRONTEND_SERVICE;"
snow sql -q "DROP SERVICE IF EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_BACKEND_SERVICE;"

echo ""
echo "Step 2: Dropping compute pool..."
snow sql -q "DROP COMPUTE POOL IF EXISTS ONTOLOGY_COMPUTE_POOL;"

echo ""
read -p "Do you want to drop the database and all data? (yes/no): " drop_db
if [ "$drop_db" = "yes" ]; then
    echo "Dropping database..."
    snow sql -q "DROP DATABASE IF EXISTS ONTOLOGY_DB;"
    echo "Database dropped"
else
    echo "Database preserved"
fi

echo ""
echo "======================================"
echo "Teardown completed!"
echo "======================================"
