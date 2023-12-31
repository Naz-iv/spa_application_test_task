from django.apps import AppConfig


class SpaCommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "spa_comments"

    def ready(self):
        import spa_comments.signals
