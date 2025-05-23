# backend/RelayEntry/urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.index, name='index'), 
    # logged-in
    path('api/dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # create event, update event, get event data plural + singular for logged-in user
    path('api/dashboard/events/create/', views.EventCreateUpdateView.as_view(), name='event-create'),
    path('api/dashboard/events/update/<int:id>/', views.EventCreateUpdateView.as_view(), name='event-update'),
    path('api/dashboard/events/', views.UserEventView.as_view(), name='user-events'),
    path('api/dashboard/events/<int:event_id>/', views.UserEventView.as_view(), name='user-event'),
    # get race data for logged in user
    path('api/dashboard/events/<int:event_id>/races/', views.UserRacesView.as_view(), name='user-races'),
    path('api/dashboard/races/<int:race_id>/', views.UserRacesView.as_view(), name='user-race'),
    # create/update race for logged in user
    path('api/dashboard/races/update/<int:race_id>/', views.RaceCreateUpdateView.as_view(), name='race-update'),
    path('api/dashboard/races/create/', views.RaceCreateUpdateView.as_view(), name='race-create'),
    # auth
    # path('api/signup/', views.signup, name='signup'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', views.LogoutView.as_view(), name='token_logout'),
    # routes for anon users
    path('api/events/<slug:url_alias>/races/<int:id>/', views.RaceDetailView.as_view(), name='race-detail'),
    path('api/events/<slug:url_alias>/', views.EventDetailView.as_view(), name='event-detail'),
    path('api/get-csrf/', views.get_csrf_token, name='get_csrf_token'),
    path('api/races/<int:race_id>/team-results/', views.team_race_results, name='team-race-results'),
    path('api/events/<slug:url_alias>/register/', views.event_register, name='event_register'),
    path('api/teams/register/', views.team_register, name='team_register'),
    path('api/contact/', views.contact, name='contact'),
    path('api/events/<slug:url_alias>/request-edit-link/', views.request_edit_link, name='request-edit-link'),
    path('api/search/<slug:url_alias>/<str:name>', views.confirm_registration, name='confirm_registration'),
    # special routes
    path('api/create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('api/teams/get-team/<str:token>/', views.get_team_data, name='get-team-data'),
    path('api/edit-team/<str:token>/', views.verify_token_and_update_team, name='edit-team'),
    path('api/stripe/webhook', views.stripe_webhook, name='stripe_webhook'),
]
