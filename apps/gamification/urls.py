from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'badges', views.BadgeViewSet)
router.register(r'point-transactions', views.PointTransactionViewSet, basename='point-transaction')
router.register(r'leaderboards', views.LeaderboardViewSet)
router.register(r'challenges', views.ChallengeViewSet, basename='challenge')
router.register(r'user-challenges', views.UserChallengeViewSet, basename='user-challenge')
router.register(r'rewards', views.RewardViewSet)
router.register(r'user-rewards', views.UserRewardViewSet, basename='user-reward')
router.register(r'levels', views.LevelViewSet)
router.register(r'user-levels', views.UserLevelViewSet, basename='user-level')

urlpatterns = [
    path('', include(router.urls)),
]