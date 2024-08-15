
from django.apps import AppConfig

class TranslogixConfig(AppConfig):
    name = 'translogix'

    def ready(self):
        import translogix.signals  # Import signals to ensure they are loaded
