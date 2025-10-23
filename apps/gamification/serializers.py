from rest_framework import serializers
from .models import (
    Badge, UserBadge, PointTransaction, Leaderboard, LeaderboardEntry,
    Challenge, UserChallenge, Reward, UserReward, Level, UserLevel
)


class BadgeSerializer(serializers.ModelSerializer):
    earned_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'icon', 'category', 'criteria_type',
                 'criteria_value', 'points_reward', 'is_active', 'created_at', 'earned_by_user']

    def get_earned_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserBadge.objects.filter(user=request.user, badge=obj).exists()
        return False


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer()

    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'earned_at']


class PointTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointTransaction
        fields = ['id', 'points', 'transaction_type', 'reason', 'related_object_type',
                 'related_object_id', 'created_at']


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = LeaderboardEntry
        fields = ['user', 'score', 'rank', 'updated_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    entries = LeaderboardEntrySerializer(many=True, read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'name', 'description', 'category', 'metric', 'course',
                 'course_name', 'start_date', 'end_date', 'is_active', 'entries']


class ChallengeSerializer(serializers.ModelSerializer):
    user_progress = serializers.SerializerMethodField()
    badge_reward_name = serializers.CharField(source='badge_reward.name', read_only=True)

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'challenge_type', 'category',
                 'criteria_type', 'criteria_value', 'points_reward', 'badge_reward',
                 'badge_reward_name', 'start_date', 'end_date', 'is_active',
                 'max_completions', 'user_progress']

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                user_challenge = UserChallenge.objects.get(user=request.user, challenge=obj)
                return {
                    'progress': user_challenge.progress,
                    'is_completed': user_challenge.is_completed,
                    'times_completed': user_challenge.times_completed,
                    'completed_at': user_challenge.completed_at
                }
            except UserChallenge.DoesNotExist:
                return None
        return None


class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer()

    class Meta:
        model = UserChallenge
        fields = ['id', 'challenge', 'progress', 'completed_at', 'is_completed', 'times_completed']


class RewardSerializer(serializers.ModelSerializer):
    redeemed_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Reward
        fields = ['id', 'name', 'description', 'reward_type', 'points_cost',
                 'image', 'is_active', 'stock', 'created_at', 'redeemed_by_user']

    def get_redeemed_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserReward.objects.filter(user=request.user, reward=obj).exists()
        return False


class UserRewardSerializer(serializers.ModelSerializer):
    reward = RewardSerializer()

    class Meta:
        model = UserReward
        fields = ['id', 'reward', 'redeemed_at', 'status']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name', 'level_number', 'points_required', 'description', 'badge']


class UserLevelSerializer(serializers.ModelSerializer):
    level = LevelSerializer()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = UserLevel
        fields = ['current_level', 'total_points', 'points_to_next', 'updated_at',
                 'level', 'progress_percentage']

    def get_progress_percentage(self, obj):
        if obj.points_to_next > 0:
            return min(100, int((obj.total_points / (obj.total_points + obj.points_to_next)) * 100))
        return 100