"""
Views for user authentication and profile management.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from backend.utils import success_response, error_response
from .models import User, LearningStyleAssessment, UserPreferences
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    LearningStyleAssessmentSerializer,
    UserPreferencesSerializer,
    UserListSerializer
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """Register a new user."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # UserPreferences is automatically created by signal handler
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return success_response(
            data={
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            },
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED
        )
    return error_response(
        message="Registration failed",
        details=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    """Login user and return JWT tokens."""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return error_response(
            message="Email and password are required",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=email, password=password)
    
    if user is not None:
        if not user.is_active:
            return error_response(
                message="Account is disabled",
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return success_response(
            data={
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            },
            message="Login successful"
        )
    
    return error_response(
        message="Invalid credentials",
        status_code=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """Logout user by blacklisting refresh token."""
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return success_response(message="Logout successful")
    except Exception as e:
        return error_response(
            message="Logout failed",
            details=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_current_user(request):
    """Get current user profile."""
    serializer = UserProfileSerializer(request.user)
    return success_response(data=serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """Update user profile."""
    serializer = UserUpdateSerializer(
        request.user,
        data=request.data,
        partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return success_response(
            data=UserProfileSerializer(request.user).data,
            message="Profile updated successfully"
        )
    return error_response(
        message="Update failed",
        details=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Change user password."""
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return error_response(
                message="Old password is incorrect",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return success_response(message="Password changed successfully")
    
    return error_response(
        message="Password change failed",
        details=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


class LearningStyleAssessmentView(generics.CreateAPIView):
    """Create learning style assessment."""
    
    serializer_class = LearningStyleAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            assessment = serializer.save()
            return success_response(
                data=serializer.data,
                message="Assessment completed successfully",
                status_code=status.HTTP_201_CREATED
            )
        return error_response(
            message="Assessment failed",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class LearningStyleAssessmentListView(generics.ListAPIView):
    """List user's learning style assessments."""
    
    serializer_class = LearningStyleAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return LearningStyleAssessment.objects.filter(user=self.request.user)


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    """Get and update user preferences."""
    
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preferences, created = UserPreferences.objects.get_or_create(
            user=self.request.user
        )
        return preferences
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=serializer.data,
                message="Preferences updated successfully"
            )
        return error_response(
            message="Update failed",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class UserListView(generics.ListAPIView):
    """List all users (admin/teacher only)."""
    
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin can see all users
        if user.is_admin:
            return User.objects.all()
        
        # Teachers can see students
        if user.is_teacher:
            return User.objects.filter(role='student')
        
        # Students can only see themselves
        return User.objects.filter(id=user.id)