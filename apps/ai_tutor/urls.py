"""
URL patterns for AI tutor functionality.
"""
from django.urls import path
from . import views

app_name = 'ai_tutor'

urlpatterns = [
    # Chat Sessions
    path('chat/', views.ChatSessionListCreateView.as_view(), name='chat-list-create'),
    path('chat/<uuid:pk>/', views.ChatSessionDetailView.as_view(), name='chat-detail'),
    path('chat/<uuid:session_id>/message/', views.send_chat_message, name='send-message'),
    
    # Content Generation
    path('generate/lesson/', views.generate_lesson_content, name='generate-lesson'),
    path('generate/quiz/', views.generate_quiz, name='generate-quiz'),
    path('explain/', views.explain_concept, name='explain-concept'),
    
    # Recommendations
    path('recommendations/', views.StudyRecommendationListView.as_view(), name='recommendations'),
    path('recommendations/<uuid:recommendation_id>/complete/', views.mark_recommendation_completed, name='complete-recommendation'),
]