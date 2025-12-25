#!/bin/bash
# Quick launcher for SecureML Interactive Watermarking Demo

echo "=========================================="
echo "SecureML Interactive Watermarking Demo"
echo "=========================================="
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Look for venv in multiple possible locations
VENV_PATH=""
if [ -d "$PROJECT_ROOT/venv" ]; then
    VENV_PATH="$PROJECT_ROOT/venv"
elif [ -d "$SCRIPT_DIR/../venv" ]; then
    VENV_PATH="$SCRIPT_DIR/../venv"
elif [ -d "$HOME/dev/code/SecureML/secureml/venv" ]; then
    VENV_PATH="$HOME/dev/code/SecureML/secureml/venv"
fi

if [ -z "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found"
    echo "Searched in:"
    echo "  - $PROJECT_ROOT/venv"
    echo "  - $SCRIPT_DIR/../venv"
    echo "  - $HOME/dev/code/SecureML/secureml/venv"
    echo ""
    echo "Please create a virtual environment first:"
    echo "  cd $PROJECT_ROOT"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -e src"
    exit 1
fi

echo "Found virtual environment at: $VENV_PATH"

# Activate venv
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Check if secureml is installed
if ! python3 -c "import secureml" 2>/dev/null; then
    echo "Error: SecureML not installed in virtual environment"
    echo "Please install SecureML:"
    echo "  cd $PROJECT_ROOT"
    echo "  source venv/bin/activate"
    echo "  pip install -e src"
    exit 1
fi

# Run the demo
echo "Starting interactive demo..."
echo ""
cd "$SCRIPT_DIR"
python3 interactive_watermarking_demo.py

# Deactivate venv
deactivate

echo ""
echo "Demo session ended. Thank you!"
