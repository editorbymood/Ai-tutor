from django.apps import AppConfig


class MlModelsConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'  # type: ignore[assignment]
    name = 'apps.ml_models'
    verbose_name = 'Machine Learning Models'