from django.apps import AppConfig

class HrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hrm'

    def ready(self):
        try:
            import hrm.signals
        except ImportError:
            pass
