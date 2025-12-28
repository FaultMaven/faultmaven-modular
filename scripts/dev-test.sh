#!/bin/bash
# ==============================================================================
# FaultMaven Development Test Runner
# ==============================================================================
# Runs tests for the FaultMaven modular monolith.
# Supports unit tests, integration tests, and coverage reporting.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VENV_PATH=".venv"
COVERAGE=false
VERBOSE=false
MODULE=""
MARKER=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -m|--module)
            MODULE="$2"
            shift 2
            ;;
        -k|--keyword)
            MARKER="-k $2"
            shift 2
            ;;
        -h|--help)
            cat <<EOF
Usage: $0 [OPTIONS]

Run FaultMaven tests with pytest.

OPTIONS:
    -c, --coverage          Run with coverage report
    -v, --verbose           Verbose output
    -m, --module MODULE     Run tests for specific module (auth, case, etc.)
    -k, --keyword KEYWORD   Run tests matching keyword expression
    -h, --help              Show this help message

EXAMPLES:
    $0                      # Run all tests
    $0 -c                   # Run all tests with coverage
    $0 -m auth              # Run only auth module tests
    $0 -k "test_login"      # Run tests matching "test_login"
    $0 -v -c                # Verbose output with coverage

MODULES:
    auth        - Authentication and authorization
    session     - Session management
    case        - Case management
    knowledge   - Knowledge base and vector search
    evidence    - Evidence and file management
    agent       - AI agent and LLM integration
    api_gateway - API routing and middleware

EOF
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Run '$0 --help' for usage information"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🧪 FaultMaven Test Runner${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}✗${NC} Virtual environment not found at $VENV_PATH"
    echo ""
    echo "Create it with:"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -e .[dev]"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}✓${NC} Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Build pytest command
PYTEST_CMD="pytest"

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=faultmaven --cov-report=term-missing --cov-report=html"
fi

if [ -n "$MODULE" ]; then
    if [ -d "tests/$MODULE" ]; then
        PYTEST_CMD="$PYTEST_CMD tests/$MODULE"
        echo -e "${BLUE}ℹ${NC} Running tests for module: $MODULE"
    else
        echo -e "${RED}✗${NC} Module directory not found: tests/$MODULE"
        echo ""
        echo "Available modules:"
        ls -d tests/*/ 2>/dev/null | sed 's|tests/||' | sed 's|/||' || echo "  (no test directories found)"
        exit 1
    fi
else
    PYTEST_CMD="$PYTEST_CMD tests/"
    echo -e "${BLUE}ℹ${NC} Running all tests"
fi

if [ -n "$MARKER" ]; then
    PYTEST_CMD="$PYTEST_CMD $MARKER"
    echo -e "${BLUE}ℹ${NC} Filtering tests with: $MARKER"
fi

echo ""
echo -e "${YELLOW}Command:${NC} $PYTEST_CMD"
echo ""

# Run tests
if eval "$PYTEST_CMD"; then
    echo ""
    echo -e "${GREEN}✓${NC} Tests passed!"

    if [ "$COVERAGE" = true ]; then
        echo ""
        echo -e "${GREEN}✓${NC} Coverage report generated: htmlcov/index.html"
        echo "  Open with: xdg-open htmlcov/index.html"
    fi
else
    echo ""
    echo -e "${RED}✗${NC} Tests failed"
    exit 1
fi
