"""
Views for AI tutor functionality.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from backend.utils import success_response, error_response
from .models import ChatSession, ChatMessage, AIGeneratedContent, StudyRecommendation
from .serializers import (
    ChatSessionSerializer, ChatMessageSerializer,
    AIGeneratedContentSerializer, StudyRecommendationSerializer
)
from .hybrid_ai_service import hybrid_ai_service
from .tasks import generate_content_async
import logging

logger = logging.getLogger(__name__)


class ChatSessionListCreateView(generics.ListCreateAPIView):
    """List and create chat sessions."""
    
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="Chat sessions retrieved successfully"
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(
            data=serializer.data,
            message="Chat session created successfully",
            status_code=status.HTTP_201_CREATED
        )


class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a chat session."""
    
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_chat_message(request, session_id):
    """Send a message in a chat session and get AI response."""
    
    session = get_object_or_404(
        ChatSession,
        id=session_id,
        user=request.user
    )
    
    user_message = request.data.get('message')
    if not user_message:
        return error_response(
            message="Message is required",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Save user message
    user_msg = ChatMessage.objects.create(
        session=session,
        role='user',
        content=user_message
    )
    
    # Get conversation history
    messages = list(session.messages.values('role', 'content'))
    
    # Get user's learning style for context
    learning_style = request.user.learning_style
    
    # Add system context
    system_context = f"""You are an AI tutor helping a student with {learning_style} learning style. 
    Be encouraging, clear, and adapt your explanations to their learning style."""
    
    messages.insert(0, {'role': 'system', 'content': system_context})
    
    # Get AI response using hybrid service
    response = hybrid_ai_service.chat(messages, task_type='chat')
    
    if response['success']:
        # Save AI response
        ai_msg = ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=response['content'],
            model_used=response['model'],
            response_time=response['response_time']
        )
        
        return success_response(
            data={
                'user_message': ChatMessageSerializer(user_msg).data,
                'ai_response': ChatMessageSerializer(ai_msg).data
            },
            message="Message sent successfully"
        )
    else:
        return error_response(
            message="Failed to get AI response",
            details=response.get('error'),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_lesson_content(request):
    """Generate lesson content using AI."""
    
    topic = request.data.get('topic')
    difficulty = request.data.get('difficulty', 'intermediate')
    learning_style = request.user.learning_style
    
    if not topic:
        return error_response(
            message="Topic is required",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Generate content using hybrid service
    response = hybrid_ai_service.generate_lesson(
        topic=topic,
        learning_style=learning_style,
        difficulty=difficulty
    )
    
    if response['success']:
        # Save generated content
        content = AIGeneratedContent.objects.create(
            created_by=request.user,
            content_type='lesson',
            prompt=f"Topic: {topic}, Style: {learning_style}, Difficulty: {difficulty}",
            generated_content=response['content'],
            model_used=response['model'],
            learning_style=learning_style,
            difficulty_level=difficulty
        )
        
        return success_response(
            data=AIGeneratedContentSerializer(content).data,
            message="Lesson generated successfully"
        )
    else:
        return error_response(
            message="Failed to generate lesson",
            details=response.get('error'),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_quiz(request):
    """Generate quiz questions using AI."""
    
    topic = request.data.get('topic')
    num_questions = request.data.get('num_questions', 5)
    difficulty = request.data.get('difficulty', 'intermediate')
    
    if not topic:
        return error_response(
            message="Topic is required",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    response = hybrid_ai_service.generate_quiz(
        topic=topic,
        num_questions=num_questions,
        difficulty=difficulty
    )
    
    if response['success']:
        content = AIGeneratedContent.objects.create(
            created_by=request.user,
            content_type='quiz',
            prompt=f"Topic: {topic}, Questions: {num_questions}, Difficulty: {difficulty}",
            generated_content=response['content'],
            model_used=response['model'],
            difficulty_level=difficulty
        )
        
        return success_response(
            data=AIGeneratedContentSerializer(content).data,
            message="Quiz generated successfully"
        )
    else:
        return error_response(
            message="Failed to generate quiz",
            details=response.get('error'),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def explain_concept(request):
    """Get AI explanation of a concept."""
    
    concept = request.data.get('concept')
    context = request.data.get('context', '')
    
    if not concept:
        return error_response(
            message="Concept is required",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    response = hybrid_ai_service.explain_concept(
        concept=concept,
        learning_style=request.user.learning_style,
        context=context
    )
    
    if response['success']:
        return success_response(
            data={'explanation': response['content']},
            message="Explanation generated successfully"
        )
    else:
        return error_response(
            message="Failed to generate explanation",
            details=response.get('error'),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class StudyRecommendationListView(generics.ListAPIView):
    """List study recommendations for the user."""
    
    serializer_class = StudyRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return StudyRecommendation.objects.filter(
            user=self.request.user,
            is_completed=False,
            is_dismissed=False
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_recommendation_completed(request, recommendation_id):
    """Mark a recommendation as completed."""
    
    recommendation = get_object_or_404(
        StudyRecommendation,
        id=recommendation_id,
        user=request.user
    )
    
    recommendation.is_completed = True
    recommendation.save()
    
    return success_response(
        data=StudyRecommendationSerializer(recommendation).data,
        message="Recommendation marked as completed"
    )