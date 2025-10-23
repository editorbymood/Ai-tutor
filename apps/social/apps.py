from django.apps import AppConfig


class SocialConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'  # type: ignore[assignment]
    name = 'apps.social'