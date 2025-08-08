from django.apps import AppConfig

class SharedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shared'
    verbose_name = 'Shared'

    def ready(self):
        import shared.signals  # noqa
