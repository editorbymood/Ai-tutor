"""
Health check and monitoring endpoints.
"""
from django.http import JsonResponse
from django.core.cache import cache
from django.db import connection
from django.conf import settings
import redis
import time
import logging

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Basic health check endpoint.
    
    Returns:
        JSON response with health status
    """
    return JsonResponse({
        'status': 'healthy',
        'timestamp': time.time()
    })


def readiness_check(request):
    """
    Readiness check - verifies all dependencies are available.
    
    Checks:
    - Database connection
    - Redis connection
    - Cache availability
    
    Returns:
        JSON response with detailed status
    """
    checks = {
        'database': False,
        'redis': False,
        'cache': False,
    }
    
    overall_status = 'healthy'
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks['database'] = True
    except Exception as e:
        logger.error(f"Database check failed: {str(e)}")
        overall_status = 'unhealthy'
    
    # Check Redis
    try:
        redis_client = redis.from_url(settings.CELERY_BROKER_URL)
        redis_client.ping()
        checks['redis'] = True
    except Exception as e:
        logger.error(f"Redis check failed: {str(e)}")
        overall_status = 'unhealthy'
    
    # Check cache
    try:
        cache_key = 'health_check_test'
        cache.set(cache_key, 'test', 10)
        result = cache.get(cache_key)
        if result == 'test':
            checks['cache'] = True
        cache.delete(cache_key)
    except Exception as e:
        logger.error(f"Cache check failed: {str(e)}")
        overall_status = 'unhealthy'
    
    status_code = 200 if overall_status == 'healthy' else 503
    
    return JsonResponse({
        'status': overall_status,
        'checks': checks,
        'timestamp': time.time()
    }, status=status_code)


def liveness_check(request):
    """
    Liveness check - verifies the application is running.
    
    Returns:
        JSON response with liveness status
    """
    return JsonResponse({
        'status': 'alive',
        'timestamp': time.time()
    })


def metrics(request):
    """
    Basic metrics endpoint.
    
    Returns:
        JSON response with system metrics
    """
    import psutil
    import os
    
    try:
        process = psutil.Process(os.getpid())
        
        metrics_data = {
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count()
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'process_memory': process.memory_info().rss
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent
            },
            'process': {
                'pid': os.getpid(),
                'threads': process.num_threads(),
                'connections': len(process.connections())
            },
            'timestamp': time.time()
        }
        
        return JsonResponse(metrics_data)
    
    except Exception as e:
        logger.error(f"Metrics collection failed: {str(e)}")
        return JsonResponse({
            'error': 'Failed to collect metrics',
            'timestamp': time.time()
        }, status=500)


def cache_stats(request):
    """
    Cache statistics endpoint.
    
    Returns:
        JSON response with cache statistics
    """
    try:
        redis_client = redis.from_url(settings.CELERY_BROKER_URL)
        info = redis_client.info()
        
        stats = {
            'redis_version': info.get('redis_version'),
            'connected_clients': info.get('connected_clients'),
            'used_memory': info.get('used_memory'),
            'used_memory_human': info.get('used_memory_human'),
            'total_commands_processed': info.get('total_commands_processed'),
            'instantaneous_ops_per_sec': info.get('instantaneous_ops_per_sec'),
            'keyspace_hits': info.get('keyspace_hits'),
            'keyspace_misses': info.get('keyspace_misses'),
            'timestamp': time.time()
        }
        
        # Calculate hit rate
        hits = stats.get('keyspace_hits', 0)
        misses = stats.get('keyspace_misses', 0)
        total = hits + misses
        
        if total > 0:
            stats['hit_rate'] = (hits / total) * 100
        else:
            stats['hit_rate'] = 0
        
        return JsonResponse(stats)
    
    except Exception as e:
        logger.error(f"Cache stats collection failed: {str(e)}")
        return JsonResponse({
            'error': 'Failed to collect cache stats',
            'timestamp': time.time()
        }, status=500)


def database_stats(request):
    """
    Database statistics endpoint.
    
    Returns:
        JSON response with database statistics
    """
    try:
        from django.contrib.auth import get_user_model
        from apps.courses.models import Course, Enrollment
        from apps.assessments.models import Quiz, QuizAttempt
        from apps.ai_tutor.models import ChatSession, ChatMessage
        
        User = get_user_model()
        
        stats = {
            'users': {
                'total': User.objects.count(),
                'students': User.objects.filter(role='student').count(),
                'teachers': User.objects.filter(role='teacher').count(),
            },
            'courses': {
                'total': Course.objects.count(),
                'published': Course.objects.filter(is_published=True).count(),
            },
            'enrollments': {
                'total': Enrollment.objects.count(),
            },
            'assessments': {
                'quizzes': Quiz.objects.count(),
                'attempts': QuizAttempt.objects.count(),
            },
            'ai_tutor': {
                'sessions': ChatSession.objects.count(),
                'messages': ChatMessage.objects.count(),
            },
            'timestamp': time.time()
        }
        
        return JsonResponse(stats)
    
    except Exception as e:
        logger.error(f"Database stats collection failed: {str(e)}")
        return JsonResponse({
            'error': 'Failed to collect database stats',
            'timestamp': time.time()
        }, status=500)