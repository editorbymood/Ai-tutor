"""
Google Gemini AI service for content generation and chat.
"""
import google.generativeai as genai
from django.conf import settings
from django.core.cache import cache
import time
import logging
import hashlib
import json
from functools import wraps

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


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
                'kwargs': kwargs
            }
            cache_string = json.dumps(cache_data, sort_keys=True, default=str)
            cache_hash = hashlib.md5(cache_string.encode()).hexdigest()
            cache_key = f"ai_response:{func.__name__}:{cache_hash}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"AI cache hit: {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            logger.info(f"AI cache miss: {func.__name__}")
            result = func(self, *args, **kwargs)
            
            # Only cache successful responses
            if result.get('success'):
                cache.set(cache_key, result, timeout)
            
            return result
        
        return wrapper
    return decorator


class GeminiService:
    """Service class for interacting with Google Gemini API with caching and retry logic."""
    
    def __init__(self, model_name='gemini-pro'):
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
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
        Generate content using Gemini with retry logic.
        
        Args:
            prompt: The prompt text
            **kwargs: Additional generation parameters
        
        Returns:
            dict: Response with content and metadata
        """
        try:
            start_time = time.time()
            
            def _generate():
                return self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=kwargs.get('temperature', 0.7),
                        top_p=kwargs.get('top_p', 0.95),
                        top_k=kwargs.get('top_k', 40),
                        max_output_tokens=kwargs.get('max_tokens', 2048),
                    )
                )
            
            response = self._retry_with_backoff(_generate)
            response_time = time.time() - start_time
            
            return {
                'success': True,
                'content': response.text,
                'model': self.model_name,
                'response_time': response_time,
                'prompt_tokens': response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else None,
                'completion_tokens': response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else None,
            }
        
        except Exception as e:
            logger.error(f"Gemini API error after {self.max_retries} attempts: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def chat(self, messages, **kwargs):
        """
        Have a conversation with Gemini.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters
        
        Returns:
            dict: Response with content and metadata
        """
        try:
            # Convert messages to Gemini format
            chat = self.model.start_chat(history=[])
            
            # Add previous messages to context
            for msg in messages[:-1]:
                if msg['role'] == 'user':
                    chat.send_message(msg['content'])
            
            # Send the latest message
            start_time = time.time()
            response = chat.send_message(messages[-1]['content'])
            response_time = time.time() - start_time
            
            return {
                'success': True,
                'content': response.text,
                'model': self.model_name,
                'response_time': response_time,
            }
        
        except Exception as e:
            logger.error(f"Gemini chat error: {str(e)}")
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
    
    def generate_study_plan(self, user_data, goals):
        """Generate personalized study plan."""
        
        prompt = f"""
        Create a personalized study plan for a student with:
        
        Learning Style: {user_data.get('learning_style')}
        Current Level: {user_data.get('level')}
        Available Time: {user_data.get('daily_time')} minutes per day
        Goals: {goals}
        
        Provide:
        1. Weekly schedule
        2. Recommended topics and order
        3. Study techniques suited to their learning style
        4. Milestones and checkpoints
        5. Tips for staying motivated
        """
        
        return self.generate_content(prompt, max_tokens=3000)
    
    def provide_feedback(self, student_answer, correct_answer, question):
        """Provide constructive feedback on student answers."""
        
        prompt = f"""
        Question: {question}
        Correct Answer: {correct_answer}
        Student's Answer: {student_answer}
        
        Provide constructive feedback that:
        1. Acknowledges what the student got right
        2. Gently corrects misconceptions
        3. Explains the correct answer
        4. Offers tips for improvement
        
        Be encouraging and supportive.
        """
        
        return self.generate_content(prompt, temperature=0.8)


# Singleton instance
gemini_service = GeminiService()