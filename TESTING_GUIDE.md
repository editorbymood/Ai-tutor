# Testing Guide

## Overview

This guide covers comprehensive testing strategies for the AI-Powered Personal Tutor platform, including unit tests, integration tests, load tests, and performance benchmarks.

## Table of Contents

1. [Setup Testing Environment](#setup-testing-environment)
2. [Unit Tests](#unit-tests)
3. [Integration Tests](#integration-tests)
4. [Load Testing](#load-testing)
5. [Performance Testing](#performance-testing)
6. [CI/CD Integration](#cicd-integration)

---

## Setup Testing Environment

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Configure Test Database

Tests use a separate test database automatically created by pytest-django.

### Environment Variables

Create a `.env.test` file:

```env
DEBUG=True
SECRET_KEY=test-secret-key
MONGODB_NAME=ai_tutor_test_db
REDIS_URL=redis://localhost:6379/15
GEMINI_API_KEY=your-test-api-key
```

---

## Unit Tests

### Running Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest tests/test_authentication.py

# Run specific test class
pytest tests/test_authentication.py::TestUserRegistration

# Run specific test method
pytest tests/test_authentication.py::TestUserRegistration::test_register_student

# Run tests in parallel (faster)
pytest -n auto
```

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_authentication.py   # Auth tests
├── test_courses.py          # Course tests
├── test_ai_tutor.py         # AI tutor tests
├── test_assessments.py      # Assessment tests
└── test_analytics.py        # Analytics tests
```

### Writing Tests

Example test:

```python
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
```

### Test Coverage Goals

- **Minimum**: 80% code coverage
- **Target**: 90% code coverage
- **Critical paths**: 100% coverage (authentication, payments, data integrity)

---

## Integration Tests

### API Integration Tests

Test complete API workflows:

```bash
# Run integration tests
pytest tests/integration/

# Run with verbose output
pytest tests/integration/ -v
```

### Example Integration Test

```python
@pytest.mark.django_db
class TestCourseEnrollmentFlow:
    def test_complete_enrollment_flow(self, authenticated_client, course):
        # 1. View course
        response = authenticated_client.get(f'/api/courses/{course.id}/')
        assert response.status_code == 200
        
        # 2. Enroll in course
        response = authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        assert response.status_code == 200
        
        # 3. View enrolled courses
        response = authenticated_client.get('/api/courses/enrolled/')
        assert response.status_code == 200
        assert len(response.data['results']) > 0
```

---

## Load Testing

### Using Locust

Locust is a Python-based load testing tool that simulates thousands of concurrent users.

#### Install Locust

```bash
pip install locust
```

#### Run Load Tests

```bash
# Start Locust web interface
locust -f tests/load_test.py --host=http://localhost:8000

# Run headless (no web UI)
locust -f tests/load_test.py --host=http://localhost:8000 \
       --users 1000 --spawn-rate 10 --run-time 5m --headless

# Run with specific user distribution
locust -f tests/load_test.py --host=http://localhost:8000 \
       --users 1000 --spawn-rate 50 --run-time 10m
```

#### Access Locust Dashboard

Open http://localhost:8089 in your browser to:
- Configure number of users
- Set spawn rate
- Start/stop tests
- View real-time statistics
- Download reports

### Load Test Scenarios

#### Scenario 1: Normal Load
- **Users**: 100 concurrent users
- **Duration**: 5 minutes
- **Expected**: < 200ms average response time

```bash
locust -f tests/load_test.py --host=http://localhost:8000 \
       --users 100 --spawn-rate 10 --run-time 5m --headless
```

#### Scenario 2: Peak Load
- **Users**: 1,000 concurrent users
- **Duration**: 10 minutes
- **Expected**: < 500ms average response time

```bash
locust -f tests/load_test.py --host=http://localhost:8000 \
       --users 1000 --spawn-rate 50 --run-time 10m --headless
```

#### Scenario 3: Stress Test
- **Users**: 10,000 concurrent users
- **Duration**: 15 minutes
- **Expected**: System remains stable, no crashes

```bash
locust -f tests/load_test.py --host=http://localhost:8000 \
       --users 10000 --spawn-rate 100 --run-time 15m --headless
```

#### Scenario 4: Spike Test
- **Users**: Rapid increase from 100 to 5,000
- **Duration**: 5 minutes
- **Expected**: System handles sudden traffic spike

```bash
locust -f tests/load_test.py --host=http://localhost:8000 \
       --users 5000 --spawn-rate 500 --run-time 5m --headless
```

### Interpreting Results

Key metrics to monitor:

1. **Response Time**
   - P50 (median): < 200ms
   - P95: < 500ms
   - P99: < 1000ms

2. **Throughput**
   - Requests per second (RPS)
   - Target: > 1000 RPS

3. **Error Rate**
   - Target: < 0.1%

4. **Resource Usage**
   - CPU: < 80%
   - Memory: < 80%
   - Database connections: < 80% of pool

---

## Performance Testing

### Database Query Performance

```bash
# Enable query logging
python manage.py shell

from django.db import connection
from django.test.utils import override_settings

# Run queries and check count
print(len(connection.queries))
```

### API Endpoint Benchmarking

Using Apache Bench (ab):

```bash
# Test course list endpoint
ab -n 1000 -c 10 -H "Authorization: Bearer YOUR_TOKEN" \
   http://localhost:8000/api/courses/

# Test AI chat endpoint
ab -n 100 -c 5 -p chat_payload.json -T application/json \
   -H "Authorization: Bearer YOUR_TOKEN" \
   http://localhost:8000/api/ai-tutor/chat/
```

### Cache Performance

```bash
# Test cache hit rate
curl http://localhost:8000/metrics/cache/

# Expected output:
{
  "hit_rate": 85.5,  # Target: > 80%
  "keyspace_hits": 8550,
  "keyspace_misses": 1450
}
```

### Monitoring Endpoints

```bash
# Health check
curl http://localhost:8000/health/

# Readiness check
curl http://localhost:8000/health/ready/

# System metrics
curl http://localhost:8000/metrics/

# Cache statistics
curl http://localhost:8000/metrics/cache/

# Database statistics
curl http://localhost:8000/metrics/database/
```

---

## Performance Benchmarks

### Target Performance Metrics

#### For 1 Million Users

| Metric | Target | Notes |
|--------|--------|-------|
| Concurrent Users | 10,000+ | Peak load |
| Response Time (P95) | < 500ms | API endpoints |
| Response Time (P99) | < 1000ms | API endpoints |
| AI Response Time | < 3s | Gemini API calls |
| Throughput | 5,000+ RPS | Requests per second |
| Error Rate | < 0.1% | 4xx/5xx errors |
| Database Queries | < 10 per request | N+1 prevention |
| Cache Hit Rate | > 80% | Redis cache |
| CPU Usage | < 70% | Average load |
| Memory Usage | < 80% | Average load |
| Database Connections | < 80 | Connection pool |

### Scaling Strategy

#### Horizontal Scaling

```yaml
# docker-compose.production.yml
# Add more backend instances:
backend-3:
  # Same config as backend-1
backend-4:
  # Same config as backend-1

# Add more Celery workers:
celery-worker-3:
  # Same config as celery-worker-1
```

#### Database Scaling

1. **MongoDB Replica Set** (High Availability)
2. **Sharding** (Horizontal partitioning)
3. **Read Replicas** (Distribute read load)

#### Caching Strategy

1. **Redis Cluster** (Distributed caching)
2. **CDN** (Static assets)
3. **Application-level caching** (Query results)

---

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mongodb:
        image: mongo:6.0
        ports:
          - 27017:27017
      
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest --cov=apps --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### Pre-commit Hooks

Install pre-commit:

```bash
pip install pre-commit
pre-commit install
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

---

## Continuous Monitoring

### Production Monitoring

1. **Sentry** - Error tracking
2. **Prometheus + Grafana** - Metrics visualization
3. **ELK Stack** - Log aggregation
4. **New Relic / DataDog** - APM

### Key Metrics to Monitor

1. **Application Metrics**
   - Request rate
   - Response time
   - Error rate
   - Active users

2. **Infrastructure Metrics**
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network traffic

3. **Business Metrics**
   - User registrations
   - Course enrollments
   - AI chat sessions
   - Quiz completions

---

## Troubleshooting

### Common Issues

#### Slow Tests

```bash
# Identify slow tests
pytest --durations=10

# Run tests in parallel
pytest -n auto
```

#### Database Connection Issues

```bash
# Check MongoDB connection
python manage.py dbshell

# Check connection pool
curl http://localhost:8000/metrics/database/
```

#### Cache Issues

```bash
# Clear cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Check Redis
redis-cli ping
```

---

## Best Practices

1. **Write tests first** (TDD approach)
2. **Keep tests isolated** (no dependencies between tests)
3. **Use fixtures** (DRY principle)
4. **Mock external services** (AI APIs, email, etc.)
5. **Test edge cases** (empty data, invalid input, etc.)
6. **Monitor test coverage** (aim for 90%+)
7. **Run tests in CI/CD** (automated testing)
8. **Load test regularly** (before major releases)

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Locust Documentation](https://docs.locust.io/)
- [Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)

---

## Support

For testing issues or questions, please:
1. Check this guide
2. Review test logs
3. Check monitoring dashboards
4. Contact the development team