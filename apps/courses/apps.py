from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'  # type: ignore[assignment]
    name = 'apps.courses'
    verbose_name = 'Course Management'