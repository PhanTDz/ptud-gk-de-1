@echo off
echo Starting the Blog Application...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
python app.py

if %ERRORLEVEL% NEQ 0 (
    echo Error running the application!
    pause
    exit /b 1
)

pause 