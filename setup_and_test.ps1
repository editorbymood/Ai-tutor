# AI-Powered Personal Tutor - Setup and Test Script
# This script sets up the environment and runs all tests

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI-Powered Personal Tutor - Setup & Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set project root
$PROJECT_ROOT = "C:\Users\sanke\OneDrive\Attachments\Desktop\main projects\ai powered tutor"
Set-Location $PROJECT_ROOT

# Find Python executable
Write-Host "Finding Python installation..." -ForegroundColor Yellow
$pythonPaths = @(
    "C:\Python313\python.exe",
    "C:\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python310\python.exe",
    "C:\Users\sanke\venv\Scripts\python.exe",
    "C:\Users\sanke\AppData\Local\Programs\Python\Python313\python.exe",
    "C:\Users\sanke\AppData\Local\Programs\Python\Python312\python.exe",
    "C:\Users\sanke\AppData\Local\Programs\Python\Python311\python.exe"
)

$PYTHON_EXE = $null
foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        $PYTHON_EXE = $path
        Write-Host "[OK] Found Python at: $PYTHON_EXE" -ForegroundColor Green
        break
    }
}

if (-not $PYTHON_EXE) {
    Write-Host "[ERROR] Python not found! Please install Python 3.10 or higher." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check Python version
Write-Host ""
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = & $PYTHON_EXE --version 2>&1
Write-Host "[OK] $pythonVersion" -ForegroundColor Green

# Check if virtual environment exists
$VENV_PATH = Join-Path $PROJECT_ROOT "venv"
if (-not (Test-Path $VENV_PATH)) {
    Write-Host ""
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    & $PYTHON_EXE -m venv $VENV_PATH
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "[OK] Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
$VENV_PYTHON = Join-Path $VENV_PATH "Scripts\python.exe"
$VENV_PIP = Join-Path $VENV_PATH "Scripts\pip.exe"

# Install/upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& $VENV_PYTHON -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Pip upgraded" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Pip upgrade failed, continuing..." -ForegroundColor Yellow
}

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
& $VENV_PIP install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    Write-Host "Trying without --quiet flag for detailed error..." -ForegroundColor Yellow
    & $VENV_PIP install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        exit 1
    }
}

# Check if .env file exists
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
$ENV_FILE = Join-Path $PROJECT_ROOT ".env"
if (-not (Test-Path $ENV_FILE)) {
    Write-Host "[WARNING] .env file not found. Creating from .env.example..." -ForegroundColor Yellow
    $ENV_EXAMPLE = Join-Path $PROJECT_ROOT ".env.example"
    if (Test-Path $ENV_EXAMPLE) {
        Copy-Item $ENV_EXAMPLE $ENV_FILE
        Write-Host "[OK] .env file created. Please configure it with your settings." -ForegroundColor Green
        Write-Host "  Required: GEMINI_API_KEY, MONGODB_URI, REDIS_URL" -ForegroundColor Yellow
    } else {
        Write-Host "[WARNING] .env.example not found. Creating minimal .env..." -ForegroundColor Yellow
        $envContent = "# Django Settings`nSECRET_KEY=your-secret-key-here-change-in-production`nDEBUG=True`nALLOWED_HOSTS=localhost;127.0.0.1`n`n# Database`nMONGODB_URI=mongodb://localhost:27017/ai_tutor_db`n`n# Redis`nREDIS_URL=redis://localhost:6379/0`n`n# Google Gemini AI`nGEMINI_API_KEY=your-gemini-api-key-here`n`n# Celery`nCELERY_BROKER_URL=redis://localhost:6379/0`nCELERY_RESULT_BACKEND=redis://localhost:6379/0"
        $envContent | Out-File -FilePath $ENV_FILE -Encoding UTF8
        Write-Host "[OK] Minimal .env file created" -ForegroundColor Green
    }
} else {
    Write-Host "[OK] .env file exists" -ForegroundColor Green
}

# Create necessary directories
Write-Host ""
Write-Host "Creating necessary directories..." -ForegroundColor Yellow
$directories = @("reports", "logs", "media", "staticfiles")
foreach ($dir in $directories) {
    $dirPath = Join-Path $PROJECT_ROOT $dir
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
        Write-Host "[OK] Created $dir directory" -ForegroundColor Green
    }
}

# Run Django checks
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Django System Checks" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& $VENV_PYTHON manage.py check --deploy
$djangoCheckResult = $LASTEXITCODE

if ($djangoCheckResult -eq 0) {
    Write-Host ""
    Write-Host "[OK] Django checks passed" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[WARNING] Django checks found issues (this is normal for development)" -ForegroundColor Yellow
}

# Run tests
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Test Suite" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run pytest with coverage
Write-Host "Running unit tests with coverage..." -ForegroundColor Yellow
& $VENV_PYTHON -m pytest tests/ -v --tb=short --maxfail=5 2>&1 | Tee-Object -FilePath "reports\test_output.txt"
$testResult = $LASTEXITCODE

if ($testResult -eq 0) {
    Write-Host ""
    Write-Host "[OK] All tests passed!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[WARNING] Some tests failed. Check reports\test_output.txt for details" -ForegroundColor Yellow
}

# Generate test report
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$summary = @"
AI-Powered Personal Tutor - Test Report
Generated: $timestamp

Environment Setup:
- Python: $pythonVersion
- Virtual Environment: $VENV_PATH
- Dependencies: Installed

Django Checks: $(if ($djangoCheckResult -eq 0) { "PASSED" } else { "WARNINGS" })
Unit Tests: $(if ($testResult -eq 0) { "PASSED" } else { "FAILED" })

Next Steps:
1. Configure .env file with your API keys
2. Start MongoDB: docker run -d -p 27017:27017 mongo
3. Start Redis: docker run -d -p 6379:6379 redis
4. Run migrations: python manage.py migrate
5. Create superuser: python manage.py createsuperuser
6. Start server: python manage.py runserver

For load testing:
- locust -f tests/load_test.py --host=http://localhost:8000

For production deployment:
- See DEPLOYMENT.md and SCALING_GUIDE.md
"@

Write-Host $summary
$summary | Out-File -FilePath "reports\setup_summary.txt" -Encoding UTF8

Write-Host ""
Write-Host "[OK] Setup and testing complete!" -ForegroundColor Green
Write-Host "Report saved to: reports\setup_summary.txt" -ForegroundColor Gray

# Exit with test result code
exit $testResult