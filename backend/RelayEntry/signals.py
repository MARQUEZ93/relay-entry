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

# send email on registration (Registration.email) (to either Registration.race.event.email or Registration.event.email)
# send email to team captain when team is created (team.captain.email) + race.event.email
# send email to the team member when a team member is created  (TeamMember.email)
# email team captain when a registration is created, 
# and the email of the registration matches a team member email (that belong to the team captain's team) + Team.race.event equals (registartion.event - null check bTW optional field)
# @receiver(post_save, sender=Registration)
# def send_registration_email(sender, instance, created, **kwargs):
#     if created:
#         def send_emails():
#             if instance.race and instance.race.event:
#                 race_director_email = instance.race.event.email
#                 race_name = instance.race.name
#             elif instance.event:
#                 race_director_email = instance.event.email
#                 event_name = instance.event.name
#             else:
#                 race_director_email = None
#                 race_name = None
#                 event_name = None

#             try:
#                 # Email the registrant
#                 send_mail(
#                     'Registration Successful',
#                     'Thank you for registering.',
#                     settings.DEFAULT_FROM_EMAIL,
#                     [instance.email],
#                     fail_silently=True,
#                 )
#             except Exception as e:
#                 logger.error(f"Failed to send registration email to {instance.email}: {e}")

#             try:
#                 if race_director_email:
#                     send_mail(
#                         'New Registration For Your Race',
#                         f'A new registration has been made by {instance.email}.',
#                         settings.DEFAULT_FROM_EMAIL,
#                         [race_director_email],
#                         fail_silently=True,
#                     )
#             except Exception as e:
#                 logger.error(f"Failed to send email to race director for {instance.email}: {e}")
#             try:
#                 if instance.event:  # This means the registrant only registered & did not pay/is not the team captain
#                     print(f"Processing email notification for registration {instance.email} for event {instance.event.name}")
#                     # Query all teams with team.race.event that matches instance.event
#                     for race in instance.event.races.all():
#                         print(f"Checking race {race.name}")
#                         # Iterate through all teams for the race
#                         for team in race.teams.all():
#                             print(f"Checking team {team.name}")
#                             # Check if a team member's email matches the registration email
#                             captain_email = team.captain.email
#                             team_member = team.members.filter(email=instance.email).first()
#                             if team_member:
#                                 print(f"Found matching team member {team_member.email}, sending email to captain {captain_email}")
#                                 send_mail(
#                                     'Team Member Registration For Your Team',
#                                     f'Team member {instance.email} has registered.',
#                                     settings.DEFAULT_FROM_EMAIL,
#                                     [captain_email],
#                                     fail_silently=True,
#                                 )
#                                 break  # No need to check further once the team is found
#             except Exception as e:
#                 logger.error(f"Failed to send team member registration email for {instance.email}: {e}")
#                 print(f"Error sending team member registration email for {instance.email}: {e}")

#         # Use transaction.on_commit to ensure emails are sent only after the transaction is committed
#         transaction.on_commit(send_emails)

# @receiver(post_save, sender=Team)
# def send_team_creation_email(sender, instance, created, **kwargs):
#     if created:
#         def send_emails():
#             try:
#                 # Email the race director
#                 if instance.race and instance.race.event:
#                     race_director_email = instance.race.event.email
#                     send_mail(
#                         'New Team Created',
#                         f'A new team has been created by {instance.captain.email}.',
#                         settings.DEFAULT_FROM_EMAIL,
#                         [race_director_email],
#                         fail_silently=True,
#                     )
#             except Exception as e:
#                 logger.error(f"Failed to send team creation email to race director for {instance.captain.email}: {e}")
        
#         # Use transaction.on_commit to ensure emails are sent only after the transaction is committed
#         transaction.on_commit(send_emails)
# @receiver(post_save, sender=TeamMember)
# def send_team_member_creation_email(sender, instance, created, **kwargs):
#     if created:
#         def send_emails():
#             try:
#                 # Email the team member
#                 send_mail(
#                     'You have been added to a team.',
#                     'You have been added to a team.',
#                     settings.DEFAULT_FROM_EMAIL,
#                     [instance.email],
#                     fail_silently=True,
#                 )
#             except Exception as e:
#                 logger.error(f"Failed to send team member creation email to {instance.email}: {e}")
#         transaction.on_commit(send_emails)


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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# @receiver(post_save, sender=Registration)
# def set_team_member(sender, instance, created, **kwargs):
#     if created:
#         def set_member():
#             try:
#                 print(f"Processing registration {instance.email} for event {instance.event.name}")
#                 # Iterate through all races for the event
#                 for race in instance.event.races.all():
#                     print(f"Checking race {race.name}")
#                     # Iterate through all teams for the race
#                     for team in race.teams.all():
#                         print(f"Checking team {team.name}")
#                         team_members = team.members.all()
#                         print(f"Team members for team {team.name}: {[member.email for member in team_members]}")
#                         # Check if a team member's email matches the registration email
#                         team_member = team.members.filter(email=instance.email).first()
#                         if team_member:
#                             print(f"Found matching team member {team_member.email}")
#                             # TODO: fool proof this - later
#                             instance.member = team_member
#                             instance.save()
#                             break
#                     if instance.member:
#                         break
#             except Exception as e:
#                 logger.error(f"Failed to set team member for registration {instance.email}: {e}")

#         # Use transaction.on_commit to ensure the team member is set only after the transaction is committed
#         transaction.on_commit(set_member)
