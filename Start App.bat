@echo off
setlocal enabledelayedexpansion
title AI Translator - Startup

echo ============================================================
echo   AI Translator - Startup Script (Windows)
echo ============================================================
echo.

REM ------------------------------------------------------------------
REM Make sure we run from the folder this script lives in, so it works
REM correctly no matter where the user double-clicks it from.
REM ------------------------------------------------------------------
cd /d "%~dp0"

REM ------------------------------------------------------------------
REM Step 1 - Verify Python is installed
REM ------------------------------------------------------------------
echo [1/6] Checking for Python...

where python >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        set "PYTHON_CMD=py"
    ) else (
        echo.
        echo [ERROR] Python was not found on this computer.
        echo.
        echo Please install Python 3.10 or newer from:
        echo     https://www.python.org/downloads/
        echo.
        echo IMPORTANT: During installation, check the box that says
        echo "Add python.exe to PATH" before clicking Install.
        echo.
        echo After installing, double-click this file again.
        echo.
        pause
        exit /b 1
    )
)

for /f "tokens=2" %%v in ('%PYTHON_CMD% --version 2^>^&1') do set "PY_VERSION=%%v"
echo       Found Python !PY_VERSION! ^(using command: %PYTHON_CMD%^)
echo.

REM ------------------------------------------------------------------
REM Step 2 - Create the virtual environment if it doesn't exist yet
REM ------------------------------------------------------------------
echo [2/6] Checking for virtual environment...

if not exist "venv\Scripts\activate.bat" (
    echo       No virtual environment found. Creating one now...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create the virtual environment.
        echo Please check the error message above.
        echo.
        pause
        exit /b 1
    )
    echo       Virtual environment created successfully.
    set "FIRST_RUN=1"
) else (
    echo       Virtual environment already exists.
    set "FIRST_RUN=0"
)
echo.

REM ------------------------------------------------------------------
REM Step 3 - Activate the virtual environment
REM ------------------------------------------------------------------
echo [3/6] Activating virtual environment...
call "venv\Scripts\activate.bat"
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to activate the virtual environment.
    echo.
    pause
    exit /b 1
)
echo       Virtual environment active.
echo.

REM ------------------------------------------------------------------
REM Step 4 - Install missing dependencies
REM ------------------------------------------------------------------
echo [4/6] Checking dependencies from requirements.txt...

if not exist "requirements.txt" (
    echo.
    echo [ERROR] requirements.txt was not found in this folder.
    echo Make sure this script is inside the ai-translator project folder.
    echo.
    pause
    exit /b 1
)

pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install one or more dependencies.
    echo Check your internet connection and the error message above.
    echo.
    pause
    exit /b 1
)
echo       Dependencies are installed and up to date.
echo.

REM ------------------------------------------------------------------
REM Step 5 - Verify the .env file exists
REM ------------------------------------------------------------------
echo [5/6] Checking for .env configuration file...

if not exist ".env" (
    if exist ".env.example" (
        echo       No .env file found. Creating one from .env.example...
        copy /y ".env.example" ".env" >nul
        echo.
        echo ============================================================
        echo   ACTION REQUIRED
        echo ============================================================
        echo   A new .env file was created for you, but it still has a
        echo   placeholder API key.
        echo.
        echo   Please open the .env file in this folder with a text
        echo   editor, replace the line:
        echo       OPENAI_API_KEY=sk-your-api-key-here
        echo   with your real OpenAI API key, save the file, and then
        echo   double-click this script again.
        echo.
        echo   Get a key at: https://platform.openai.com/api-keys
        echo ============================================================
        echo.
        pause
        exit /b 1
    ) else (
        echo.
        echo [ERROR] Neither .env nor .env.example was found.
        echo This project cannot start without configuration.
        echo.
        pause
        exit /b 1
    )
) else (
    echo       .env file found.
)
echo.

REM ------------------------------------------------------------------
REM Step 6 - Launch the application
REM ------------------------------------------------------------------
echo [6/6] Starting AI Translator...
echo.
echo ============================================================
echo   The app will open at: http://127.0.0.1:5000
echo   ^(the port may differ if you customized FLASK_PORT in .env^)
echo.
echo   Keep this window open while using the app.
echo   Press CTRL+C in this window to stop the server.
echo ============================================================
echo.

python app.py

REM ------------------------------------------------------------------
REM If the app exits/crashes, keep the window open so the user can
REM read the error instead of it flashing closed.
REM ------------------------------------------------------------------
if errorlevel 1 (
    echo.
    echo ============================================================
    echo   The application stopped with an error. See the messages
    echo   above for details. Check INSTRUCTION.md's Troubleshooting
    echo   section for help with common problems.
    echo ============================================================
    echo.
    pause
) else (
    echo.
    echo Application stopped.
    pause
)

endlocal
