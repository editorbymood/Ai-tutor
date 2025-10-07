"""
Tests for course management.
"""
import pytest
from rest_framework import status
from apps.courses.models import Course, Enrollment


@pytest.mark.django_db
class TestCourseList:
    """Test course listing."""
    
    def test_list_courses(self, authenticated_client, course):
        """Test listing all courses."""
        response = authenticated_client.get('/api/courses/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_list_courses_pagination(self, authenticated_client, bulk_courses):
        """Test course listing with pagination."""
        response = authenticated_client.get('/api/courses/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'count' in response.data
        assert 'next' in response.data
    
    def test_search_courses(self, authenticated_client, course):
        """Test searching courses."""
        response = authenticated_client.get('/api/courses/?search=Test')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_filter_courses_by_difficulty(self, authenticated_client, course):
        """Test filtering courses by difficulty."""
        response = authenticated_client.get('/api/courses/?difficulty=intermediate')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCourseDetail:
    """Test course detail operations."""
    
    def test_get_course_detail(self, authenticated_client, course):
        """Test getting course details."""
        response = authenticated_client.get(f'/api/courses/{course.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Course'
    
    def test_get_nonexistent_course(self, authenticated_client):
        """Test getting nonexistent course."""
        response = authenticated_client.get('/api/courses/999999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCourseCreation:
    """Test course creation."""
    
    def test_teacher_create_course(self, teacher_client, teacher_user):
        """Test teacher creating a course."""
        data = {
            'title': 'New Course',
            'description': 'New course description',
            'difficulty': 'beginner',
            'category': 'programming',
            'is_published': True
        }
        response = teacher_client.post('/api/courses/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.filter(title='New Course').exists()
    
    def test_student_cannot_create_course(self, authenticated_client):
        """Test student cannot create a course."""
        data = {
            'title': 'New Course',
            'description': 'New course description',
            'difficulty': 'beginner',
            'category': 'programming'
        }
        response = authenticated_client.post('/api/courses/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCourseEnrollment:
    """Test course enrollment."""
    
    def test_enroll_in_course(self, authenticated_client, student_user, course):
        """Test enrolling in a course."""
        response = authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        assert response.status_code == status.HTTP_200_OK
        assert Enrollment.objects.filter(student=student_user, course=course).exists()
    
    def test_duplicate_enrollment(self, authenticated_client, student_user, course):
        """Test duplicate enrollment prevention."""
        # First enrollment
        authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        # Second enrollment attempt
        response = authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_unenroll_from_course(self, authenticated_client, student_user, course):
        """Test unenrolling from a course."""
        # Enroll first
        Enrollment.objects.create(student=student_user, course=course)
        # Unenroll
        response = authenticated_client.post(f'/api/courses/{course.id}/unenroll/')
        assert response.status_code == status.HTTP_200_OK
        assert not Enrollment.objects.filter(student=student_user, course=course).exists()


@pytest.mark.django_db
class TestLessonProgress:
    """Test lesson progress tracking."""
    
    def test_mark_lesson_complete(self, authenticated_client, student_user, course, lesson):
        """Test marking a lesson as complete."""
        # Enroll in course first
        Enrollment.objects.create(student=student_user, course=course)
        
        response = authenticated_client.post(
            f'/api/courses/{course.id}/lessons/{lesson.id}/complete/'
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_lesson_progress(self, authenticated_client, student_user, course, lesson):
        """Test getting lesson progress."""
        # Enroll in course first
        Enrollment.objects.create(student=student_user, course=course)
        
        response = authenticated_client.get(
            f'/api/courses/{course.id}/lessons/{lesson.id}/progress/'
        )
        assert response.status_code == status.HTTP_200_OK