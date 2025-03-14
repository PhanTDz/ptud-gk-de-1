@echo off
echo Setting up the Blog Application...

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed! Please install Python 3.7 or later.
    pause
    exit /b 1
)

REM Check if pip is installed
where pip >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo pip is not installed! Please install pip.
    pause
    exit /b 1
)

REM Remove old virtual environment if it exists
if exist "venv" (
    echo Removing old virtual environment...
    rmdir /s /q venv
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Initialize database
echo Initializing database...
python -c "from app import app, db; app.app_context().push(); db.create_all()"

echo Setup completed successfully!
echo To run the application, use: run.bat
pause 