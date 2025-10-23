from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'  # type: ignore[assignment]
    name = 'apps.analytics'
    verbose_name = 'Analytics & Progress Tracking'