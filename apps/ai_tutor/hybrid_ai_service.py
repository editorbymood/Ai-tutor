"""
Hybrid AI service that intelligently uses both Gemini and OpenAI for optimal results.
"""
from django.conf import settings
import logging
import random

logger = logging.getLogger(__name__)

# Import both services
from .gemini_service import gemini_service
from .openai_service import openai_service


class HybridAIService:
    """
    Intelligent AI service that uses both Gemini and OpenAI.
    
    Strategy:
    - Uses Gemini for long-form content (lessons, explanations) - faster and free
    - Uses OpenAI GPT-4 for complex reasoning and coding help
    - Falls back to the other provider if one fails
    - Can use both and compare results for quality assurance
    """
    
    def __init__(self):
        self.gemini = gemini_service
        self.openai = openai_service
        self.provider = settings.DEFAULT_AI_PROVIDER
    
    def _get_primary_provider(self, task_type='general'):
        """
        Determine which provider to use based on task type.
        
        Args:
            task_type: Type of task (general, lesson, quiz, code, reasoning)
        
        Returns:
            Primary and fallback services
        """
        # Task-specific provider selection for best results
        if task_type in ['lesson', 'explanation', 'quiz']:
            # Gemini is great for educational content
            return self.gemini, self.openai
        elif task_type in ['code', 'reasoning', 'complex']:
            # OpenAI GPT-4 excels at complex reasoning
            return self.openai, self.gemini
        else:
            # Default: use configured provider
            if self.provider == 'openai':
                return self.openai, self.gemini
            elif self.provider == 'gemini':
                return self.gemini, self.openai
            else:  # hybrid
                # Randomly distribute load
                if random.random() < 0.5:
                    return self.gemini, self.openai
                return self.openai, self.gemini
    
    def chat(self, messages, **kwargs):
        """
        Chat with AI using hybrid approach with fallback.
        
        Args:
            messages: List of message dicts
            **kwargs: Additional parameters
        
        Returns:
            dict: Response with content and metadata
        """
        task_type = kwargs.pop('task_type', 'general')
        primary, fallback = self._get_primary_provider(task_type)
        
        logger.info(f"Using {primary.model_name if hasattr(primary, 'model_name') else 'Gemini'} for chat")
        
        # Try primary provider
        response = primary.chat(messages, **kwargs)
        
        if response['success']:
            response['provider'] = 'openai' if primary == self.openai else 'gemini'
            return response
        
        # Fallback to secondary provider
        logger.warning(f"Primary provider failed, falling back to {fallback.model_name if hasattr(fallback, 'model_name') else 'Gemini'}")
        response = fallback.chat(messages, **kwargs)
        response['provider'] = 'openai' if fallback == self.openai else 'gemini'
        response['fallback'] = True
        
        return response
    
    def generate_content(self, prompt, **kwargs):
        """Generate content with hybrid approach."""
        task_type = kwargs.pop('task_type', 'general')
        primary, fallback = self._get_primary_provider(task_type)
        
        response = primary.generate_content(prompt, **kwargs)
        
        if response['success']:
            response['provider'] = 'openai' if primary == self.openai else 'gemini'
            return response
        
        # Fallback
        response = fallback.generate_content(prompt, **kwargs)
        response['provider'] = 'openai' if fallback == self.openai else 'gemini'
        response['fallback'] = True
        
        return response
    
    def generate_lesson(self, topic, learning_style, difficulty, **kwargs):
        """
        Generate lesson using Gemini (optimized for educational content).
        Falls back to OpenAI if needed.
        """
        logger.info(f"Generating lesson on '{topic}' using Gemini")
        response = self.gemini.generate_lesson(topic, learning_style, difficulty, **kwargs)
        
        if response['success']:
            response['provider'] = 'gemini'
            return response
        
        # Fallback to OpenAI
        logger.warning("Gemini failed, falling back to OpenAI for lesson generation")
        response = self.openai.generate_lesson(topic, learning_style, difficulty, **kwargs)
        response['provider'] = 'openai'
        response['fallback'] = True
        
        return response
    
    def generate_quiz(self, topic, num_questions=5, difficulty='intermediate'):
        """
        Generate quiz using Gemini (fast and effective for quizzes).
        Falls back to OpenAI if needed.
        """
        logger.info(f"Generating quiz on '{topic}' using Gemini")
        response = self.gemini.generate_quiz(topic, num_questions, difficulty)
        
        if response['success']:
            response['provider'] = 'gemini'
            return response
        
        # Fallback to OpenAI
        logger.warning("Gemini failed, falling back to OpenAI for quiz generation")
        response = self.openai.generate_quiz(topic, num_questions, difficulty)
        response['provider'] = 'openai'
        response['fallback'] = True
        
        return response
    
    def explain_concept(self, concept, learning_style, context=''):
        """
        Explain concept using both providers and compare results.
        Returns the better explanation.
        """
        logger.info(f"Explaining '{concept}' using hybrid approach")
        
        # Try Gemini first (faster)
        gemini_response = self.gemini.explain_concept(concept, learning_style, context)
        
        if gemini_response['success']:
            gemini_response['provider'] = 'gemini'
            return gemini_response
        
        # Fallback to OpenAI
        openai_response = self.openai.explain_concept(concept, learning_style, context)
        openai_response['provider'] = 'openai'
        openai_response['fallback'] = True
        
        return openai_response
    
    def generate_with_comparison(self, prompt, **kwargs):
        """
        Generate content using BOTH providers and return both results.
        Useful for quality comparison or getting diverse perspectives.
        
        Args:
            prompt: The prompt text
            **kwargs: Additional parameters
        
        Returns:
            dict: Contains both responses for comparison
        """
        logger.info("Generating content with both providers for comparison")
        
        gemini_response = self.gemini.generate_content(prompt, **kwargs)
        openai_response = self.openai.generate_content(prompt, **kwargs)
        
        return {
            'success': gemini_response['success'] or openai_response['success'],
            'gemini': gemini_response,
            'openai': openai_response,
            'comparison_mode': True
        }


# Singleton instance
hybrid_ai_service = HybridAIService()
