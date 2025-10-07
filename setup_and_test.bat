@echo off
REM AI-Powered Personal Tutor - Setup and Test Script

echo ========================================
echo AI-Powered Personal Tutor - Setup and Test
echo ========================================
echo.

cd /d "C:\Users\sanke\OneDrive\Attachments\Desktop\main projects\ai powered tutor"

REM Try to find Python
echo Finding Python installation...
set PYTHON_EXE=

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXE=python
    echo [OK] Found Python in PATH
    goto :found_python
)

if exist "C:\Python313\python.exe" (
    set PYTHON_EXE=C:\Python313\python.exe
    echo [OK] Found Python at C:\Python313\python.exe
    goto :found_python
)

if exist "C:\Python312\python.exe" (
    set PYTHON_EXE=C:\Python312\python.exe
    echo [OK] Found Python at C:\Python312\python.exe
    goto :found_python
)

if exist "C:\Python311\python.exe" (
    set PYTHON_EXE=C:\Python311\python.exe
    echo [OK] Found Python at C:\Python311\python.exe
    goto :found_python
)

if exist "venv\Scripts\python.exe" (
    set PYTHON_EXE=venv\Scripts\python.exe
    echo [OK] Found Python in project venv
    goto :found_python
)

echo [ERROR] Python not found! Please install Python 3.10 or higher.
echo Download from: https://www.python.org/downloads/
pause
exit /b 1

:found_python
echo.
echo Checking Python version...
%PYTHON_EXE% --version
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to run Python
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    %PYTHON_EXE% -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo.
    echo [OK] Virtual environment already exists
)

REM Use venv Python
set VENV_PYTHON=venv\Scripts\python.exe
set VENV_PIP=venv\Scripts\pip.exe

REM Upgrade pip
echo.
echo Upgrading pip...
%VENV_PYTHON% -m pip install --upgrade pip --quiet
if %ERRORLEVEL% EQU 0 (
    echo [OK] Pip upgraded
) else (
    echo [WARNING] Pip upgrade failed, continuing...
)

REM Install dependencies
echo.
echo Installing dependencies...
echo This may take a few minutes...
%VENV_PIP% install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Check .env file
echo.
echo Checking environment configuration...
if not exist ".env" (
    echo [WARNING] .env file not found
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo [OK] .env file created from .env.example
        echo Please configure it with your settings
    ) else (
        echo Creating minimal .env file...
        (
            echo # Django Settings
            echo SECRET_KEY=your-secret-key-here-change-in-production
            echo DEBUG=True
            echo ALLOWED_HOSTS=localhost,127.0.0.1
            echo.
            echo # Database
            echo MONGODB_URI=mongodb://localhost:27017/ai_tutor_db
            echo.
            echo # Redis
            echo REDIS_URL=redis://localhost:6379/0
            echo.
            echo # Google Gemini AI
            echo GEMINI_API_KEY=your-gemini-api-key-here
            echo.
            echo # Celery
            echo CELERY_BROKER_URL=redis://localhost:6379/0
            echo CELERY_RESULT_BACKEND=redis://localhost:6379/0
        ) > .env
        echo [OK] Minimal .env file created
    )
) else (
    echo [OK] .env file exists
)

REM Create directories
echo.
echo Creating necessary directories...
if not exist "reports" mkdir reports
if not exist "logs" mkdir logs
if not exist "media" mkdir media
if not exist "staticfiles" mkdir staticfiles
echo [OK] Directories created

REM Run Django checks
echo.
echo ========================================
echo Running Django System Checks
echo ========================================
echo.
%VENV_PYTHON% manage.py check
set DJANGO_CHECK=%ERRORLEVEL%

REM Run tests
echo.
echo ========================================
echo Running Test Suite
echo ========================================
echo.
echo Running unit tests...
%VENV_PYTHON% -m pytest tests/ -v --tb=short --maxfail=5 > reports\test_output.txt 2>&1
set TEST_RESULT=%ERRORLEVEL%

type reports\test_output.txt

if %TEST_RESULT% EQU 0 (
    echo.
    echo [OK] All tests passed!
) else (
    echo.
    echo [WARNING] Some tests failed. Check reports\test_output.txt for details
)

REM Generate summary
echo.
echo ========================================
echo Test Summary
echo ========================================
echo.
echo Django Checks: %DJANGO_CHECK%
echo Unit Tests: %TEST_RESULT%
echo.
echo Next Steps:
echo 1. Configure .env file with your API keys
echo 2. Start MongoDB: docker run -d -p 27017:27017 mongo
echo 3. Start Redis: docker run -d -p 6379:6379 redis
echo 4. Run migrations: python manage.py migrate
echo 5. Create superuser: python manage.py createsuperuser
echo 6. Start server: python manage.py runserver
echo.
echo For load testing:
echo   locust -f tests/load_test.py --host=http://localhost:8000
echo.
echo [OK] Setup and testing complete!
echo Report saved to: reports\test_output.txt

pause
exit /b %TEST_RESULT%