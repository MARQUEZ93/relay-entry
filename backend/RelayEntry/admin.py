from django.contrib import admin
from .models import UserProfile, Team, Event, Race, Registration, TeamMember, PhotoPackage, CouponCode, Leg
from django.contrib.auth.models import User, Group

from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .forms import RaceAdminForm

# Customize the admin site header
admin.site.site_header = "RelayEntry Administration"
admin.site.site_title = "RelayEntry Admin Portal"
admin.site.index_title = "Welcome to RelayEntry Admin"

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('username',)

class CustomGroupAdmin(admin.ModelAdmin):
    pass

class CustomUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(UserProfile, CustomUserProfileAdmin)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date', 'created_at', 'updated_at', 'url_alias', 'event_url', )
    search_fields = ('name',)
    prepopulated_fields = {"url_alias": ("name",)}

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def event_url(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.get_event_url(), obj.get_event_url())
    event_url.short_description = 'Event URL'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    form = RaceAdminForm
    list_display = ('name', 'date', 'description', 'distance', 'price', 'custom_distance_value', 'custom_distance_unit', 'is_relay', 'num_runners', 'team_type', 'same_distance', 'event', 'created_at', 'updated_at', 'course_map', 'hour', 'minute', 'time_indicator','projected_team_time_choices',)
    search_fields = ('name', 'event__name', 'distance',)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'race', 'first_name', 'last_name', 'email', 'amount_paid', 'created_at', 'updated_at', 'ip_address', 'parent_guardian_name', 'minor')
    search_fields = ('email', 'event__name', 'race__name')
    
class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1  # Number of extra forms to display
    
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'projected_team_time', 'race_name',)
    search_fields = ('name', 'race__name',)
    inlines = [TeamMemberInline]

    def race_name(self, obj):
        return obj.race.name


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('email', 'team', 'leg_order', 'race_name', 'registration_info')
    search_fields = ('email', 'team__name', 'team__race__name')
    list_filter = ('team__race__name',)
    ordering = ('team', 'leg_order')

    def race_name(self, obj):
        return obj.team.race.name
    
    def registration_info(self, obj):
        registration = Registration.objects.filter(member=obj).first()
        if registration:
            return f"Registration ID: {registration.id} - Email: {registration.email}"
        return "No Registration"
    
    registration_info.short_description = 'Registration'
    race_name.short_description = 'Race'