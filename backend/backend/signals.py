from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        send_welcome_email(instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

def send_welcome_email(user):
    send_mail(
        'Welcome to My Site',
        'Thank you for registering with our site. We are excited to have you on board!',
        'your_email@example.com',  # Replace with your actual "from" email
        [user.email],
        fail_silently=False,
    )
