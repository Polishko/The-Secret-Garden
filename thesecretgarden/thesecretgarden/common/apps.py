from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'thesecretgarden.common'

    def ready(self):
        import thesecretgarden.common.signals
