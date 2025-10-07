@echo off
echo ========================================
echo AI-Powered Personal Tutor - Quick Start
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your GEMINI_API_KEY
    echo Press any key to open .env file...
    pause > nul
    notepad .env
)

echo.
echo Starting services...
echo.

REM Start MongoDB (if installed)
echo Starting MongoDB...
start "MongoDB" cmd /k "mongod"
timeout /t 3 > nul

REM Start Redis (if installed)
echo Starting Redis...
start "Redis" cmd /k "redis-server"
timeout /t 3 > nul

REM Activate virtual environment and start Django
echo Starting Django Backend...
start "Django Backend" cmd /k "venv\Scripts\activate && python manage.py runserver"
timeout /t 5 > nul

REM Start Celery worker
echo Starting Celery Worker...
start "Celery Worker" cmd /k "venv\Scripts\activate && celery -A backend worker -l info"
timeout /t 3 > nul

REM Start React frontend
echo Starting React Frontend...
start "React Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo All services started!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo Admin: http://localhost:8000/admin
echo.
echo Press any key to stop all services...
pause > nul

REM Stop all services
taskkill /FI "WindowTitle eq MongoDB*" /T /F
taskkill /FI "WindowTitle eq Redis*" /T /F
taskkill /FI "WindowTitle eq Django Backend*" /T /F
taskkill /FI "WindowTitle eq Celery Worker*" /T /F
taskkill /FI "WindowTitle eq React Frontend*" /T /F

echo All services stopped.
pause