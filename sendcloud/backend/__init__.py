import logging
import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from sendcloud.exceptions import SendCloudAPIError
from ..conf import (
    get_send_mail_url,
    get_send_cloud_spark_user,
    get_send_cloud_spark_key,
)

logger = logging.getLogger("sendcloud")


class SendCloudBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, *args, **kwargs):

        super(SendCloudBackend, self).__init__(
            fail_silently=fail_silently, *args, **kwargs
        )

    @property
    def app_user(self):
        _app_user = get_send_cloud_spark_user()
        logger.info(_app_user)
        return _app_user

    @property
    def app_key(self):
        _app_key = get_send_cloud_spark_key()
        logger.info(_app_key)
        return _app_key

    @property
    def api_url(self):
        _api_url = get_send_mail_url()
        return _api_url

    def open(self):
        pass

    def close(self):
        pass

    def _send(self, email_message, template=None):
        """A helper method that does the actual sending."""
        # print (dir(email_message))
        if not email_message.recipients():
            return False
        from_email = sanitize_address(email_message.from_email, email_message.encoding)
        recipients = [
            sanitize_address(addr, email_message.encoding)
            for addr in email_message.recipients()
        ]

        params = {
            "apiUser": self.app_user,
            "apiKey": self.app_key,
            # "templateInvokeName": template,
            "subject": email_message.subject,
            "from": from_email,
            "to": recipients,
            "html": email_message.body,
        }
        if template:
            params.update({"templateInvokeName": template})

        r = requests.post(self.api_url, files={}, data=params)

        if r.status_code != 200:
            if not self.fail_silently:
                raise SendCloudAPIError(r.text)
            return False

        res = r.json()
        if not res["result"]:
            logger.info(res["message"])
            raise SendCloudAPIError(res["message"])
        return True

    def send_messages(self, email_messages):
        """Sends one or more EmailMessage objects and returns the number of
        email messages sent.
        """
        if not email_messages:
            return

        num_sent = 0
        for message in email_messages:
            if self._send(message):
                num_sent += 1

        return num_sent
