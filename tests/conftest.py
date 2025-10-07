"""
Pytest configuration and fixtures for testing.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.courses.models import Course, Lesson
from apps.assessments.models import Quiz, Question
from apps.ai_tutor.models import ChatSession
import random

User = get_user_model()


@pytest.fixture
def api_client():
    """Return API client for testing."""
    return APIClient()


@pytest.fixture
def student_user(db):
    """Create a student user."""
    return User.objects.create_user(
        email='student@test.com',
        password='testpass123',
        first_name='Test',
        last_name='Student',
        role='student'
    )


@pytest.fixture
def teacher_user(db):
    """Create a teacher user."""
    return User.objects.create_user(
        email='teacher@test.com',
        password='testpass123',
        first_name='Test',
        last_name='Teacher',
        role='teacher'
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        email='admin@test.com',
        password='testpass123',
        first_name='Test',
        last_name='Admin'
    )


@pytest.fixture
def authenticated_client(api_client, student_user):
    """Return authenticated API client."""
    api_client.force_authenticate(user=student_user)
    return api_client


@pytest.fixture
def teacher_client(api_client, teacher_user):
    """Return authenticated teacher API client."""
    api_client.force_authenticate(user=teacher_user)
    return api_client


@pytest.fixture
def course(teacher_user):
    """Create a test course."""
    return Course.objects.create(
        title='Test Course',
        description='Test course description',
        instructor=teacher_user,
        difficulty='intermediate',
        category='programming',
        is_published=True
    )


@pytest.fixture
def lesson(course):
    """Create a test lesson."""
    return Lesson.objects.create(
        course=course,
        title='Test Lesson',
        content='Test lesson content',
        order=1,
        duration=30
    )


@pytest.fixture
def quiz(course):
    """Create a test quiz."""
    return Quiz.objects.create(
        course=course,
        title='Test Quiz',
        description='Test quiz description',
        passing_score=70,
        time_limit=30
    )


@pytest.fixture
def question(quiz):
    """Create a test question."""
    return Question.objects.create(
        quiz=quiz,
        question_text='What is 2+2?',
        question_type='multiple_choice',
        options=['2', '3', '4', '5'],
        correct_answer='4',
        points=10
    )


@pytest.fixture
def chat_session(student_user):
    """Create a test chat session."""
    return ChatSession.objects.create(
        user=student_user,
        title='Test Chat Session'
    )


@pytest.fixture
def bulk_users(db):
    """Create multiple users for load testing."""
    users = []
    for i in range(100):
        user = User.objects.create_user(
            email=f'user{i}@test.com',
            password='testpass123',
            first_name=f'User{i}',
            last_name='Test',
            role=random.choice(['student', 'teacher'])
        )
        users.append(user)
    return users


@pytest.fixture
def bulk_courses(teacher_user):
    """Create multiple courses for load testing."""
    courses = []
    for i in range(50):
        course = Course.objects.create(
            title=f'Course {i}',
            description=f'Description for course {i}',
            instructor=teacher_user,
            difficulty=random.choice(['beginner', 'intermediate', 'advanced']),
            category=random.choice(['programming', 'math', 'science']),
            is_published=True
        )
        courses.append(course)
    return courses