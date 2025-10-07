"""
Views for assessments and quizzes.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.utils import timezone
from backend.utils import success_response, error_response
from .models import Quiz, Question, QuizAttempt, QuestionResponse
from .serializers import (
    QuizSerializer, QuizListSerializer, QuizAttemptSerializer,
    QuestionResponseSerializer
)


class QuizListView(generics.ListAPIView):
    """List quizzes for a course."""
    
    serializer_class = QuizListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        queryset = Quiz.objects.filter(is_published=True)
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        return queryset


class QuizDetailView(generics.RetrieveAPIView):
    """Get quiz details."""
    
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Quiz.objects.filter(is_published=True)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_quiz_attempt(request, quiz_id):
    """Start a new quiz attempt."""
    
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    
    # Check attempt limit
    attempts_count = QuizAttempt.objects.filter(
        quiz=quiz,
        student=request.user
    ).count()
    
    if attempts_count >= quiz.max_attempts:
        return error_response(
            message=f"Maximum attempts ({quiz.max_attempts}) reached",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Create new attempt
    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        student=request.user,
        attempt_number=attempts_count + 1
    )
    
    return success_response(
        data=QuizAttemptSerializer(attempt).data,
        message="Quiz attempt started",
        status_code=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_answer(request, attempt_id):
    """Submit an answer for a question."""
    
    attempt = get_object_or_404(
        QuizAttempt,
        id=attempt_id,
        student=request.user,
        status='in_progress'
    )
    
    question_id = request.data.get('question_id')
    selected_answer_id = request.data.get('selected_answer_id')
    text_answer = request.data.get('text_answer', '')
    
    question = get_object_or_404(Question, id=question_id, quiz=attempt.quiz)
    
    # Create or update response
    response, created = QuestionResponse.objects.get_or_create(
        attempt=attempt,
        question=question
    )
    
    if selected_answer_id:
        from .models import Answer
        selected_answer = get_object_or_404(Answer, id=selected_answer_id)
        response.selected_answer = selected_answer
        response.is_correct = selected_answer.is_correct
        response.points_earned = question.points if selected_answer.is_correct else 0
    
    if text_answer:
        response.text_answer = text_answer
    
    response.save()
    
    return success_response(
        data=QuestionResponseSerializer(response).data,
        message="Answer submitted"
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_quiz_attempt(request, attempt_id):
    """Complete a quiz attempt and calculate score."""
    
    attempt = get_object_or_404(
        QuizAttempt,
        id=attempt_id,
        student=request.user,
        status='in_progress'
    )
    
    # Calculate score
    attempt.calculate_score()
    attempt.status = 'completed'
    attempt.completed_at = timezone.now()
    attempt.time_taken = (attempt.completed_at - attempt.started_at).seconds
    attempt.save()
    
    return success_response(
        data=QuizAttemptSerializer(attempt).data,
        message="Quiz completed"
    )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_quiz_attempts(request):
    """Get user's quiz attempts."""
    
    attempts = QuizAttempt.objects.filter(student=request.user)
    serializer = QuizAttemptSerializer(attempts, many=True)
    return success_response(data=serializer.data)