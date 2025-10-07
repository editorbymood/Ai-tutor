"""
URL patterns for analytics.
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Dashboards
    path('dashboard/student/', views.get_student_dashboard, name='student-dashboard'),
    path('dashboard/teacher/', views.get_teacher_dashboard, name='teacher-dashboard'),
    
    # Course Analytics
    path('course/<uuid:course_id>/', views.get_course_analytics, name='course-analytics'),
    
    # Activity Logging
    path('activity/log/', views.log_activity, name='log-activity'),
]