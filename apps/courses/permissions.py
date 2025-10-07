"""
Custom permissions for course management.
"""
from rest_framework import permissions


class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Allow teachers to create/edit, others can only read.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_teacher


class IsEnrolledStudent(permissions.BasePermission):
    """
    Check if user is enrolled in the course.
    """
    
    def has_object_permission(self, request, view, obj):
        from .models import Enrollment
        return Enrollment.objects.filter(
            student=request.user,
            course=obj.course if hasattr(obj, 'course') else obj
        ).exists()