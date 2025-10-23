from django.apps import AppConfig


class AssessmentsConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'  # type: ignore[assignment]
    name = 'apps.assessments'
    verbose_name = 'Assessments & Quizzes'