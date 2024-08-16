import os
from django.apps import AppConfig
class BackendConfig(AppConfig):
    name = 'RelayEntry'

    def ready(self):
        environment = os.getenv('ENVIRONMENT', 'development')
        import RelayEntry.signals as signals