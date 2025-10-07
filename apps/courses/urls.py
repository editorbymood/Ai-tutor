"""
URL patterns for course management.
"""
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Courses
    path('', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('<uuid:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    
    # Enrollment
    path('<uuid:course_id>/enroll/', views.enroll_course, name='enroll'),
    path('my-enrollments/', views.my_enrollments, name='my-enrollments'),
    
    # Lesson Progress
    path('lessons/<uuid:lesson_id>/progress/', views.update_lesson_progress, name='lesson-progress'),
    
    # Reviews
    path('<uuid:course_id>/reviews/', views.CourseReviewListCreateView.as_view(), name='course-reviews'),
]