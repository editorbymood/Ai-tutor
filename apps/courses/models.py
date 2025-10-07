"""
Models for course and lesson management.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import User
import uuid


class Course(models.Model):
    """Course model."""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses_taught',
        limit_choices_to={'role': 'teacher'}
    )
    
    # Course details
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=100)
    tags = models.JSONField(default=list, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Metadata
    estimated_duration = models.IntegerField(help_text="Duration in hours")
    prerequisites = models.TextField(blank=True)
    learning_objectives = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Enrollment
    enrolled_students = models.ManyToManyField(
        User,
        through='Enrollment',
        related_name='enrolled_courses'
    )
    
    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'difficulty']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def total_lessons(self):
        return self.lessons.count()
    
    @property
    def total_students(self):
        return self.enrolled_students.count()


class Lesson(models.Model):
    """Lesson model."""
    
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('video', 'Video'),
        ('interactive', 'Interactive'),
        ('mixed', 'Mixed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Content
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content = models.TextField(help_text="Main lesson content")
    video_url = models.URLField(blank=True)
    attachments = models.JSONField(default=list, blank=True)
    
    # Order and duration
    order = models.IntegerField(default=0)
    duration = models.IntegerField(help_text="Duration in minutes")
    
    # AI-generated content flags
    is_ai_generated = models.BooleanField(default=False)
    ai_generation_prompt = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lessons'
        ordering = ['course', 'order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    """Student enrollment in courses."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Progress
    progress_percentage = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    completed_lessons = models.JSONField(default=list, blank=True)
    
    # Timestamps
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'enrollments'
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.student.email} - {self.course.title}"
    
    def update_progress(self):
        """Calculate and update progress percentage."""
        total_lessons = self.course.total_lessons
        if total_lessons > 0:
            self.progress_percentage = (len(self.completed_lessons) / total_lessons) * 100
            self.save()


class LessonProgress(models.Model):
    """Track student progress on individual lessons."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='lesson_progress'
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    
    # Progress tracking
    is_completed = models.BooleanField(default=False)
    time_spent = models.IntegerField(default=0, help_text="Time spent in seconds")
    completion_percentage = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    
    # Interaction data
    notes = models.TextField(blank=True)
    bookmarks = models.JSONField(default=list, blank=True)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lesson_progress'
        unique_together = ['enrollment', 'lesson']
        ordering = ['lesson__order']
    
    def __str__(self):
        return f"{self.enrollment.student.email} - {self.lesson.title}"


class CourseReview(models.Model):
    """Student reviews for courses."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_reviews')
    
    # Review content
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=255)
    comment = models.TextField()
    
    # Sentiment analysis (will be populated by ML model)
    sentiment_score = models.FloatField(null=True, blank=True)
    sentiment_label = models.CharField(max_length=20, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'course_reviews'
        unique_together = ['course', 'student']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.email} - {self.course.title} ({self.rating}★)"