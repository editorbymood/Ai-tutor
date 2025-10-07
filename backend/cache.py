"""
Caching utilities for high-performance operations.
"""
from django.core.cache import cache
from django.conf import settings
from functools import wraps
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


def generate_cache_key(prefix, *args, **kwargs):
    """
    Generate a unique cache key based on function arguments.
    
    Args:
        prefix: Cache key prefix
        *args: Positional arguments
        **kwargs: Keyword arguments
    
    Returns:
        str: Unique cache key
    """
    # Create a string representation of arguments
    key_data = {
        'args': args,
        'kwargs': kwargs
    }
    key_string = json.dumps(key_data, sort_keys=True, default=str)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()
    return f"{prefix}:{key_hash}"


def cache_result(timeout=300, key_prefix='default'):
    """
    Decorator to cache function results.
    
    Args:
        timeout: Cache timeout in seconds (default: 5 minutes)
        key_prefix: Prefix for cache key
    
    Usage:
        @cache_result(timeout=600, key_prefix='user_profile')
        def get_user_profile(user_id):
            return expensive_operation(user_id)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = generate_cache_key(f"{key_prefix}:{func.__name__}", *args, **kwargs)
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return result
            
            # Execute function and cache result
            logger.debug(f"Cache miss: {cache_key}")
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        
        return wrapper
    return decorator


def invalidate_cache(key_prefix, *args, **kwargs):
    """
    Invalidate a specific cache entry.
    
    Args:
        key_prefix: Cache key prefix
        *args: Positional arguments used in cache key
        **kwargs: Keyword arguments used in cache key
    """
    cache_key = generate_cache_key(key_prefix, *args, **kwargs)
    cache.delete(cache_key)
    logger.debug(f"Cache invalidated: {cache_key}")


def invalidate_pattern(pattern):
    """
    Invalidate all cache entries matching a pattern.
    
    Args:
        pattern: Pattern to match (e.g., 'user:*')
    """
    try:
        cache.delete_pattern(pattern)
        logger.debug(f"Cache pattern invalidated: {pattern}")
    except AttributeError:
        logger.warning("Cache backend does not support pattern deletion")


class CacheManager:
    """Manager for common caching operations."""
    
    # Cache timeouts (in seconds)
    TIMEOUT_SHORT = 60  # 1 minute
    TIMEOUT_MEDIUM = 300  # 5 minutes
    TIMEOUT_LONG = 3600  # 1 hour
    TIMEOUT_DAY = 86400  # 24 hours
    
    @staticmethod
    def get_user_profile(user_id):
        """Get cached user profile."""
        cache_key = f"user_profile:{user_id}"
        return cache.get(cache_key)
    
    @staticmethod
    def set_user_profile(user_id, profile_data):
        """Cache user profile."""
        cache_key = f"user_profile:{user_id}"
        cache.set(cache_key, profile_data, CacheManager.TIMEOUT_MEDIUM)
    
    @staticmethod
    def invalidate_user_profile(user_id):
        """Invalidate user profile cache."""
        cache_key = f"user_profile:{user_id}"
        cache.delete(cache_key)
    
    @staticmethod
    def get_course_list(filters=None):
        """Get cached course list."""
        cache_key = generate_cache_key("course_list", filters=filters)
        return cache.get(cache_key)
    
    @staticmethod
    def set_course_list(course_data, filters=None):
        """Cache course list."""
        cache_key = generate_cache_key("course_list", filters=filters)
        cache.set(cache_key, course_data, CacheManager.TIMEOUT_MEDIUM)
    
    @staticmethod
    def get_course_detail(course_id):
        """Get cached course detail."""
        cache_key = f"course_detail:{course_id}"
        return cache.get(cache_key)
    
    @staticmethod
    def set_course_detail(course_id, course_data):
        """Cache course detail."""
        cache_key = f"course_detail:{course_id}"
        cache.set(cache_key, course_data, CacheManager.TIMEOUT_LONG)
    
    @staticmethod
    def invalidate_course(course_id):
        """Invalidate course-related caches."""
        cache.delete(f"course_detail:{course_id}")
        invalidate_pattern("course_list:*")
    
    @staticmethod
    def get_analytics(user_id, analytics_type):
        """Get cached analytics data."""
        cache_key = f"analytics:{analytics_type}:{user_id}"
        return cache.get(cache_key)
    
    @staticmethod
    def set_analytics(user_id, analytics_type, data):
        """Cache analytics data."""
        cache_key = f"analytics:{analytics_type}:{user_id}"
        cache.set(cache_key, data, CacheManager.TIMEOUT_MEDIUM)
    
    @staticmethod
    def get_ai_response(prompt_hash):
        """Get cached AI response."""
        cache_key = f"ai_response:{prompt_hash}"
        return cache.get(cache_key)
    
    @staticmethod
    def set_ai_response(prompt_hash, response_data):
        """Cache AI response."""
        cache_key = f"ai_response:{prompt_hash}"
        # Cache AI responses for longer since they're expensive
        cache.set(cache_key, response_data, CacheManager.TIMEOUT_DAY)
    
    @staticmethod
    def clear_all():
        """Clear all cache (use with caution)."""
        cache.clear()
        logger.warning("All cache cleared")


# Rate limiting utilities
class RateLimiter:
    """Simple rate limiter using cache."""
    
    @staticmethod
    def is_rate_limited(identifier, max_requests=100, window=60):
        """
        Check if an identifier is rate limited.
        
        Args:
            identifier: Unique identifier (e.g., user_id, IP address)
            max_requests: Maximum requests allowed in window
            window: Time window in seconds
        
        Returns:
            bool: True if rate limited, False otherwise
        """
        cache_key = f"rate_limit:{identifier}"
        current_count = cache.get(cache_key, 0)
        
        if current_count >= max_requests:
            return True
        
        # Increment counter
        cache.set(cache_key, current_count + 1, window)
        return False
    
    @staticmethod
    def get_remaining_requests(identifier, max_requests=100, window=60):
        """Get remaining requests for an identifier."""
        cache_key = f"rate_limit:{identifier}"
        current_count = cache.get(cache_key, 0)
        return max(0, max_requests - current_count)