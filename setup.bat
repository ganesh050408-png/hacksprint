@echo off
REM Student Attendance System - Installation and Setup Script for Windows

echo.
echo ========================================
echo Student Attendance System Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detected
python --version

REM Create virtual environment
echo.
echo [1/5] Creating virtual environment...
if exist venv (
    echo [INFO] Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Install requirements
echo.
echo [3/5] Installing dependencies...
echo This may take a few minutes...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies may have installation issues
    echo Please check if face-recognition and dlib are properly installed
    echo You may need to install them separately
)
echo [OK] Dependencies installed

REM Create directories
echo.
echo [4/5] Creating required directories...
if not exist uploads mkdir uploads
if not exist student_faces mkdir student_faces
echo [OK] Directories created

REM Initialize database
echo.
echo [5/5] Initializing database...
python setup.py
if errorlevel 1 (
    echo [ERROR] Failed to initialize database
    pause
    exit /b 1
)
echo [OK] Database initialized

REM Final message
echo.
echo ========================================
echo Setup Completed Successfully!
echo ========================================
echo.
echo To run the application, execute:
echo   python run.py
echo.
echo The application will be available at:
echo   http://localhost:5000
echo.
echo Default Login Credentials:
echo   Student:    student1 / password123
echo   Teacher:    teacher1 / password123
echo   Counsellor: counsellor1 / password123
echo.
echo Documentation:
echo   README.md        - Full documentation
echo   QUICKSTART.md    - Getting started
echo   USER_GUIDE.md    - User workflows
echo.
echo ========================================
echo.
pause
