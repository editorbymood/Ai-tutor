"""
Views for machine learning model predictions and training.
"""
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from backend.utils import success_response, error_response
from .learning_style_detector import learning_style_detector
from .performance_predictor import performance_predictor
from .sentiment_analyzer import sentiment_analyzer
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def predict_learning_style(request):
    """Predict user's learning style based on interaction data."""
    try:
        user_data = request.data
        
        # Extract required features
        if not all(key in user_data for key in ['video_time', 'text_time', 'interactive_time']):
            return error_response(
                message="Missing required interaction data",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Predict learning style
        predicted_style = learning_style_detector.predict(user_data)
        
        # Update user's learning style
        user = request.user
        user.learning_style = predicted_style
        user.save()
        
        return success_response(
            data={
                'predicted_style': predicted_style,
                'user_id': str(user.id)
            },
            message="Learning style predicted successfully"
        )
    
    except Exception as e:
        logger.error(f"Learning style prediction error: {str(e)}")
        return error_response(
            message="Failed to predict learning style",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def predict_performance(request):
    """Predict student performance and identify at-risk students."""
    try:
        student_data = request.data
        
        # Add user's current data
        user = request.user
        student_data['learning_style'] = user.learning_style
        
        # Predict performance
        prediction = performance_predictor.predict(student_data)
        
        return success_response(
            data=prediction,
            message="Performance predicted successfully"
        )
    
    except Exception as e:
        logger.error(f"Performance prediction error: {str(e)}")
        return error_response(
            message="Failed to predict performance",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def analyze_sentiment(request):
    """Analyze sentiment of text (review, feedback, etc.)."""
    try:
        text = request.data.get('text')
        
        if not text:
            return error_response(
                message="Text is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Analyze sentiment
        sentiment_result = sentiment_analyzer.analyze(text)
        
        return success_response(
            data=sentiment_result,
            message="Sentiment analyzed successfully"
        )
    
    except Exception as e:
        logger.error(f"Sentiment analysis error: {str(e)}")
        return error_response(
            message="Failed to analyze sentiment",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_model_info(request):
    """Get information about available ML models."""
    try:
        models_info = {
            'learning_style_detector': {
                'name': 'Learning Style Detector',
                'algorithm': 'K-means Clustering',
                'features': 10,
                'clusters': 4
            },
            'performance_predictor': {
                'name': 'Performance Predictor',
                'algorithm': 'Random Forest Classifier',
                'features': 10,
                'classes': 3
            },
            'sentiment_analyzer': {
                'name': 'Sentiment Analyzer',
                'algorithm': 'TextBlob NLP',
                'output': 'polarity and subjectivity scores'
            }
        }
        
        return success_response(
            data=models_info,
            message="Model information retrieved"
        )
    
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        return error_response(
            message="Failed to get model info",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
