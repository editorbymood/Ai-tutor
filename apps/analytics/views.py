"""
Views for analytics and progress tracking.
"""
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from datetime import timedelta
from backend.utils import success_response
from .models import UserActivity, LearningAnalytics, CourseAnalytics
from apps.courses.models import Enrollment
from apps.assessments.models import QuizAttempt


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_student_dashboard(request):
    """Get comprehensive dashboard data for students."""
    
    user = request.user
    
    # Get or create learning analytics
    analytics, created = LearningAnalytics.objects.get_or_create(user=user)
    
    # Get enrollments
    enrollments = Enrollment.objects.filter(student=user)
    
    # Recent activity
    recent_activities = UserActivity.objects.filter(user=user)[:10]
    
    # Quiz performance
    recent_quizzes = QuizAttempt.objects.filter(
        student=user,
        status='completed'
    ).order_by('-completed_at')[:5]
    
    # Calculate weekly progress
    week_ago = timezone.now() - timedelta(days=7)
    weekly_activities = UserActivity.objects.filter(
        user=user,
        created_at__gte=week_ago
    ).values('activity_type').annotate(count=Count('id'))
    
    dashboard_data = {
        'user_info': {
            'name': user.full_name,
            'email': user.email,
            'learning_style': user.learning_style,
        },
        'analytics': {
            'total_study_time': analytics.total_study_time,
            'current_streak': analytics.current_streak,
            'courses_enrolled': analytics.courses_enrolled,
            'courses_completed': analytics.courses_completed,
            'average_quiz_score': analytics.average_quiz_score,
        },
        'enrollments': {
            'total': enrollments.count(),
            'active': enrollments.filter(status='active').count(),
            'completed': enrollments.filter(status='completed').count(),
        },
        'recent_quizzes': [
            {
                'quiz_title': attempt.quiz.title,
                'score': attempt.score,
                'passed': attempt.passed,
                'completed_at': attempt.completed_at,
            }
            for attempt in recent_quizzes
        ],
        'weekly_activity': list(weekly_activities),
    }
    
    return success_response(data=dashboard_data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_teacher_dashboard(request):
    """Get comprehensive dashboard data for teachers."""
    
    if not request.user.is_teacher:
        return success_response(
            data={'error': 'Only teachers can access this endpoint'},
            status_code=403
        )
    
    from apps.courses.models import Course
    
    # Get teacher's courses
    courses = Course.objects.filter(instructor=request.user)
    
    # Aggregate statistics
    total_students = Enrollment.objects.filter(
        course__in=courses
    ).values('student').distinct().count()
    
    total_enrollments = Enrollment.objects.filter(course__in=courses).count()
    
    # Course performance
    course_stats = []
    for course in courses:
        enrollments = Enrollment.objects.filter(course=course)
        analytics, _ = CourseAnalytics.objects.get_or_create(course=course)
        
        course_stats.append({
            'course_id': str(course.id),
            'title': course.title,
            'total_students': enrollments.count(),
            'active_students': enrollments.filter(status='active').count(),
            'average_progress': enrollments.aggregate(
                avg=Avg('progress_percentage')
            )['avg'] or 0,
            'average_rating': analytics.average_rating,
        })
    
    dashboard_data = {
        'summary': {
            'total_courses': courses.count(),
            'total_students': total_students,
            'total_enrollments': total_enrollments,
        },
        'courses': course_stats,
    }
    
    return success_response(data=dashboard_data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_course_analytics(request, course_id):
    """Get detailed analytics for a specific course."""
    
    from apps.courses.models import Course
    
    course = Course.objects.get(id=course_id)
    
    # Check permission
    if not (request.user.is_teacher and course.instructor == request.user):
        return success_response(
            data={'error': 'Permission denied'},
            status_code=403
        )
    
    analytics, _ = CourseAnalytics.objects.get_or_create(course=course)
    
    # Get detailed enrollment data
    enrollments = Enrollment.objects.filter(course=course)
    
    # Student progress distribution
    progress_distribution = {
        '0-25%': enrollments.filter(progress_percentage__lt=25).count(),
        '25-50%': enrollments.filter(
            progress_percentage__gte=25,
            progress_percentage__lt=50
        ).count(),
        '50-75%': enrollments.filter(
            progress_percentage__gte=50,
            progress_percentage__lt=75
        ).count(),
        '75-100%': enrollments.filter(progress_percentage__gte=75).count(),
    }
    
    # Quiz performance
    from apps.assessments.models import Quiz, QuizAttempt
    quizzes = Quiz.objects.filter(course=course)
    quiz_stats = []
    
    for quiz in quizzes:
        attempts = QuizAttempt.objects.filter(quiz=quiz, status='completed')
        quiz_stats.append({
            'quiz_title': quiz.title,
            'total_attempts': attempts.count(),
            'average_score': attempts.aggregate(avg=Avg('score'))['avg'] or 0,
            'pass_rate': (
                attempts.filter(passed=True).count() / attempts.count() * 100
                if attempts.count() > 0 else 0
            ),
        })
    
    analytics_data = {
        'course_info': {
            'title': course.title,
            'total_lessons': course.total_lessons,
        },
        'enrollment_stats': {
            'total': enrollments.count(),
            'active': enrollments.filter(status='active').count(),
            'completed': enrollments.filter(status='completed').count(),
            'completion_rate': analytics.completion_rate,
        },
        'progress_distribution': progress_distribution,
        'quiz_performance': quiz_stats,
        'ratings': {
            'average_rating': analytics.average_rating,
            'total_reviews': analytics.total_reviews,
        },
    }
    
    return success_response(data=analytics_data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def log_activity(request):
    """Log user activity."""
    
    activity_type = request.data.get('activity_type')
    description = request.data.get('description', '')
    metadata = request.data.get('metadata', {})
    
    activity = UserActivity.objects.create(
        user=request.user,
        activity_type=activity_type,
        description=description,
        metadata=metadata
    )
    
    return success_response(
        data={'activity_id': str(activity.id)},
        message="Activity logged"
    )