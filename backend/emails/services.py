from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailLog

def send_and_log(user, recipient, email_type, subject, body):
    """
    Creates an EmailLog entry, attempts to send the email, and updates the log with the result.
    """

    log = EmailLog.objects.create(
        user=user,
        recipient=recipient,
        email_type=email_type,
        subject=subject,
        body=body,
        status=EmailLog.STATUS_QUEUED,
    )

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        log.status = EmailLog.STATUS_SENT
        log.sent_at = timezone.now()
        log.save(update_fields=['status', 'sent_at'])

    except Exception as e :
        log.status = EmailLog.STATUS_FAILED
        log.error_message = str(e)
        log.save(update_fields=['status', 'error_message'])

    return log