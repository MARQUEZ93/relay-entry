# docker exec -it backend python manage.py send_results --test
import sys
from django.core.management.base import BaseCommand, CommandError
from RelayEntry.models import UserProfile, Registration
from django.conf import settings
from mailjet_rest import Client
import os

# Initialize MailJet client
mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')

class Command(BaseCommand):
    help = 'Send emails to team members'

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', help='Run in test mode')
        parser.add_argument('--dangerous', action='store_true', help='Run the dangerous action')

    def handle(self, *args, **options):
        if options['test']:
            self.run_test()
        elif options['dangerous']:
            self.run_dangerous_action()
        else:
            self.run_main_function()

    def run_test(self):
        print('Running test action')
        send_mailjet_email("marqueza@utexas.edu")

    def run_dangerous_action(self):
        print('Running dangerous action')
        registrations = Registration.objects.all()
        for registration in registrations:
            try:
                send_mailjet_email(registration.email)
                print(f"Email sent to {registration.email}")
            except Exception as e:
                print(f"Failed to send email to {registration.email}: {e}")

    def run_main_function(self):
        print('Main function does nothing')

def send_mailjet_email(recipient_email):
        html_part = f"""
                <h3>Sunrise Track Club Sunset Relays Results!</h3>
                <p>https://www.relayentry.com/events/sunrise-track-club-sunset-relays/results/</p>
                """
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
                            "Name": "Participant"
                        }
                    ],
                    "Subject": "Sunrise Track Club Sunset Relays Results",
                    "TextPart": "Thank you for participating!",
                    "HTMLPart": html_part
                }
            ]
        }
        try:
            result = mailjet.send.create(data=data)
            print(result.status_code)
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")