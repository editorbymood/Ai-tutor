"""
Serializers for AI tutor models.
"""
from rest_framework import serializers
from .models import ChatSession, ChatMessage, AIGeneratedContent, StudyRecommendation


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages."""
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'role', 'content', 'model_used', 'tokens_used',
            'response_time', 'is_helpful', 'feedback_comment', 'created_at'
        ]
        read_only_fields = [
            'id', 'model_used', 'tokens_used', 'response_time', 'created_at'
        ]


class ChatSessionSerializer(serializers.ModelSerializer):
    """Serializer for chat sessions."""
    
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = [
            'id', 'title', 'course', 'lesson', 'is_active',
            'messages', 'message_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()


class AIGeneratedContentSerializer(serializers.ModelSerializer):
    """Serializer for AI-generated content."""
    
    class Meta:
        model = AIGeneratedContent
        fields = [
            'id', 'content_type', 'prompt', 'generated_content',
            'model_used', 'course', 'lesson', 'learning_style',
            'difficulty_level', 'quality_score', 'is_approved', 'created_at'
        ]
        read_only_fields = ['id', 'model_used', 'created_at']


class StudyRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for study recommendations."""
    
    class Meta:
        model = StudyRecommendation
        fields = [
            'id', 'recommendation_type', 'title', 'description',
            'reason', 'course', 'lesson', 'priority', 'is_completed',
            'is_dismissed', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at']