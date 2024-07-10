from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import anonymous_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
import os
import logging
import json
from .models import UserProfile, Event, Race, Registration, Team, TeamMember
from .serializers import EventSerializer, RaceSerializer, EventWithRacesSerializer
from rest_framework import generics
from django.views.decorators.http import require_POST
from django.db import transaction
from .stripe_utils import retrieve_payment_intent 
import stripe
from .conversion import convert_keys_to_snake_case, convert_keys_to_camel_case
stripe.api_key = settings.STRIPE_SECRET_KEY

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

# @anonymous_required
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()  # load the profile instance created by the signal
#             user.userprofile.is_approved = False
#             user.save()
#             # Send email to admin
#             send_mail(
#                 'New User Signup Requires Approval',
#                 f'A new user {user.username} has signed up and requires approval.',
#                 settings.DEFAULT_FROM_EMAIL,
#                 ['admin@example.com'],  # TODO: Replace with the admin's email address
#                 fail_silently=False,
#             )
#             # Send email to the user
#             send_mail(
#                 'Signup Successful - Approval Pending',
#                 f'Thank you for signing up, {user.username}. Your account is currently pending approval by an admin. You will be notified once your account is approved.',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [user.email],  # TODO: Send to the user's email address
#                 fail_silently=False,
#             )
#             return redirect('signup_success')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})


# Set up logging
logger = logging.getLogger(__name__)

