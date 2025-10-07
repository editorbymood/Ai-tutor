"""
Models for analytics and progress tracking.
"""
from django.db import models
from apps.users.models import User
from apps.courses.models import Course
import uuid


class UserActivity(models.Model):
    """Track user activity for analytics."""
    
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('course_view', 'Course View'),
        ('lesson_view', 'Lesson View'),
        ('quiz_attempt', 'Quiz Attempt'),
        ('chat_message', 'Chat Message'),
        ('content_generation', 'Content Generation'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPE_CHOICES)
    
    # Activity details
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.activity_type}"


class LearningAnalytics(models.Model):
    """Aggregated learning analytics for students."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learning_analytics')
    
    # Time metrics
    total_study_time = models.IntegerField(default=0, help_text="Total study time in minutes")
    average_daily_time = models.FloatField(default=0.0)
    current_streak = models.IntegerField(default=0, help_text="Current daily streak")
    longest_streak = models.IntegerField(default=0)
    
    # Course metrics
    courses_enrolled = models.IntegerField(default=0)
    courses_completed = models.IntegerField(default=0)
    lessons_completed = models.IntegerField(default=0)
    
    # Assessment metrics
    quizzes_taken = models.IntegerField(default=0)
    quizzes_passed = models.IntegerField(default=0)
    average_quiz_score = models.FloatField(default=0.0)
    
    # Engagement metrics
    chat_messages_sent = models.IntegerField(default=0)
    ai_content_generated = models.IntegerField(default=0)
    
    # Performance prediction (from ML model)
    predicted_success_rate = models.FloatField(null=True, blank=True)
    at_risk = models.BooleanField(default=False)
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'learning_analytics'
    
    def __str__(self):
        return f"Analytics for {self.user.email}"


class CourseAnalytics(models.Model):
    """Analytics for courses (for teachers)."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='analytics')
    
    # Enrollment metrics
    total_enrollments = models.IntegerField(default=0)
    active_students = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0.0)
    
    # Engagement metrics
    average_progress = models.FloatField(default=0.0)
    average_time_to_complete = models.FloatField(default=0.0, help_text="In days")
    
    # Performance metrics
    average_quiz_score = models.FloatField(default=0.0)
    pass_rate = models.FloatField(default=0.0)
    
    # Feedback metrics
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'course_analytics'
    
    def __str__(self):
        return f"Analytics for {self.course.title}"