from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from .constants import STATES, TEAM_GENDER_CHOICES, GENDER_CHOICES, UNIT_CHOICES_CONSTANT
import uuid

UNIT_CHOICES = UNIT_CHOICES_CONSTANT
TEAM_TYPE_CHOICES = TEAM_GENDER_CHOICES

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

class Document(models.Model):
    file = models.FileField(upload_to='event_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
    
class PhotoPackage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Event(models.Model):

    STATE_CHOICES = STATES

    name = models.CharField(max_length=200)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    published = models.BooleanField(default=False)

    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    google_maps_link = models.URLField(max_length=200, blank=True, null=True)
    media_file = models.FileField(upload_to='event_media/', blank=True, null=True)
    logo = models.ImageField(upload_to='event_logos/', blank=True, null=True)
    waivers = models.ManyToManyField(Document, blank=True)

    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    email_url = models.URLField(max_length=200, blank=True, null=True)
    website_url = models.URLField(max_length=200, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='races')
    name = models.CharField(max_length=200)
    distance = models.CharField(max_length=50, choices=DISTANCE_CHOICES)
    custom_distance_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    custom_distance_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, blank=True, null=True)
    is_relay = models.BooleanField(default=False)
    num_runners = models.PositiveIntegerField(blank=True, null=True)
    team_type = models.CharField(max_length=10, choices=TEAM_TYPE_CHOICES, blank=True, null=True)

    same_distance = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.distance in [self.CUSTOM, self.ULTRA_MARATHON]:
            return f'{self.name} ({self.custom_distance_value} {self.get_custom_distance_unit_display()}) - {self.event.name}'
        return f'{self.name} ({self.get_distance_display()}) - {self.event.name}'

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
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_uses = models.PositiveIntegerField(default=1)
    usage_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
    
class Team(models.Model):
    name = models.CharField(max_length=255)
    captain = models.ForeignKey('TeamMember', null=True, blank=True, on_delete=models.SET_NULL, related_name='captained_teams')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return f'{self.name} - {self.race.name}'
    
class Registration(models.Model):
    confirmation_code = models.CharField(max_length=16, unique=True, editable=False)  # Increased length to 16
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    email = models.EmailField()
    dob = models.DateField()

    photo_package = models.ForeignKey(PhotoPackage, null=True, blank=True, on_delete=models.SET_NULL)
    coupon_code = models.ForeignKey(CouponCode, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)

    def clean(self):
        if not self.price:
            raise ValidationError("Race price must be set.")
        if self.coupon_code and self._state.adding:
            if self.coupon_code.usage_count >= self.coupon_code.max_uses:
                raise ValidationError("Coupon code has reached its maximum number of uses.")
        if self.race.is_relay and not self.team:
            raise ValidationError('Relay race registration must be associated with a team.')
        super().clean()

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = str(uuid.uuid4()).replace('-', '')[:16]

        self.full_clean()  # Ensure all validations are checked

        # Set the price and handle coupon logic
        if self.coupon_code and self._state.adding:
            self.coupon_code.usage_count += 1
            self.coupon_code.save()
            discount = (self.coupon_code.percentage / 100) * self.price
            self.amount_paid = self.price - discount
        else:
            self.amount_paid = self.price

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.email} - {self.race.name}'

    class Meta:
        ordering = ['-registered_at']

class Leg(models.Model):
    race = models.ForeignKey(Race, related_name='legs', on_delete=models.CASCADE)
    leg_number = models.PositiveIntegerField()

    custom_distance_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    custom_distance_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, blank=True, null=True)

    class Meta:
        unique_together = ('race', 'leg_number')

    def __str__(self):
        return f"Leg {self.leg_number} - {self.distance}"

class TeamMember(models.Model):
    dob = models.DateField()
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    leg_order = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    leg = models.OneToOneField(Leg, related_name='teammember', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.name} ({self.email}) - {self.registration.race.name}'