@require_POST
def team_register(request):
    try:
        data = json.loads(request.body)
        data = convert_keys_to_snake_case(data)
        race_id = data['race_id']
        registration_data = data['registration_data']
        team_data = registration_data.get('team_data', {})
        # Calculate the amount based on the race price
        try:
            race = Race.objects.get(id=race_id)
            race_name = race.name
            amount = race.price
        except Race.DoesNotExist:
            logger.error("Race not found.")
            return JsonResponse({'error': "Race not found."}, status=404)
        print(data)
        payment_intent_id = data['payment_intent_id']
         # Retrieve the PaymentIntent to confirm payment
        intent, error = retrieve_payment_intent(payment_intent_id, race)
        if error:
            logger.error(f"Error retrieving PaymentIntent: {error}")
            return JsonResponse({'error': 'Payment not confirmed.'}, status=400)

        race_price = int(race.price * 100)

        # Confirm payment intent status and amount received
        if intent.status != 'succeeded':
            logger.error("Payment not confirmed.")
            return JsonResponse({'error': 'Payment not confirmed.'}, status=400)

        if intent.amount_received != race_price:
            logger.error("Mismatch payment")
            return JsonResponse({'error': 'Payment amount does not match the race price.'}, status=400)

        # add unique paymentIntent field to registration

        with transaction.atomic():
            try: 
                print(registration_data)
                registration = Registration.objects.create(
                    race=race,
                    payment_intent_id=payment_intent_id,
                    amount_paid=intent.amount_received,
                    first_name=registration_data['first_name'],
                    last_name=registration_data['last_name'],
                    email=registration_data['email'],
                    # phone=registration_data.get('phone', ''),
                    gender=registration_data['gender'],
                    dob=registration_data['date_of_birth'],
                    waiver_text=race.event.waiver_text,
                    ip_address=registration_data['ip_address'],
                    # minor=registration_data['minor'],
                    # parent_guardian_name=registration_data.get('parentGuardianName', ''),
                    # parent_guardian_signature=registration_data.get('parentGuardianSignature', ''),
                )
                emails = team_data.get('emails', {})  # includes leg order
                if len(emails) != race.num_runners:
                    return JsonResponse({'error': f'The number of emails must be equal to {race.num_runners}.'}, status=400)
                team = Team.objects.create(
                    name=team_data['name'],
                    race=race,
                    projected_team_time=team_data['projected_team_time'],
                    captain=registration,
                )
                team_name = team.name
                # Create TeamMember instances
                for member in emails:
                    team_member = TeamMember.objects.create(
                        team=team,
                        email=member['email'],
                        leg_order=member['leg_order'],
                    )
                    # for team captain, connect their registration to the team member (if the registration email is part of the team)
                    if member['email'] and member['email'].lower() == registration.email:
                        registration.member = team_member
                        registration.save()
                        print(f"Connected registration {registration.id} to team member {team_member.email}")

                registrant_name = f"{registration_data['first_name']} {registration_data['last_name']}"
                response_data = {
                    'payment_data': {
                        'amount': intent.amount_received,
                        'receipt_email': intent.receipt_email,
                    },
                    'registration_data': {
                        'name': registration.first_name + " " + registration.last_name,
                        'email': registration.email,
                        'confirmation_code': registration.confirmation_code,
                    },
                    'race_data': {
                        'name': race.name,
                        'time': f"{race.hour:02}:{race.minute:02} {race.time_indicator}",
                        'date': race.date,
                        'description': race.description,
                        'event': race.event.name,
                        'contact': race.event.email,
                        'address': race.event.address,
                        'city': race.event.city,
                        'state': race.event.state,
                        'website_url': race.event.website_url,
                        'instagram_url': race.event.instagram_url,
                    },
                    'team_data': {
                        'race': race.name,
                        'date': race.date,
                        'projected_team_time': team.projected_team_time,
                        'name': team.name,
                        'emails': [{'email': member.email, 'leg_order': member.leg_order} for member in team.members.all()],
                    }
                }
                # Convert response data keys to camelCase
                response_data = convert_keys_to_camel_case(response_data)
                return JsonResponse(response_data)
            except Exception as e:
                logger.error(f"Error during transaction: {str(e)}")
                raise
    except json.JSONDecodeError as e:
        print(e)
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': "Invalid JSON data."}, status=400)
    except Exception as e:
        print(e)
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': "An unexpected error occurred."}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_POST
def event_register(request, url_alias):
    try:
        data = json.loads(request.body)
        data = convert_keys_to_snake_case(data)
        event_id = data['event_id']
        
        registration_data = data['registration_data']
        try:
            event = Event.objects.get(id=event_id)
            event_name = event.name
        except Event.DoesNotExist:
            logger.error("Event not found.")
            return JsonResponse({'error': "Event not found."}, status=404)
        with transaction.atomic():
            try: 
                registration = Registration.objects.create(
                    event=event,
                    first_name=registration_data['first_name'],
                    last_name=registration_data['last_name'],
                    email=registration_data['email'],
                    gender=registration_data['gender'],
                    dob=registration_data['date_of_birth'],
                    waiver_text=event.waiver_text,
                    ip_address=registration_data['ip_address'],
                )
                registrant_name = f"{registration_data['first_name']} {registration_data['last_name']}"
                response_data = {
                    'registration_response_data': {
                        'name': registration.first_name + " " + registration.last_name,
                        'email': registration.email,
                        'confirmation_code': registration.confirmation_code,
                    },
                    'event_data': {
                        'name': event.name,
                        'date': event.date,
                        'description': event.description,
                        'event': event.name,
                        'contact': event.email,
                        'address': event.address,
                        'city': event.city,
                        'state': event.state,
                        'website_url': event.website_url,
                        'instagram_url': event.instagram_url,
                    },
                }
                # Convert response data keys to camelCase
                response_data = convert_keys_to_camel_case(response_data)
                return JsonResponse(response_data)
            except Exception as e:
                logger.error(f"Error during transaction: {str(e)}")
                raise
    except json.JSONDecodeError as e:
        print(e)
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': "Invalid JSON data."}, status=400)
    except Exception as e:
        print(e)
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': "An unexpected error occurred."}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_POST
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        data = convert_keys_to_snake_case(data)
        race_id = data['race_id']
        currency = 'usd'

        # Calculate the amount based on the race price
        try:
            race = Race.objects.get(id=race_id)
        except Race.DoesNotExist:
            logger.error("Race not found.")
            return JsonResponse({'error': "Race not found."}, status=404)
        amount = int(race.price * 100)  # Convert to cents
        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )
        return JsonResponse({
            'clientSecret': intent.client_secret,
            'id': intent.id,
            'amount': intent.amount,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)
