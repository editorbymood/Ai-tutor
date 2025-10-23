"""
Comprehensive integration tests for all functionalities.
This file tests the complete user journey and all API endpoints.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from apps.courses.models import Course, Lesson, Enrollment
from apps.assessments.models import Quiz, Question, Answer, QuizAttempt
from apps.ai_tutor.models import ChatSession, ChatMessage
from apps.analytics.models import LearningAnalytics, UserActivity

User = get_user_model()


@pytest.mark.django_db
class TestCompleteUserJourney:
    """Test the complete student learning journey."""
    
    def test_student_registration_and_login(self, api_client):
        """Test student can register and login."""
        # Registration
        register_data = {
            'email': 'newstudent@test.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'full_name': 'New Student',
            'role': 'student'
        }
        response = api_client.post('/api/auth/register/', register_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'tokens' in response.data['data']
        assert 'user' in response.data['data']
        
        # Login
        login_data = {
            'email': 'newstudent@test.com',
            'password': 'SecurePass123!'
        }
        response = api_client.post('/api/auth/login/', login_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'tokens' in response.data['data']
    
    def test_teacher_registration_and_login(self, api_client):
        """Test teacher can register and login."""
        register_data = {
            'email': 'newteacher@test.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'full_name': 'New Teacher',
            'role': 'teacher',
            'specialization': 'Mathematics'
        }
        response = api_client.post('/api/auth/register/', register_data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_learning_style_assessment(self, authenticated_client):
        """Test student can complete learning style assessment."""
        assessment_data = {
            'visual_score': 85,
            'auditory_score': 60,
            'reading_writing_score': 70,
            'kinesthetic_score': 55
        }
        response = authenticated_client.post('/api/auth/assessment/', assessment_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['determined_style'] == 'visual'
    
    def test_profile_update(self, authenticated_client, student_user):
        """Test user can update their profile."""
        update_data = {
            'full_name': 'Updated Name',
            'bio': 'Test bio',
            'grade_level': '10th Grade'
        }
        response = authenticated_client.put('/api/auth/profile/update/', update_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['full_name'] == 'Updated Name'
    
    def test_password_change(self, authenticated_client):
        """Test user can change password."""
        password_data = {
            'old_password': 'testpass123',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        response = authenticated_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCourseManagement:
    """Test course creation, enrollment, and management."""
    
    def test_teacher_create_course(self, teacher_client):
        """Test teacher can create a course."""
        course_data = {
            'title': 'Python Programming',
            'description': 'Learn Python from scratch',
            'difficulty': 'beginner',
            'category': 'programming',
            'estimated_duration': 40,
            'status': 'published'
        }
        response = teacher_client.post('/api/courses/', course_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Python Programming'
    
    def test_list_published_courses(self, authenticated_client, course):
        """Test student can list published courses."""
        response = authenticated_client.get('/api/courses/')
        assert response.status_code == status.HTTP_200_OK
        # Response is paginated: {count, next, previous, results}
        assert 'results' in response.data
        assert len(response.data['results']) >= 1
    
    def test_filter_courses_by_category(self, authenticated_client, course):
        """Test filtering courses by category."""
        response = authenticated_client.get('/api/courses/?category=programming')
        assert response.status_code == status.HTTP_200_OK
    
    def test_filter_courses_by_difficulty(self, authenticated_client, course):
        """Test filtering courses by difficulty."""
        response = authenticated_client.get('/api/courses/?difficulty=intermediate')
        assert response.status_code == status.HTTP_200_OK
    
    def test_search_courses(self, authenticated_client, course):
        """Test searching courses by title."""
        response = authenticated_client.get('/api/courses/?search=Test')
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_course_details(self, authenticated_client, course):
        """Test getting detailed course information."""
        response = authenticated_client.get(f'/api/courses/{course.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == course.title
    
    def test_student_enroll_in_course(self, authenticated_client, course):
        """Test student can enroll in a course."""
        response = authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify enrollment created
        enrollment = Enrollment.objects.filter(
            student=authenticated_client.handler._force_user,
            course=course
        ).first()
        assert enrollment is not None
    
    def test_duplicate_enrollment_prevented(self, authenticated_client, course):
        """Test student cannot enroll twice in same course."""
        # First enrollment
        authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        
        # Second enrollment should fail
        response = authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_my_enrollments(self, authenticated_client, course):
        """Test student can view their enrollments."""
        # Enroll first
        authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        
        # Get enrollments
        response = authenticated_client.get('/api/courses/my-enrollments/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']) >= 1
    
    def test_update_lesson_progress(self, authenticated_client, course, lesson):
        """Test student can update lesson progress."""
        # Enroll in course first
        authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        
        # Update lesson progress
        progress_data = {
            'time_spent': 600,
            'completion_percentage': 100,
            'notes': 'Completed lesson'
        }
        response = authenticated_client.post(
            f'/api/courses/lessons/{lesson.id}/progress/',
            progress_data
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['is_completed'] == True
    
    def test_course_review(self, authenticated_client, course):
        """Test student can review a course."""
        # Enroll first
        authenticated_client.post(f'/api/courses/{course.id}/enroll/')
        
        # Submit review
        review_data = {
            'rating': 5,
            'title': 'Excellent Course',
            'comment': 'Very informative and well structured'
        }
        response = authenticated_client.post(
            f'/api/courses/{course.id}/reviews/',
            review_data
        )
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_teacher_update_course(self, teacher_client, teacher_user):
        """Test teacher can update their own course."""
        # Create course
        course = Course.objects.create(
            title='Test Course',
            description='Test',
            instructor=teacher_user,
            difficulty='beginner',
            category='test',
            estimated_duration=30,
            status='published'
        )
        
        # Update course
        update_data = {
            'title': 'Updated Course Title',
            'description': 'Updated description'
        }
        response = teacher_client.patch(f'/api/courses/{course.id}/', update_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Course Title'


@pytest.mark.django_db
class TestAssessments:
    """Test quiz and assessment functionality."""
    
    def setup_quiz_with_questions(self, course, teacher_user):
        """Helper to create a quiz with questions."""
        quiz = Quiz.objects.create(
            title='Python Basics Quiz',
            description='Test your Python knowledge',
            course=course,
            created_by=teacher_user,
            difficulty='beginner',
            passing_score=70,
            max_attempts=3,
            is_published=True
        )
        
        # Create questions
        q1 = Question.objects.create(
            quiz=quiz,
            question_text='What is Python?',
            question_type='multiple_choice',
            points=10,
            order=1
        )
        
        # Create answers
        Answer.objects.create(
            question=q1,
            answer_text='A programming language',
            is_correct=True,
            order=1
        )
        Answer.objects.create(
            question=q1,
            answer_text='A snake',
            is_correct=False,
            order=2
        )
        
        return quiz, q1
    
    def test_list_quizzes(self, authenticated_client, course, teacher_user):
        """Test listing quizzes for a course."""
        quiz, _ = self.setup_quiz_with_questions(course, teacher_user)
        
        response = authenticated_client.get(f'/api/assessments/quizzes/?course={course.id}')
        assert response.status_code == status.HTTP_200_OK
        # Response might be paginated or direct list
        if 'results' in response.data:
            assert len(response.data['results']) >= 1
        elif 'data' in response.data:
            assert len(response.data['data']) >= 1
        else:
            assert len(response.data) >= 1
    
    def test_get_quiz_details(self, authenticated_client, course, teacher_user):
        """Test getting quiz details."""
        quiz, _ = self.setup_quiz_with_questions(course, teacher_user)
        
        response = authenticated_client.get(f'/api/assessments/quizzes/{quiz.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Python Basics Quiz'
    
    def test_start_quiz_attempt(self, authenticated_client, course, teacher_user):
        """Test student can start a quiz attempt."""
        quiz, _ = self.setup_quiz_with_questions(course, teacher_user)
        
        response = authenticated_client.post(f'/api/assessments/quizzes/{quiz.id}/start/')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['attempt_number'] == 1
    
    def test_submit_answer(self, authenticated_client, course, teacher_user):
        """Test student can submit an answer."""
        quiz, question = self.setup_quiz_with_questions(course, teacher_user)
        
        # Start attempt
        attempt_response = authenticated_client.post(f'/api/assessments/quizzes/{quiz.id}/start/')
        attempt_id = attempt_response.data['data']['id']
        
        # Get correct answer
        correct_answer = Answer.objects.filter(question=question, is_correct=True).first()
        
        # Submit answer
        answer_data = {
            'question_id': str(question.id),
            'selected_answer_id': str(correct_answer.id)
        }
        response = authenticated_client.post(
            f'/api/assessments/attempts/{attempt_id}/answer/',
            answer_data
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['is_correct'] == True
    
    def test_complete_quiz(self, authenticated_client, course, teacher_user):
        """Test completing a quiz and getting score."""
        quiz, question = self.setup_quiz_with_questions(course, teacher_user)
        
        # Start attempt
        attempt_response = authenticated_client.post(f'/api/assessments/quizzes/{quiz.id}/start/')
        attempt_id = attempt_response.data['data']['id']
        
        # Submit answer
        correct_answer = Answer.objects.filter(question=question, is_correct=True).first()
        authenticated_client.post(
            f'/api/assessments/attempts/{attempt_id}/answer/',
            {
                'question_id': str(question.id),
                'selected_answer_id': str(correct_answer.id)
            }
        )
        
        # Complete quiz
        response = authenticated_client.post(f'/api/assessments/attempts/{attempt_id}/complete/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['status'] == 'completed'
        assert response.data['data']['score'] > 0
    
    def test_max_attempts_limit(self, authenticated_client, course, teacher_user):
        """Test quiz max attempts limit is enforced."""
        quiz, _ = self.setup_quiz_with_questions(course, teacher_user)
        quiz.max_attempts = 2
        quiz.save()
        
        # Start and complete first attempt
        attempt1 = authenticated_client.post(f'/api/assessments/quizzes/{quiz.id}/start/')
        authenticated_client.post(f'/api/assessments/attempts/{attempt1.data["data"]["id"]}/complete/')
        
        # Start and complete second attempt
        attempt2 = authenticated_client.post(f'/api/assessments/quizzes/{quiz.id}/start/')
        authenticated_client.post(f'/api/assessments/attempts/{attempt2.data["data"]["id"]}/complete/')
        
        # Third attempt should fail
        response = authenticated_client.post(f'/api/assessments/quizzes/{quiz.id}/start/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_my_quiz_attempts(self, authenticated_client, course, teacher_user):
        """Test getting user's quiz attempts."""
        quiz, _ = self.setup_quiz_with_questions(course, teacher_user)
        
        # Start attempt
        authenticated_client.post(f'/api/assessments/quizzes/{quiz.id}/start/')
        
        # Get attempts
        response = authenticated_client.get('/api/assessments/my-attempts/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']) >= 1


