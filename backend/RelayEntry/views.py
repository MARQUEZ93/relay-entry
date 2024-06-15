from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import anonymous_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
import stripe
import os
import json
from .models import UserProfile, Event, Race
from .serializers import EventSerializer, RaceSerializer, EventWithRacesSerializer
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class RaceDetailView(generics.RetrieveAPIView):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer
    lookup_field = 'id'

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventWithRacesSerializer

    lookup_field = 'url_alias'    

    def get_queryset(self):
        return Event.objects.prefetch_related('races').filter(published=True)

@login_required
def index(request):
    return render(request, 'index.html')

@anonymous_required
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.userprofile.is_approved = False
            user.save()
            # Send email to admin
            send_mail(
                'New User Signup Requires Approval',
                f'A new user {user.username} has signed up and requires approval.',
                settings.DEFAULT_FROM_EMAIL,
                ['admin@example.com'],  # TODO: Replace with the admin's email address
                fail_silently=False,
            )
            # Send email to the user
            send_mail(
                'Signup Successful - Approval Pending',
                f'Thank you for signing up, {user.username}. Your account is currently pending approval by an admin. You will be notified once your account is approved.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],  # TODO: Send to the user's email address
                fail_silently=False,
            )
            return redirect('signup_success')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Initialize the Stripe API key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@login_required
def connect_stripe_account(request):
    if request.method == 'POST':
        account = stripe.Account.create(
            type='standard',
            country='US',
            email=request.user.email,
        )
        UserProfile.objects.update_or_create(
            user=request.user,
            defaults={'stripe_account_id': account.id}
        )
        return redirect(account.links.url)
    return render(request, 'connect_stripe.html')

@login_required
def stripe_callback(request):
    code = request.GET.get('code')
    if code:
        account_response = stripe.OAuth.token(grant_type='authorization_code', code=code)
        account_id = account_response['stripe_user_id']
        UserProfile.objects.update_or_create(
            user=request.user,
            defaults={'stripe_account_id': account_id, 'stripe_account_verified': True}
        )
        return redirect('profile')
    return redirect('connect_stripe')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data['amount']  # Ensure the amount is sent in the request body

            # Create a PaymentIntent with the specified amount in test mode
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )

            return JsonResponse({
                'status': intent['status'],
                'clientSecret': intent['client_secret'],
                'id': intent['id']  # Make sure to include the ID here
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def confirm_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_intent_id = data['payment_intent_id']

            # Confirm the PaymentIntent using a test payment method
            intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                payment_method='pm_card_visa',  # Use a test payment method ID
            )

            return JsonResponse({
                'status': intent['status'],
                'clientSecret': intent['client_secret'],
                'id': intent['id']  # Make sure to include the ID here
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
