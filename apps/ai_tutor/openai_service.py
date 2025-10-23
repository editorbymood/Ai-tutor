"""
OpenAI GPT service for content generation and chat.
"""
from django.conf import settings
from django.core.cache import cache
import time
import logging
import hashlib
import json
from functools import wraps

logger = logging.getLogger(__name__)

# Import OpenAI
try:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
except ImportError:
    client = None
    logger.warning("OpenAI library not installed. Install with: pip install openai")


def cache_ai_response(timeout=3600):
    """
    Decorator to cache AI responses.
    
    Args:
        timeout: Cache timeout in seconds (default: 1 hour)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Generate cache key from function arguments
            cache_data = {
                'func': func.__name__,
                'args': args,
                'kwargs': kwargs,
                'provider': 'openai'
            }
            cache_string = json.dumps(cache_data, sort_keys=True, default=str)
            cache_hash = hashlib.md5(cache_string.encode()).hexdigest()
            cache_key = f"ai_response:openai:{func.__name__}:{cache_hash}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"OpenAI cache hit: {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            logger.info(f"OpenAI cache miss: {func.__name__}")
            result = func(self, *args, **kwargs)
            
            # Only cache successful responses
            if result.get('success'):
                cache.set(cache_key, result, timeout)
            
            return result
        
        return wrapper
    return decorator


class OpenAIService:
    """Service class for interacting with OpenAI API with caching and retry logic."""
    
    def __init__(self, model_name='gpt-4o-mini'):
        self.model_name = model_name
        self.client = client
        self.max_retries = 3
        self.retry_delay = 1  # seconds
    
    def _retry_with_backoff(self, func, *args, **kwargs):
        """
        Retry a function with exponential backoff.
        
        Args:
            func: Function to retry
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Function result
        """
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = self.retry_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
    
    def generate_content(self, prompt, **kwargs):
        """
        Generate content using OpenAI with retry logic.
        
        Args:
            prompt: The prompt text
            **kwargs: Additional generation parameters
        
        Returns:
            dict: Response with content and metadata
        """
        if not self.client:
            return {
                'success': False,
                'error': 'OpenAI client not initialized. Please check your API key.'
            }
        
        try:
            start_time = time.time()
            
            def _generate():
                return self.client.chat.completions.create(  # type: ignore[union-attr]
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=kwargs.get('temperature', 0.7),
                    max_tokens=kwargs.get('max_tokens', 2048),
                    top_p=kwargs.get('top_p', 1.0),
                )
            
            response = self._retry_with_backoff(_generate)
            response_time = time.time() - start_time
            
            return {
                'success': True,
                'content': response.choices[0].message.content,  # type: ignore[union-attr]
                'model': self.model_name,
                'response_time': response_time,
                'prompt_tokens': response.usage.prompt_tokens if response.usage else None,  # type: ignore[union-attr]
                'completion_tokens': response.usage.completion_tokens if response.usage else None,  # type: ignore[union-attr]
            }
        
        except Exception as e:
            logger.error(f"OpenAI API error after {self.max_retries} attempts: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def chat(self, messages, **kwargs):
        """
        Have a conversation with OpenAI GPT.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters
        
        Returns:
            dict: Response with content and metadata
        """
        if not self.client:
            return {
                'success': False,
                'error': 'OpenAI client not initialized. Please check your API key.'
            }
        
        try:
            start_time = time.time()
            
            # Convert messages to OpenAI format
            openai_messages = []
            for msg in messages:
                role = msg['role']
                if role == 'assistant':
                    role = 'assistant'
                elif role == 'system':
                    role = 'system'
                else:
                    role = 'user'
                openai_messages.append({
                    'role': role,
                    'content': msg['content']
                })
            
            response = self.client.chat.completions.create(  # type: ignore[union-attr]
                model=self.model_name,
                messages=openai_messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 2048),
            )
            
            response_time = time.time() - start_time
            
            return {
                'success': True,
                'content': response.choices[0].message.content,  # type: ignore[union-attr]
                'model': self.model_name,
                'response_time': response_time,
                'prompt_tokens': response.usage.prompt_tokens if response.usage else None,  # type: ignore[union-attr]
                'completion_tokens': response.usage.completion_tokens if response.usage else None,  # type: ignore[union-attr]
            }
        
        except Exception as e:
            logger.error(f"OpenAI chat error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @cache_ai_response(timeout=7200)  # Cache for 2 hours
    def generate_lesson(self, topic, learning_style, difficulty, **kwargs):
        """Generate a personalized lesson with caching."""
        
        prompt = f"""
        Create a comprehensive lesson on the topic: {topic}
        
        Learning Style: {learning_style}
        Difficulty Level: {difficulty}
        
        Please structure the lesson with:
        1. Introduction and learning objectives
        2. Main content (adapted to {learning_style} learning style)
        3. Key concepts and examples
        4. Practice exercises
        5. Summary and takeaways
        
        Make it engaging and appropriate for {difficulty} level students.
        """
        
        return self.generate_content(prompt, **kwargs)
    
    @cache_ai_response(timeout=7200)  # Cache for 2 hours
    def generate_quiz(self, topic, num_questions=5, difficulty='intermediate'):
        """Generate quiz questions with caching."""
        
        prompt = f"""
        Create {num_questions} multiple-choice questions about: {topic}
        
        Difficulty: {difficulty}
        
        Format each question as:
        Question: [question text]
        A) [option]
        B) [option]
        C) [option]
        D) [option]
        Correct Answer: [letter]
        Explanation: [brief explanation]
        
        Make questions challenging but fair for {difficulty} level.
        """
        
        return self.generate_content(prompt, max_tokens=2048)
    
    @cache_ai_response(timeout=3600)  # Cache for 1 hour
    def explain_concept(self, concept, learning_style, context=''):
        """Explain a concept based on learning style with caching."""
        
        style_instructions = {
            'visual': 'Use visual descriptions, diagrams, and imagery',
            'auditory': 'Use verbal explanations, analogies, and discussions',
            'reading_writing': 'Use detailed text, lists, and written examples',
            'kinesthetic': 'Use hands-on examples, real-world applications, and activities'
        }
        
        instruction = style_instructions.get(learning_style, 'Use clear explanations')
        
        prompt = f"""
        Explain the concept: {concept}
        
        Context: {context}
        
        Learning Style: {learning_style}
        Instructions: {instruction}
        
        Provide a clear, engaging explanation that helps the student understand.
        """
        
        return self.generate_content(prompt)


# Singleton instance
openai_service = OpenAIService()
