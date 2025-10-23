from rest_framework import serializers
from .models import (
    StudyGroup, StudyGroupMember, ForumPost, Comment, PeerTutoring,
    Message, Announcement, Like, Bookmark
)


class StudyGroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = StudyGroupMember
        fields = ['id', 'user', 'user_id', 'role', 'joined_at']


class StudyGroupSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    course_name = serializers.CharField(source='course.name', read_only=True)
    member_count = serializers.ReadOnlyField()
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'description', 'creator', 'course', 'course_name',
                 'is_private', 'max_members', 'member_count', 'is_member',
                 'created_at', 'updated_at']

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(user=request.user).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'parent', 'replies', 'like_count',
                 'is_liked_by_user', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class ForumPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    course_name = serializers.CharField(source='course.name', read_only=True)
    study_group_name = serializers.CharField(source='study_group.name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    reply_count = serializers.ReadOnlyField()
    like_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()
    is_bookmarked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'content', 'author', 'course', 'course_name',
                 'study_group', 'study_group_name', 'is_pinned', 'is_locked',
                 'comments', 'reply_count', 'like_count', 'is_liked_by_user',
                 'is_bookmarked_by_user', 'created_at', 'updated_at']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_bookmarked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False


class PeerTutoringSerializer(serializers.ModelSerializer):
    tutor = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = PeerTutoring
        fields = ['id', 'title', 'description', 'tutor', 'student', 'course',
                 'course_name', 'scheduled_at', 'duration_minutes', 'status',
                 'meeting_link', 'notes', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'subject', 'content', 'is_read',
                 'read_at', 'created_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    course_name = serializers.CharField(source='course.name', read_only=True)
    study_group_name = serializers.CharField(source='study_group.name', read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'author', 'course', 'course_name',
                 'study_group', 'study_group_name', 'is_important', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'comment', 'created_at']


class BookmarkSerializer(serializers.ModelSerializer):
    post = ForumPostSerializer()

    class Meta:
        model = Bookmark
        fields = ['id', 'post', 'created_at']