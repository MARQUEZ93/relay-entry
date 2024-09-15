# backend/RelayEntry/urls.py

from django.urls import path
from . import views
from .views import EventDetailView, RaceDetailView, DashboardView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.index, name='index'), 
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    # path('signup/', views.signup, name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='token_logout'),
    path('api/events/<slug:url_alias>/races/<int:id>/', RaceDetailView.as_view(), name='race-detail'),
    path('api/events/<slug:url_alias>/', EventDetailView.as_view(), name='event-detail'),
    path('api/get-csrf/', views.get_csrf_token, name='get_csrf_token'),
    path('api/races/<int:race_id>/team-results/', views.team_race_results, name='team-race-results'),
    path('api/events/<slug:url_alias>/register/', views.event_register, name='event_register'),
    path('api/teams/register/', views.team_register, name='team_register'),
    path('api/create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('api/contact/', views.contact, name='contact'),
    path('api/stripe/webhook', views.stripe_webhook, name='stripe_webhook'),
    path('api/events/<slug:url_alias>/request-edit-link/', views.request_edit_link, name='request-edit-link'),
    path('api/edit-team/<str:token>/', views.verify_token_and_update_team, name='edit-team'),
    path('api/teams/get-team/<str:token>/', views.get_team_data, name='get-team-data'),
    path('api/search/<slug:url_alias>/<str:name>', views.confirm_registration, name='confirm_registration'),
]
