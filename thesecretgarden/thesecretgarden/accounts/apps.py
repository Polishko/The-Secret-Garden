from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'thesecretgarden.accounts'

    def ready(self):
        import thesecretgarden.accounts.signals
        