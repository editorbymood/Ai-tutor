"""
Admin configuration for user models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LearningStyleAssessment, UserPreferences


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    
    list_display = [
        'email', 'full_name', 'role', 'learning_style',
        'is_active', 'created_at', 'last_active'
    ]
    list_filter = ['role', 'learning_style', 'is_active', 'created_at']
    search_fields = ['email', 'full_name', 'username']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': (
                'full_name', 'bio', 'avatar', 'phone_number',
                'date_of_birth'
            )
        }),
        ('Role & Learning', {
            'fields': (
                'role', 'learning_style', 'grade_level',
                'specialization', 'years_of_experience'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Settings', {
            'fields': ('email_notifications', 'push_notifications')
        }),
        ('Important dates', {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'role', 'password1', 'password2'
            ),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']


@admin.register(LearningStyleAssessment)
class LearningStyleAssessmentAdmin(admin.ModelAdmin):
    """Admin interface for Learning Style Assessment."""
    
    list_display = [
        'user', 'determined_style', 'visual_score',
        'auditory_score', 'reading_writing_score',
        'kinesthetic_score', 'completed_at'
    ]
    list_filter = ['determined_style', 'completed_at']
    search_fields = ['user__email', 'user__full_name']
    readonly_fields = ['completed_at']
    ordering = ['-completed_at']


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    """Admin interface for User Preferences."""
    
    list_display = [
        'user', 'preferred_difficulty', 'daily_learning_goal',
        'ai_response_style', 'theme', 'updated_at'
    ]
    list_filter = ['preferred_difficulty', 'theme', 'ai_response_style']
    search_fields = ['user__email', 'user__full_name']
    readonly_fields = ['created_at', 'updated_at']