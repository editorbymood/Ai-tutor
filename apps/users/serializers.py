"""
Serializers for user-related models.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, LearningStyleAssessment, UserPreferences


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'full_name',
            'role', 'phone_number', 'date_of_birth', 'grade_level',
            'specialization', 'years_of_experience'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'role', 'bio', 'avatar',
            'phone_number', 'date_of_birth', 'learning_style',
            'grade_level', 'specialization', 'years_of_experience',
            'created_at', 'last_active', 'email_notifications',
            'push_notifications'
        ]
        read_only_fields = ['id', 'email', 'role', 'created_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = [
            'full_name', 'bio', 'avatar', 'phone_number',
            'date_of_birth', 'grade_level', 'specialization',
            'years_of_experience', 'email_notifications',
            'push_notifications'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs


class LearningStyleAssessmentSerializer(serializers.ModelSerializer):
    """Serializer for learning style assessment."""
    
    class Meta:
        model = LearningStyleAssessment
        fields = [
            'id', 'visual_score', 'auditory_score',
            'reading_writing_score', 'kinesthetic_score',
            'determined_style', 'completed_at'
        ]
        read_only_fields = ['id', 'determined_style', 'completed_at']
    
    def create(self, validated_data):
        # Determine learning style based on highest score
        scores = {
            'visual': validated_data['visual_score'],
            'auditory': validated_data['auditory_score'],
            'reading_writing': validated_data['reading_writing_score'],
            'kinesthetic': validated_data['kinesthetic_score'],
        }
        determined_style = max(scores, key=scores.get)
        validated_data['determined_style'] = determined_style
        
        # Update user's learning style
        user = self.context['request'].user
        user.learning_style = determined_style
        user.save()
        
        validated_data['user'] = user
        return super().create(validated_data)


class UserPreferencesSerializer(serializers.ModelSerializer):
    """Serializer for user preferences."""
    
    class Meta:
        model = UserPreferences
        fields = [
            'id', 'preferred_difficulty', 'daily_learning_goal',
            'preferred_study_time', 'ai_response_style',
            'theme', 'language', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class UserListSerializer(serializers.ModelSerializer):
    """Minimal serializer for user lists."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'avatar', 'last_active']