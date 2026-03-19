# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root to ensure relative paths work
cd "$PROJECT_ROOT" || exit 1

# Launch Python with environment variables
VENV_PATH="./.venv/bin/python3"
PYTHON_CMD="python3"

if [ -f "$VENV_PATH" ]; then
    PYTHON_CMD="$VENV_PATH"
fi

QT_QPA_PLATFORM=xcb \
QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox" \
QT_DEBUG_PLUGINS=1 \
$PYTHON_CMD sources/main.py