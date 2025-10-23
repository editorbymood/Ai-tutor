"""
URL patterns for ML model endpoints.
"""
from django.urls import path
from . import views

app_name = 'ml_models'

urlpatterns = [
    path('predict/learning-style/', views.predict_learning_style, name='predict-learning-style'),
    path('predict/performance/', views.predict_performance, name='predict-performance'),
    path('analyze/sentiment/', views.analyze_sentiment, name='analyze-sentiment'),
    path('info/', views.get_model_info, name='model-info'),
]
