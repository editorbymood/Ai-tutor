"""
Serializers for assessment models.
"""
from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizAttempt, QuestionResponse


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for answers."""
    
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct', 'order']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for questions."""
    
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'question_type', 'points',
            'order', 'explanation', 'answers'
        ]
        read_only_fields = ['id']


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for quizzes."""
    
    questions = QuestionSerializer(many=True, read_only=True)
    total_questions = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'course', 'lesson',
            'difficulty', 'time_limit', 'passing_score', 'max_attempts',
            'is_ai_generated', 'is_published', 'questions', 'total_questions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuizListSerializer(serializers.ModelSerializer):
    """Minimal serializer for quiz lists."""
    
    total_questions = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'difficulty',
            'time_limit', 'passing_score', 'total_questions', 'created_at'
        ]


class QuestionResponseSerializer(serializers.ModelSerializer):
    """Serializer for question responses."""
    
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = QuestionResponse
        fields = [
            'id', 'question', 'selected_answer', 'text_answer',
            'is_correct', 'points_earned', 'ai_feedback', 'answered_at'
        ]
        read_only_fields = ['id', 'is_correct', 'points_earned', 'ai_feedback', 'answered_at']


class QuizAttemptSerializer(serializers.ModelSerializer):
    """Serializer for quiz attempts."""
    
    quiz = QuizListSerializer(read_only=True)
    responses = QuestionResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'quiz', 'attempt_number', 'status', 'score',
            'total_points', 'earned_points', 'passed', 'responses',
            'started_at', 'completed_at', 'time_taken'
        ]
        read_only_fields = [
            'id', 'score', 'total_points', 'earned_points',
            'passed', 'started_at'
        ]