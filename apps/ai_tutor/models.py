"""
Models for AI tutor chat and content generation.
"""
from django.db import models
from apps.users.models import User
from apps.courses.models import Course, Lesson
import uuid


class ChatSession(models.Model):
    """Chat session between student and AI tutor."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_sessions'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_sessions'
    )
    
    # Session metadata
    title = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Chat: {self.user.email} - {self.title or 'Untitled'}"


class ChatMessage(models.Model):
    """Individual messages in a chat session."""
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    
    # AI metadata
    model_used = models.CharField(max_length=100, blank=True)
    tokens_used = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True, help_text="Response time in seconds")
    
    # Feedback
    is_helpful = models.BooleanField(null=True, blank=True)
    feedback_comment = models.TextField(blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class AIGeneratedContent(models.Model):
    """Track AI-generated educational content."""
    
    CONTENT_TYPE_CHOICES = [
        ('lesson', 'Lesson'),
        ('quiz', 'Quiz'),
        ('explanation', 'Explanation'),
        ('summary', 'Summary'),
        ('practice', 'Practice Exercise'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ai_generated_content'
    )
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    
    # Generation details
    prompt = models.TextField()
    generated_content = models.TextField()
    model_used = models.CharField(max_length=100)
    
    # Context
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Metadata
    learning_style = models.CharField(max_length=20, blank=True)
    difficulty_level = models.CharField(max_length=20, blank=True)
    
    # Quality metrics
    quality_score = models.FloatField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_generated_content'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.content_type} - {self.created_at}"


class StudyRecommendation(models.Model):
    """AI-generated study recommendations for students."""
    
    RECOMMENDATION_TYPE_CHOICES = [
        ('course', 'Course Recommendation'),
        ('lesson', 'Lesson Recommendation'),
        ('review', 'Review Topic'),
        ('practice', 'Practice Exercise'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='study_recommendations'
    )
    recommendation_type = models.CharField(
        max_length=20,
        choices=RECOMMENDATION_TYPE_CHOICES
    )
    
    # Recommendation details
    title = models.CharField(max_length=255)
    description = models.TextField()
    reason = models.TextField(help_text="Why this is recommended")
    
    # Related content
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # Priority and status
    priority = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'study_recommendations'
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"