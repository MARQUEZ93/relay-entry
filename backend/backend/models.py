# backend/backend/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.user.username

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='events')
    published = models.BooleanField(default=False)  # New field for published status

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

    MILES = 'mi'
    KILOMETERS = 'km'

    UNIT_CHOICES = [
        (MILES, 'Miles'),
        (KILOMETERS, 'Kilometers'),
    ]

    MALE = 'Male'
    FEMALE = 'Female'
    MIXED = 'Mixed'
    COED = 'Coed'

    TEAM_TYPE_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (MIXED, 'Mixed'),
        (COED, 'Coed'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='races')
    name = models.CharField(max_length=200)
    distance = models.CharField(max_length=50, choices=DISTANCE_CHOICES)
    custom_distance_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    custom_distance_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, blank=True, null=True)
    is_relay = models.BooleanField(default=False)
    num_runners = models.PositiveIntegerField(blank=True, null=True)
    team_type = models.CharField(max_length=10, choices=TEAM_TYPE_CHOICES, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.distance in [self.CUSTOM, self.ULTRA_MARATHON]:
            return f'{self.name} ({self.custom_distance_value} {self.get_custom_distance_unit_display()}) - {self.event.name}'
        return f'{self.name} ({self.get_distance_display()}) - {self.event.name}'

    def save(self, *args, **kwargs):
        if self.distance == self.ULTRA_MARATHON and not self.custom_distance_value:
            raise ValueError('Ultra Marathon requires a custom distance value.')
        if self.distance == self.CUSTOM and not self.custom_distance_value:
            raise ValueError('Custom distance requires a custom distance value.')
        if self.is_relay and not self.num_runners:
            raise ValueError('Relay race requires the number of runners.')
        super().save(*args, **kwargs)

    def get_current_price(self):
        today = timezone.now().date()
        prices = self.raceprice_set.filter(effective_date__lte=today).order_by('-effective_date')
        if prices.exists():
            return prices.first().price
        return None

class RacePrice(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    effective_date = models.DateField()

    class Meta:
        unique_together = ('race', 'effective_date')

    def __str__(self):
        return f'{self.race.name} - {self.price} effective from {self.effective_date}'

class Registration(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registrations')
    anon_user_email = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)  # Default value added

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.anon_user_email} - {self.race.name}'

class TeamMember(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.email}) - {self.registration.race.name}'
