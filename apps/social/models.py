from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class StudyGroup(models.Model):
    """Collaborative study groups"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    max_members = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.count()


class StudyGroupMember(models.Model):
    """Members of study groups"""
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ], default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['group', 'user']

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class ForumPost(models.Model):
    """Discussion forum posts"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True)
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    @property
    def reply_count(self):
        return self.comments.count()


class Comment(models.Model):
    """Comments on posts and replies"""
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    @property
    def is_reply(self):
        return self.parent is not None

    @property
    def reply_count(self):
        return self.replies.count()


class PeerTutoring(models.Model):
    """Peer tutoring sessions"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutoring_sessions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_sessions')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='scheduled')
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.tutor.username} tutoring {self.student.username}"


class Message(models.Model):
    """Private messaging system"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"


class Announcement(models.Model):
    """Teacher announcements"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True)
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, null=True, blank=True)
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Like(models.Model):
    """Likes on posts and comments"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post', 'comment']

    def __str__(self):
        if self.post:
            return f"{self.user.username} liked post: {self.post.title}"
        elif self.comment:
            return f"{self.user.username} liked comment by {self.comment.author.username}"


class Bookmark(models.Model):
    """User bookmarks for posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"