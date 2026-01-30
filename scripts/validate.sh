#!/bin/bash

# Validation script to check if everything is set up correctly
# Run this before deployment to catch issues early

set -e

echo "======================================"
echo "Snowflake Ontology Engine - Validation"
echo "======================================"

ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}✗ ERROR: $1${NC}"
    ERRORS=$((ERRORS + 1))
}

warning() {
    echo -e "${YELLOW}⚠ WARNING: $1${NC}"
    WARNINGS=$((WARNINGS + 1))
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo "ℹ $1"
}

echo ""
echo "Step 1: Checking prerequisites..."
echo "-----------------------------------"

# Check Snow CLI
if command -v snow &> /dev/null; then
    SNOW_VERSION=$(snow --version 2>&1 | head -n 1)
    success "Snow CLI installed: $SNOW_VERSION"
else
    error "Snow CLI not found. Install with: pip install snowflake-cli-labs"
fi

# Check Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    success "Docker installed: $DOCKER_VERSION"
    
    # Check if Docker is running
    if docker ps &> /dev/null; then
        success "Docker daemon is running"
    else
        error "Docker daemon is not running. Start Docker Desktop or Docker service."
    fi
else
    error "Docker not found. Install from: https://www.docker.com/get-started"
fi

# Check Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    success "Git installed: $GIT_VERSION"
else
    warning "Git not found. Recommended for version control."
fi

# Check jq (for JSON parsing)
if command -v jq &> /dev/null; then
    success "jq installed (for JSON parsing)"
else
    warning "jq not found. Install with: brew install jq (macOS) or apt-get install jq (Linux)"
fi

echo ""
echo "Step 2: Checking configuration files..."
echo "----------------------------------------"

# Check .env file
if [ -f .env ]; then
    success ".env file exists"
    
    # Check required variables
    source .env
    
    if [ -z "$SNOWFLAKE_ACCOUNT" ]; then
        error "SNOWFLAKE_ACCOUNT not set in .env"
    else
        success "SNOWFLAKE_ACCOUNT is set"
    fi
    
    if [ -z "$SNOWFLAKE_USER" ]; then
        error "SNOWFLAKE_USER not set in .env"
    else
        success "SNOWFLAKE_USER is set"
    fi
    
    if [ -z "$SNOWFLAKE_PASSWORD" ]; then
        error "SNOWFLAKE_PASSWORD not set in .env"
    else
        success "SNOWFLAKE_PASSWORD is set"
    fi
else
    error ".env file not found. Copy from .env.example and configure."
fi

# Check Snow CLI configuration
if [ -f ~/.snowflake/config.toml ]; then
    success "Snow CLI config exists (~/.snowflake/config.toml)"
else
    warning "Snow CLI config not found. Run: snow connection add"
fi

echo ""
echo "Step 3: Testing Snowflake connection..."
echo "----------------------------------------"

if command -v snow &> /dev/null && [ -f .env ]; then
    source .env
    
    # Test connection
    if snow sql -q "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE();" &> /dev/null; then
        success "Snowflake connection successful"
        
        # Get connection details
        USER_INFO=$(snow sql -q "SELECT CURRENT_USER() as user, CURRENT_ROLE() as role, CURRENT_WAREHOUSE() as warehouse;" --format json 2>/dev/null)
        if [ $? -eq 0 ]; then
            info "Connected as: $(echo $USER_INFO | jq -r '.[0].USER' 2>/dev/null || echo 'N/A')"
            info "Role: $(echo $USER_INFO | jq -r '.[0].ROLE' 2>/dev/null || echo 'N/A')"
            info "Warehouse: $(echo $USER_INFO | jq -r '.[0].WAREHOUSE' 2>/dev/null || echo 'N/A')"
        fi
    else
        error "Snowflake connection failed. Check credentials and network."
    fi
else
    warning "Skipping Snowflake connection test (prerequisites missing)"
fi

echo ""
echo "Step 4: Checking project structure..."
echo "--------------------------------------"

# Check backend files
if [ -f backend/main.py ]; then
    success "Backend main.py exists"
else
    error "Backend main.py not found"
fi

if [ -f backend/requirements.txt ]; then
    success "Backend requirements.txt exists"
else
    error "Backend requirements.txt not found"
fi

