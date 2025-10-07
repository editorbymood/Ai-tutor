"""
Celery tasks for async AI operations.
"""
from celery import shared_task
from .gemini_service import gemini_service
import logging

logger = logging.getLogger(__name__)


@shared_task
def generate_content_async(prompt, **kwargs):
    """Generate content asynchronously."""
    try:
        response = gemini_service.generate_content(prompt, **kwargs)
        return response
    except Exception as e:
        logger.error(f"Async content generation failed: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task
def generate_study_recommendations(user_id):
    """Generate personalized study recommendations for a user."""
    from apps.users.models import User
    from apps.courses.models import Enrollment
    from .models import StudyRecommendation
    
    try:
        user = User.objects.get(id=user_id)
        enrollments = Enrollment.objects.filter(student=user, status='active')
        
        # Analyze user's progress and generate recommendations
        # This is a placeholder - implement actual recommendation logic
        
        logger.info(f"Generated recommendations for user {user.email}")
        return {'success': True}
    except Exception as e:
        logger.error(f"Failed to generate recommendations: {str(e)}")
        return {'success': False, 'error': str(e)}