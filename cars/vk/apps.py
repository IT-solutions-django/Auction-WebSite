from django.apps import AppConfig


class VkConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vk"

    def ready(self):
        import vk.signals  # Подключение сигналов