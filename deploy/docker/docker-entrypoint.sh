#!/bin/bash
# ==============================================================================
# FaultMaven Docker Entrypoint Script
# ==============================================================================
# Automates database migrations and starts the application.
# This ensures the database schema is always up-to-date before the app starts.

set -e  # Exit on any error

echo "=================================="
echo "FaultMaven Startup"
echo "=================================="

# ==============================================================================
# Step 1: Database Migrations
# ==============================================================================
echo "📊 Running database migrations..."

# Check if alembic is available
if command -v alembic &> /dev/null; then
    # Run migrations (creates tables if they don't exist, upgrades if needed)
    alembic upgrade head
    echo "✅ Database migrations complete"
else
    echo "⚠️  Alembic not found - skipping migrations"
    echo "   (This is normal for development setups)"
fi

# ==============================================================================
# Step 2: Start Application
# ==============================================================================
echo "🚀 Starting FaultMaven..."
echo ""

# Execute the CMD from Dockerfile (passed as arguments to this script)
exec "$@"
