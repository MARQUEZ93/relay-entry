from django.contrib import admin
from .models import UserProfile, Event, Race, Registration, TeamMember, Document, PhotoPackage, CouponCode

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__email',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name', 'created_by__user__email')

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance', 'custom_distance_value', 'custom_distance_unit', 'is_relay', 'num_runners', 'team_type', 'event', 'created_at', 'updated_at')
    search_fields = ('name', 'event__name', 'distance')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('race', 'anon_user_email', 'registered_at', 'amount_paid', 'created_at', 'updated_at')
    search_fields = ('anon_user_email', 'race__name')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'dob', 'gender', 'registration')
    search_fields = ('name', 'email', 'registration__race__name')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('file', 'name', 'required', 'uploaded_at')
    search_fields = ('file', 'name')

@admin.register(PhotoPackage)
class PhotoPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')

@admin.register(CouponCode)
class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'valid_until', 'is_active', 'max_uses', 'usage_count')
    search_fields = ('code',)
