from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from .constants import STATES, TEAM_GENDER_CHOICES, GENDER_CHOICES, UNIT_CHOICES_CONSTANT, AM, PM, TIME_INDICATORS, HOURS, MINUTES
import uuid
from zoneinfo import ZoneInfo
from django.contrib.postgres.fields import ArrayField
import os
from django.conf import settings

from django.utils.text import slugify

UNIT_CHOICES = UNIT_CHOICES_CONSTANT
TEAM_TYPE_CHOICES = TEAM_GENDER_CHOICES

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False, help_text="Whether user is approved to create content.")

    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_account_verified = models.BooleanField(default=False)
    
class Event(models.Model):

    STATE_CHOICES = STATES

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Only if the event spans multiple days. Must be after the date field.")
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    published = models.BooleanField(default=False, help_text="Whether the event can be viewed by the public.")

    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    google_maps_link = models.URLField(max_length=200, blank=True, null=True)
    google_maps_html = models.TextField(blank=True, null=True, help_text="Embed HTML for the Google Maps location. You can get this from the 'Embed a map' section of the Google Maps share options.")
    media_file = models.FileField(upload_to='event_media/', blank=True, null=True)
    logo = models.ImageField(upload_to='event_logos/', blank=True, null=True)

    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    website_url = models.URLField(max_length=200, blank=True, null=True)

    waiver_text = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    url_alias = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def get_event_url(self):
        ui_base_url = settings.WWW_HOST
        return f"{ui_base_url}/events/{self.url_alias}"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        if not self.url_alias:
            self.url_alias = slugify(self.name)
        super().save(*args, **kwargs)

class PhotoPackage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='photo_packages',
                              help_text="Which event the photo package is associated with.")

    def __str__(self):
        return self.name

class Race(models.Model):
    FIVE_K = '5K'
    TEN_K = '10K'
    HALF_MARATHON = 'Half Marathon'
    MARATHON = 'Marathon'
    ULTRA_MARATHON = 'Ultra Marathon'
    CUSTOM = 'Custom'

    DISTANCE_CHOICES = [
        (FIVE_K, '5K'),
        (TEN_K, '10K'),
        (HALF_MARATHON, 'Half Marathon'),
        (MARATHON, 'Marathon'),
        (ULTRA_MARATHON, 'Ultra Marathon'),
        (CUSTOM, 'Custom'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='races', 
                              help_text="The event you created that this race belongs to.")
    name = models.CharField(max_length=200)
    date = models.DateField(help_text="The day of the race.")
    description = models.TextField(null=True, blank=True)
    distance = models.CharField(max_length=50, choices=DISTANCE_CHOICES)
    custom_distance_value = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, help_text="If each leg is the same distance, put that distance here. Otherwise put the total distance (if legs differ in distance.)")
    custom_distance_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, blank=True, null=True)
    is_relay = models.BooleanField(default=False, help_text="Is the race a team relay race?")
    num_runners = models.PositiveIntegerField(blank=True, null=True, help_text="The amount of runners per team in a relay race.")
    team_type = models.CharField(max_length=10, choices=TEAM_TYPE_CHOICES, blank=True, null=True)

    same_distance = models.BooleanField(default=False, help_text="Whether each leg of the team relay race is the same distance.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="The price of registration before a discount may or may not have been applied.")

    course_map = models.FileField(upload_to='race_course_maps/', blank=True, null=True)
    hour = models.IntegerField(
        choices=HOURS,
        default=7,
    )
    minute = models.IntegerField(
        choices=MINUTES,
        default=0,
    )
    time_indicator = models.CharField(
        max_length=2,
        choices=TIME_INDICATORS,
        default=AM,
    )

    projected_team_time_choices = ArrayField(models.CharField(max_length=50), blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.event.name}'

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure all validations are checked
        super().save(*args, **kwargs)

    def clean(self):
        if self.distance in [self.ULTRA_MARATHON, self.CUSTOM] and not self.custom_distance_value:
            raise ValidationError('Custom distance requires a custom distance value.')
        if self.is_relay and not self.num_runners:
            raise ValidationError('Relay race requires the number of runners.')
        super().clean()

    class Meta:
        ordering = ['name', 'event__name']

class CouponCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    valid_until = models.DateTimeField(help_text="When the coupon code expires.")
    is_active = models.BooleanField(default=True)
    max_uses = models.PositiveIntegerField(default=1, help_text="Max number of times the coupon code can be used.")
    usage_count = models.PositiveIntegerField(default=0, help_text="The amount of times the coupon code has been used.")
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='coupon_codes')

    def __str__(self):
        return self.code
    
