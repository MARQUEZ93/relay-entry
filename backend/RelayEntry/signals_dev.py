from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
import logging

from .models import UserProfile, Registration, Team, TeamMember, Event, Race

# Set up logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Registration)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        def send_emails():
            try:
                # Email the registrant
                send_mail(
                    'Registration Successful',
                    'Thank you for registering.',
                    settings.DEFAULT_FROM_EMAIL,
                    [instance.email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Failed to send registration email to {instance.email}: {e}")
        # Use transaction.on_commit to ensure emails are sent only after the transaction is committed
        transaction.on_commit(send_emails)

@receiver(post_save, sender=Team)
def send_team_creation_email(sender, instance, created, **kwargs):
    if created:
        def send_emails():
            try:
                # Email the race director
                if instance.race and instance.race.event:
                    race_director_email = instance.race.event.email
                    send_mail(
                        'New Team Created',
                        f'A new team has been created by {instance.captain.email}.',
                        settings.DEFAULT_FROM_EMAIL,
                        [race_director_email],
                        fail_silently=True,
                    )
            except Exception as e:
                logger.error(f"Failed to send team creation email to race director for {instance.captain.email}: {e}")
        # Use transaction.on_commit to ensure emails are sent only after the transaction is committed
        transaction.on_commit(send_emails)

@receiver(post_save, sender=TeamMember)
def send_team_member_creation_email(sender, instance, created, **kwargs):
    if created:
        def send_emails():
            try:
                send_mail(
                    'You have been added to a team.',
                    'You have been added to a team.',
                    settings.DEFAULT_FROM_EMAIL,
                    [instance.email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Failed to send team member creation email to {instance.email}: {e}")
        transaction.on_commit(send_emails)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=Registration)
def set_team_member(sender, instance, created, **kwargs):
    if created:
        def set_member():
            try:
                print(f"Processing registration {instance.email} for race {instance.race.name}")
                if instance.member:
                    print("Already is a member")
                    return
                print(f"Checking race {instance.race.name}")
                for team in instance.race.teams.all():
                  print(f"Checking team {team.name}")
                  team_members = team.members.all()
                  print(f"Team members for team {team.name}: {[member.email for member in team_members]}")
                  team_member = team.members.filter(email=instance.email).first()
                  if team_member:
                      print(f"Found matching team member {team_member.email}")
                      instance.member = team_member
                      instance.save()
                      return
            except Exception as e:
                logger.error(f"Failed to set team member for registration {instance.email}: {e}")

        # Use transaction.on_commit to ensure the team member is set only after the transaction is committed
        transaction.on_commit(set_member)