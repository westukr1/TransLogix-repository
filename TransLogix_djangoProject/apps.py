
from django.apps import AppConfig

class TranslogixConfig(AppConfig):
    name = 'TransLogix_djangoProject'

    def ready(self):
        import TransLogix_djangoProject.signals  # Import signals to ensure they are loaded
