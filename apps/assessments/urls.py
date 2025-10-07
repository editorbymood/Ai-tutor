"""
URL patterns for assessments.
"""
from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    # Quizzes
    path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<uuid:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    
    # Quiz Attempts
    path('quizzes/<uuid:quiz_id>/start/', views.start_quiz_attempt, name='start-attempt'),
    path('attempts/<uuid:attempt_id>/answer/', views.submit_answer, name='submit-answer'),
    path('attempts/<uuid:attempt_id>/complete/', views.complete_quiz_attempt, name='complete-attempt'),
    path('my-attempts/', views.my_quiz_attempts, name='my-attempts'),
]