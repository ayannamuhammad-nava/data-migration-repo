#!/bin/bash
# Data Modernization Tool — Setup
#
# Usage:
#   ./setup.sh              # Install and launch dashboard
#   ./setup.sh --install    # Install only (don't launch)

set -e

LAUNCH=true
if [ "$1" = "--install" ]; then
    LAUNCH=false
fi

echo "============================================================"
echo "  Data Modernization Tool — Setup"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required. Install from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "  Python: $PYTHON_VERSION"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt 2>&1 | tail -3
echo "  Done."

# Verify key imports
echo ""
echo "Verifying installation..."
python3 -c "
import click, pluggy, pandas, yaml, sqlglot, streamlit
print('  All dependencies OK')
" 2>&1

echo ""
echo "============================================================"
echo "  Setup Complete!"
echo "============================================================"
echo ""
echo "  To launch the dashboard:"
echo "    streamlit run dashboard.py"
echo ""
echo "  Then open http://localhost:8501"
echo "  Paste a mainframe repo URL and click Run."
echo ""
echo "  Example repos to try:"
echo "    https://github.com/aws-samples/aws-mainframe-modernization-carddemo.git"
echo "    https://github.com/ayannamuhammad-nava/customer-service-data.git"
echo ""
echo "============================================================"

if [ "$LAUNCH" = true ]; then
    echo ""
    echo "Launching dashboard..."
    streamlit run dashboard.py
fi
