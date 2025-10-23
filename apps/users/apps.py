from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'  # type: ignore[assignment]
    name = 'apps.users'
    verbose_name = 'User Management'

    def ready(self):
        import apps.users.signals