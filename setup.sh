#!/bin/bash
# Lockpicks Data Migration — Quick Setup
# Starts all infrastructure and installs the DM toolkit
#
# Usage: ./setup.sh

set -e

echo "============================================================"
echo "  Lockpicks Data Migration — Setup"
echo "============================================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed. Install from https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "ERROR: Docker Compose is not available. Install Docker Desktop or the compose plugin."
    exit 1
fi

if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "  Docker:         $(docker --version | cut -d' ' -f3 | tr -d ',')"
echo "  Docker Compose: $(docker compose version --short)"
echo "  uv:             $(uv --version)"
echo ""

# Step 1: Install Python toolkit
echo "[1/4] Installing DM toolkit..."
uv sync --extra all 2>&1 | tail -1
echo "  Done. CLI available at: .venv/bin/dm"
echo ""

# Step 2: Start infrastructure
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

echo "============================================================"
echo "  Setup Complete!"
echo "============================================================"
echo ""
echo "  Services running:"
echo "    PostgreSQL:      localhost:5432 (user: app / secret123)"
echo "    OpenMetadata:    localhost:8585"
echo "    Elasticsearch:   localhost:9200"
echo "    Dashboard:       localhost:8501 (after dm dashboard)"
echo ""
echo "  Next steps:"
echo "    1. dm init my-project"
echo "    2. Edit projects/my-project/project.yaml"
echo "    3. Load your COBOL data into legacy_db"
echo "    4. Run the pipeline: dm discover → dm dashboard"
echo ""
echo "  See OVERVIEW.md for the full process explanation."
echo "  See examples/ for working reference projects."
echo "============================================================"
