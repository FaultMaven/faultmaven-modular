#!/bin/bash
# ==============================================================================
# FaultMaven Development Server Log Viewer
# ==============================================================================
# Views logs from the FaultMaven development server.
# - If server is running in background, shows log file
# - If server is running in foreground, shows recent Docker container logs
# - Supports follow mode (-f) and line limit options

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

LOG_FILE="./data/faultmaven-dev.log"
FOLLOW_MODE=false
TAIL_LINES=100

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--follow)
            FOLLOW_MODE=true
            shift
            ;;
        -n|--lines)
            TAIL_LINES="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 [-f|--follow] [-n|--lines N]"
            echo "  -f, --follow    Follow log output (like tail -f)"
            echo "  -n, --lines N   Show last N lines (default: 100)"
            exit 1
            ;;
    esac
done

echo "📋 FaultMaven Development Server Logs"
echo ""

# Check if server is running
EXISTING_PID=$(pgrep -f "uvicorn faultmaven.app:app" 2>/dev/null)

if [ -z "$EXISTING_PID" ]; then
    echo "ℹ️  Server is not currently running"

    # Check if log file exists from previous run
    if [ -f "$LOG_FILE" ]; then
        echo "📄 Showing last $TAIL_LINES lines from previous run:"
        echo ""
        tail -n "$TAIL_LINES" "$LOG_FILE"
    else
        echo "❌ No log file found at $LOG_FILE"
        echo ""
        echo "Start the server with: ./scripts/dev-start.sh"
    fi
    exit 0
fi

echo "✅ Server is running (PID: $EXISTING_PID)"
echo ""

# Check if log file exists (background mode)
if [ -f "$LOG_FILE" ]; then
    echo "📄 Showing logs from: $LOG_FILE"
    echo ""

    if [ "$FOLLOW_MODE" = true ]; then
        tail -f -n "$TAIL_LINES" "$LOG_FILE"
    else
        tail -n "$TAIL_LINES" "$LOG_FILE"
    fi
else
    echo "⚠️  Log file not found - server may be running in foreground mode"
    echo ""
    echo "Options:"
    echo "  1. Check terminal where you started the server"
    echo "  2. Restart server in background mode: ./scripts/dev-start.sh --background"
    echo "  3. View Docker logs: ./faultmaven logs -f"
fi
