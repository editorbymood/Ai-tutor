# AI-Powered Personal Tutor - Complete Setup Guide

This guide will walk you through setting up the AI-Powered Personal Tutor platform on your local machine.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Manual Setup](#manual-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

1. **Python 3.10 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Node.js 18 or higher**
   - Download from: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **MongoDB 6.0 or higher**
   - Download from: https://www.mongodb.com/try/download/community
   - Or use Docker: `docker run -d -p 27017:27017 mongo:6.0`
   - Verify: `mongosh` or `mongo`

4. **Redis 7.0 or higher**
   - Windows: Download from https://github.com/microsoftarchive/redis/releases
   - Or use Docker: `docker run -d -p 6379:6379 redis:alpine`
   - Verify: `redis-cli ping` (should return PONG)

5. **Git**
   - Download from: https://git-scm.com/downloads
   - Verify: `git --version`

### API Keys

1. **Google Gemini API Key**
   - Get it from: https://makersuite.google.com/app/apikey
   - Free tier available

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd "ai powered tutor"

# Run setup script
python setup.py
```

The setup script will:
- Create .env file
- Install all dependencies
- Run database migrations
- Prompt to create superuser

### Option 2: Docker Setup (Easiest)

```bash
# Clone the repository
git clone <repository-url>
cd "ai powered tutor"

# Copy and configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start all services
docker-compose up -d

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin Panel: http://localhost:8000/admin

## Manual Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd "ai powered tutor"
```

### Step 2: Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Go back to root
cd ..
```

### Step 4: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and set:
# - GEMINI_API_KEY (required)
# - SECRET_KEY (auto-generated or custom)
# - Database settings (if not using defaults)
```

### Step 5: Database Setup

```bash
# Make sure MongoDB is running
# Then run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Configuration

### Environment Variables

Edit `.env` file:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (MongoDB)
MONGODB_NAME=ai_tutor_db
MONGODB_HOST=localhost
MONGODB_PORT=27017

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Redis
REDIS_URL=redis://localhost:6379/0

# Frontend
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend Configuration

Edit `frontend/.env.local`:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Running the Application

### Development Mode

You need to run 4 services:

#### Terminal 1: MongoDB
```bash
# If not using Docker
mongod
```

#### Terminal 2: Redis
```bash
# If not using Docker
redis-server
```

#### Terminal 3: Django Backend
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run development server
python manage.py runserver
```

Backend will be available at: http://localhost:8000

#### Terminal 4: Celery Worker
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run Celery worker
celery -A backend worker -l info
```

#### Terminal 5: React Frontend
```bash
cd frontend
npm start
```

Frontend will be available at: http://localhost:3000

### Production Mode

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions.

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific test file
pytest tests/test_users.py
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## Features Overview

### For Students

1. **Personalized Learning**
   - Take learning style assessment
   - Get personalized content recommendations
   - Adaptive difficulty levels

2. **AI Tutor Chat**
   - Real-time conversation with AI
   - Context-aware responses
   - Learning style adapted explanations

3. **Course Management**
   - Browse and enroll in courses
   - Track progress
   - Complete lessons and quizzes

4. **Analytics Dashboard**
   - View learning statistics
   - Track quiz performance
   - Monitor study streaks

### For Teachers

1. **Course Creation**
   - Create courses and lessons
   - Use AI to generate content
   - Manage course materials

2. **Student Management**
   - View student progress
   - Monitor class performance
   - Generate reports

3. **AI-Assisted Content**
   - Generate lesson plans
   - Create quizzes automatically
   - Get content suggestions

### AI & ML Features

1. **Learning Style Detection**
   - K-means clustering
   - Analyzes interaction patterns
   - Adapts content delivery

2. **Performance Prediction**
   - Random Forest classifier
   - Identifies at-risk students
   - Provides early interventions

3. **Sentiment Analysis**
   - Analyzes student feedback
   - Monitors engagement
   - Improves content quality

4. **Content Generation**
   - Google Gemini integration
   - Personalized lessons
   - Custom quizzes and explanations

## Troubleshooting

### Common Issues

#### 1. MongoDB Connection Error

**Error:** `pymongo.errors.ServerSelectionTimeoutError`

**Solution:**
```bash
# Check if MongoDB is running
mongosh

# If not, start MongoDB
mongod

# Or use Docker
docker run -d -p 27017:27017 mongo:6.0
```

#### 2. Redis Connection Error

**Error:** `redis.exceptions.ConnectionError`

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# If not, start Redis
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:alpine
```

#### 3. Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'xxx'`

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

#### 4. Frontend Won't Start

**Error:** Various npm errors

**Solution:**
```bash
cd frontend

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Try starting again
npm start
```

#### 5. Gemini API Error

**Error:** `google.api_core.exceptions.PermissionDenied`

**Solution:**
- Check your GEMINI_API_KEY in .env
- Verify the API key is valid
- Check API quota limits

#### 6. CORS Error

**Error:** `Access-Control-Allow-Origin` error in browser

**Solution:**
- Check CORS_ALLOWED_ORIGINS in .env
- Make sure it includes your frontend URL
- Restart Django server after changes

### Getting Help

If you encounter issues:

1. Check the logs:
   - Django: `logs/django.log`
   - Browser console for frontend errors

2. Search existing issues on GitHub

3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version, etc.)

## Next Steps

After setup:

1. **Create Your Profile**
   - Complete learning style assessment
   - Set preferences

2. **Explore Courses**
   - Browse available courses
   - Enroll in courses

3. **Try AI Tutor**
   - Start a chat session
   - Ask questions
   - Get personalized explanations

4. **For Teachers**
   - Create your first course
   - Use AI to generate content
   - Monitor student progress

## Additional Resources

- [API Documentation](http://localhost:8000/api/docs/)
- [Deployment Guide](DEPLOYMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [License](LICENSE)

## Support

- Email: support@aitutor.com
- GitHub Issues: <repository-url>/issues
- Documentation: <docs-url>

---

**Happy Learning! 🎓🤖**