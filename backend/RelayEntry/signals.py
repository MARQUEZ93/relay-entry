from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#             'Welcome to RelayEntry',
#             "Thank you for registering with RelayEntry. Let's have a great race day!",
#             'admin@relayentry.com',
#             [instance.email],
#             fail_silently=False,
#         )
