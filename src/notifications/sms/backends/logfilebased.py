import logging
from typing import List

from notifications.sms.backends.base import BaseSmsBackend

logger = logging.getLogger(__name__)


class SmsBackend(BaseSmsBackend):
    """
    Log file based sms backend - instead of sending it logs messages to a log file.

    Configuration example.

    Modify your settings.py:
        SMS_SETTINGS = {
            "BACKEND": "notifications.sms.backends.logfilebased.SmsBackend",
        }
    """

    def send_sms(self, phone_numbers: List[str], message: str):
        logger.info(f"SMS sent to {phone_numbers!r} with the message {message!r}")
