"""
Views for course management.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.utils import timezone
from backend.utils import success_response, error_response
from .models import Course, Lesson, Enrollment, LessonProgress, CourseReview
from .serializers import (
    CourseSerializer, CourseListSerializer, LessonSerializer,
    EnrollmentSerializer, LessonProgressSerializer, CourseReviewSerializer
)
from .permissions import IsTeacherOrReadOnly, IsEnrolledStudent


class CourseListCreateView(generics.ListCreateAPIView):
    """List all courses or create a new course."""
    
    permission_classes = [IsTeacherOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseListSerializer
        return CourseSerializer
    
    def get_queryset(self):
        queryset = Course.objects.filter(status='published')
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a course."""
    
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_teacher:
            return Course.objects.filter(instructor=self.request.user)
        return Course.objects.filter(status='published')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enroll_course(request, course_id):
    """Enroll in a course."""
    course = get_object_or_404(Course, id=course_id, status='published')
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        return error_response(
            message="Already enrolled in this course",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    enrollment = Enrollment.objects.create(
        student=request.user,
        course=course
    )
    
    return success_response(
        data=EnrollmentSerializer(enrollment).data,
        message="Successfully enrolled in course",
        status_code=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_enrollments(request):
    """Get current user's enrollments."""
    enrollments = Enrollment.objects.filter(student=request.user)
    serializer = EnrollmentSerializer(enrollments, many=True)
    return success_response(data=serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_lesson_progress(request, lesson_id):
    """Update progress for a lesson."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Get enrollment
    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course=lesson.course
    )
    
    # Get or create lesson progress
    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )
    
    # Update progress
    progress.time_spent = request.data.get('time_spent', progress.time_spent)
    progress.completion_percentage = request.data.get(
        'completion_percentage',
        progress.completion_percentage
    )
    progress.notes = request.data.get('notes', progress.notes)
    
    # Mark as completed if 100%
    if progress.completion_percentage >= 100 and not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        
        # Update enrollment completed lessons
        if str(lesson.id) not in enrollment.completed_lessons:
            enrollment.completed_lessons.append(str(lesson.id))
            enrollment.update_progress()
    
    progress.save()
    
    return success_response(
        data=LessonProgressSerializer(progress).data,
        message="Progress updated successfully"
    )


class CourseReviewListCreateView(generics.ListCreateAPIView):
    """List and create course reviews."""
    
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return CourseReview.objects.filter(course_id=course_id)
    
    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        
        # Check if student is enrolled
        if not Enrollment.objects.filter(
            student=self.request.user,
            course=course
        ).exists():
            raise serializers.ValidationError(
                "You must be enrolled to review this course"
            )
        
        serializer.save(student=self.request.user, course=course)