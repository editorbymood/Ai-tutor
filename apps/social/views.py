from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from .models import (
    StudyGroup, StudyGroupMember, ForumPost, Comment, PeerTutoring,
    Message, Announcement, Like, Bookmark
)
from .serializers import (
    StudyGroupSerializer, StudyGroupMemberSerializer, ForumPostSerializer,
    CommentSerializer, PeerTutoringSerializer, MessageSerializer,
    AnnouncementSerializer, LikeSerializer, BookmarkSerializer
)


class StudyGroupViewSet(viewsets.ModelViewSet):
    serializer_class = StudyGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StudyGroup.objects.all()
        course_id = self.request.query_params.get('course', None)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a study group"""
        group = self.get_object()

        if group.members.count() >= group.max_members:
            return Response(
                {'error': 'Group is full'},
                status=status.HTTP_400_BAD_REQUEST
            )

        member, created = StudyGroupMember.objects.get_or_create(
            group=group,
            user=request.user,
            defaults={'role': 'member'}
        )

        if not created:
            return Response(
                {'error': 'Already a member of this group'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'message': 'Successfully joined the group'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a study group"""
        group = self.get_object()

        try:
            membership = StudyGroupMember.objects.get(group=group, user=request.user)
            membership.delete()
            return Response({'message': 'Successfully left the group'})
        except StudyGroupMember.DoesNotExist:
            return Response(
                {'error': 'Not a member of this group'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get group members"""
        group = self.get_object()
        members = group.members.all()
        serializer = StudyGroupMemberSerializer(members, many=True)
        return Response(serializer.data)


class ForumPostViewSet(viewsets.ModelViewSet):
    serializer_class = ForumPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ForumPost.objects.all()
        course_id = self.request.query_params.get('course', None)
        group_id = self.request.query_params.get('group', None)

        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if group_id:
            queryset = queryset.filter(study_group_id=group_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like or unlike a post"""
        post = self.get_object()

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'comment': None}
        )

        if not created:
            like.delete()
            return Response({'message': 'Post unliked'})
        else:
            return Response({'message': 'Post liked'})

    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        """Bookmark or unbookmark a post"""
        post = self.get_object()

        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            bookmark.delete()
            return Response({'message': 'Post unbookmarked'})
        else:
            return Response({'message': 'Post bookmarked'})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like or unlike a comment"""
        comment = self.get_object()

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=None,
            comment=comment
        )

        if not created:
            like.delete()
            return Response({'message': 'Comment unliked'})
        else:
            return Response({'message': 'Comment liked'})


class PeerTutoringViewSet(viewsets.ModelViewSet):
    serializer_class = PeerTutoringSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PeerTutoring.objects.filter(
            Q(tutor=user) | Q(student=user)
        )

    def perform_create(self, serializer):
        serializer.save(tutor=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a tutoring request"""
        session = self.get_object()

        if session.student != request.user:
            return Response(
                {'error': 'Only the student can accept this session'},
                status=status.HTTP_403_FORBIDDEN
            )

        if session.status != 'scheduled':
            return Response(
                {'error': 'Session is not in scheduled status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session.status = 'scheduled'  # Keep as scheduled, or change to confirmed
        session.save()
        return Response({'message': 'Session accepted'})

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a tutoring session"""
        session = self.get_object()

        if session.tutor != request.user and session.student != request.user:
            return Response(
                {'error': 'Only participants can start this session'},
                status=status.HTTP_403_FORBIDDEN
            )

        if session.status != 'scheduled':
            return Response(
                {'error': 'Session cannot be started'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session.status = 'in_progress'
        session.save()
        return Response({'message': 'Session started'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a tutoring session"""
        session = self.get_object()

        if session.tutor != request.user:
            return Response(
                {'error': 'Only the tutor can complete this session'},
                status=status.HTTP_403_FORBIDDEN
            )

        if session.status != 'in_progress':
            return Response(
                {'error': 'Session is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session.status = 'completed'
        session.save()
        return Response({'message': 'Session completed'})


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()

        if message.recipient != request.user:
            return Response(
                {'error': 'You can only mark your own messages as read'},
                status=status.HTTP_403_FORBIDDEN
            )

        message.is_read = True
        message.read_at = timezone.now()
        message.save()
        return Response({'message': 'Message marked as read'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread messages"""
        count = Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        return Response({'unread_count': count})


class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Announcement.objects.all()
        course_id = self.request.query_params.get('course', None)
        group_id = self.request.query_params.get('group', None)

        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if group_id:
            queryset = queryset.filter(study_group_id=group_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BookmarkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)