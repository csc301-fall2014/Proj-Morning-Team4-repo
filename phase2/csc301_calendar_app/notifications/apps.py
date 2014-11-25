from django.apps import AppConfig

class ReportsConfig(AppConfig):
    name = 'reports'
    verbose_name = "Reports"

    def ready(self):
        import signals
