@echo off
echo Starting Alzheimer's Prediction Tool...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Error creating virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Install dependencies if needed
if %errorlevel% equ 0 (
    echo Checking dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Warning: Some dependencies could not be installed
        echo The application may not work correctly
    )
)

REM Run the Flask app
echo.
echo Starting Flask API server...
start cmd /k python app.py

echo.
echo Waiting for API to start...
timeout /t 5

REM Open the HTML page in the default browser
echo Opening web application in browser...
start "" "prediction-tool.html"

echo.
echo Application started successfully!
echo Press any key to exit this window. The server will continue running.
pause >nul
exit /b 0 