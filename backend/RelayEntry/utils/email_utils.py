from django.core.mail import send_mail
from django.conf import settings
from mailjet_rest import Client
import os
import logging
logger = logging.getLogger(__name__)

def send_email(recipient_email, recipient_name, subject, text_part, html_part):
    """
    Determines environment.
    If production, send email via Mailjet.
    If development, send email via MailHog.
    """
    if os.getenv('DJANGO_ENV') == 'production':
        return send_mailjet_email(
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            subject=subject,
            text_part=text_part,
            html_part=html_part
        )
    else:
        return send_mailhog_email(recipient_email, recipient_name, subject, text_part, html_part)

def send_mailjet_email(recipient_email, recipient_name, subject, text_part, html_part):
    mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": settings.DEFAULT_FROM_EMAIL,
                    "Name": "RelayEntry"
                },
                "To": [
                    {
                        "Email": recipient_email,
                        "Name": recipient_name
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part or text_part  # Use text_part if html_part is not provided
            }
        ]
    }
    try:
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            print(result.json())
            return True
        else:
            logger.error(f"Failed to send email via MailJet: {result.json()}")
            return False
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email} via MailJet: {e}")
        return False

def send_mailhog_email(recipient_email, recipient_name, subject, text_part, html_part):
    try:
        send_mail(
            subject,
            html_part,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send email via MailHog: {e}")
        return False
