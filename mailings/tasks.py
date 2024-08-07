from datetime import datetime
import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
import logging
from .models import Mailing, MailingAttempt

logger = logging.getLogger(__name__)


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(start_datetime__lte=current_datetime, status='started')

    for mailing in mailings:
        for client in mailing.clients.all():
            try:
                with transaction.atomic():
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )
                    status = 'success'
                    server_response = 'Sent successfully'

                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status=status,
                        server_response=server_response,
                    )

                    logger.info(f"Mail sent successfully to {client.email} for mailing id {mailing.id}")

            except Exception as e:
                status = 'failed'
                server_response = str(e)

                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=status,
                    server_response=server_response,
                )

                logger.error(f"Failed to send mail to {client.email} for mailing id {mailing.id}: {server_response}")
