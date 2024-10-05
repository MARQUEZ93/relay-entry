from rest_framework.permissions import IsAuthenticated, BasePermission
from django.core.exceptions import ValidationError, ObjectDoesNotExist, PermissionDenied
from .models import UserProfile, Event, Race, Registration, Team, TeamMember

class IsUserApproved(BasePermission):
    def has_permission(self, request, view):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")
        return user_profile.is_approved
class IsEventCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")

        return obj.created_by == user_profile and user_profile.is_approved
        
class IsRaceEventCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")

        # Check if the event associated with the race was created by the user
        return obj.event.created_by == user_profile and user_profile.is_approved