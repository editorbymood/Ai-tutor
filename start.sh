#!/bin/bash

echo "========================================"
echo "AI-Powered Personal Tutor - Quick Start"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env and add your GEMINI_API_KEY"
    echo "Press Enter to continue..."
    read
fi

echo ""
echo "Starting services..."
echo ""

# Start MongoDB (if not running)
if ! pgrep -x "mongod" > /dev/null; then
    echo "Starting MongoDB..."
    mongod --fork --logpath /tmp/mongodb.log
fi

# Start Redis (if not running)
if ! pgrep -x "redis-server" > /dev/null; then
    echo "Starting Redis..."
    redis-server --daemonize yes
fi

# Activate virtual environment and start Django
echo "Starting Django Backend..."
source venv/bin/activate
python manage.py runserver &
DJANGO_PID=$!

# Start Celery worker
echo "Starting Celery Worker..."
celery -A backend worker -l info &
CELERY_PID=$!

# Start React frontend
echo "Starting React Frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "All services started!"
echo "========================================"
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Admin: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for Ctrl+C
trap "kill $DJANGO_PID $CELERY_PID $FRONTEND_PID; exit" INT
wait