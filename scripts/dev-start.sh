#!/bin/bash
# ==============================================================================
# FaultMaven Local Development Server Starter
# ==============================================================================
# Starts the FaultMaven backend API server for local development.
# Adapted from FaultMaven-Mono run_faultmaven.sh
#
# Features:
# - Detects if server is already running
# - Offers to restart running instances
# - Prevents port conflicts
# - Can run in foreground or background
#
# Usage:
#   ./scripts/dev-start.sh              # Run in foreground
#   ./scripts/dev-start.sh --background # Run in background
#   ./scripts/dev-start.sh --bg         # Short form

set -e

echo "🚀 Starting FaultMaven Development Server..."
echo "=============================================="

# Parse arguments
RUN_BACKGROUND=false
for arg in "$@"; do
    case $arg in
        --background|--bg|-b)
            RUN_BACKGROUND=true
            shift
            ;;
    esac
done

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found."
    echo ""
    echo "Please set up the development environment first:"
    echo "  1. Create venv:        python -m venv .venv"
    echo "  2. Activate venv:      source .venv/bin/activate"
    echo "  3. Install deps:       pip install -e .[dev]"
    echo ""
    echo "Or see: deploy/local/README.md for complete setup guide"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found."
    echo ""
    echo "Please create configuration:"
    echo "  cp .env.example .env"
    echo "  # Edit .env and add your OPENAI_API_KEY or ANTHROPIC_API_KEY"
    exit 1
fi

# Check if FaultMaven is already running
EXISTING_PID=$(pgrep -f "uvicorn faultmaven.app:app" 2>/dev/null)
if [ ! -z "$EXISTING_PID" ]; then
    echo "⚠️  FaultMaven is already running (PID: $EXISTING_PID)"
    echo ""

    # Check if running interactively
    if [ -t 0 ]; then
        read -p "🔄 Do you want to restart it? [y/N]: " -r response
        case $response in
            [yY][eE][sS]|[yY])
                echo "🛑 Stopping existing instance..."
                pkill -f "uvicorn faultmaven.app:app"
                sleep 2

                # Verify it stopped
                if pgrep -f "uvicorn faultmaven.app:app" > /dev/null; then
                    echo "❌ Failed to stop existing instance. Force killing..."
                    pkill -9 -f "uvicorn faultmaven.app:app"
                    sleep 2
                fi
                echo "✅ Existing instance stopped"
                ;;
            *)
                echo "ℹ️  Keeping existing instance running"
                echo ""
                echo "📄 View logs:  ./scripts/dev-logs.sh"
                echo "🛑 To stop:    ./scripts/dev-stop.sh"
                exit 0
                ;;
        esac
    else
        # Non-interactive mode: auto-restart
        echo "🔄 Non-interactive mode: automatically restarting..."
        echo "🛑 Stopping existing instance..."
        pkill -f "uvicorn faultmaven.app:app"
        sleep 2

        if pgrep -f "uvicorn faultmaven.app:app" > /dev/null; then
            echo "❌ Failed to stop existing instance. Force killing..."
            pkill -9 -f "uvicorn faultmaven.app:app"
            sleep 2
        fi
        echo "✅ Existing instance stopped"
    fi
fi

# Check port availability
PORT=8000
if command -v netstat >/dev/null 2>&1; then
    if netstat -ln 2>/dev/null | grep -q ":$PORT "; then
        echo "⚠️  Port $PORT is still in use. Waiting for it to be released..."
        sleep 2
        if netstat -ln 2>/dev/null | grep -q ":$PORT "; then
            echo "❌ Port $PORT is still occupied. Please check manually:"
            if command -v lsof >/dev/null 2>&1; then
                echo ""
                lsof -i:$PORT
            fi
            exit 1
        fi
    fi
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Load environment variables from .env
echo "📁 Loading configuration from .env..."
export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)

# Start the server
echo ""
echo "✅ Starting FaultMaven backend..."
echo ""
echo "📍 Server URL: http://localhost:$PORT"
echo "📖 API Docs:   http://localhost:$PORT/docs"
echo "🏥 Health:     http://localhost:$PORT/health"
echo ""

if [ "$RUN_BACKGROUND" = true ]; then
    # Run in background with logging
    LOG_FILE="./data/faultmaven-dev.log"
    mkdir -p ./data

    echo "🔄 Running in background mode..."
    echo "📄 Logs will be written to: $LOG_FILE"
    echo ""

    nohup uvicorn faultmaven.app:app \
        --host 0.0.0.0 \
        --port $PORT \
        --reload \
        > "$LOG_FILE" 2>&1 &

    BACKGROUND_PID=$!
    sleep 2

    # Verify it started
    if ps -p $BACKGROUND_PID > /dev/null; then
        echo "✅ FaultMaven started in background (PID: $BACKGROUND_PID)"
        echo ""
        echo "Next steps:"
        echo "  📄 View logs:  ./scripts/dev-logs.sh"
        echo "  🛑 To stop:    ./scripts/dev-stop.sh"
    else
        echo "❌ Failed to start FaultMaven in background"
        echo "📄 Check logs: tail -f $LOG_FILE"
        exit 1
    fi
else
    # Run in foreground
    echo "🔄 Running in foreground mode (Ctrl+C to stop)..."
    echo ""

    uvicorn faultmaven.app:app \
        --host 0.0.0.0 \
        --port $PORT \
        --reload
fi
