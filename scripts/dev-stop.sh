#!/bin/bash
# ==============================================================================
# FaultMaven Development Server Stopper
# ==============================================================================
# Stops the running FaultMaven development server.

echo "🛑 Stopping FaultMaven Development Server..."

# Find running process
EXISTING_PID=$(pgrep -f "uvicorn faultmaven.app:app" 2>/dev/null)

if [ -z "$EXISTING_PID" ]; then
    echo "ℹ️  FaultMaven is not running"
    exit 0
fi

echo "📍 Found FaultMaven running (PID: $EXISTING_PID)"

# Try graceful shutdown first
echo "🔄 Attempting graceful shutdown..."
pkill -TERM -f "uvicorn faultmaven.app:app"
sleep 2

# Check if it stopped
if pgrep -f "uvicorn faultmaven.app:app" > /dev/null; then
    echo "⚠️  Graceful shutdown failed. Force killing..."
    pkill -9 -f "uvicorn faultmaven.app:app"
    sleep 1

    if pgrep -f "uvicorn faultmaven.app:app" > /dev/null; then
        echo "❌ Failed to stop FaultMaven"
        echo "   Please check manually: ps aux | grep uvicorn"
        exit 1
    fi
fi

echo "✅ FaultMaven stopped successfully"
