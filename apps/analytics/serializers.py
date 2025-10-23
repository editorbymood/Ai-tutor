"""
Serializers for analytics models.
"""
from rest_framework import serializers
from .models import UserActivity, LearningAnalytics, CourseAnalytics


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for user activity tracking."""
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'activity_type', 'description',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LearningAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for learning analytics."""
    
    class Meta:
        model = LearningAnalytics
        fields = [
            'id', 'user', 'total_study_time', 'average_daily_time',
            'current_streak', 'longest_streak', 'courses_enrolled',
            'courses_completed', 'lessons_completed', 'quizzes_taken',
            'quizzes_passed', 'average_quiz_score', 'chat_messages_sent',
            'ai_content_generated', 'predicted_success_rate', 'at_risk',
            'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']


class CourseAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for course analytics."""
    
    class Meta:
        model = CourseAnalytics
        fields = [
            'id', 'course', 'total_enrollments', 'active_students',
            'completion_rate', 'average_progress', 'average_time_to_complete',
            'average_quiz_score', 'pass_rate', 'average_rating',
            'total_reviews', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']
