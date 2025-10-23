"""
Serializers for ML model predictions and results.
"""
from rest_framework import serializers


class LearningStylePredictionSerializer(serializers.Serializer):
    """Serializer for learning style prediction input."""
    
    video_time = serializers.FloatField(min_value=0)
    text_time = serializers.FloatField(min_value=0)
    interactive_time = serializers.FloatField(min_value=0)
    quiz_attempts = serializers.IntegerField(min_value=0, default=0)
    chat_interactions = serializers.IntegerField(min_value=0, default=0)
    visual_content_views = serializers.IntegerField(min_value=0, default=0)
    audio_content_views = serializers.IntegerField(min_value=0, default=0)
    text_content_views = serializers.IntegerField(min_value=0, default=0)
    practice_exercises_completed = serializers.IntegerField(min_value=0, default=0)
    avg_session_duration = serializers.FloatField(min_value=0, default=0)


class PerformancePredictionSerializer(serializers.Serializer):
    """Serializer for performance prediction input."""
    
    average_quiz_score = serializers.FloatField(min_value=0, max_value=100)
    total_study_time = serializers.FloatField(min_value=0)
    current_streak = serializers.IntegerField(min_value=0, default=0)
    courses_enrolled = serializers.IntegerField(min_value=0, default=0)
    lessons_completed = serializers.IntegerField(min_value=0, default=0)
    quizzes_taken = serializers.IntegerField(min_value=0, default=0)
    chat_messages_sent = serializers.IntegerField(min_value=0, default=0)
    average_session_duration = serializers.FloatField(min_value=0, default=0)
    days_since_enrollment = serializers.IntegerField(min_value=0, default=0)


class SentimentAnalysisSerializer(serializers.Serializer):
    """Serializer for sentiment analysis input."""
    
    text = serializers.CharField(max_length=5000, required=True)


class PredictionResultSerializer(serializers.Serializer):
    """Serializer for prediction results."""
    
    prediction = serializers.CharField()
    confidence = serializers.FloatField()
    probabilities = serializers.DictField(required=False)
