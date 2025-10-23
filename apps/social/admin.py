"""
Admin configuration for social app.
"""
from django.contrib import admin
from .models import StudyGroup, StudyGroupMember, ForumPost, Comment, PeerTutoring, Message, Announcement


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    """Admin for StudyGroup model."""
    list_display = ['name', 'creator', 'is_private', 'created_at']
    list_filter = ['is_private', 'created_at']
    search_fields = ['name', 'description', 'creator__email']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['creator', 'course']


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    """Admin for ForumPost model."""
    list_display = ['title', 'author', 'course', 'is_pinned', 'created_at']
    list_filter = ['is_pinned', 'created_at', 'course']
    search_fields = ['title', 'content', 'author__email']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['author', 'course']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin for Comment model."""
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__email']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['author', 'post']


@admin.register(PeerTutoring)
class PeerTutoringAdmin(admin.ModelAdmin):
    """Admin for PeerTutoring model."""
    list_display = ['tutor', 'student', 'title', 'status', 'scheduled_at']
    list_filter = ['status', 'scheduled_at']
    search_fields = ['tutor__email', 'student__email', 'title']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['tutor', 'student', 'course']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin for Message model."""
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__email', 'recipient__email', 'subject', 'content']
    readonly_fields = ['created_at', 'read_at']
    raw_id_fields = ['sender', 'recipient']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """Admin for Announcement model."""
    list_display = ['title', 'course', 'author', 'is_important', 'created_at']
    list_filter = ['is_important', 'created_at']
    search_fields = ['title', 'content', 'author__email']
    readonly_fields = ['created_at']
    raw_id_fields = ['author', 'course', 'study_group']
