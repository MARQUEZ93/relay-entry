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
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from .payments import process_payment 
from .conversion import convert_keys_to_snake_case, convert_keys_to_camel_case

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

from django.views.decorators.csrf import csrf_exempt

# Set up logging
logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def team_register_and_pay(request):
    try:
        data = json.loads(request.body)
        data = convert_keys_to_snake_case(data)
        race_id = data['race_id']
        amount_from_ui = data['price']  # Extract and convert the amount to cents
        
        registration_data = data['registration_data']
        team_data = registration_data.get('team_data', {})
        billing_info = data['billing_info']
        payment_method = data['payment_method']
        payment_method_id = payment_method.get('id', {})
        # Calculate the amount based on the race price
        try:
            race = Race.objects.get(id=race_id)
            race_name = race.name
        except Race.DoesNotExist:
            logger.error("Race not found.")
            return JsonResponse({'error': "Race not found."}, status=404)
        amount_from_ui = int(float(amount_from_ui) * 100)
        amount_from_db = int(race.price * 100)  # Convert to cents
        # Validate price match
        if amount_from_ui != amount_from_db:
            logger.error("Price mismatch error.")
            return JsonResponse({'error': "Price mismatch. Please try again."}, status=400)

        with transaction.atomic():
            try: 
                registration = Registration.objects.create(
                    race=race,
                    amount_paid=amount_from_db,
                    first_name=registration_data['first_name'],
                    last_name=registration_data['last_name'],
                    email=registration_data['email'],
                    phone=registration_data.get('phone', ''),
                    gender=registration_data['gender'],
                    dob=registration_data['date_of_birth'],
                    waiver_text=race.event.waiver_text,
                    # ip_address=registration_data['ipAddress'],
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
                    TeamMember.objects.create(
                        team=team,
                        email=member['email'],
                        leg_order=member['leg_order'],
                    )

                registrant_name = f"{registration_data['first_name']} {registration_data['last_name']}"
                # Process the payment
                payment_result = process_payment(amount_from_db, payment_method_id, billing_info, race_name, registrant_name, team_name)
                print(payment_result)
                if 'status' in payment_result and payment_result['status'] != 'succeeded':
                    raise Exception(payment_result['message'])  # This will trigger a rollback
                response_data = {
                    'payment_data': {
                        'status': payment_result.status,
                        'amount': payment_result.amount,
                        'billing_info': billing_info
                    },
                    'registration_data': {
                        'first_name': registration.first_name,
                        'last_name': registration.last_name,
                        'gender': registration.gender,
                        'email': registration.email,
                        'confirmation_code': registration.confirmation_code,
                        'phone': registration.phone,
                        'dob': registration.dob,
                    },
                    'race_data': {
                        'name': race.name,
                        'date': race.date,
                        'description': race.description,
                        'event': race.event.name,
                        'contact': race.event.email,
                        'address': race.event.address,
                        'city': race.event.city,
                        'state': race.event.state,
                        'postal_code': race.event.postal_code,
                        'website_url': race.event.website_url,
                    },
                    # TODO: is team name fixed?
                    'team_data': {
                        'projected_team_pace': team.projected_team_time,
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
