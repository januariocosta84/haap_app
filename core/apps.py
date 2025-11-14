
from django.apps import AppConfig

class UsersConfig(AppConfig):  # or CoreConfig, depending on your app name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals  # 👈 import signals here
