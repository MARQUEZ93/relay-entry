# docker exec -it backend python manage.py send_members_email --test
import sys
from django.core.management.base import BaseCommand, CommandError
from RelayEntry.models import UserProfile, Registration, Team, TeamMember, Event, Race 
from django.conf import settings
from mailjet_rest import Client
import os

# Initialize MailJet client
mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')

class Command(BaseCommand):
    help = 'Send emails to team members'

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', help='Run in test mode')
        parser.add_argument('--print', action='store_true', help='Run print logic from dangerous action')
        parser.add_argument('--dangerous', action='store_true', help='Run the dangerous action')

    def handle(self, *args, **options):
        if options['test']:
            self.run_test()
        elif options['print']:
            self.run_print()
        elif options['dangerous']:
            self.run_dangerous_action()
        else:
            self.run_main_function()

    # Send one email to marqueza@utexas.edu (my own email) w/o querying instances. Just package the email the same way. This will be for testing.
    def run_test(self):
        print('Running test function...')
        subject = "Please Register for Sunset Relays"
        text_part = "You are registered for the Sunset Relays in the Male race."
        team_members_info = ""
        for item in ['marqueza@utexas.edu', 'marqueza@utexas.edu', 'marqueza@utexas.edu', 'marqueza@utexas.edu']:
            team_members_info += f"<li>{item} (Leg Order: 1)</li>"
        html_part = f"""
        <h3>Registration Confirmation</h3>
        <p>You are registered for the Sunset Relays in the Male race.</p>
        <p>Your team: Fuckboys, created by Alejandro Marquez.</p>
        <ul>
            {team_members_info}
        </ul>
        <p>Race Date: January 6th 2021</p>
        <p>Register here: https://www.relayentry.com/events/sunrise-track-club-sunset-relays/register</p>
        <p>For more information, see: https://www.instagram.com/sunrise_track_club/</p>
        """

        send_mailjet_email("marqueza@utexas.edu", "Team Member", subject, text_part, html_part)

    # Print all logic from the dangerous action - just do not send emails! Print all variable names etc.
    def run_print(self):
        print('Running print logic action...')
        teams = Team.objects.all()
        for team in teams:
            print(f"Team: {team.name}")
            print(f"Race: {team.race.name}, Event: {team.race.event.name}")
            print(f"Team Captain: {team.captain.first_name} {team.captain.last_name} (Email: {team.captain.email})")
            print("Team Members:")
            team_members_info = ""
            for member in team.members.all():
                team_members_info += f"<li>{member.email} (Leg Order: {member.leg_order})</li>"
            print(team_members_info)
            print(f"Race Date: {team.race.date}")
            print("Register here: https://www.relayentry.com/events/sunrise-track-club-sunset-relays/register")
            print("For more information, see: https://www.instagram.com/sunrise_track_club/")


    # Go through all teams and email each member (excluding the captain). Provide team details and member info in the email.
    def run_dangerous_action(self):
        print('Running dangerous action')
        teams = Team.objects.all()
        for team in teams:
            team_members_info = ""
            for member in team.members.all():
                team_members_info += f"<li>{member.email} (Leg Order: {member.leg_order})</li>"
            subject = f"Please register for {team.race.event.name}"
            text_part = f"You were added to a team for {team.race.event.name}."
            html_part = f"""
            <h3>Join your team!</h3>
            <p>You were added to a team for the {team.race.event.name} in the {team.race.name} race.</p>
            <p>Your team: {team.name}, created by {team.captain.first_name} {team.captain.last_name}.</p>
            <ul>
                {team_members_info}
            </ul>
            <p>Your team is already paid for. You only have to register here: https://www.relayentry.com/events/sunrise-track-club-sunset-relays/register</p>
            <p>For more information, see: https://www.instagram.com/sunrise_track_club/</p>
            """
            # do not spam the team captain (they are already registered)
            for member in team.members.all():
                if member.email != team.captain.email:
                    try:
                        send_mailjet_email(member.email, "Team Member", subject, text_part, html_part)
                        print(f"Email sent to {member.email}")
                    except Exception as e:
                        print(f"Failed to send email to {member.email}: {e}")

    def run_main_function(self):
        print('Main function does nothing')

def send_mailjet_email(recipient_email, recipient_name, subject, text_part, html_part):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "no-reply@relayentry.com",
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
                "HTMLPart": html_part
            }
        ]
    }
    try:
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
