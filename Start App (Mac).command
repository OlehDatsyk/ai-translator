#!/bin/bash

# ============================================================
#   AI Translator - Startup Script (macOS)
#   Double-click this file in Finder to run it.
# ============================================================

# Move into the folder this script lives in, so it works no matter
# where it's double-clicked from.
cd "$(dirname "$0")" || exit 1

echo "============================================================"
echo "  AI Translator - Startup Script (macOS)"
echo "============================================================"
echo ""

# ------------------------------------------------------------------
# Keep the Terminal window open even if something below fails,
# so the user can read the error message.
# ------------------------------------------------------------------
pause_and_exit() {
    echo ""
    echo "Press any key to close this window..."
    read -n 1 -s -r
    exit 1
}

# ------------------------------------------------------------------
# Step 1 - Verify Python is installed
# ------------------------------------------------------------------
echo "[1/6] Checking for Python..."

PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
fi

if [ -z "$PYTHON_CMD" ]; then
    echo ""
    echo "[ERROR] Python was not found on this computer."
    echo ""
    echo "Please install Python 3.10 or newer from:"
    echo "    https://www.python.org/downloads/"
    echo ""
    echo "After installing, double-click this file again."
    pause_and_exit
fi

PY_VERSION=$("$PYTHON_CMD" --version 2>&1)
echo "      Found $PY_VERSION (using command: $PYTHON_CMD)"
echo ""

# ------------------------------------------------------------------
# Step 2 - Create the virtual environment if it doesn't exist yet
# ------------------------------------------------------------------
echo "[2/6] Checking for virtual environment..."

if [ ! -f "venv/bin/activate" ]; then
    echo "      No virtual environment found. Creating one now..."
    "$PYTHON_CMD" -m venv venv
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERROR] Failed to create the virtual environment."
        echo "Please check the error message above."
        pause_and_exit
    fi
    echo "      Virtual environment created successfully."
else
    echo "      Virtual environment already exists."
fi
echo ""

# ------------------------------------------------------------------
# Step 3 - Activate the virtual environment
# ------------------------------------------------------------------
echo "[3/6] Activating virtual environment..."
# shellcheck disable=SC1091
source "venv/bin/activate"
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to activate the virtual environment."
    pause_and_exit
fi
echo "      Virtual environment active."
echo ""

# ------------------------------------------------------------------
# Step 4 - Install missing dependencies
# ------------------------------------------------------------------
echo "[4/6] Checking dependencies from requirements.txt..."

if [ ! -f "requirements.txt" ]; then
    echo ""
    echo "[ERROR] requirements.txt was not found in this folder."
    echo "Make sure this script is inside the ai-translator project folder."
    pause_and_exit
fi

pip install -r requirements.txt --quiet --disable-pip-version-check
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to install one or more dependencies."
    echo "Check your internet connection and the error message above."
    pause_and_exit
fi
echo "      Dependencies are installed and up to date."
echo ""

# ------------------------------------------------------------------
# Step 5 - Verify the .env file exists
# ------------------------------------------------------------------
echo "[5/6] Checking for .env configuration file..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "      No .env file found. Creating one from .env.example..."
        cp ".env.example" ".env"
        echo ""
        echo "============================================================"
        echo "  ACTION REQUIRED"
        echo "============================================================"
        echo "  A new .env file was created for you, but it still has a"
        echo "  placeholder API key."
        echo ""
        echo "  Please open the .env file in this folder with a text"
        echo "  editor, replace the line:"
        echo "      OPENAI_API_KEY=sk-your-api-key-here"
        echo "  with your real OpenAI API key, save the file, and then"
        echo "  double-click this script again."
        echo ""
        echo "  Get a key at: https://platform.openai.com/api-keys"
        echo "============================================================"
        pause_and_exit
    else
        echo ""
        echo "[ERROR] Neither .env nor .env.example was found."
        echo "This project cannot start without configuration."
        pause_and_exit
    fi
else
    echo "      .env file found."
fi
echo ""

# ------------------------------------------------------------------
# Step 6 - Launch the application
# ------------------------------------------------------------------
echo "[6/6] Starting AI Translator..."
echo ""
echo "============================================================"
echo "  The app will open at: http://127.0.0.1:5000"
echo "  (the port may differ if you customized FLASK_PORT in .env)"
echo ""
echo "  Keep this window open while using the app."
echo "  Press CTRL+C in this window to stop the server."
echo "============================================================"
echo ""

"$PYTHON_CMD" app.py
APP_EXIT_CODE=$?

# ------------------------------------------------------------------
# If the app exits/crashes, keep the window open so the user can
# read the error instead of it closing immediately.
# ------------------------------------------------------------------
if [ $APP_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "============================================================"
    echo "  The application stopped with an error. See the messages"
    echo "  above for details. Check INSTRUCTION.md's Troubleshooting"
    echo "  section for help with common problems."
    echo "============================================================"
else
    echo ""
    echo "Application stopped."
fi

echo ""
echo "Press any key to close this window..."
read -n 1 -s -r
