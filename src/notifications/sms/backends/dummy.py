from typing import List

from notifications.sms.backends.base import BaseSmsBackend


class SmsBackend(BaseSmsBackend):
    """
    Dummy sms backend that does nothing.

    Configuration example.

    Modify your settings.py:
        SMS_SETTINGS = {
            "BACKEND": "notifications.sms.backends.dummy.SmsBackend",
        }
    """

    def send_sms(self, phone_numbers: List[str], message: str):
        pass