class Team(models.Model):
    name = models.CharField(max_length=255)
    captain = models.ForeignKey('Registration', null=True, blank=True, on_delete=models.SET_NULL, related_name='captained_teams')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='teams')
    projected_team_time = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} - {self.race.name}'
    
    def save(self, *args, **kwargs):
        base_name = self.name
        counter = 1

        # Check for other teams with the same name in the same race, excluding the current instance if it's an update
        while Team.objects.filter(race=self.race, name=self.name).exclude(pk=self.pk).exists():
            self.name = f"{base_name}_{counter}"
            counter += 1

        super().save(*args, **kwargs)

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    email = models.EmailField()
    leg_order = models.PositiveIntegerField()
    # leg = models.OneToOneField(Leg, related_name='teammember', on_delete=models.CASCADE, null=True, blank=True, help_text="The leg the team member is running (if applicable).")
    def __str__(self):
        return f'{self.email} - {self.team.name} - {self.team.race.name}'
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
    
class Registration(models.Model):
    payment_intent_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    confirmation_code = models.CharField(max_length=16, unique=True, editable=False)  # Increased length to 16
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registrations')
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="The price of registration before a discount may or may not have been applied.")
    email = models.EmailField()
    dob = models.DateField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    photo_package = models.ForeignKey(PhotoPackage, null=True, blank=True, on_delete=models.SET_NULL)
    coupon_code = models.ForeignKey(CouponCode, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)

    first_name = models.CharField(max_length=255, help_text="First name of the participant")
    last_name = models.CharField(max_length=255, help_text="Last name of the participant")
    waiver_text = models.TextField()  # Store the waiver text at the time of registration
    signed_at = models.DateTimeField(auto_now_add=True)

    parent_guardian_name = models.CharField(max_length=255, blank=True, null=True)
    parent_guardian_signature = models.TextField(blank=True, null=True)  # Assuming signature can be stored as text
    minor = models.BooleanField(default=False, help_text="Parent/Guardian for Minors (Under 18 years old)")

    def clean(self):
        # Check if a registration with the same email and race already exists
        # if Registration.objects.filter(race=self.race, email=self.email).exists():
        #     raise ValidationError('A registration with this email for the same race already exists.')
        # if self.coupon_code and self._state.adding:
        #     if self.coupon_code.usage_count >= self.coupon_code.max_uses:
        #         raise ValidationError("Coupon code has reached its maximum number of uses.")
        super().clean()

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        # Generate confirmation code if not present
        if not self.confirmation_code:
            self.confirmation_code = uuid.uuid4().hex[:16]
        
        # ensure waiver text cannot be altered after the fact
        if self.pk is not None:
            original = Registration.objects.get(pk=self.pk)
            if original.waiver_text != self.waiver_text:
                raise ValidationError("You cannot change the value of this field.")


        # Validate minor fields
        # if self.minor and not (self.parent_guardian_name and self.parent_guardian_signature):
            # raise ValueError("Parent/Guardian name and signature are required for minors.")

        # Run full validation
        self.full_clean()

        # Set the price and handle coupon logic
        # if self.coupon_code and self._state.adding:
        #     discount = (self.coupon_code.percentage / 100) * self.price
        #     self.amount_paid = self.price - discount
        #     self.coupon_code.usage_count += 1
        #     self.coupon_code.save()
        # else:
        #     self.amount_paid = self.price

        super().save(*args, **kwargs)

    def __str__(self):
        if (self.race): 
            return f'{self.email} - {self.race.name}'
        elif (self.event):
            return f'{self.email} - {self.event.name}'
        return self.email


class Leg(models.Model):
    race = models.ForeignKey(Race, related_name='legs', on_delete=models.CASCADE)
    leg_number = models.PositiveIntegerField()
    leg_map = models.FileField(upload_to='leg_maps/', blank=True, null=True)

    custom_distance_value = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    custom_distance_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, blank=True, null=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('race', 'leg_number')

    def __str__(self):
        return f"Leg {self.leg_number} - {self.distance}"