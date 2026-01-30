#!/bin/bash

# Local development script
# Runs the application locally using docker-compose

set -e

echo "======================================"
echo "Snowflake Ontology Engine - Local Dev"
echo "======================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp backend/.env.example .env
    echo ""
    echo "Please edit .env file with your Snowflake credentials"
    echo "Then run this script again"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check required variables
if [ -z "$SNOWFLAKE_ACCOUNT" ] || [ -z "$SNOWFLAKE_USER" ] || [ -z "$SNOWFLAKE_PASSWORD" ]; then
    echo "Error: Missing required Snowflake credentials in .env"
    exit 1
fi

echo ""
echo "Step 1: Setting up database schema..."
snow sql -f sql/setup_database.sql

echo ""
echo "Step 2: Starting services with docker-compose..."
docker-compose up --build -d

echo ""
echo "Step 3: Waiting for services to be ready..."
sleep 10

echo ""
echo "======================================"
echo "Local development environment ready!"
echo "======================================"
echo ""
echo "Frontend: http://localhost"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
