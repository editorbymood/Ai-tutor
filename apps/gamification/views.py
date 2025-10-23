from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import (
    Badge, UserBadge, PointTransaction, Leaderboard, LeaderboardEntry,
    Challenge, UserChallenge, Reward, UserReward, Level, UserLevel
)
from .serializers import (
    BadgeSerializer, UserBadgeSerializer, PointTransactionSerializer,
    LeaderboardSerializer, LeaderboardEntrySerializer, ChallengeSerializer, UserChallengeSerializer,
    RewardSerializer, UserRewardSerializer, LevelSerializer, UserLevelSerializer
)


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.filter(is_active=True)
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def earned(self, request):
        """Get badges earned by the current user"""
        user_badges = UserBadge.objects.filter(user=request.user)
        serializer = UserBadgeSerializer(user_badges, many=True)
        return Response(serializer.data)


class PointTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PointTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PointTransaction.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get points summary for the user"""
        transactions = self.get_queryset()
        total_earned = transactions.filter(transaction_type='earned').aggregate(
            total=Sum('points'))['total'] or 0
        total_spent = transactions.filter(transaction_type='spent').aggregate(
            total=Sum('points'))['total'] or 0
        current_balance = total_earned - total_spent

        return Response({
            'total_earned': total_earned,
            'total_spent': total_spent,
            'current_balance': current_balance
        })


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.filter(is_active=True)
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def user_rankings(self, request):
        """Get user's position in active leaderboards"""
        user_entries = LeaderboardEntry.objects.filter(
            user=request.user,
            leaderboard__is_active=True
        ).select_related('leaderboard')
        serializer = LeaderboardEntrySerializer(user_entries, many=True)
        return Response(serializer.data)


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Challenge.objects.filter(
            is_active=True,
            end_date__gt=timezone.now()
        )

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a challenge as completed"""
        challenge = self.get_object()
        user_challenge, created = UserChallenge.objects.get_or_create(
            user=request.user,
            challenge=challenge
        )

        if user_challenge.is_completed and user_challenge.times_completed >= challenge.max_completions:
            return Response(
                {'error': 'Challenge already completed maximum times'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if criteria are met (simplified - in real implementation, check actual progress)
        user_challenge.progress = challenge.criteria_value
        user_challenge.is_completed = True
        user_challenge.completed_at = timezone.now()
        user_challenge.times_completed += 1
        user_challenge.save()

        # Award points
        PointTransaction.objects.create(
            user=request.user,
            points=challenge.points_reward,
            transaction_type='earned',
            reason=f'Completed challenge: {challenge.title}'
        )

        # Award badge if applicable
        if challenge.badge_reward:
            UserBadge.objects.get_or_create(
                user=request.user,
                badge=challenge.badge_reward
            )

        return Response({'message': 'Challenge completed successfully'})


class UserChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserChallenge.objects.filter(user=self.request.user)


class RewardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reward.objects.filter(is_active=True)
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def redeem(self, request, pk=None):
        """Redeem a reward"""
        reward = self.get_object()

        # Check if user already redeemed this reward
        if UserReward.objects.filter(user=request.user, reward=reward).exists():
            return Response(
                {'error': 'Reward already redeemed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check points balance
        points_summary = PointTransaction.objects.filter(user=request.user).aggregate(
            earned=Sum('points', filter=Q(transaction_type='earned')),
            spent=Sum('points', filter=Q(transaction_type='spent'))
        )
        current_balance = (points_summary['earned'] or 0) - (points_summary['spent'] or 0)

        if current_balance < reward.points_cost:
            return Response(
                {'error': 'Insufficient points'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check stock
        if reward.stock > 0:
            reward.stock -= 1
            reward.save()

        # Create redemption record
        UserReward.objects.create(user=request.user, reward=reward)

        # Deduct points
        PointTransaction.objects.create(
            user=request.user,
            points=reward.points_cost,
            transaction_type='spent',
            reason=f'Redeemed reward: {reward.name}'
        )

        return Response({'message': 'Reward redeemed successfully'})


class UserRewardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserRewardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserReward.objects.filter(user=self.request.user)


class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [IsAuthenticated]


class UserLevelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserLevelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserLevel.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current user level"""
        try:
            user_level = UserLevel.objects.get(user=request.user)
            serializer = self.get_serializer(user_level)
            return Response(serializer.data)
        except UserLevel.DoesNotExist:
            return Response(
                {'error': 'User level not found'},
                status=status.HTTP_404_NOT_FOUND
            )