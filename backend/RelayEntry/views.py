from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import anonymous_required
from django.core.mail import send_mail
from django.core import signing
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q, Value, CharField, OuterRef, Subquery, Value
from django.db.models.functions import Concat
from django.http import JsonResponse
import os
import logging
import json
from .models import UserProfile, Event, Race, Registration, Team, TeamMember
from .serializers import EventSerializer, RaceSerializer, EventWithRacesSerializer, TeamResultSerializer, TeamSerializer, EventDashboardSerializer, RaceDashboardSerializer
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.db import transaction
from .utils.stripe_utils import retrieve_payment_intent 
import stripe
from .conversion import convert_keys_to_snake_case, convert_keys_to_camel_case
from datetime import timedelta
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.middleware.csrf import get_token
from decimal import Decimal
from django.utils.html import escape
from django.core.validators import validate_email, URLValidator
from .utils.email_utils import send_email, generate_token, send_team_edit_link
from django.core.cache import cache
from django.core.exceptions import ValidationError, ObjectDoesNotExist, PermissionDenied

from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from .permissions import IsUserApproved, IsObjectEventCreator

# Set up logging for Stripe
stripe_logger = logging.getLogger('stripe')

class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'

class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token is None:
                logger.error("Logout attempt without refresh token.")
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # This blacklists the token
            except Exception as e:
                logger.error(f"Invalid or expired refresh token: {refresh_token} - Error: {str(e)}")
                return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        email = request.user.email
        return JsonResponse({
            'message': f"",
            'username': username,
        })

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
#                 ['relayentry@gmail.com'],
#                 fail_silently=False,
#             )
#             # Send email to the user
#             send_mail(
#                 'Signup Successful - Approval Pending',
#                 f'Thank you for signing up, {user.username}. Your account is currently pending approval by an admin. You will be notified once your account is approved.',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [user.email],
#                 fail_silently=False,
#             )
#             return redirect('signup_success')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})

