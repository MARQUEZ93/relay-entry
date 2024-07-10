# RelayEntry/management/commands/send_test_email.py

# from django.core.management.base import BaseCommand
# from django.core.mail import send_mail

# class Command(BaseCommand):
#     help = 'Send a test email to verify MailHog setup'

#     def handle(self, *args, **kwargs):
#         send_mail(
#             'John W birthday!',
#             'This is the body of the test email.',
#             'from@example.com',  # Replace with a valid from address
#             ['to@example.com'],  # Replace with a valid to address
#             fail_silently=False,
#         )
#         self.stdout.write(self.style.SUCCESS('Happy Birthday John!!!'))
