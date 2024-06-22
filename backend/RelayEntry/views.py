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
import logging
import json
from .models import UserProfile, Event, Race, Registration, Team
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

from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY  # Use secret key on the server side

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def team_register_and_pay(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method_id = data['payment_method_id']
            race_id = data['race_id']
            racer_data = data['racer_data']
            billing_info = data['billing_info']
            team_data = data['team_data']
            
            # Calculate the amount based on the race price
            try:
                race = Race.objects.get(id=race_id)
            except Race.DoesNotExist:
                logger.error("Race not found.")
                return JsonResponse({'error': "Race not found."}, status=404)
            
            amount = int(race.price * 100)  # Convert to cents

            try:
                # Create the registration instance
                registration = Registration.objects.create(
                    race=race,
                    amount_paid=amount,
                    first_name=racer_data['firstName'],
                    last_name=racer_data['lastName'],
                    email=racer_data['email'],
                    phone=racer_data.get('phone', ''),
                    gender=racer_data['gender'],
                    dob=racer_data['dateOfBirth'],
                    minor=racer_data['minor'],
                    waiver_text=race.event.waiver_text,
                    parent_guardian_name=racer_data.get('parentGuardianName', ''),
                    parent_guardian_signature=racer_data.get('parentGuardianSignature', ''),
                )

                 # Create the registration instance
                registration = Team.objects.create(
                    race=race,
                    amount_paid=amount,
                    first_name=racer_data['firstName'],
                    last_name=racer_data['lastName'],
                    email=racer_data['email'],
                    phone=racer_data.get('phone', ''),
                    gender=racer_data['gender'],
                    dob=racer_data['dateOfBirth'],
                    minor=racer_data['minor'],
                    waiver_text=race.event.waiver_text,
                    parent_guardian_name=racer_data.get('parentGuardianName', ''),
                    parent_guardian_signature=racer_data.get('parentGuardianSignature', ''),
                )

                # Create a PaymentIntent with the amount and currency
                intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency='usd',
                    return_url="http://localhost:8080/confirmation",  # Update with your actual return URL
                    payment_method=payment_method_id,
                    confirmation_method='manual',
                    confirm=True,
                    metadata={
                        'race_id': race_id,
                        'racer_name': f"{racer_data['firstName']} {racer_data['lastName']}",
                        'billing_name': billing_info['name'],
                        'billing_email': billing_info['email'],
                    },
                )
                # Return client secret, confirmation code, race   r data, and race data
                return JsonResponse({
                    'payment_intent': intent,
                    'confirmation_code': registration.confirmation_code,
                    'racer_data': racer_data,
                    'race_data': {
                        'name': race.name,
                        'date': race.date,
                        'description': race.description,
                        'event': race.event.name
                    },
                    'team_data': {
                        'name': team.name,
                    }
                })

            except stripe.error.CardError as e:
                logger.error(f"Card error: {e.user_message}")
                return JsonResponse({'error': e.user_message}, status=400)
            except stripe.error.RateLimitError as e:
                logger.error(f"Rate limit error: {e.user_message}")
                return JsonResponse({'error': "Too many requests made to the API too quickly."}, status=400)
            except stripe.error.InvalidRequestError as e:
                logger.error(f"Invalid parameters were supplied to Stripe's API: {e.user_message}")
                return JsonResponse({'error': "Invalid parameters."}, status=400)
            except stripe.error.AuthenticationError as e:
                logger.error(f"Authentication with Stripe's API failed: {e.user_message}")
                return JsonResponse({'error': "Authentication failed."}, status=401)
            except stripe.error.APIConnectionError as e:
                logger.error(f"Network communication with Stripe failed: {e.user_message}")
                return JsonResponse({'error': "Network error."}, status=400)
            except stripe.error.StripeError as e:
                logger.error(f"Stripe error: {e.user_message}")
                return JsonResponse({'error': "Something went wrong. You were not charged. Please try again."}, status=400)
            except Exception as e:
                logger.error(f"General error: {str(e)}")
                return JsonResponse({'error': "An error occurred. Please try again."}, status=400)
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({'error': "Invalid JSON data."}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': "An unexpected error occurred."}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
