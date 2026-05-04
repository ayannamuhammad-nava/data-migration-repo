#!/bin/bash
# Lockpicks Data Migration — Quick Setup
# Starts all infrastructure and installs the DM toolkit
#
# Usage:
#   ./setup.sh                          # Full setup with Docker infrastructure
#   ./setup.sh --no-docker              # Install toolkit only (for flat file / copybook projects)
#   ./setup.sh --repo <url>             # Setup + scaffold project from git repo

set -e

REPO_URL=""
NO_DOCKER=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --repo) REPO_URL="$2"; shift 2;;
        --no-docker) NO_DOCKER=true; shift;;
        *) echo "Unknown option: $1"; exit 1;;
    esac
done

echo "============================================================"
echo "  Lockpicks Data Migration — Setup"
echo "============================================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "  Python:          $PYTHON_VERSION"

if [ "$NO_DOCKER" = false ]; then
    if ! command -v docker &> /dev/null; then
        echo "ERROR: Docker is not installed. Install from https://docs.docker.com/get-docker/"
        echo "  Or run: ./setup.sh --no-docker (for flat file / copybook projects only)"
        exit 1
    fi

    if ! command -v docker compose &> /dev/null; then
        echo "ERROR: Docker Compose is not available."
        exit 1
    fi

    echo "  Docker:          $(docker --version | cut -d' ' -f3 | tr -d ',')"
    echo "  Docker Compose:  $(docker compose version --short)"
fi

# Check for uv or pip
if command -v uv &> /dev/null; then
    INSTALLER="uv"
    echo "  Installer:       uv $(uv --version 2>/dev/null | head -1)"
else
    INSTALLER="pip"
    echo "  Installer:       pip3"
fi
echo ""

# Step 1: Install Python toolkit
echo "[1/4] Installing DM toolkit..."
if [ "$INSTALLER" = "uv" ]; then
    uv sync --extra all 2>&1 | tail -1
    DM_CMD=".venv/bin/dm"
else
    pip3 install -e "." 2>&1 | tail -3
    pip3 install pandas pluggy psycopg2-binary pyyaml click sqlglot pandera numpy requests 2>&1 | tail -1
    DM_CMD="python3 -m dm.cli"
fi
echo "  Done."
echo ""

# Step 2: Start infrastructure (unless --no-docker)
if [ "$NO_DOCKER" = false ]; then
    echo "[2/4] Starting infrastructure (PostgreSQL + OpenMetadata)..."
    echo "  This may take a few minutes on first run (pulling images)..."
    docker compose up -d 2>&1 | tail -3
    echo ""

    # Step 3: Wait for OpenMetadata
    echo "[3/4] Waiting for OpenMetadata to be ready..."
    for i in $(seq 1 30); do
        if curl -s http://localhost:8585/api/v1/system/version > /dev/null 2>&1; then
            VERSION=$(curl -s http://localhost:8585/api/v1/system/version | python3 -c "import sys,json; print(json.load(sys.stdin).get('version','unknown'))" 2>/dev/null || echo "unknown")
            echo "  OpenMetadata $VERSION is ready!"
            break
        fi
        echo "  Waiting... ($i/30)"
        sleep 10
    done

    if ! curl -s http://localhost:8585/api/v1/system/version > /dev/null 2>&1; then
        echo "WARNING: OpenMetadata did not start within 5 minutes."
        echo "  Check logs: docker compose logs openmetadata-server"
        echo "  You can continue setup and retry later."
    fi
    echo ""

    # Step 4: Create databases
    echo "[4/4] Creating legacy and modern databases..."
    docker exec -e PGPASSWORD=secret123 dm_postgres psql -U app -d postgres \
        -c "SELECT 1 FROM pg_database WHERE datname='legacy_db'" | grep -q 1 || \
        docker exec -e PGPASSWORD=secret123 dm_postgres psql -U app -d postgres \
        -c "CREATE DATABASE legacy_db;"

    docker exec -e PGPASSWORD=secret123 dm_postgres psql -U app -d postgres \
        -c "SELECT 1 FROM pg_database WHERE datname='modern_db'" | grep -q 1 || \
        docker exec -e PGPASSWORD=secret123 dm_postgres psql -U app -d postgres \
        -c "CREATE DATABASE modern_db;"
    echo "  Databases ready: legacy_db, modern_db"
    echo ""
else
    echo "[2/4] Skipping Docker infrastructure (--no-docker mode)"
    echo "[3/4] Skipping OpenMetadata"
    echo "[4/4] Skipping database creation"
    echo ""
fi

# Optional: scaffold project from repo
if [ -n "$REPO_URL" ]; then
    echo "============================================================"
    echo "  Scaffolding project from: $REPO_URL"
    echo "============================================================"
    PROJECT_NAME=$(basename "$REPO_URL" .git | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
    $DM_CMD init "$PROJECT_NAME" --repo "$REPO_URL"
    echo ""
fi

echo "============================================================"
echo "  Setup Complete!"
echo "============================================================"
echo ""
if [ "$NO_DOCKER" = false ]; then
    echo "  Services running:"
    echo "    PostgreSQL:      localhost:5432 (user: app / secret123)"
    echo "    OpenMetadata:    localhost:8585"
    echo "    Dashboard:       localhost:8501 (after dm dashboard)"
    echo ""
fi
echo "  Supported input sources:"
echo "    - Git repo:      dm init my-project --repo <url>"
echo "    - Local files:   dm init my-project --data /path/to/files"
echo "    - COBOL copybooks + flat files (.cpy, .dat, EBCDIC)"
echo "    - CSV / TSV files"
echo "    - DB2, Oracle, PostgreSQL databases"
echo ""
echo "  Supported output targets:"
echo "    - PostgreSQL, Snowflake, Oracle, AWS (Redshift)"
echo "    - Select target in the dashboard or via --target flag"
echo ""
echo "  Quick start:"
echo "    1. dm init my-project --repo <url>"
echo "    2. dm discover --enrich --project projects/my-project"
echo "    3. dm rationalize --project projects/my-project"
echo "    4. dm generate-schema --all --project projects/my-project"
echo "    5. dm validate --phase pre --dataset <name> --project projects/my-project"
echo "    6. dm dashboard --project projects/my-project"
echo ""
echo "  For flat file / copybook projects (no database needed):"
echo "    ./setup.sh --no-docker --repo <url>"
echo ""
echo "  See CHANGELOG.md for the full feature list."
echo "============================================================"
