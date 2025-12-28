#!/bin/bash
# ==============================================================================
# Production Build Test Script
# ==============================================================================
# This script tests the production Docker build without actually deploying.
# It verifies:
# 1. Multi-stage Dockerfile builds successfully
# 2. Dashboard assets are bundled correctly
# 3. Static files are accessible in the image
# ==============================================================================

set -e  # Exit on error

echo "================================"
echo "FaultMaven Production Build Test"
echo "================================"
echo

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${YELLOW}[1/4] Checking prerequisites...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

# Step 2: Build the production image
echo
echo -e "${YELLOW}[2/4] Building production Docker image...${NC}"
echo "This may take 5-10 minutes on first build..."

if docker build -f Dockerfile.production -t faultmaven/core:test .; then
    echo -e "${GREEN}✅ Production image built successfully${NC}"
else
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
fi

# Step 3: Verify static files are in the image
echo
echo -e "${YELLOW}[3/4] Verifying static files are bundled...${NC}"

# Check if /app/static directory exists and contains files
STATIC_CHECK=$(docker run --rm faultmaven/core:test ls -la /app/static 2>/dev/null | wc -l)

if [ "$STATIC_CHECK" -gt 3 ]; then
    echo -e "${GREEN}✅ Static files found in image${NC}"
    docker run --rm faultmaven/core:test ls -la /app/static
else
    echo -e "${RED}❌ Static files NOT found in image${NC}"
    exit 1
fi

# Step 4: Check for index.html
echo
echo -e "${YELLOW}[4/4] Verifying dashboard index.html exists...${NC}"

if docker run --rm faultmaven/core:test test -f /app/static/index.html; then
    echo -e "${GREEN}✅ index.html found${NC}"
else
    echo -e "${RED}❌ index.html NOT found${NC}"
    exit 1
fi

# Success
echo
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ Production Build Test PASSED${NC}"
echo -e "${GREEN}================================${NC}"
echo
echo "Image: faultmaven/core:test"
echo "Size: $(docker images faultmaven/core:test --format "{{.Size}}")"
echo
echo "To run the production container:"
echo "  docker-compose -f docker-compose.prod.yml up -d"
echo
echo "To clean up test image:"
echo "  docker rmi faultmaven/core:test"
