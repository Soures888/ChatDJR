from django.apps import AppConfig


class ChatConfig(AppConfig):
    name = 'isiTestApp.chat'

    def ready(self):
        import isiTestApp.chat.signals  # noqa