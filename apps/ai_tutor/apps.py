from django.apps import AppConfig


class AiTutorConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'  # type: ignore[assignment]
    name = 'apps.ai_tutor'
    verbose_name = 'AI Tutor'