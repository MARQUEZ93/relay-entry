# backend/RelayEntry/urls.py

from django.urls import path
from . import views
from .views import EventDetailView, RaceDetailView

urlpatterns = [
    path('', views.index, name='index'), 
    # path('signup/', views.signup, name='signup'),
    path('api/events/<int:event_id>/request-edit-link/', views.request_edit_link, name='request-edit-link'),
    path('api/events/<slug:url_alias>/races/<int:id>/', RaceDetailView.as_view(), name='race-detail'),
    path('api/events/<slug:url_alias>/', EventDetailView.as_view(), name='event-detail'),
    path('api/get-csrf/', views.get_csrf_token, name='get_csrf_token'),
    path('api/races/<int:race_id>/teamResults/', views.team_race_results, name='team-race-results'),
    path('api/events/<slug:url_alias>/register/', views.event_register, name='event_register'),
    path('api/teams/register/', views.team_register, name='team_register'),
    path('api/create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('api/contact/', views.contact, name='contact'),
    path('api/stripe/webhook', views.stripe_webhook, name='stripe_webhook'),
    path('api/edit-team/<str:token>/', verify_token_and_update_team, name='edit-team'),
]
