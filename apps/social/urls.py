from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'study-groups', views.StudyGroupViewSet, basename='study-group')
router.register(r'forum-posts', views.ForumPostViewSet, basename='forum-post')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'peer-tutoring', views.PeerTutoringViewSet, basename='peer-tutoring')
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'announcements', views.AnnouncementViewSet, basename='announcement')
router.register(r'bookmarks', views.BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
]