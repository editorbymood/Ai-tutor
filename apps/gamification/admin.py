"""
Admin configuration for gamification app.
"""
from django.contrib import admin
from .models import Badge, UserBadge, PointTransaction, Leaderboard, LeaderboardEntry, Challenge, UserChallenge, Reward, UserReward, Level, UserLevel


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    """Admin for Badge model."""
    list_display = ['name', 'category', 'criteria_type', 'points_reward', 'is_active', 'created_at']
    list_filter = ['category', 'criteria_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    """Admin for UserBadge model."""
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['earned_at', 'badge__category']
    search_fields = ['user__email', 'badge__name']
    readonly_fields = ['earned_at']
    raw_id_fields = ['user', 'badge']


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    """Admin for PointTransaction model."""
    list_display = ['user', 'points', 'transaction_type', 'reason', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user__email', 'reason']
    readonly_fields = ['created_at']
    raw_id_fields = ['user']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin for Leaderboard model."""
    list_display = ['name', 'category', 'metric', 'is_active', 'start_date', 'end_date']
    list_filter = ['category', 'metric', 'is_active', 'start_date']
    search_fields = ['name', 'description']
    raw_id_fields = ['course']


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    """Admin for Challenge model."""
    list_display = ['title', 'challenge_type', 'category', 'points_reward', 'start_date', 'end_date', 'is_active']
    list_filter = ['challenge_type', 'category', 'is_active', 'start_date']
    search_fields = ['title', 'description']
    raw_id_fields = ['badge_reward']


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    """Admin for Reward model."""
    list_display = ['name', 'reward_type', 'points_cost', 'stock', 'is_active', 'created_at']
    list_filter = ['reward_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
