"""
User models for authentication and profile management.
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with role-based access."""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    
    LEARNING_STYLE_CHOICES = [
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('reading_writing', 'Reading/Writing'),
        ('kinesthetic', 'Kinesthetic'),
        ('unknown', 'Unknown'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # Profile fields
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Student-specific fields
    learning_style = models.CharField(
        max_length=20,
        choices=LEARNING_STYLE_CHOICES,
        default='unknown'
    )
    grade_level = models.CharField(max_length=50, blank=True)
    
    # Teacher-specific fields
    specialization = models.CharField(max_length=255, blank=True)
    years_of_experience = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)
    
    # Settings
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['learning_style']),
        ]
    
    def __str__(self):
        return f"{self.full_name or self.email} ({self.role})"
    
    def save(self, *args, **kwargs):
        # Auto-generate username from email if not provided
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_teacher(self):
        return self.role == 'teacher'
    
    @property
    def is_admin(self):
        return self.role == 'admin'


class LearningStyleAssessment(models.Model):
    """Store learning style assessment results."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments')
    
    # Assessment scores (0-100)
    visual_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    auditory_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    reading_writing_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    kinesthetic_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Determined learning style
    determined_style = models.CharField(max_length=20)
    
    # Metadata
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'learning_style_assessments'
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.determined_style}"


class UserPreferences(models.Model):
    """Store user preferences and settings."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Learning preferences
    preferred_difficulty = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='intermediate'
    )
    daily_learning_goal = models.IntegerField(default=30)  # minutes
    preferred_study_time = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('night', 'Night'),
        ],
        default='evening'
    )
    
    # AI Tutor preferences
    ai_response_style = models.CharField(
        max_length=20,
        choices=[
            ('concise', 'Concise'),
            ('detailed', 'Detailed'),
            ('conversational', 'Conversational'),
        ],
        default='conversational'
    )
    
    # UI preferences
    theme = models.CharField(
        max_length=10,
        choices=[('light', 'Light'), ('dark', 'Dark')],
        default='light'
    )
    language = models.CharField(max_length=10, default='en')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_preferences'
    
    def __str__(self):
        return f"Preferences for {self.user.email}"