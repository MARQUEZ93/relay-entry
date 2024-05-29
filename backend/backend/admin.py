from django.contrib import admin
from .models import Event, Race, Registration, TeamMember, Document, PhotoPackage, CouponCode
from django.contrib.auth.models import User

class BaseOwnerAdmin(admin.ModelAdmin):
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

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
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
    list_display = ('file', 'name', 'required', 'uploaded_at')
    search_fields = ('file', 'name')

@admin.register(PhotoPackage)
class PhotoPackageAdmin(BaseOwnerAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')

@admin.register(CouponCode)
class CouponCodeAdmin(BaseOwnerAdmin):
    list_display = ('code', 'discount_percentage', 'valid_until', 'is_active', 'max_uses', 'usage_count')
    search_fields = ('code',)
