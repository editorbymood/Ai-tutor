"""
Models for assessments, quizzes, and tests.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import User
from apps.courses.models import Course, Lesson
import uuid


class Quiz(models.Model):
    """Quiz model."""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Relations
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='quizzes'
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    
    # Quiz settings
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    time_limit = models.IntegerField(null=True, blank=True, help_text="Time limit in minutes")
    passing_score = models.IntegerField(
        default=70,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_attempts = models.IntegerField(default=3)
    
    # AI generation
    is_ai_generated = models.BooleanField(default=False)
    
    # Status
    is_published = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quizzes'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def total_questions(self):
        return self.questions.count()


class Question(models.Model):
    """Question model."""
    
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    
    # Question content
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    
    # Explanation
    explanation = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['quiz', 'order']
        unique_together = ['quiz', 'order']
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


class Answer(models.Model):
    """Answer options for questions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    
    # Answer content
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'answers'
        ordering = ['question', 'order']
    
    def __str__(self):
        return f"{self.question} - {self.answer_text[:30]}"


class QuizAttempt(models.Model):
    """Student's quiz attempt."""
    
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    
    # Attempt details
    attempt_number = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    
    # Scoring
    score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    total_points = models.IntegerField(default=0)
    earned_points = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.IntegerField(null=True, blank=True, help_text="Time taken in seconds")
    
    class Meta:
        db_table = 'quiz_attempts'
        ordering = ['-started_at']
        unique_together = ['quiz', 'student', 'attempt_number']
    
    def __str__(self):
        return f"{self.student.email} - {self.quiz.title} (Attempt {self.attempt_number})"
    
    def calculate_score(self):
        """Calculate the score for this attempt."""
        responses = self.responses.all()
        total_points = sum(r.question.points for r in responses)
        earned_points = sum(r.points_earned for r in responses)
        
        self.total_points = total_points
        self.earned_points = earned_points
        self.score = (earned_points / total_points * 100) if total_points > 0 else 0
        self.passed = self.score >= self.quiz.passing_score
        self.save()


class QuestionResponse(models.Model):
    """Student's response to a question."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # Response
    selected_answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    text_answer = models.TextField(blank=True)
    
    # Grading
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    
    # AI feedback
    ai_feedback = models.TextField(blank=True)
    
    # Timestamp
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'question_responses'
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt} - {self.question}"