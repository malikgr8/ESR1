from django.apps import AppConfig


class FeedApp(AppConfig):
    name = 'project.feed'
    verbose_name = "ESR Application"

    def ready(self):
        from . import signals  # noqa