@require_POST
def team_register(request):
    try:
        data = json.loads(request.body)
        data = convert_keys_to_snake_case(data)
        race_id = data['race_id']
        registration_data = data['registration_data']
        if registration_data['email'] != registration_data['confirm_email']:
            logger.error(f"Confirm email error for team register: {registration_data['email']}")
            return JsonResponse({'error': 'Confirm email must match email.'}, status=400)
        team_data = registration_data.get('team_data', {})
        # Calculate the amount based on the race price
        try:
            race = Race.objects.get(id=race_id)
            if race.registration_closed:
                return JsonResponse({'error': "Race registration is closed"}, status=403)
            race_name = race.name
            amount = race.price
        except Race.DoesNotExist:
            logger.error("Race not found.")
            return JsonResponse({'error': "Race not found."}, status=404)
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
        # Assuming `intent` is the payment intent object from Stripe
        amount_received_cents = intent['amount_received']

        minor_value = registration_data['minor']
        minor = False
        if minor_value in ['true', 'True', True]:
            minor = True

        # Convert from cents to dollars (or the base unit of your currency)
        amount_received_dollars = Decimal(amount_received_cents) / 100
        with transaction.atomic():
            try: 
                registration = Registration.objects.create(
                    race=race,
                    payment_intent_id=payment_intent_id,
                    amount_paid=amount_received_dollars,
                    first_name=registration_data['first_name'],
                    last_name=registration_data['last_name'],
                    email=registration_data['email'],
                    phone=registration_data.get('phone', ''),
                    gender=registration_data['gender'],
                    dob=registration_data['date_of_birth'],
                    waiver_text=race.event.waiver_text,
                    ip_address=registration_data['ip_address'],
                    minor=minor,
                    parent_guardian_name=registration_data.get('parent_guardian_name', ''),
                    parent_guardian_signature=registration_data.get('parent_guardian_signature', ''),
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
                        logger.info(f"Connected registration {registration.id} to team member {team_member.email}")

                registrant_name = f"{registration_data['first_name']} {registration_data['last_name']}"
                response_data = {
                    'payment_data': {
                        'amount': registration.amount_paid,
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
                transaction.on_commit(lambda: logger.info(f'Team created: {team.id} for race: {race.id}'))
                return JsonResponse(response_data)
            except Exception as e:
                logger.error(f"Error during transaction: {str(e)}")
                raise
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': "Invalid JSON data."}, status=400)
    except ValidationError as e:
        error_message = str(e)
        logger.error(f"ValidationError error: {str(e)}")
        return JsonResponse({"error": error_message}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': f"An unexpected error occurred"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_POST
def event_register(request, url_alias):
    try:
        data = json.loads(request.body)
        data = convert_keys_to_snake_case(data)
        event_id = data['event_id']
        
        registration_data = data['registration_data']
        if registration_data['email'] != registration_data['confirm_email']:
            logger.error(f"Confirm email error for team register: {registration_data['email']}")
            return JsonResponse({'error': 'Confirm email must match email.'}, status=400)
        race_id = registration_data['selected_race']
        try:
            event = Event.objects.get(id=event_id)
            event_name = event.name
            if event.registration_closed:
                return JsonResponse({'error': "Event registration is closed"}, status=403)
        except Event.DoesNotExist:
            logger.error("Event not found.")
            return JsonResponse({'error': "Event not found."}, status=404)
        
        try:
            race = Race.objects.get(id=race_id)
            if race.registration_closed:
                return JsonResponse({'error': "Race registration is closed"}, status=403)
            race_name = race.name
        except Race.DoesNotExist:
            logger.error("Race not found.")
            return JsonResponse({'error': "Race not found."}, status=404)
        
        minor_value = registration_data['minor']
        minor = False
        if minor_value in ['true', 'True', True]:
            minor = True
        
        with transaction.atomic():
            try: 
                registration = Registration.objects.create(
                    race=race,
                    first_name=registration_data['first_name'],
                    last_name=registration_data['last_name'],
                    email=registration_data['email'],
                    gender=registration_data['gender'],
                    dob=registration_data['date_of_birth'],
                    waiver_text=event.waiver_text,
                    ip_address=registration_data['ip_address'],
                    minor=minor,
                    parent_guardian_name=registration_data.get('parent_guardian_name', ''),
                    parent_guardian_signature=registration_data.get('parent_guardian_signature', ''),
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
                transaction.on_commit(lambda: logger.info(f'Registration : {registration.id} for race: {race.id}'))
                return JsonResponse(response_data)
            except Exception as e:
                logger.error(f"Error during transaction: {str(e)}")
                raise
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': "Invalid JSON data."}, status=400)
    except ValidationError as e:
        error_message = str(e)
        logger.error(f"ValidationError error: {str(e)}")
        return JsonResponse({"error": error_message}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': "Unexpected error"}, status=400)

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
            if race.registration_closed:
                return JsonResponse({'error': "Race registration is closed"}, status=403)
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
        stripe_logger.error(f"Failed to create Payment Intent: {e}")
        return JsonResponse({'error': "Failed to create Payment Intent"}, status=403)

@require_GET
def team_race_results(request, race_id):
    try:
        # Get the race or return 404 if not found
        try:
            race = Race.objects.get(id=race_id)
        except Race.DoesNotExist:
            logger.error("Race not found.")
            return JsonResponse({'error': "Race not found."}, status=404)
        
        # Get all teams for the race
        teams = Team.objects.filter(race=race).select_related('captain')
        
        # Serialize the data
        serializer = TeamResultSerializer(teams, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        logger.error(f"Failure to get Team Relay Race results: {str(e)}")
        return JsonResponse({'error': "Failure to get Team Relay Race results"}, status=403)

@require_POST
def contact(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    # List of required fields
    required_fields = ['name', 'email', 'role', 'message', 'ip']
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return JsonResponse({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=400)

    name = escape(str(data.get('name', '')).strip())
    email = str(data.get('email', '')).strip()
    role = escape(str(data.get('role', '')).strip())
    message = escape(str(data.get('message', '')).strip())
    ip = escape(str(data.get('ip', '')).strip())
    confirmation = escape(str(data.get('confirmation', '')).strip())
    honey = str(data.get('honey', '')).strip()

    if not ip:
        return JsonResponse({'error':'Could not determine your IP address.'}, status=400)
    if honey:  # If honeypot is filled, likely a bot
        return JsonResponse({'error': 'Spam detected'}, status=400)
    
    request_count = cache.get(ip, 0)
    # Limit to 2 requests per 24hrs per IP address
    if request_count >= 2:
        return JsonResponse({'error': 'Too many requests.'}, status=429)
    
    # Increment the request count
    cache.set(ip, request_count + 1, timeout=86400)  # 86400 seconds = 24 hours
        # Validate that confirmation number is provided if role is 'Registrant'
    if role == 'Registrant' and not confirmation:
        return JsonResponse({'error': 'Confirmation number is required for Registrants.'}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'error': 'Invalid email address'}, status=400)

    # Compose the email content
    subject = f"New Contact Form Submission from {name}"
    text_part = f"""
    Name: {name}
    Email: {email}
    Role: {role}
    Message: {message}
    IP: {ip}
    Confirmation: {confirmation}
    """
    html_part = f"""
    <h3>New Contact Form Submission</h3>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Role:</strong> {role}</p>
    <p><strong>Message:</strong> {message}</p>
    <p><strong>IP:</strong> {ip}</p>
    <p><strong>Confirmation:</strong> {confirmation}</p>
    """
    if send_email(
        recipient_email=settings.CONTACT_EMAIL,
        recipient_name="RelayEntry",
        subject=subject,
        text_part=text_part,
        html_part=html_part
    ):
        return JsonResponse({'status': 'success', 'message': 'Your message has been sent successfully!'})
    else:
        return JsonResponse({'error': 'Failed to send your message. Please try again later.'}, status=500)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    expected_events = ['payment_intent.succeeded', 'payment_intent.failed']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        stripe_logger.error(f"Invalid payload: {e}")
        return JsonResponse({'error': 'Invalid request'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        stripe_logger.error(f"Invalid signature: {e}")
        return JsonResponse({'error': 'Invalid request'}, status=400)
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        # Find the corresponding registration
        try:
            with transaction.atomic():
                # Find the corresponding registration
                registration = Registration.objects.get(payment_intent_id=payment_intent['id'])
                if not registration.paid:
                    registration.paid = True
                    registration.save()

                # Log the successful payment and registration update
                stripe_logger.info(f"Payment Successful: PaymentIntent ID: {payment_intent['id']}, Amount: {payment_intent['amount']}, Customer: {payment_intent['customer']}")
                stripe_logger.info(f"Registration Paid: Registration ID: {registration.id}, User: {registration.user}, Event: {registration.event}")
        except ObjectDoesNotExist:
            stripe_logger.error(f"Registration with intent_id {payment_intent['id']} does not exist.")
        except Exception as e:
            stripe_logger.error(f"An error occurred while processing payment intent {payment_intent['id']}: {e}")
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        stripe_logger.error(f"Payment Failed: {payment_intent['id']}")
        # Handle the payment method attached event
    # elif event['type'] == 'payment_method.attached':
    #     payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Handle the payment method attached event
    # Handle other event types
    else:
        stripe_logger.error(f"Unhandled event type {event['type']}")
    return JsonResponse({'status': 'success'}, status=200)

@require_POST
def request_edit_link(request, url_alias):
    try:
        data = json.loads(request.body)
        data = convert_keys_to_snake_case(data)
        event_id = data['event_id']
        email = data['email']
        # Filter teams by event and captain's email
        team = Team.objects.filter(
            race__event__url_alias=url_alias,
            race__event__id=event_id,
            captain__email=email
        ).first()
        token = generate_token(team.id, team.captain.email)
        send_team_edit_link(team)
    except Team.DoesNotExist:
        pass  # Do nothing, continue to return the generic response

    # Always return the same generic response
    return JsonResponse({'message': 'If your email is associated with a team, an email has been sent with the link to edit your team.'})

@require_GET
def get_team_data(request, token):
    try:
        # Validate the token and extract the data
        data = signing.loads(token, max_age=timedelta(minutes=30))
        team_id = data['team_id']
        email = data['email']

        # Retrieve the team and its members
        team = Team.objects.get(id=team_id, captain__email=email)
        event = team.race.event
        team_data = {
            'name': team.name,
            'projected_team_time_choices': team.race.projected_team_time_choices,
            'projected_team_time': team.projected_team_time,
            'members': list(team.members.values('email', 'leg_order')),
        }
        event_data = {
            'name': event.name,
            'date': event.date,
            'end_date': event.end_date,
            'url_alias': event.url_alias,
            'address': event.address,
            'city': event.city,
            'state': event.state,
            'postal_code': event.postal_code,
            'facebook_url': event.facebook_url,
            'twitter_url': event.twitter_url,
            'email': event.email,
            'website_url': event.website_url,
        }

        return JsonResponse({'team': team_data, 'event': event_data})

    except (Team.DoesNotExist, signing.SignatureExpired, signing.BadSignature):
        return JsonResponse({'error': 'Invalid or expired token'}, status=400)

@require_http_methods(["PUT"])
def verify_token_and_update_team(request, token):
    try:
        # Validate the token and extract data
        token_data = signing.loads(token, max_age=timedelta(minutes=30))  # Token expires in 30 minutes
        team_id = token_data['team_id']
        email = token_data['email']
        with transaction.atomic():
            team = Team.objects.select_for_update().get(id=team_id, captain__email=email)
            # Parse the request body
            data = json.loads(request.body)
            data = convert_keys_to_snake_case(data)
            # Update team fields
            team_changed = False
            if data.get('name') and data.get('name') != team.name:
                team.name = data.get('name', team.name)
                team_changed = True
            if data.get('projected_team_time') and data.get('projected_team_time') != team.projected_team_time:
                team.projected_team_time = data.get('projected_team_time', team.projected_team_time)
                team_changed = True
            if team_changed:
                team.save()
            # Update members
            members_data = data.get('members', [])
            existing_members = {member.email: member for member in team.members.all()}
            for member_data in members_data:
                email = member_data['email'].lower()  # Normalize email
                leg_order = member_data['leg_order']
                if email in existing_members:
                    # Update existing member
                    member = existing_members.pop(email)
                    if leg_order != member.leg_order:
                        member.leg_order = leg_order
                        member.save()
                else:
                    # Create a new member
                    TeamMember.objects.create(team=team, email=email, leg_order=leg_order)
            # Delete members that are no longer in the list
            for member in existing_members.values():
                member.delete()
            logger.info(f"Team Updated: {team.id}")
            return JsonResponse({'message': 'Team updated successfully'})
    except (Team.DoesNotExist, signing.SignatureExpired, signing.BadSignature):
        return JsonResponse({'error': 'Invalid or expired token'}, status=400)
    except ValueError as ve:
        logger.error(f"ValueError when editing team: {str(ve)}")
        return JsonResponse({'error': str(ve)}, status=400)
    except ValidationError as e:
        error_message = str(e)
        logger.error(f"Error when editing team: {str(e)}")
        return JsonResponse({"error": error_message}, status=400)
    except Exception as e:
        logger.error(f"Error when editing team: {str(e)}")
        return JsonResponse({'error': "Unexpected error when editing team"}, status=500)

@require_GET
def confirm_registration(request, url_alias, name):
    name = name.strip()
    if len(name) < 3:
        return JsonResponse({
            'error': 'Input needs to be at least 3 characters long.'
        }, status=400)
    if name:
        registrations = Registration.objects.filter(
            race__event__url_alias=url_alias
        ).filter(
            Q(first_name__icontains=name) |  # Match on first name
            Q(last_name__icontains=name)  # Match on last name
        ).annotate(
            full_name=Concat(
                'first_name', 
                Value(' '), 
                'last_name',
                output_field=CharField()
            ),
            team_name=Subquery(
                Team.objects.filter(
                    members__registration=OuterRef('pk')  # Match the registration with the team members
                ).values('name')[:1],  # Get the team name if it exists
                output_field=CharField()
            )
        ).values('first_name', 'last_name', 'full_name', 'race__name', 'team_name')
        return JsonResponse(list(registrations), safe=False)
    
    return JsonResponse([], safe=False)

class EventCreateUpdateView(generics.GenericAPIView):
    serializer_class = EventDashboardSerializer
    permission_classes = [IsAuthenticated, IsUserApproved]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'id'

    def get_queryset(self):
        """
        This queryset is used to retrieve the events for updating.
        It filters the events based on the user.
        """
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Event.objects.filter(created_by=user_profile)

    def create(self, request, *args, **kwargs):
        """
        Handles event creation logic.
        """
        user_profile = UserProfile.objects.get(user=self.request.user)

        # Ensure the user is approved to create events
        if not user_profile.is_approved:
            raise PermissionDenied("You are not approved to create events.")
        
        # Perform the creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=user_profile)

        # Customize response
        return Response({
            "message": "Event created successfully!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Handles event update logic.
        """
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Event updated successfully!",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Direct POST requests to the create method.
        """
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Allow partial updates using PATCH.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class UserEventView(generics.GenericAPIView):
    serializer_class = EventWithRacesSerializer
    permission_classes = [IsAuthenticated, IsUserApproved]

    def get_queryset(self):
        """
        Returns the queryset for the events created by the user.
        If 'id' is provided, filters the queryset to retrieve a specific event.
        """
        user_profile = UserProfile.objects.get(user=self.request.user)

        if 'id' in self.kwargs:
            # If retrieving a single event, ensure it belongs to the user
            return Event.objects.filter(id=self.kwargs['id'], created_by=user_profile)

        # If no id is provided, return all events created by the user
        return Event.objects.filter(created_by=user_profile)

    def get(self, request, *args, **kwargs):
        """
        Handles both retrieving a single event and listing events.
        """
        if 'id' in self.kwargs:
            # Retrieve a specific event if 'id' is in the URL
            event = self.get_queryset().first()
            if not event:
                raise PermissionDenied("You do not have permission to view this event.")
            serializer = self.get_serializer(event)
            return Response(serializer.data)
        else:
            # List all events created by the user
            events = self.get_queryset()
            serializer = self.get_serializer(events, many=True)
            return Response(serializer.data)

# this shit needs to be examined
class RaceCreateUpdateView(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    serializer_class = RaceDashboardSerializer
    permission_classes = [IsAuthenticated, IsUserApproved, IsObjectEventCreator]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'id'

    def get_queryset(self):
        """
        Retrieve queryset for the races. 
        If updating, ensure race belongs to an event created by the user.
        """
        user_profile = UserProfile.objects.get(user=self.request.user)

        if 'id' in self.kwargs:
            # When updating, we check if the race's event was created by the user
            return Race.objects.filter(event__created_by=user_profile)
        return None

    def get_object(self):
        """
        When updating, ensure the race belongs to an event created by the user.
        """
        obj = super().get_object()
        user_profile = UserProfile.objects.get(user=self.request.user)

        if obj.event.created_by != user_profile:
            raise PermissionDenied("You are not allowed to update this race.")

        return obj

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        """
        When creating, ensure the user is approved and save the race with the user's profile.
        """
        user_profile = UserProfile.objects.get(user=self.request.user)

        if not user_profile.is_approved:
            raise PermissionDenied("You are not approved to create races.")

        # Save the race with the created_by field set to the user's profile
        serializer.save(created_by=user_profile)

    def create(self, request, *args, **kwargs):
        """
        Customize the response after creating a race.
        """
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Race created successfully!",
            "data": response.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Handles event update logic.
        """
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Race updated successfully!",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Direct POST requests to the create method.
        """
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Allow partial updates using PATCH.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

# get single / all races for a user
class UserRacesView(generics.GenericAPIView):
    serializer_class = RaceDashboardSerializer
    permission_classes = [IsAuthenticated, IsUserApproved, IsObjectEventCreator]

    def get_queryset(self):
        """
        Returns a queryset of races based on the presence of event_id in the URL.
        If event_id is present, it fetches all races for that event.
        Otherwise, it assumes the user is fetching a single race by id.
        """
        user_profile = UserProfile.objects.get(user=self.request.user)

        # Check if event_id is in the URL for retrieving races by event
        event_id = self.kwargs.get('event_id', None)
        if event_id:
            # Fetch all races for a specific event
            try:
                event = Event.objects.get(id=event_id, created_by=user_profile)
            except Event.DoesNotExist:
                raise PermissionDenied("You do not have permission to view races for this event.")
            return Race.objects.filter(event=event)

        # If no event_id, fetch by race id
        race_id = self.kwargs.get('id', None)
        if race_id:
            try:
                race = Race.objects.get(id=race_id, event__created_by=user_profile)
            except Race.DoesNotExist:
                raise PermissionDenied("You are not allowed to view this race.")
            return Race.objects.filter(id=race_id)
        else:
            raise PermissionDenied("Race ID or Event ID is required.")

    def get(self, request, *args, **kwargs):
        """
        Handles both retrieving a single race and listing races for an event.
        """
        queryset = self.get_queryset()

        # Check if we are retrieving a single race or a list of races
        if 'id' in self.kwargs:
            # Single race retrieval
            race = queryset.first()  # We are filtering by id, so this should be a single race
            serializer = self.get_serializer(race)
        else:
            # List of races for a specific event
            serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)