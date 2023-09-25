from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FileVersionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "propylon_document_manager.file_versions"
    verbose_name = _("File Versions")

    def ready(self):
        try:
            import propylon_document_manager.file_versions.signals  # noqa F401
        except ImportError:
            pass

