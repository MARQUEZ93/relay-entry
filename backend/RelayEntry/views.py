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

        race_id = data['race_id']
        amount_from_ui = data['price']  # Extract and convert the amount to cents
        
        registration_data = data['registration_data']
        team_data = data['team_data']
        payment_method = data['payment_method']

        payment_method_id = payment_method.id
        # Calculate the amount based on the race price
        try:
            race = Race.objects.get(id=race_id)
        except Race.DoesNotExist:
            logger.error("Race not found.")
            return JsonResponse({'error': "Race not found."}, status=404)
        
        amount_from_db = int(race.price * 100)  # Convert to cents
        
        # Validate price match
        if amount_from_ui != amount_from_db:
            logger.error("Price mismatch error.")
            return JsonResponse({'error': "Price mismatch. Please try again."}, status=400)

        with transaction.atomic():
            registration = Registration.objects.create(
                race=race,
                amount_paid=amount_from_db,
                first_name=racer_data['firstName'],
                last_name=racer_data['lastName'],
                email=racer_data['email'],
                phone=racer_data.get('phone', ''),
                gender=racer_data['gender'],
                dob=racer_data['dateOfBirth'],
                waiver_text=race.event.waiver_text,
                # ip_address=racer_data['ipAddress'],
                # minor=racer_data['minor'],
                # parent_guardian_name=racer_data.get('parentGuardianName', ''),
                # parent_guardian_signature=racer_data.get('parentGuardianSignature', ''),
            )
            member = TeamMember.objects.create(
                race=race,
                amount_paid=amount_from_db,
                registration=registration,
                email=racer_data['email'],
                waiver_text=race.event.waiver_text,
                # minor=racer_data['minor'],
                # parent_guardian_name=racer_data.get('parentGuardianName', ''),
                # parent_guardian_signature=racer_data.get('parentGuardianSignature', ''),
            )
            team = Team.objects.create(
                name=team_data['name'],
                race=race,
                expected_pace=team_data['expected_pace'],
                captain=member,
                emails=team_data['emails'],
                leg_order=team_data['leg_order'],
            )

             # Process the payment
            payment_result = process_payment(amount_from_db, payment_method_id, billing_info, race_name, racer_data, team.name)

            if 'status' in payment_result and payment_result['status'] != 'succeeded':
                raise Exception(payment_result['message'])  # This will trigger a rollback

            # Return client secret, confirmation code, race   r data, and race data
            return JsonResponse({
                'payment_intent': intent,
                'confirmation_code': registration.confirmation_code,
                'racer_data': {
                    first_name: registration.first_name,
                    last_name: registration.last_name,
                    email: registration.email,
                },
                'registration_data': {
                    'name': race.name,
                    'date': race.date,
                    'description': race.description,
                    'event': race.event.name,
                    'contact': race.event.email,
                },
                'team': {
                    'team_name': team.name,
                    'emails': team.emails,
                    'leg_order': team.leg_order,
                }
            })
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': "Invalid JSON data."}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': "An unexpected error occurred."}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
