@echo off

:: Check admin rights and restart with privileges
net session >nul 2>&1 || (
    powershell -Command "Start-Process cmd -ArgumentList '/k cd /d \"%CD%\" && \"%~f0\"' -Verb RunAs"
    exit /b
)


title AnyaAI

:: Create venv if missing
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv || (
        echo ERROR: Failed to create venv
        echo Possible solutions:
        echo 1. Install Python
        echo 2. Add Python to PATH
        echo 3. Check disk space
        pause
        exit
    )
)

:: Activate venv
call venv\Scripts\activate.bat || (
    echo ERROR: Virtual environment activation failed
    pause
    exit
)

:: Upgrade pip
python -m pip install --upgrade pip

:: Install requirements
if exist "requirements.txt" (
    pip install -r requirements.txt || (
        echo ERROR: Failed to install dependencies
        pause
        exit
    )
) else (
    echo ERROR: requirements.txt not found
    echo Directory content:
    dir
    pause
    exit
)

:: Run main script
if exist "main.py" (
    python main.py
) else (
    echo ERROR: main.py not found
    echo Directory content:
    dir
    pause
    exit
)

pause