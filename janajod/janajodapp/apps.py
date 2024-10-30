# from django.apps import AppConfig


# class JanajodappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'janajodapp'





# janajodapp/apps.py

from django.apps import AppConfig

class JanajodappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'janajodapp'

    def ready(self):
        import janajodapp.signals  # Import signals to connect them
