from django.apps import AppConfig

class BackendConfig(AppConfig):
    name = 'RelayEntry'

    def ready(self):
        import RelayEntry.signals