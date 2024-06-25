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
    list_display = ('user', 'stripe_account_id', 'stripe_account_verified', 'connect_stripe_link')
    def connect_stripe_link(self, obj):
        url = reverse('connect_stripe')
        return format_html('<a href="{}">Connect Stripe</a>', url)

    connect_stripe_link.short_description = 'Connect Stripe'

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(UserProfile, CustomUserProfileAdmin)

class StaffUserPermissionsMixin:
    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff

class BaseOwnerAdmin(StaffUserPermissionsMixin, admin.ModelAdmin):
    exclude = ('created_by',)  # Hide created_by field in the form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            return qs.filter(created_by=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change or not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.created_by != request.user and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # When editing an existing object
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event":
            if not request.user.is_superuser:
                kwargs["queryset"] = Event.objects.filter(created_by=request.user)
            else:
                kwargs["queryset"] = Event.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Event)
class EventAdmin(BaseOwnerAdmin):
    list_display = ('name', 'description', 'date', 'created_by', 'created_at', 'updated_at', 'url_alias', 'event_url', )
    search_fields = ('name', 'created_by__email',)
    prepopulated_fields = {"url_alias": ("name",)}

    def event_url(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.get_event_url(), obj.get_event_url())
    event_url.short_description = 'Event URL'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Race)
class RaceAdmin(BaseOwnerAdmin):
    form = RaceAdminForm
    list_display = ('name', 'date', 'description', 'distance', 'price', 'custom_distance_value', 'custom_distance_unit', 'is_relay', 'num_runners', 'team_type', 'same_distance', 'event', 'created_at', 'updated_at', 'course_map', 'hour', 'minute', 'time_indicator','projected_team_time_choices',)
    search_fields = ('name', 'event__name', 'distance',)

    # the events dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event":
            kwargs["queryset"] = Event.objects.filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('race', 'first_name', 'last_name', 'email', 'amount_paid', 'created_at', 'updated_at', 'ip_address', 'parent_guardian_name', 'minor')
    search_fields = ('email', 'race__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            # Only show registrations for races created by the current user
            return qs.filter(race__created_by=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if obj and obj.race.created_by != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.race.created_by != request.user and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(PhotoPackage)
class PhotoPackageAdmin(BaseOwnerAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')

    #  the event dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event":
            kwargs["queryset"] = Event.objects.filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(CouponCode)
class CouponCodeAdmin(BaseOwnerAdmin):
    list_display = ('code', 'percentage', 'valid_until', 'is_active', 'max_uses', 'usage_count')
    search_fields = ('code',)

    #  the event dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event":
            kwargs["queryset"] = Event.objects.filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Usage count read-only
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('usage_count',)

@admin.register(Leg)
class LegAdmin(BaseOwnerAdmin):
    list_display = ('race', 'leg_number', 'custom_distance_value', 'custom_distance_unit', 'leg_map')
    search_fields = ('race__name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "race":
            kwargs["queryset"] = Race.objects.filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Team)
class TeamAdmin(BaseOwnerAdmin):
    list_display = ('name', 'projected_team_time',)
    search_fields = ('name', 'race__name',)