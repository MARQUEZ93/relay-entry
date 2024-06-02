from django.contrib import admin
from .models import UserProfile, Event, Race, Registration, TeamMember, Document, PhotoPackage, CouponCode, Leg
from django.contrib.auth.models import User, Group

from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
    list_display = ('user', 'is_approved')

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
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            return qs.filter(created_by=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change or not obj.created_by:
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

@admin.register(Event)
class EventAdmin(BaseOwnerAdmin):
    list_display = ('name', 'date', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name', 'created_by__user__email')

@admin.register(Race)
class RaceAdmin(BaseOwnerAdmin):
    list_display = ('name', 'distance', 'custom_distance_value', 'custom_distance_unit', 'is_relay', 'num_runners', 'team_type', 'event', 'created_at', 'updated_at')
    search_fields = ('name', 'event__name', 'distance')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('race', 'email', 'registered_at', 'amount_paid', 'created_at', 'updated_at')
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


@admin.register(Document)
class DocumentAdmin(BaseOwnerAdmin):
    list_display = ('file', 'name', 'uploaded_at')
    search_fields = ('file', 'name')

@admin.register(PhotoPackage)
class PhotoPackageAdmin(BaseOwnerAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')

@admin.register(CouponCode)
class CouponCodeAdmin(BaseOwnerAdmin):
    list_display = ('code', 'percentage', 'valid_until', 'is_active', 'max_uses', 'usage_count')
    search_fields = ('code',)

    # Usage count read-only
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('usage_count',)

@admin.register(Leg)
class LegAdmin(BaseOwnerAdmin):
    list_display = ('race', 'leg_number', 'custom_distance_value', 'custom_distance_unit',)
    search_fields = ('race__name',)
