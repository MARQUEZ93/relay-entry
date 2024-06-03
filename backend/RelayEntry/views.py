from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import anonymous_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import stripe

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

stripe.api_key = settings.STRIPE_SECRET_KEY

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
