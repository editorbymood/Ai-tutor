"""
Serializers for course-related models.
"""
from rest_framework import serializers
from .models import Course, Lesson, Enrollment, LessonProgress, CourseReview
from apps.users.serializers import UserListSerializer


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for lessons."""
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'content_type', 'content',
            'video_url', 'attachments', 'order', 'duration',
            'is_ai_generated', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for courses."""
    
    instructor = UserListSerializer(read_only=True)
    total_lessons = serializers.IntegerField(read_only=True)
    total_students = serializers.IntegerField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor', 'difficulty',
            'category', 'tags', 'thumbnail', 'status', 'estimated_duration',
            'prerequisites', 'learning_objectives', 'total_lessons',
            'total_students', 'lessons', 'created_at', 'updated_at',
            'published_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseListSerializer(serializers.ModelSerializer):
    """Minimal serializer for course lists."""
    
    instructor = UserListSerializer(read_only=True)
    total_lessons = serializers.IntegerField(read_only=True)
    total_students = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor', 'difficulty',
            'category', 'thumbnail', 'status', 'estimated_duration',
            'total_lessons', 'total_students', 'created_at'
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for enrollments."""
    
    course = CourseListSerializer(read_only=True)
    student = UserListSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'status', 'progress_percentage',
            'completed_lessons', 'enrolled_at', 'completed_at', 'last_accessed'
        ]
        read_only_fields = ['id', 'enrolled_at', 'last_accessed']


class LessonProgressSerializer(serializers.ModelSerializer):
    """Serializer for lesson progress."""
    
    lesson = LessonSerializer(read_only=True)
    
    class Meta:
        model = LessonProgress
        fields = [
            'id', 'lesson', 'is_completed', 'time_spent',
            'completion_percentage', 'notes', 'bookmarks',
            'started_at', 'completed_at', 'last_accessed'
        ]
        read_only_fields = ['id', 'started_at', 'last_accessed']


class CourseReviewSerializer(serializers.ModelSerializer):
    """Serializer for course reviews."""
    
    student = UserListSerializer(read_only=True)
    
    class Meta:
        model = CourseReview
        fields = [
            'id', 'student', 'rating', 'title', 'comment',
            'sentiment_score', 'sentiment_label', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'sentiment_score', 'sentiment_label',
            'created_at', 'updated_at'
        ]