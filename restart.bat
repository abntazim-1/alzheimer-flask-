@echo off
echo Restarting Alzheimer's Prediction Tool...

REM Kill existing python processes for app.py
taskkill /f /im python.exe /fi "WINDOWTITLE eq python app.py" >nul 2>&1

REM Clear processed images directory to avoid buildup
echo Cleaning processed images...
if exist static\processed_images (
    del /q static\processed_images\* >nul 2>&1
)

REM Start the Flask app
echo Starting Flask API server...
start cmd /k python app.py

echo Waiting for API to start...
timeout /t 5

REM Open the HTML page in the default browser
echo Opening web application in browser...
start "" "prediction-tool.html"

echo Application restarted successfully!
echo Press any key to exit this window. The server will continue running.
pause >nul 