from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from notifications.sms.backends.base import BaseSmsBackend as _BaseSmsBackend

__all__ = ['get_sms_backend']


def get_sms_backend() -> _BaseSmsBackend:
    backend_import = getattr(settings, "SMS_SETTINGS", {}).get("BACKEND")
    if not backend_import:
        raise ImproperlyConfigured(
            "Please specify BACKEND in SMS_SETTINGS within your settings"
        )

    backend_cls = import_string(backend_import)
    if settings.SMS_SETTINGS.get("OPTIONS", None):
        return backend_cls(**settings.SMS_SETTINGS["OPTIONS"])
    else:
        return backend_cls(**{})
