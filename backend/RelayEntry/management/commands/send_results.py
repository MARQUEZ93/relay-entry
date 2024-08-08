# docker exec -it backend python manage.py send_results --test
import sys
from django.core.management.base import BaseCommand, CommandError
from RelayEntry.models import UserProfile, Registration
from django.conf import settings
from mailjet_rest import Client
import os

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

    def run_dangerous_action(self):
        print('Running dangerous action')

    def run_main_function(self):
        print('Main function does nothing')