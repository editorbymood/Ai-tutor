"""
URL configuration for AI-Powered Personal Tutor project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView
from backend import health

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Health check endpoints (for load balancers and monitoring)
    path("health/", health.health_check, name="health_check"),
    path("health/ready/", health.readiness_check, name="readiness_check"),
    path("health/live/", health.liveness_check, name="liveness_check"),
    path("metrics/", health.metrics, name="metrics"),
    path("metrics/cache/", health.cache_stats, name="cache_stats"),
    path("metrics/database/", health.database_stats, name="database_stats"),
    # API endpoints
    path("api/auth/", include("apps.users.urls")),
    path("api/courses/", include("apps.courses.urls")),
    path("api/assessments/", include("apps.assessments.urls")),
    path("api/ai-tutor/", include("apps.ai_tutor.urls")),
    path("api/analytics/", include("apps.analytics.urls")),
    path("api/gamification/", include("apps.gamification.urls")),
    path("api/social/", include("apps.social.urls")),
    path("api/voice/", include("apps.voice.urls")),
    # JWT Token endpoints
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "AI Tutor Admin"
admin.site.site_title = "AI Tutor Admin Portal"
admin.site.index_title = "Welcome to AI Tutor Administration"