@pytest.mark.django_db
class TestAITutor:
    """Test AI tutor functionality."""
    
    def test_create_chat_session(self, authenticated_client):
        """Test creating a chat session."""
        session_data = {
            'title': 'Help with Python'
        }
        response = authenticated_client.post('/api/ai-tutor/chat/', session_data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_list_chat_sessions(self, authenticated_client, chat_session):
        """Test listing user's chat sessions."""
        response = authenticated_client.get('/api/ai-tutor/chat/')
        assert response.status_code == status.HTTP_200_OK
        # Response might be paginated or direct list
        if 'results' in response.data:
            assert len(response.data['results']) >= 1
        elif 'data' in response.data:
            assert len(response.data['data']) >= 1
        else:
            assert len(response.data) >= 1
    
    def test_get_chat_session_details(self, authenticated_client, chat_session):
        """Test getting chat session details."""
        response = authenticated_client.get(f'/api/ai-tutor/chat/{chat_session.id}/')
        assert response.status_code == status.HTTP_200_OK
    
    @pytest.mark.skip(reason="Requires Gemini API key")
    def test_send_chat_message(self, authenticated_client, chat_session):
        """Test sending a message in chat session."""
        message_data = {
            'message': 'Explain Python functions'
        }
        response = authenticated_client.post(
            f'/api/ai-tutor/chat/{chat_session.id}/message/',
            message_data
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'user_message' in response.data['data']
        assert 'ai_response' in response.data['data']
    
    @pytest.mark.skip(reason="Requires Gemini API key")
    def test_generate_lesson(self, authenticated_client):
        """Test AI lesson generation."""
        lesson_data = {
            'topic': 'Python Lists',
            'difficulty': 'beginner'
        }
        response = authenticated_client.post('/api/ai-tutor/generate/lesson/', lesson_data)
        assert response.status_code == status.HTTP_200_OK
    
    @pytest.mark.skip(reason="Requires Gemini API key")
    def test_generate_quiz(self, authenticated_client):
        """Test AI quiz generation."""
        quiz_data = {
            'topic': 'Python Basics',
            'num_questions': 5,
            'difficulty': 'intermediate'
        }
        response = authenticated_client.post('/api/ai-tutor/generate/quiz/', quiz_data)
        assert response.status_code == status.HTTP_200_OK
    
    @pytest.mark.skip(reason="Requires Gemini API key")
    def test_explain_concept(self, authenticated_client):
        """Test AI concept explanation."""
        concept_data = {
            'concept': 'Object-Oriented Programming',
            'context': 'Python programming'
        }
        response = authenticated_client.post('/api/ai-tutor/explain/', concept_data)
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_study_recommendations(self, authenticated_client):
        """Test getting study recommendations."""
        response = authenticated_client.get('/api/ai-tutor/recommendations/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAnalytics:
    """Test analytics and dashboard functionality."""
    
    def test_student_dashboard(self, authenticated_client):
        """Test student dashboard data."""
        response = authenticated_client.get('/api/analytics/dashboard/student/')
        assert response.status_code == status.HTTP_200_OK
        assert 'user_info' in response.data['data']
        assert 'analytics' in response.data['data']
    
    def test_teacher_dashboard(self, teacher_client):
        """Test teacher dashboard data."""
        response = teacher_client.get('/api/analytics/dashboard/teacher/')
        assert response.status_code == status.HTTP_200_OK
        assert 'summary' in response.data['data']
    
    def test_teacher_dashboard_student_access_denied(self, authenticated_client):
        """Test student cannot access teacher dashboard."""
        response = authenticated_client.get('/api/analytics/dashboard/teacher/')
        assert response.status_code == status.HTTP_403_FORBIDDEN or response.data['data'].get('error')
    
    def test_course_analytics(self, teacher_client, course, teacher_user):
        """Test course analytics for teacher."""
        # Update course instructor
        course.instructor = teacher_user
        course.save()
        
        response = teacher_client.get(f'/api/analytics/course/{course.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert 'course_info' in response.data['data']
        assert 'enrollment_stats' in response.data['data']
    
    def test_log_activity(self, authenticated_client):
        """Test logging user activity."""
        import json
        activity_data = {
            'activity_type': 'course_view',
            'description': 'Viewed Python course',
            'metadata': json.dumps({'course_id': 'test-uuid'})
        }
        response = authenticated_client.post('/api/analytics/activity/log/', activity_data, format='json')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPermissions:
    """Test role-based permissions."""
    
    def test_student_cannot_create_course(self, authenticated_client):
        """Test student cannot create courses."""
        course_data = {
            'title': 'Unauthorized Course',
            'description': 'Should fail',
            'difficulty': 'beginner',
            'category': 'test'
        }
        response = authenticated_client.post('/api/courses/', course_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_student_cannot_update_others_course(self, authenticated_client, course):
        """Test student cannot update courses."""
        update_data = {'title': 'Hacked Title'}
        response = authenticated_client.patch(f'/api/courses/{course.id}/', update_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_teacher_can_only_update_own_course(self, teacher_client, course, teacher_user):
        """Test teacher can only update their own courses."""
        # Create another teacher's course
        other_teacher = User.objects.create_user(
            email='other@test.com',
            password='test123',
            role='teacher'
        )
        other_course = Course.objects.create(
            title='Other Course',
            description='Test',
            instructor=other_teacher,
            difficulty='beginner',
            category='test',
            estimated_duration=30,
            status='published'
        )
        
        # Try to update other teacher's course
        response = teacher_client.patch(
            f'/api/courses/{other_course.id}/',
            {'title': 'Hacked'}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND or \
               response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_unauthenticated_access_denied(self, api_client, course):
        """Test unauthenticated users cannot access protected endpoints."""
        # Courses list requires authentication (or returns empty with 200 for public access)
        # Try a clearly protected endpoint instead
        response = api_client.get('/api/courses/my-enrollments/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDataValidation:
    """Test data validation and error handling."""
    
    def test_registration_with_invalid_email(self, api_client):
        """Test registration with invalid email format."""
        data = {
            'email': 'invalid-email',
            'password': 'Test123!',
            'password_confirm': 'Test123!',
            'full_name': 'Test User',
            'role': 'student'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_registration_password_mismatch(self, api_client):
        """Test registration with mismatched passwords."""
        data = {
            'email': 'test@test.com',
            'password': 'Test123!',
            'password_confirm': 'Different123!',
            'full_name': 'Test User',
            'role': 'student'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_duplicate_email_registration(self, api_client, student_user):
        """Test cannot register with existing email."""
        data = {
            'email': student_user.email,
            'password': 'Test123!',
            'password_confirm': 'Test123!',
            'full_name': 'Test User',
            'role': 'student'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_invalid_login_credentials(self, api_client):
        """Test login with invalid credentials."""
        data = {
            'email': 'nonexistent@test.com',
            'password': 'WrongPass123'
        }
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_course_creation_missing_fields(self, teacher_client):
        """Test course creation with missing required fields."""
        data = {
            'title': 'Incomplete Course'
            # Missing description, difficulty, category, etc.
        }
        response = teacher_client.post('/api/courses/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_enroll_in_nonexistent_course(self, authenticated_client):
        """Test enrolling in non-existent course."""
        import uuid
        fake_id = uuid.uuid4()
        response = authenticated_client.post(f'/api/courses/{fake_id}/enroll/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_progress_without_enrollment(self, authenticated_client, lesson):
        """Test updating lesson progress without enrollment."""
        progress_data = {
            'time_spent': 100,
            'completion_percentage': 50
        }
        response = authenticated_client.post(
            f'/api/courses/lessons/{lesson.id}/progress/',
            progress_data
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_learning_style_assessment_invalid_scores(self, authenticated_client):
        """Test assessment with invalid score ranges."""
        data = {
            'visual_score': 150,  # Invalid: > 100
            'auditory_score': -10,  # Invalid: < 0
            'reading_writing_score': 70,
            'kinesthetic_score': 60
        }
        response = authenticated_client.post('/api/auth/assessment/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_quiz_with_zero_passing_score(self, teacher_user, course):
        """Test creating quiz with edge case passing scores."""
        quiz = Quiz.objects.create(
            title='Easy Quiz',
            description='Test',
            course=course,
            created_by=teacher_user,
            difficulty='beginner',
            passing_score=0,
            is_published=True
        )
        assert quiz.passing_score == 0
    
    def test_empty_chat_message(self, authenticated_client, chat_session):
        """Test sending empty chat message."""
        response = authenticated_client.post(
            f'/api/ai-tutor/chat/{chat_session.id}/message/',
            {'message': ''}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestConcurrency:
    """Test concurrent operations."""
    
    def test_simultaneous_enrollments(self, student_user, course):
        """Test handling simultaneous enrollment requests."""
        from apps.courses.models import Enrollment
        
        # Try to create duplicate enrollments
        enrollment1, created1 = Enrollment.objects.get_or_create(
            student=student_user,
            course=course
        )
        enrollment2, created2 = Enrollment.objects.get_or_create(
            student=student_user,
            course=course
        )
        
        # Only one should be created
        assert created1 == True
        assert created2 == False
        assert enrollment1.id == enrollment2.id
    
    def test_concurrent_quiz_attempts(self, authenticated_client, course, teacher_user):
        """Test concurrent quiz attempt creation."""
        quiz = Quiz.objects.create(
            title='Concurrent Test',
            description='Test',
            course=course,
            created_by=teacher_user,
            difficulty='beginner',
            is_published=True
        )
        
        # Start multiple attempts
        response1 = authenticated_client.post(f'/api/assessments/quizzes/{quiz.id}/start/')
        response2 = authenticated_client.post(f'/api/assessments/quizzes/{quiz.id}/start/')
        
        # Both should succeed but with different attempt numbers
        assert response1.status_code == status.HTTP_201_CREATED
        assert response2.status_code == status.HTTP_201_CREATED
        assert response1.data['data']['attempt_number'] != response2.data['data']['attempt_number']


@pytest.mark.django_db
class TestCleanup:
    """Test cleanup and deletion operations."""
    
    def test_user_deletion_cascades(self, student_user, course):
        """Test deleting user cascades to related objects."""
        # Create enrollment
        Enrollment.objects.create(student=student_user, course=course)
        
        # Create chat session
        ChatSession.objects.create(user=student_user)
        
        user_id = student_user.id
        student_user.delete()
        
        # Verify cascading deletion
        assert Enrollment.objects.filter(student_id=user_id).count() == 0
        assert ChatSession.objects.filter(user_id=user_id).count() == 0
    
    def test_course_deletion_cascades(self, course):
        """Test deleting course cascades to lessons and quizzes."""
        # Create lessons
        Lesson.objects.create(
            course=course,
            title='Test Lesson',
            content='Test',
            order=1,
            duration=30
        )
        
        course_id = course.id
        course.delete()
        
        # Verify cascading deletion
        assert Lesson.objects.filter(course_id=course_id).count() == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
