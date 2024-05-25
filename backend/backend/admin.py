# backend/backend/admin.py
from django.contrib import admin
from .models import UserProfile, Event, Race, RacePrice, Registration, TeamMember

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at', 'updated_at')
    search_fields = ('user__username', 'role')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name', 'created_by__user__username')

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance', 'custom_distance_value', 'custom_distance_unit', 'is_relay', 'num_runners', 'team_type', 'event', 'created_at', 'updated_at')
    search_fields = ('name', 'event__name', 'distance')

@admin.register(RacePrice)
class RacePriceAdmin(admin.ModelAdmin):
    list_display = ('race', 'price', 'effective_date')
    search_fields = ('race__name', 'price')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('race', 'anon_user_email', 'registered_at', 'amount_paid', 'created_at', 'updated_at')
    search_fields = ('anon_user_email', 'race__name')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'age', 'gender', 'registration')
    search_fields = ('name', 'email', 'registration__race__name')
