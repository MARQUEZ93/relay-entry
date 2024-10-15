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

class IsObjectEventCreator(BasePermission):
    """
    Generic permission class that checks if the user is the creator of an Event
    or if the user is the creator of the event associated with a Race.
    """
    def has_object_permission(self, request, view, obj):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")

        # Check if the object is an Event
        if isinstance(obj, Event):
            return obj.created_by == user_profile and user_profile.is_approved
        
        # Check if the object is a Race (associated with an Event)
        elif isinstance(obj, Race):
            print("hit")
            return obj.event.created_by == user_profile and user_profile.is_approved

        # If it's neither Event nor Race, deny permission
        return False