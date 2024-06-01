# backend/tests/test_user.py
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core import mail
from backend.RelayEntry.models import UserProfile

class UserSignalsTestCase(TestCase):
    
    def test_user_profile_created(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_welcome_email_sent(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to My Site')
        self.assertIn('Thank you for registering with our site. We are excited to have you on board!', mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to, [user.email])
