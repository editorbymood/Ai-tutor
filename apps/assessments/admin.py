"""
Admin configuration for assessment models.
"""
from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt, QuestionResponse


class AnswerInline(admin.TabularInline):
    """Inline admin for answers."""
    model = Answer
    extra = 4


class QuestionInline(admin.StackedInline):
    """Inline admin for questions."""
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin interface for Quiz."""
    
    list_display = [
        'title', 'course', 'difficulty', 'passing_score',
        'is_published', 'is_ai_generated', 'created_at'
    ]
    list_filter = ['difficulty', 'is_published', 'is_ai_generated', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question."""
    
    list_display = ['quiz', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text']
    inlines = [AnswerInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Admin interface for Quiz Attempt."""
    
    list_display = [
        'student', 'quiz', 'attempt_number', 'status',
        'score', 'passed', 'started_at', 'completed_at'
    ]
    list_filter = ['status', 'passed', 'started_at']
    search_fields = ['student__email', 'quiz__title']
    readonly_fields = ['started_at', 'completed_at']