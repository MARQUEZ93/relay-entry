from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.db import transaction
import logging

from .models import UserProfile, Registration, Team, TeamMember, Event, Race
from .utils.email_utils import send_email

import os

# Set up logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Registration)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        def send_emails():
            race_name = instance.race.name
            event_name = instance.race.event.name
            confirmation_code = instance.confirmation_code
            if instance.race.event.instagram_url:
                url = instance.race.event.instagram_url
            elif instance.race.event.website_url:
                url = instance.race.event.website_url
            else:
                url = "https://default.url"  # Default URL if none provided
            contact = "relayentry@gmail.com" # email this if you have questions

            html_content = f"""
            <h3>Dear {instance.first_name}, welcome to RelayEntry!</h3>
            <p>You are registered for the <strong>{race_name}</strong> race in the event <strong>{event_name}</strong>.</p>
            <p>For updates about the event, please visit {url}</p>
            <p>Your confirmation code: {confirmation_code}.</p>
            <p>Please email {contact} if help is needed with your registration. Include your confirmation code!</p>
            """

            send_email(
                recipient_email=instance.email,
                recipient_name=instance.first_name,
                subject=f'You are registered for {event_name}',
                text_part="Greetings from RelayEntry!",
                html_part=html_content,
            )
        # Use transaction.on_commit to ensure emails are sent only after the transaction is committed
        transaction.on_commit(send_emails)

@receiver(post_save, sender=Team)
def send_team_creation_email(sender, instance, created, **kwargs):
    if created:
        def send_emails():
            if instance.race and instance.race.event:
                race_director_email = instance.race.event.email
                team_name = instance.name
                race_name = instance.race.name
                event_name = instance.race.event.name
                captain_first_name = instance.captain.first_name
                captain_last_name = instance.captain.last_name
                captain_email = instance.captain.email
                html_content = f"""
                <h3>Dear Race Director,</h3>
                <p>The team: {team_name} registered for the {race_name} race in {event_name}.</p>
                <p>The team captain: {captain_first_name} {captain_last_name}</p>
                <p>The team captain email: {captain_email}</p>
                <br />
                <p>Please email relayentry@gmail.com if you need help!</p>
                """
                send_email(
                    recipient_email=race_director_email,
                    recipient_name="Race Director",
                    subject=f'A new team registered for {race_name} in {event_name}',
                    text_part="Greetings from RelayEntry!",
                    html_part=html_content,
                )

                confirmation_code = instance.captain.confirmation_code

                # iterate team.members & provide info in the confirmation email
                team_members_info = ""
                for member in instance.members.all():
                    team_members_info += f"<li>{member.email} (Leg Order: {member.leg_order})</li>"

                html_content = f"""
                <h3>Dear Team Captain,</h3>
                <p>Your team registered for the {race_name} race in {event_name}.</p>
                <p>{team_name} Members:</p>
                <ul>
                    {team_members_info}
                </ul>
                <p>Your confirmation code: {confirmation_code}.</p>
                <p>Please email relayentry@gmail.com if help is needed with your team registration. Include your confirmation code!</p>
                """
                send_email(
                    recipient_email=captain_email,
                    recipient_name=captain_first_name,
                    subject=f'Your registered team for {event_name}',
                    text_part="Greetings from RelayEntry!",
                    html_part=html_content,
                )
                for member in instance.members.all():
                    if member.email != captain_email:
                        html_content = f"""
                        <h3>Join your team!</h3>
                        <p>You were added to a team for the {race_name} race in {event_name}.</p>
                        <p>Your team: {team_name}, created by {captain_first_name} {captain_last_name}.</p>
                        <p>{team_name} Members:</p>
                        <ul>
                            {team_members_info}
                        </ul>
                        <p>Your team is already paid for. You only have to register here: https://www.relayentry.com/events/{event.race.event.url_alias}/register</p>
                        """

                        send_email(
                            recipient_email=member.email,
                            recipient_name="Team Member",
                            subject=f'Please register for {event_name}',
                            text_part="Greetings from RelayEntry!",
                            html_part=html_content,
                        )


        transaction.on_commit(send_emails)

@receiver(post_save, sender=Registration)
def set_team_member(sender, instance, created, **kwargs):
    if created:
        def set_member():
            try:
                if instance.member:
                    logger.warning(f"Did not set team member for registration {instance.email}: due to already being tied to a team member")
                    return
                for team in instance.race.teams.all():
                    team_members = team.members.all()
                    team_member = team.members.filter(email=instance.email).first()
                    if team_member:
                        instance.member = team_member
                        instance.save()
            except Exception as e:
                logger.error(f"Failed to set team member for registration {instance.email}: {e}")

        # Use transaction.on_commit to ensure the team member is set only after the transaction is committed
        transaction.on_commit(set_member)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
