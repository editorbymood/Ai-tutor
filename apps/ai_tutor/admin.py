"""
Admin configuration for AI tutor models.
"""
from django.contrib import admin
from .models import ChatSession, ChatMessage, AIGeneratedContent, StudyRecommendation


class ChatMessageInline(admin.TabularInline):
    """Inline admin for chat messages."""
    model = ChatMessage
    extra = 0
    readonly_fields = ['created_at']
    fields = ['role', 'content', 'is_helpful', 'created_at']


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    """Admin interface for Chat Session."""
    
    list_display = ['user', 'title', 'course', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__email', 'title']
    inlines = [ChatMessageInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Admin interface for Chat Message."""
    
    list_display = ['session', 'role', 'content_preview', 'is_helpful', 'created_at']
    list_filter = ['role', 'is_helpful', 'created_at']
    search_fields = ['content', 'session__user__email']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(AIGeneratedContent)
class AIGeneratedContentAdmin(admin.ModelAdmin):
    """Admin interface for AI Generated Content."""
    
    list_display = [
        'content_type', 'created_by', 'learning_style',
        'difficulty_level', 'is_approved', 'created_at'
    ]
    list_filter = ['content_type', 'learning_style', 'difficulty_level', 'is_approved']
    search_fields = ['prompt', 'generated_content', 'created_by__email']
    readonly_fields = ['created_at']


@admin.register(StudyRecommendation)
class StudyRecommendationAdmin(admin.ModelAdmin):
    """Admin interface for Study Recommendation."""
    
    list_display = [
        'user', 'recommendation_type', 'title', 'priority',
        'is_completed', 'is_dismissed', 'created_at'
    ]
    list_filter = ['recommendation_type', 'is_completed', 'is_dismissed', 'created_at']
    search_fields = ['user__email', 'title', 'description']
    readonly_fields = ['created_at']