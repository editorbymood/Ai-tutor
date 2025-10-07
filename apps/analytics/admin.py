"""
Admin configuration for analytics models.
"""
from django.contrib import admin
from .models import UserActivity, LearningAnalytics, CourseAnalytics


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin interface for User Activity."""
    
    list_display = ['user', 'activity_type', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__email', 'description']
    readonly_fields = ['created_at']


@admin.register(LearningAnalytics)
class LearningAnalyticsAdmin(admin.ModelAdmin):
    """Admin interface for Learning Analytics."""
    
    list_display = [
        'user', 'total_study_time', 'current_streak',
        'courses_enrolled', 'average_quiz_score', 'at_risk'
    ]
    list_filter = ['at_risk', 'last_updated']
    search_fields = ['user__email']
    readonly_fields = ['last_updated']


@admin.register(CourseAnalytics)
class CourseAnalyticsAdmin(admin.ModelAdmin):
    """Admin interface for Course Analytics."""
    
    list_display = [
        'course', 'total_enrollments', 'completion_rate',
        'average_quiz_score', 'average_rating'
    ]
    list_filter = ['last_updated']
    search_fields = ['course__title']
    readonly_fields = ['last_updated']