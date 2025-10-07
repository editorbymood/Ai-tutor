"""
Admin configuration for course models.
"""
from django.contrib import admin
from .models import Course, Lesson, Enrollment, LessonProgress, CourseReview


class LessonInline(admin.TabularInline):
    """Inline admin for lessons."""
    model = Lesson
    extra = 1
    fields = ['title', 'order', 'content_type', 'duration', 'is_ai_generated']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""
    
    list_display = [
        'title', 'instructor', 'difficulty', 'category',
        'status', 'total_students', 'created_at'
    ]
    list_filter = ['status', 'difficulty', 'category', 'created_at']
    search_fields = ['title', 'description', 'instructor__email']
    inlines = [LessonInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'instructor', 'thumbnail')
        }),
        ('Course Details', {
            'fields': (
                'difficulty', 'category', 'tags', 'estimated_duration',
                'prerequisites', 'learning_objectives'
            )
        }),
        ('Status', {
            'fields': ('status', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin interface for Lesson model."""
    
    list_display = [
        'title', 'course', 'order', 'content_type',
        'duration', 'is_ai_generated', 'created_at'
    ]
    list_filter = ['content_type', 'is_ai_generated', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin interface for Enrollment model."""
    
    list_display = [
        'student', 'course', 'status', 'progress_percentage',
        'enrolled_at', 'last_accessed'
    ]
    list_filter = ['status', 'enrolled_at']
    search_fields = ['student__email', 'course__title']
    readonly_fields = ['enrolled_at', 'last_accessed']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    """Admin interface for Lesson Progress."""
    
    list_display = [
        'enrollment', 'lesson', 'is_completed',
        'completion_percentage', 'time_spent', 'last_accessed'
    ]
    list_filter = ['is_completed', 'completed_at']
    search_fields = ['enrollment__student__email', 'lesson__title']
    readonly_fields = ['started_at', 'last_accessed']


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    """Admin interface for Course Review."""
    
    list_display = [
        'course', 'student', 'rating', 'sentiment_label',
        'created_at'
    ]
    list_filter = ['rating', 'sentiment_label', 'created_at']
    search_fields = ['course__title', 'student__email', 'comment']
    readonly_fields = ['sentiment_score', 'sentiment_label', 'created_at', 'updated_at']