if [ -f backend/Dockerfile ]; then
    success "Backend Dockerfile exists"
else
    error "Backend Dockerfile not found"
fi

# Check frontend files
if [ -f frontend/package.json ]; then
    success "Frontend package.json exists"
else
    error "Frontend package.json not found"
fi

if [ -f frontend/Dockerfile ]; then
    success "Frontend Dockerfile exists"
else
    error "Frontend Dockerfile not found"
fi

if [ -f frontend/src/main.tsx ]; then
    success "Frontend main.tsx exists"
else
    error "Frontend main.tsx not found"
fi

# Check SQL files
if [ -f sql/setup_database.sql ]; then
    success "Database setup SQL exists"
else
    error "Database setup SQL not found"
fi

# Check SPCS files
if [ -f spcs/service_spec_backend.yaml ]; then
    success "Backend service spec exists"
else
    error "Backend service spec not found"
fi

if [ -f spcs/service_spec_frontend.yaml ]; then
    success "Frontend service spec exists"
else
    error "Frontend service spec not found"
fi

# Check scripts
if [ -f scripts/deploy.sh ]; then
    success "Deployment script exists"
    if [ -x scripts/deploy.sh ]; then
        success "Deployment script is executable"
    else
        warning "Deployment script is not executable. Run: chmod +x scripts/deploy.sh"
    fi
else
    error "Deployment script not found"
fi

echo ""
echo "Step 5: Validating Docker configurations..."
echo "--------------------------------------------"

# Validate backend Dockerfile
if [ -f backend/Dockerfile ]; then
    if grep -q "FROM python:3.11" backend/Dockerfile; then
        success "Backend Dockerfile uses Python 3.11"
    else
        warning "Backend Dockerfile may not use recommended Python version"
    fi
fi

# Validate frontend Dockerfile
if [ -f frontend/Dockerfile ]; then
    if grep -q "FROM node:20" frontend/Dockerfile; then
        success "Frontend Dockerfile uses Node 20"
    else
        warning "Frontend Dockerfile may not use recommended Node version"
    fi
fi

# Validate docker-compose.yml
if [ -f docker-compose.yml ]; then
    success "docker-compose.yml exists"
    
    if grep -q "backend:" docker-compose.yml && grep -q "frontend:" docker-compose.yml; then
        success "docker-compose.yml defines both services"
    else
        error "docker-compose.yml missing service definitions"
    fi
else
    error "docker-compose.yml not found"
fi

echo ""
echo "Step 6: Checking Python dependencies..."
echo "----------------------------------------"

if [ -f backend/requirements.txt ]; then
    # Check for key dependencies
    if grep -q "fastapi" backend/requirements.txt; then
        success "FastAPI dependency found"
    else
        error "FastAPI dependency missing"
    fi
    
    if grep -q "snowflake-connector-python" backend/requirements.txt; then
        success "Snowflake connector dependency found"
    else
        error "Snowflake connector dependency missing"
    fi
    
    if grep -q "uvicorn" backend/requirements.txt; then
        success "Uvicorn dependency found"
    else
        error "Uvicorn dependency missing"
    fi
fi

echo ""
echo "Step 7: Checking frontend dependencies..."
echo "------------------------------------------"

if [ -f frontend/package.json ]; then
    # Check for key dependencies
    if grep -q "\"react\"" frontend/package.json; then
        success "React dependency found"
    else
        error "React dependency missing"
    fi
    
    if grep -q "\"typescript\"" frontend/package.json; then
        success "TypeScript dependency found"
    else
        error "TypeScript dependency missing"
    fi
    
    if grep -q "\"vite\"" frontend/package.json; then
        success "Vite dependency found"
    else
        error "Vite dependency missing"
    fi
fi

echo ""
echo "======================================"
echo "Validation Summary"
echo "======================================"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Ready to deploy.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. For local development: ./scripts/local_dev.sh"
    echo "  2. For SPCS deployment: ./scripts/deploy.sh"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Validation completed with $WARNINGS warning(s).${NC}"
    echo "You can proceed, but review the warnings above."
    exit 0
else
    echo -e "${RED}✗ Validation failed with $ERRORS error(s) and $WARNINGS warning(s).${NC}"
    echo "Please fix the errors before deploying."
    exit 1
fi
