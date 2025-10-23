from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Badge(models.Model):
    """Achievement badges that users can earn"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=[
        ('achievement', 'Achievement'),
        ('streak', 'Streak'),
        ('social', 'Social'),
        ('learning', 'Learning'),
        ('completion', 'Completion'),
    ])
    criteria_type = models.CharField(max_length=50, choices=[
        ('quiz_score', 'Quiz Score Threshold'),
        ('streak_days', 'Streak Days'),
        ('courses_completed', 'Courses Completed'),
        ('total_points', 'Total Points Earned'),
        ('social_interactions', 'Social Interactions'),
        ('time_spent', 'Time Spent Learning'),
    ])
    criteria_value = models.IntegerField()
    points_reward = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """Badges earned by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class PointTransaction(models.Model):
    """Tracks point earnings and spendings"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_transactions')
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=[
        ('earned', 'Earned'),
        ('spent', 'Spent'),
        ('bonus', 'Bonus'),
        ('penalty', 'Penalty'),
    ])
    reason = models.CharField(max_length=100)
    related_object_type = models.CharField(max_length=50, blank=True)  # e.g., 'quiz', 'course'
    related_object_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.points} points ({self.transaction_type})"


class Leaderboard(models.Model):
    """Dynamic leaderboards for competitions"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('global', 'Global'),
        ('course', 'Course-based'),
        ('subject', 'Subject-based'),
        ('class', 'Class-based'),
        ('weekly', 'Weekly Challenge'),
        ('monthly', 'Monthly Challenge'),
    ])
    metric = models.CharField(max_length=50, choices=[
        ('points', 'Total Points'),
        ('streak', 'Current Streak'),
        ('courses_completed', 'Courses Completed'),
        ('time_spent', 'Time Spent'),
        ('quiz_average', 'Quiz Average Score'),
    ])
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_entries = models.IntegerField(default=100)

    class Meta:
        ordering = ['-end_date']

    def __str__(self):
        return self.name


class LeaderboardEntry(models.Model):
    """Entries in leaderboards"""
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    rank = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['leaderboard', 'user']
        ordering = ['rank']

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} ({self.score})"


class Challenge(models.Model):
    """Daily/weekly challenges for users"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=50, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ])
    category = models.CharField(max_length=50, choices=[
        ('learning', 'Learning Activity'),
        ('social', 'Social Interaction'),
        ('quiz', 'Quiz Performance'),
        ('streak', 'Streak Maintenance'),
        ('time', 'Time-based'),
    ])
    criteria_type = models.CharField(max_length=50)
    criteria_value = models.IntegerField()
    points_reward = models.IntegerField(default=50)
    badge_reward = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_completions = models.IntegerField(default=1)  # How many times can be completed

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    """User progress on challenges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    times_completed = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'challenge']

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"


class Reward(models.Model):
    """Redeemable rewards using points"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    reward_type = models.CharField(max_length=50, choices=[
        ('virtual', 'Virtual Item'),
        ('certificate', 'Certificate'),
        ('badge', 'Special Badge'),
        ('feature', 'Feature Unlock'),
        ('discount', 'Discount'),
    ])
    points_cost = models.IntegerField()
    image = models.ImageField(upload_to='rewards/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=-1)  # -1 for unlimited
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['points_cost']

    def __str__(self):
        return f"{self.name} ({self.points_cost} points)"


class UserReward(models.Model):
    """Rewards redeemed by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.name}"


class Level(models.Model):
    """User levels and progression"""
    name = models.CharField(max_length=50)
    level_number = models.IntegerField(unique=True)
    points_required = models.IntegerField()
    description = models.TextField(blank=True)
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['level_number']

    def __str__(self):
        return f"Level {self.level_number}: {self.name}"


class UserLevel(models.Model):
    """User's current level and progress"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='level')
    current_level = models.ForeignKey(Level, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    points_to_next = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Level {self.current_level.level_number}"