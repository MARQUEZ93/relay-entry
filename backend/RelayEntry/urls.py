# backend/RelayEntry/urls.py

from django.urls import path
from . import views
from .views import EventDetailView, RaceDetailView

urlpatterns = [
    path('', views.index, name='index'), 
    # path('signup/', views.signup, name='signup'),
    path('api/events/<slug:url_alias>/races/<int:id>/', RaceDetailView.as_view(), name='race-detail'),
    path('api/events/<slug:url_alias>/', EventDetailView.as_view(), name='event-detail'),
    path('api/events/<slug:url_alias>/register/', views.event_register, name='event_register'),
    path('api/teams/register/', views.team_register, name='team_register'),
    path('api/create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
]
