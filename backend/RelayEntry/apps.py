import os
from django.apps import AppConfig
class BackendConfig(AppConfig):
    name = 'RelayEntry'

    def ready(self):
        environment = os.getenv('ENVIRONMENT', 'development')
        if environment == 'production':
            import RelayEntry.signals as signals
        else:
            import RelayEntry.signals_dev as signals