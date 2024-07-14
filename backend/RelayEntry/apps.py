import os
from django.apps import AppConfig
class BackendConfig(AppConfig):
    name = 'RelayEntry'

    def ready(self):
        environment = os.getenv('DJANGO_ENV', 'development')
        if environment == 'production':
            import RelayEntry.signals as signals
        else:
            import RelayEntry.signals_dev as signals