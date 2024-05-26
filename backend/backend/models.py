# backend/backend/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Document(models.Model):
    file = models.FileField(upload_to='event_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    
class PhotoPackage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.user.username

class Event(models.Model):

    STATE_CHOICES = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    ]

    name = models.CharField(max_length=200)
    date = models.DateField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='events')
    published = models.BooleanField(default=False)  # New field for published status

    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    google_maps_link = models.URLField(max_length=200, blank=True)
    media_file = models.FileField(upload_to='event_media/', blank=True, null=True)
    logo_or_branch_photo = models.ImageField(upload_to='event_logos/', blank=True, null=True)
    documents = models.ManyToManyField(Document, blank=True)

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

class CouponCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_uses = models.PositiveIntegerField(default=1)
    usage_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code
    
class PhotoPackage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Registration(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registrations')
    anon_user_email = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    photo_package = models.ForeignKey(PhotoPackage, null=True, blank=True, on_delete=models.SET_NULL)
    race_price = models.ForeignKey(RacePrice, on_delete=models.PROTECT)
    coupon_code = models.ForeignKey(CouponCode, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Set the price from the RacePrice model
        if not self.race_price:
            raise ValueError("Race price must be set.")

        # If coupon code is used, check its usage and apply discount
        if self.coupon_code and self._state.adding:
            if self.coupon_code.usage_count < self.coupon_code.max_uses:
                self.coupon_code.usage_count += 1
                self.coupon_code.save()
                discount = (self.coupon_code.discount_percentage / 100) * self.race_price.price
                self.amount_paid = self.race_price.price - discount
            else:
                raise ValueError("Coupon code has reached its maximum number of uses.")
        else:
            self.amount_paid = self.race_price.price

        super().save(*args, **kwargs)

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
